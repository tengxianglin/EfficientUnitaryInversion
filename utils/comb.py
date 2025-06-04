# !/usr/bin/env python3
# Copyright (c) 2024 QuAIR team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""
The source file of the PQCombNet class.
"""

import csv
import itertools
import os
import time
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import torch
from torch.nn import ModuleList

from quairkit.circuit import Circuit
from quairkit.core import set_seed, to_state, utils
from quairkit.database import bell_state, random_unitary, zero_state, eye
from quairkit.operator import ParamOracle
from quairkit.qinfo import channel_repr_convert

__all__ = ["PQCombNet"]


class PQCombNet:
    """Parameterized Quantum Comb Network.

    This model implements a trainable quantum comb for learning a target process
    over a set of unitaries. It supports three modes: 'process', 'comb', and 'swap'.

    Attributes:
        target_function: Maps input unitaries to the desired output operator.
        num_slots: Number of query slots (int).
        num_parallels: Number of parallel ancilla copies (int).
        ancilla_dim_list: List of ancilla dimensions.
        slot_dim: Dimension of each slot system (int).
        train_mode: One of {'process', 'comb', 'swap'}.
        task_name: Identifier used for logging and saving data.
        is_ctrl_U: If True, interprets the query as controlled-U.
        seed: Random seed for reproducibility.
    """

    def __init__(
        self,
        target_function: Callable[[torch.Tensor], torch.Tensor],
        num_slots: int = 1,
        num_parallels: int = 1,
        ancilla: Union[int, List[int]] = 0,
        slot_dim: int = 2,
        train_unitary_info: Union[int, torch.Tensor] = 1000,
        test_unitary_info: Union[int, torch.Tensor] = 0,
        train_mode: str = "process",
        task_name: Optional[str] = None,
        is_ctrl_U: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        """Initialize parameters, datasets, and the training environment."""
        _setup_parameters(
            self,
            target_function,
            num_slots,
            num_parallels,
            ancilla,
            slot_dim,
            train_mode,
            task_name,
            is_ctrl_U,
            seed,
        )
        _setup_unitary_sets(self, train_unitary_info, test_unitary_info)
        _initialize_training_environment(self)

    # -----------------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------------
    @property
    def target_function(self) -> Callable[[torch.Tensor], torch.Tensor]:
        """The current target_function mapping unitaries to desired output."""
        return self._target_function

    @target_function.setter
    def target_function(self, fn: Callable[[torch.Tensor], torch.Tensor]) -> None:
        """Assign a new target_function and trigger omega recalculation."""
        self._target_function = fn
        _calculate_omegas(self)

    @property
    def num_slots(self) -> int:
        """Number of query slots."""
        return self._num_slots

    @num_slots.setter
    def num_slots(self, value: int) -> None:
        """Adjust the slot count and update dependent variables."""
        self._num_slots = value
        self._num_V = value + 1
        if self._train_mode == "comb":
            _calculate_omegas(self)

    @property
    def num_parallels(self) -> int:
        """Number of parallel ancilla copies."""
        return self._num_parallel

    @num_parallels.setter
    def num_parallels(self, value: int) -> None:
        """Set the number of parallel ancilla copies."""
        self._num_parallel = value

    @property
    def ancilla_dim_list(self) -> List[int]:
        """List of ancilla dimensions."""
        return self._ancilla_dim_list

    @ancilla_dim_list.setter
    def ancilla_dim_list(self, value: List[int]) -> None:
        """Set the ancilla dimension list and update system dimensions."""
        self._ancilla_dim_list = value
        self._system_dim_list = self._ancilla_dim_list + [self.slot_dim]

    @property
    def ancilla_dim(self) -> int:
        """Total ancilla dimension (product of individual dimensions)."""
        return np.prod(self.ancilla_dim_list).__int__()

    @property
    def slot_dim(self) -> int:
        """Dimension of each slot system."""
        return self._slot_dim

    @property
    def train_mode(self) -> str:
        """Current training mode."""
        return self._train_mode

    @train_mode.setter
    def train_mode(self, value: str) -> None:
        """Set the training mode (process, comb, or swap)."""
        if self.is_ctrl_U:
            raise ValueError("Cannot set train_mode when is_ctrl_U is True")
        self._train_mode = value

    @property
    def LR(self) -> float:
        """Learning rate."""
        return self._LR

    @LR.setter
    def LR(self, value: float) -> None:
        """Set the learning rate."""
        self._LR = value

    @property
    def NUM_ITR(self) -> int:
        """Number of iterations (epochs)."""
        return self._NUM_ITR

    @property
    def task_name(self) -> str:
        """Task identifier for logging and storage."""
        return self._task_name

    @property
    def seed(self) -> int:
        """Random seed."""
        return self._seed

    @seed.setter
    def seed(self, value: int) -> None:
        """Set the random seed and update internal state."""
        self._seed = value
        set_seed(self._seed)

    @property
    def is_ctrl_U(self) -> bool:
        """Flag indicating controlled-U interpretation."""
        return self._is_ctrl_U

    @property
    def num_V(self) -> int:
        """Number of V circuits (slots + 1)."""
        return self._num_V

    @property
    def train_unitary_set(self) -> torch.Tensor:
        """Training unitary set."""
        return self._train_unitary_set

    @train_unitary_set.setter
    def train_unitary_set(self, value: torch.Tensor) -> None:
        """Set the training unitary set and update omegas."""
        self._train_unitary_set = value
        _calculate_omegas(self)

    @property
    def test_unitary_set(self) -> torch.Tensor:
        """Testing unitary set."""
        return self._test_unitary_set

    @test_unitary_set.setter
    def test_unitary_set(self, value: torch.Tensor) -> None:
        """Set the testing unitary set and update omegas."""
        self._test_unitary_set = value
        _calculate_omegas(self)

    @property
    def omega_train(self) -> torch.Tensor:
        """Omega tensor for training."""
        return self._omega_train

    @property
    def omega_test(self) -> torch.Tensor:
        """Omega tensor for testing."""
        return self._omega_test

    @property
    def V_circuit_list(self) -> ModuleList:
        """List of V circuits (quantum comb components)."""
        return self._V_circuit_list

    @V_circuit_list.setter
    def V_circuit_list(self, value: ModuleList) -> None:
        """Set the V circuit list and update slot count."""
        self.num_slots = value.__len__() - 1
        self._V_circuit_list = value

    @property
    def data_directory_name(self) -> str:
        """Directory name for saving data."""
        return self._data_directory_name

    @data_directory_name.setter
    def data_directory_name(self, value: str) -> None:
        """Set the data directory name."""
        self._data_directory_name = value

    @property
    def system_dim_list(self) -> List[int]:
        """List of system dimensions (ancilla + slots)."""
        return self._system_dim_list

    @property
    def system_dim(self) -> int:
        """Total system dimension (product of all dimensions)."""
        return np.prod(self.system_dim_list).__int__()

    # -----------------------------------------------------------------------
    # Static helper example
    # -----------------------------------------------------------------------
    @staticmethod
    def _prepare_initial_state(
        ancilla_dims: List[int], slot_dim: int, num_V: int, is_choi_mode: bool
    ) -> torch.Tensor:
        """Prepare the initial joint state (ancilla ⊗ Bell) for the circuit."""
        ancilla_state = zero_state(
            num_systems=len(ancilla_dims), system_dim=ancilla_dims
        )
        bell_states = bell_state(
            num_systems=2 * (num_V if is_choi_mode else 1), system_dim=slot_dim
        )
        full_ket = utils.linalg._nkron(ancilla_state.ket, bell_states.ket)
        return to_state(full_ket, ancilla_state.system_dim + bell_states.system_dim)

    def update_V_circuit(
        self,
        index: int,
        new_V: Union[
            Circuit, ParamOracle, torch.Tensor, Tuple[torch.Tensor, List[int]]
        ],
    ) -> None:
        r"""
        Update the V circuit at the specified index with a new circuit.

        Args:
            index: The index of the V circuit to update.
            new_V: The new V circuit, which can be a ParamOracle, Circuit, torch.Tensor or Tuple[torch.Tensor, List[int]].

        Raises:
            ValueError: If the index is out of range or if the dimension of the provided Circuit does not match the dimension of the existing Circuit.
            TypeError: If the new_V is not a Circuit, ParamOracle, torch.Tensor, or Tuple[torch.Tensor, List[int]].
        """
        if not (0 <= index < len(self.V_circuit_list)):
            raise ValueError(f"Index out of range: {index}")

        if not isinstance(V := new_V, Circuit):
            V = Circuit(system_dim=self.system_dim_list)
            if isinstance(new_V, ParamOracle):
                V.append(new_V)
            elif isinstance(new_V, torch.Tensor):
                V.oracle(oracle=new_V, system_idx=self.system_dim_list)
            elif (
                isinstance(new_V, tuple)
                and isinstance(new_V[0], torch.Tensor)
                and isinstance(new_V[1], list)
            ):
                V.oracle(oracle=new_V[0], system_idx=new_V[1])
            else:
                raise TypeError(
                    "new_V must be a Circuit, ParamOracle, torch.Tensor, Tuple[torch.Tensor, or List[int]]"
                )

        self.V_circuit_list[index] = V

    def train(
        self,
        projector: Optional[torch.Tensor] = None,
        eval_func: Optional[
            Callable[["PQCombNet", str, Optional[torch.Tensor]], torch.Tensor]
        ] = None,
        base_lr: float = 0.1,
        alpha: Optional[float] = None,
        max_epochs: int = 10000,
        is_save_data: bool = False,
        is_auto_stop: bool = True,
        verbose: bool = True,
    ) -> torch.Tensor:
        r"""
        Train the PQCombNet model.

        Args:
            projector: The projector to apply to the ancilla system of the output state.
            eval_func: Optional custom evaluation function to replace _average_fidelity. Default is None.
            base_lr: The base learning rate for the optimizer.
            max_epochs: The maximum number of epochs to train for.
            is_save_data: A flag to indicate whether to save the training data.
            is_auto_stop: A flag to indicate whether to stop training early if the learning rate is too low.
            verbose: A flag to indicate whether to output training information and progress bars.
        """
        if eval_func is None:
            eval_func = _average_fidelity
        train_func = _swap_train if self.train_mode == "swap" else _train
        alpha = 0.9 if projector is not None and alpha is None else (alpha if alpha is not None else 1.0)

        return train_func(
            self=self,
            projector=projector,
            eval_func=eval_func,
            base_lr=base_lr,
            max_epochs=max_epochs,
            is_save_data=is_save_data,
            is_auto_stop=is_auto_stop,
            verbose=verbose,
            alpha=alpha,
        )

    def extract_highest_fidelity(self) -> None:
        r"""
        Call the _extract_highest_fidelity function to generate the fidelity tables.
        If the file does not exist, prompt the user to set is_save_data to True.
        """
        filepath = os.path.join(
            self.data_directory_name, f"{self.task_name}_train_log.csv"
        )
        if not os.path.exists(filepath):
            print(
                f"File {filepath} does not exist. Consider setting is_save_data to True."
            )
            return

        _extract_highest_fidelity(
            self.data_directory_name, f"{self.task_name}_train_log.csv"
        )

    def plot(self, **kwargs):
        r"""
        Plot the quantum comb circuit.

        All arguments are passed directly to Circuit.plot.

        Returns:
            None, or a ``matplotlib.figure.Figure`` instance depending on Circuit.plot.
        """
        cir = Circuit(system_dim=self.system_dim_list)
        for index, V_circuit in enumerate(self.V_circuit_list):
            cir.extend(deepcopy(V_circuit))
            if index < self.num_slots:
                if self.is_ctrl_U:
                    cir.control_oracle(
                        eye(self.slot_dim),
                        [len(self.ancilla_dim_list) - 1, len(self.ancilla_dim_list)],
                        latex_name=(r"U" if index % 2 == 0 else r"U^{\dagger}"),
                    )
                else:
                    cir.oracle(
                        eye(self.slot_dim),
                        len(self.ancilla_dim_list),
                        latex_name=(r"U"),
                    )
        return cir.plot(**kwargs)


def _construct_circuit(
    self: PQCombNet,
    system_dim_loss: int,
    unitary_set: torch.Tensor,
    V_list_applied_index: list,
) -> Circuit:
    r"""
    Construct the quantum circuit for the loss calculation.

    Args:
        system_dim_loss: The system dimension for the loss calculation.
        unitary_set: The set of unitary matrices to apply.
        V_list_applied_index: List of indices for applying V circuits.

    Returns:
        The constructed quantum circuit.
    """
    cir_loss = Circuit(system_dim=system_dim_loss)
    _apply_V_circuits(self, cir_loss, V_list_applied_index, unitary_set)
    return cir_loss


def _average_fidelity(
    self: PQCombNet,
    fid_type: str,
    projector: torch.Tensor = None,
    alpha: float = 1.0,
) -> torch.Tensor:
    r"""
    Compute the average fidelity for a given set of unitaries and omega tensor.

    Args:
        fid_type: Type of fidelity calculation ('train' or 'test').
        projector: The projector to apply to the ancilla system of output state.
        max_batch_size: The maximum number of unitary matrices to be processed in parallel.

    Returns:
        The average fidelity as a real-valued tensor.
    """
    if fid_type == "test" and self.test_unitary_set.__len__() == 0:
        return torch.tensor(-1.0)
    # Set up the parameters
    is_comb_mode = self.train_mode == "comb"
    num_target_systems = 2 * self.num_V if is_comb_mode else 2
    system_dim_loss = self.ancilla_dim_list + [self.slot_dim] * num_target_systems
    V_list_applied_index = _get_V_list_applied_index(self, is_comb_mode)

    # Prepare the input state
    Psi_in = self._prepare_initial_state(
        ancilla_dims=self.ancilla_dim_list,
        slot_dim=self.slot_dim,
        num_V=self.num_V,
        is_choi_mode=is_comb_mode,
    )

    # Construct the circuit
    circuit = _construct_circuit(
        self,
        system_dim_loss,
        self.train_unitary_set if fid_type == "train" else self.test_unitary_set,
        V_list_applied_index,
    )
    if projector is not None and utils.qinfo._state_fidelity(
        projector, zero_state(1, self.ancilla_dim).density_matrix
    ):
        psi_out_ket = circuit(Psi_in).ket[:, : self.slot_dim**num_target_systems]
        psi_out_density_matrix = psi_out_ket @ utils.linalg._dagger(psi_out_ket)
        prob_success_list = utils.linalg._trace(psi_out_density_matrix).real
        prob_success = prob_success_list.mean()
        psi_out_density_matrix /= prob_success_list.view(-1, 1, 1)
    else:
        prob_success_list, psi_out = circuit(Psi_in).measure(
            measured_op=(projector or eye(self.ancilla_dim)).kron(
                eye(self.slot_dim**num_target_systems)
            ),
            sys_idx=list(range(self.ancilla_dim_list.__len__())),
            keep_state=True,
        )

        prob_success = prob_success_list.mean()

        # Trace out the ancilla system
        if self.ancilla_dim_list:
            psi_out = psi_out.trace(list(range(len(self.ancilla_dim_list))))
        psi_out_density_matrix = psi_out.density_matrix

    omega = self.omega_train if fid_type == "train" else self.omega_test
    fidelities = utils.linalg._trace(psi_out_density_matrix @ omega).real
    fidelity = (
        fidelities * self.slot_dim ** (self.num_V - 2)
        if is_comb_mode
        else torch.mean(fidelities)
    )

    return alpha * fidelity + (1 - alpha) * prob_success


def _save_results(
    self: PQCombNet,
    itr: int,
    fidelity: float,
    loss: float,
    base_lr: float,
    current_lr: float,
) -> None:
    data = {
        "slot_dim": self.slot_dim,
        "num_slots": self.num_slots,
        "ancilla_dim": self.ancilla_dim,
        "train_mode": self.train_mode,
        "base_lr": base_lr,
        "current_lr": current_lr,
        "num_test_unitary": len(self.train_unitary_set),
        "num_train_unitary": len(self.train_unitary_set),
        "seed": self.seed,
        "max_epochs": itr,
        "loss": loss,
        "fidelity": fidelity,
    }
    _save_results_to_csv(
        data=data,
        filename=f"{self.task_name}_train_log.csv",
        directory=self.data_directory_name,
    )


def _setup_parameters(
    self: PQCombNet,
    target_function: Callable[[torch.Tensor], torch.Tensor],
    num_slots: int,
    num_parallels: int,
    ancilla: Union[List[int], int] = 0,
    slot_dim: int = 2,
    train_mode: str = "comb",
    task_name: Optional[str] = None,
    is_ctrl_U: bool = False,
    seed: Optional[int] = None,
) -> None:
    r"""
    Combines the setup of basic parameters and training-specific parameters for quantum computation and training.

    Args:
        target_function: The function to apply to each unitary in the dataset
        num_slots: The number of unitaries to be queried
        ancilla: The ancilla dimension or dimension list
        slot_dim: The slot dimension for the unitaries to be queried
        train_mode: The training mode, which can be "process", "comb", or "swap"
        task_name: Optional name for the task, useful for data logging and storage
        is_ctrl_U: Flag to indicate if a controlled-U operation is used in the training process
        seed: Optional seed for random number generation, enhancing reproducibility
    """
    # Basic parameters setup
    self._target_function = target_function
    self._is_ctrl_U = is_ctrl_U
    self._slot_dim = slot_dim
    self._num_slots = num_slots
    self._num_parallel = num_parallels
    self._ancilla_dim_list = (
        [2] * ancilla + [slot_dim] * (num_parallels - 1)
        if isinstance(ancilla, int) and num_parallels > 1
        else (
            [2] * ancilla
            if isinstance(ancilla, int)
            else [dim for dim in ancilla if dim != 0]
        )
    )
    self._num_V = num_slots + 1
    self._system_dim_list = self._ancilla_dim_list + [slot_dim]
    self._task_name = (
        task_name or f"pqcomb_{target_function.__name__}{'_ctrl' if is_ctrl_U else ''}"
    )

    # Training parameters setup
    self._seed = seed or np.random.randint(1e6)

    _validate_training_mode(self, train_mode)


def _setup_unitary_sets(
    self: PQCombNet,
    train_unitary_info: Union[int, torch.Tensor],
    test_unitary_info: Union[int, torch.Tensor],
) -> None:
    r"""
    Prepares the unitary sets for training and testing.

    Args:
        train_unitary_info: Information or data for training unitaries.
        test_unitary_info: Information or data for testing unitaries.
    """
    self._train_unitary_set = _generate_unitary_set(train_unitary_info, self.slot_dim)
    self._test_unitary_set = (
        _generate_unitary_set(test_unitary_info, self.slot_dim)
        if (isinstance(test_unitary_info, int) and test_unitary_info > 0)
        or (isinstance(test_unitary_info, torch.Tensor) and len(test_unitary_info) > 0)
        else torch.tensor([])
    )

    _calculate_omegas(self)


def _calculate_omegas(self: PQCombNet) -> None:
    r"""
    Calculate omega for train and test unitary sets.
    """
    try:
        self._omega_train = _get_omega(self, self.train_unitary_set)
        self._omega_test = _get_omega(self, self.test_unitary_set)
    except RuntimeError as e:
        if "not enough memory" not in str(e) or self.train_mode != "comb":
            raise e

        print(
            f"[{self.task_name} | {self.train_mode} | {self.seed}] "
            f"Out of memory error caught, switching train_mode from '{self.train_mode}' to ",
            end="",
        )
        self.train_mode = "process"
        print(f"'{self.train_mode}'...")
        self._omega_train = _get_omega(self, self.train_unitary_set)
        self._omega_test = _get_omega(self, self.test_unitary_set)


def _validate_training_mode(self: PQCombNet, train_mode: str) -> None:
    r"""
    Validates the training mode against supported modes.

    Args:
        train_mode: Training mode to validate.
    """
    train_mode_list = ["comb", "process", "swap"]
    if (train_mode := train_mode.lower()) not in train_mode_list:
        raise ValueError(
            f"Invalid train_mode: {train_mode}, must be one of {train_mode_list}"
        )
    if train_mode == "comb" and self.is_ctrl_U:
        raise ValueError("Controlled-U operation is not supported in 'comb' mode.")
    self._train_mode = train_mode


def _initialize_training_environment(self: PQCombNet) -> None:
    r"""
    Sets up the data directories and initializes the training environment.

    Initializes the omega tensors and the list of variable quantum circuits for the simulation.
    """
    self._data_directory_name = f"{self.task_name}_data"
    self._V_circuit_list = _create_V_circuit_list(self)


def _get_omega(self: PQCombNet, unitary_set: torch.Tensor) -> torch.Tensor:
    r"""
    Compute the omega tensor for a given task.

    Args:
        unitary_set: The set of unitary matrices.

    Returns:
        torch.Tensor: The omega tensor.
    """
    if unitary_set.__len__() == 0:
        return torch.tensor(-1)
    if self.train_mode == "comb":
        return _compute_omega_choi(
            self.target_function, unitary_set, self.slot_dim, self.num_slots
        )
    else:
        return _compute_omega_process(self.target_function, unitary_set, self.slot_dim)


def _create_V_circuit_list(self: PQCombNet) -> ModuleList:
    r"""
    Create a list of V circuits.

    Returns:
        ModuleList: The list of V circuits.
    """
    V_circuit_list = ModuleList()

    for _ in range(self.num_V):
        V = Circuit(system_dim=self.system_dim_list)
        V.universal_qudits(system_idx=list(range(len(self.system_dim_list))))
        V_circuit_list.append(V)

    return V_circuit_list


def _get_V_list_applied_index(
    self: PQCombNet, is_comb_mode: bool
) -> Union[List[List[int]], List[int]]:
    r"""
    Returns the list of indices where V circuits are applied, depending on the training mode.

    Args:
        is_choi_mode: Indicates whether the 'choi' mode is used for determining the index list.

    Returns:
        Union[List[List[int]], List[int]]: The list of indices where V circuits are applied.
    """
    if is_comb_mode:
        return [
            list(range(len(self.ancilla_dim_list)))
            + [len(self.ancilla_dim_list) + 2 * j + 1]
            for j in range(self.num_V)
        ]
    else:
        return list(range(len(self.system_dim_list)))


def _apply_V_circuits(
    self: PQCombNet,
    cir_loss: Circuit,
    V_list_applied_index: List[Union[List[int], int]],
    unitary_set: torch.Tensor,
) -> None:
    r"""
    Applies the V circuits to the circuit loss object.

    Args:
        cir_loss: The circuit to which the V circuits are applied.
        V_list_applied_index: A list or a list of lists of indices where V circuits should be applied.
        unitary_set: The set of unitary matrices used in the control operations.
    """
    for index, V_circuit in enumerate(self._V_circuit_list):
        cir_loss.oracle(
            V_circuit.unitary_matrix(),
            (
                V_list_applied_index[index]
                if self.train_mode == "comb"
                else V_list_applied_index
            ),
            latex_name=f"\\mathcal{{V}}_{{{index}}}",
        )
        if self.train_mode != "comb" and index < self.num_slots:
            _apply_controlled_U(self, cir_loss, unitary_set, index)


def _apply_controlled_U(
    self: PQCombNet, cir_loss: Circuit, unitary_set: torch.Tensor, index: int
) -> None:
    r"""
    Applies the controlled U or U† depending on the configuration.

    Args:
        cir_loss: The circuit to which the controlled operations are applied.
        unitary_set: The set of unitary matrices.
        index: The index of the current operation in the sequence.
    """
    if self.is_ctrl_U:
        cir_loss.control_oracle(
            unitary_set if index % 2 == 0 else utils.linalg._dagger(unitary_set),
            [len(self.ancilla_dim_list) - 1, len(self.ancilla_dim_list)],
            latex_name=(r"U" if index % 2 == 0 else r"U^{\dagger}"),
        )
    else:
        for idx_paral in range(self.num_parallels):
            cir_loss.oracle(
                unitary_set,
                len(self.ancilla_dim_list) - idx_paral,
                latex_name=(r"$U$"),
            )


def _log_progress(
    self: PQCombNet,
    itr: int,
    loss: torch.Tensor,
    time_list: list,
    base_lr: float,
    current_lr: float,
    max_epochs: int,
    projector: torch.Tensor = None,
    is_save_data: bool = False,
    is_auto_stop: bool = True,
    verbose: bool = True,
) -> bool:
    r"""
    Logs the training progress at specified intervals and saves the results.
    It provides insights into the current state of training, including loss, fidelity, and learning rate.

    This function checks if the current iteration is a multiple of 100 or the last iteration.
    If so, it calculates the average fidelity, constructs a log message with relevant metrics,
    and prints it. The function also saves the results and may determine if training should stop early.

    Args:
        itr: The current iteration number.
        loss: The current loss value.
        time_list: A list of time taken for each iteration.
        base_lr: The initial learning rate.
        current_lr: The current learning rate.
        max_epochs: The total number of iterations.
        projector: The projector to apply to the ancilla system of the output state.
        is_save_data: A flag to indicate whether to save the training data.
        is_auto_stop: A flag to indicate whether to stop training early if the learning rate is too low.
        verbose: A flag to indicate whether to output training information and progress bars.

    Returns:
        Returns True if training should be stopped early, otherwise None.
    """
    # early_stop_condition = (current_lr < 1e-4 * base_lr or loss < 1e-4) and is_auto_stop
    early_stop_condition = (current_lr < 1e-4 * base_lr or loss < 0.0001) and is_auto_stop
    if itr % 100 == 0 or itr == max_epochs - 1 or early_stop_condition:
        fidelity = _average_fidelity(self, "test", projector, alpha=1).item()
        prob_success = _average_fidelity(self, "test", projector, alpha=0).item()

        if verbose:
            print(
                (
                    f"[{self.task_name} | {self.train_mode} | {self.seed} | \033[90m{itr}\t{np.mean(time_list):.4f}s\033[0m] "
                    f"slot_dim: {self.slot_dim}, slots: {self.num_slots}, "
                    + (
                        f"ancilla_dim: {self.ancilla_dim}"
                        if all(dim == 2 for dim in self.ancilla_dim_list)
                        or not self.ancilla_dim_list
                        else f"aux_dim: {self.ancilla_dim}"
                    )
                    + f", \033[93mLR: {current_lr:.2e}\033[0m"
                    + f", \033[91mLoss: {loss.item():.8f}\033[0m"
                    + (f", \033[92mFid: {fidelity:.8f}\033[0m" if fidelity >= 0 else "")
                    + (f", \033[92mProb: {prob_success:.8f}\033[0m" if projector is not None else "")
                ),
            )

        time_list.clear()
        # Save results and possibly stop training
        if is_save_data:
            _save_results(self, itr, fidelity, loss.item(), base_lr, current_lr)

    return early_stop_condition


def _compute_omega_choi(
    target_function: Callable[[torch.Tensor], torch.Tensor],
    unitary_set: torch.Tensor,
    slot_dim: int,
    num_slots: int,
) -> torch.Tensor:
    r"""
    Compute the omega tensor using the 'choi' mode.

    Args:
        target_function: The function to apply to each tensor in the dataset.
        unitary_set: The set of unitary matrices.
        slot_dim: The slot dimension for the unitaries to be queried.
        num_slots: The parameter 'num_slots' used in computation.

    Returns:
        torch.Tensor: The computed omega tensor.
    """
    omega = 0
    for u in unitary_set:
        u_transformed_choi = channel_repr_convert(
            target_function(u), source="kraus", target="choi"
        )
        u_conj_choi = channel_repr_convert(u.conj(), source="kraus", target="choi")
        omega += utils.linalg._nkron(
            *([u_transformed_choi] + [u_conj_choi] * num_slots)
        )
    omega /= len(unitary_set)
    perm_list = [0, 2 * num_slots + 1] + list(range(1, 2 * num_slots + 1))
    return utils.linalg._permute_systems(
        omega, perm_list, [slot_dim] * 2 * (num_slots + 1)
    )


def _generate_unitary_set(
    unitary_info: Union[int, torch.Tensor], slot_dim: int
) -> torch.Tensor:
    r"""
    Generates a set of unitary matrices based on provided info.

    Args:
        unitary_info: Details to generate or directly provide the unitaries.
        slot_dim: slot_dim for the unitary matrices.
    """
    return (
        random_unitary(num_systems=1, size=unitary_info, system_dim=slot_dim)
        if isinstance(unitary_info, int)
        else unitary_info
    )


def _compute_omega_process(
    target_function: Callable[[torch.Tensor], torch.Tensor],
    unitary_set: torch.Tensor,
    slot_dim: int,
) -> torch.Tensor:
    r"""
    Compute the omega tensor for the 'process' or 'swap' mode.

    Args:
        target_function: The function to apply to each unitary in the dataset.
        unitary_set: The set of unitary.
        slot_dim: The slot dimension for the unitaries to be queried.

    Returns:
        torch.Tensor: The computed omega tensor.
    """
    target_unitary = target_function(unitary_set)
    return (
        bell_state(num_systems=2, system_dim=slot_dim)
        .evolve(target_unitary.kron(eye(slot_dim)))
        .density_matrix
    )


def _print_progress_bar(
    iteration: int,
    total: int,
    prefix: str = "",
    suffix: str = "",
    decimals: int = 1,
    length: int = 50,
    fill: str = "█",
    verbose: bool = True,
) -> None:
    r"""
    Call in a loop to create a terminal progress bar.

    Args:
        iteration: Current iteration.
        total: Total iterations.
        prefix: Prefix string.
        suffix: Suffix string.
        decimals: Positive number of decimals in percent complete.
        length: Character length of the bar.
        fill: Bar fill character.
        verbose: A flag to indicate whether to output the progress bar.
    """
    if verbose:
        percent = f"{100 * (iteration / float(total)):.{decimals}f}"
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + "-" * (length - filled_length)
        print(f"\r{prefix} |{bar}| {percent}% {suffix}", end="\r")
        if iteration == total:
            print()


def _save_results_to_csv(data: Dict[str, Any], filename: str, directory: str) -> None:
    r"""
    Save the results to a CSV file.

    Args:
        data: A dictionary containing the data to be saved.
        filename: The name of the CSV file.
        directory: The directory where the CSV file will be saved.
    """
    filepath = os.path.join(directory, filename)

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Define the column names
    fieldnames = list(data.keys())

    # Write to the CSV file
    file_exists = os.path.isfile(filepath)

    with open(filepath, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


def _extract_highest_fidelity(data_directory: str, filename: str) -> None:
    r"""
    Extract the highest fidelity for each combination of num_slots and ancilla_dim and generate a table.

    Args:
        data_directory: The directory where the CSV file is saved.
        filename: The name of the CSV file.
    """
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError(
            "The pandas library is required to run this function. Please install it using 'pip install pandas'."
        ) from e

    # Construct the full file path
    filepath = os.path.join(data_directory, filename)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(filepath)

    # Find unique slot_dim values
    slot_dim_values = df["slot_dim"].unique()

    # Create a directory to save the result tables
    result_dir = os.path.join(data_directory, "fidelity_tables")
    os.makedirs(result_dir, exist_ok=True)

    # Iterate over each unique slot_dim value
    for slot_dim in slot_dim_values:
        # Filter the DataFrame for the current slot_dim
        df_filtered = df[df["slot_dim"] == slot_dim]

        # Pivot the table to have num_slots as rows and ancilla_dim as columns, with max fidelity as values
        pivot_table = df_filtered.pivot_table(
            index="num_slots",
            columns="ancilla_dim",
            values="fidelity",
            aggfunc="max",
        )

        # Save the pivot table to a CSV file
        output_filename = f"fidelity_table_slot_dim_{slot_dim}.csv"
        output_filepath = os.path.join(result_dir, output_filename)
        pivot_table.to_csv(output_filepath)
        print(f"Saved table for slot_dim = {slot_dim} to {output_filepath}")


def _qudit_swap_matrix(dim: int):
    """
    Returns the SWAP gate for a qudit of dimension dim.

    Args:
        dim (int): The dimension of the qudit.
    """
    qudit_swap_matrix = torch.zeros(dim**2, dim**2)
    for x, y in itertools.product(range(dim), range(dim)):
        qudit_swap_matrix[y * dim + x, x * dim + y] = 1
    return qudit_swap_matrix


def _train_swap_circuit(
    self: PQCombNet,
    depth: int = 1,
    base_lr: float = 0.1,
    max_epochs: int = 1000,
    loss_threshold: float = 1e-3,
    verbose: bool = True,
) -> Tuple[Circuit, float]:
    r"""
    Train the SWAP gate circuit to pass the last unitary in the comb.

    Args:
        depth: The depth of the SWAP gate circuit.
        base_lr: The base learning rate for the optimizer.
        max_epochs: The maximum number of training epochs.
        loss_threshold: The loss threshold for stopping the training.
        verbose: A flag to indicate whether to output training information.

    Returns:
        Tuple[Circuit, float]: The trained SWAP gate circuit and the final loss value.
    """
    # check if the slot_dim is greater than or equal to the ancilla_dim
    assert self.slot_dim <= self.ancilla_dim, (
        f"slot_dim must be greater than or equal to ancilla_dim, "
        f"but got slot_dim={self.slot_dim} and ancilla_dim={self.ancilla_dim}"
    )

    assert self.slot_dim == self.ancilla_dim_list[-1], (
        f"slot_dim must be equal to the last element of ancilla_dim_list to construct the SWAP gate, "
        f"but got slot_dim={self.slot_dim} and ancilla_dim_list={self.ancilla_dim_list}"
    )
    actual_swap_cir = Circuit(system_dim=self.system_dim_list)
    for _ in range(depth):
        actual_swap_cir.universal_qudits(list(range(actual_swap_cir.num_systems)))
    ideal_swap_cir = Circuit(system_dim=self.system_dim_list)
    ideal_swap_cir.oracle(
        _qudit_swap_matrix(self.slot_dim),
        [len(self.system_dim_list) - 2, len(self.system_dim_list) - 1],
    )

    ideal_unitary_matrix = ideal_swap_cir.unitary_matrix()
    ideal_choi_ket = (
        ideal_unitary_matrix.kron(eye(self.system_dim))
        @ bell_state(2, self.system_dim).ket
    )

    # define the loss function as 1 minus the fidelity between the Choi matrices of the actual and desired circuits
    def swap_loss_func():
        actual_choi_ket = (
            actual_swap_cir.unitary_matrix().kron(eye(self.system_dim))
            @ bell_state(2, self.system_dim).ket
        )
        # calculate the fidelity between the actual and desired density matrices
        return 1 - abs(utils.linalg._dagger(actual_choi_ket) @ ideal_choi_ket) ** 2

    # initialize the optimizer and scheduler
    opt = torch.optim.Adam(actual_swap_cir.parameters(), lr=base_lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, "min")

    # start the training process
    for itr in range(max_epochs):
        _print_progress_bar(itr + 1, max_epochs, prefix="Progress", verbose=verbose)
        # calculate the loss
        loss = swap_loss_func()
        # obtain the updated learning rate
        lr = scheduler.optimizer.param_groups[0]["lr"]
        if loss.item() < loss_threshold or lr < base_lr * 1e-4:
            if verbose:
                print(
                    f"[pqc_search_swap | \033[90m{itr}\033[0m | {depth}] ",
                    f"Stop training SWAP with lr={lr:.2e}, loss={loss.item():.8f}.",
                )
            break

        # zero the gradients
        opt.zero_grad()
        # backpropagation
        loss.backward()
        # update the parameters
        opt.step()
        # adjust the learning rate according to the loss value
        scheduler.step(loss)

        # print training information every 40 iterations or on the last iteration
        if verbose and (itr % 100 == 0 or itr == max_epochs - 1):
            print(
                f"[pqc_search_swap | \033[90m{itr}\033[0m | {depth}] "
                f"slot_dim: {self.slot_dim}, "
                + (
                    f"ancilla_dim: {self.ancilla_dim}"
                    if all(dim == 2 for dim in self.ancilla_dim_list)
                    or not self.ancilla_dim_list
                    else f"aux_dim: {self.ancilla_dim}"
                )
                + f", \033[93mLR: {lr:.2e}\033[0m, "
                f"\033[91mLoss: {loss.item():.8f}\033[0m"
            )

    if loss.item() < loss_threshold:
        if verbose:
            print(f"Applying SWAP gate with lr={lr:.2e}, loss={loss.item():.8f}.")
        return actual_swap_cir, loss.item()
    else:
        if verbose:
            print("Retrain SWAP gate...")
        return _train_swap_circuit(self, depth=depth + 1, verbose=verbose)


def _swap_train(
    self: PQCombNet,
    projector: Optional[torch.Tensor],
    eval_func: Optional[
        Callable[[PQCombNet, str, Optional[torch.Tensor]], torch.Tensor]
    ] = None,  # Optional custom evaluation function to replace _average_fidelity.
    base_lr: float = 0.1,
    max_epochs: int = 1000,
    is_save_data: bool = False,
    is_auto_stop: bool = True,
    verbose: bool = True,
) -> None:
    """
    Trains the PQCombNet model using the SWAP gate approach.

    This method incrementally adds parameterized SWAP gates to the model and trains them to enhance the model's capacity. The training process involves:
    - Initializing and training a SWAP gate.
    - Sequentially adding SWAP gates to the model until the desired number of slots is achieved.
    - Training only the newly added SWAP gates.
    - Training all gates in the model for fine-tuning.

    Optionally, it records training data such as fidelity metrics and timing information.

    Args:
        projector: The projector tensor used for fidelity calculations. If `None`, a default projector is used.
        eval_func: Optional custom evaluation function to replace _average_fidelity. Default is None.
        base_lr: The base learning rate for the optimizer.
        max_epochs: The maximum number of training epochs for each training phase.
        is_save_data: If `True`, saves the training data and results to the specified directory.
        is_auto_stop: If `True`, enables early stopping based on convergence criteria.
        verbose: A flag to indicate whether to output training information.
    """
    if eval_func is None:
        eval_func = _average_fidelity
    n_s = self.num_slots
    if verbose:
        print(
            f"Training SWAP gate with slot_dim={self.slot_dim} and ancilla_dim={self.ancilla_dim}"
        )
    start_time_overall = time.time()
    param_swap_gate, swap_loss = _train_swap_circuit(self, verbose=verbose)
    time_train_swap = time.time() - start_time_overall
    self.V_circuit_list = torch.nn.ModuleList(
        [Circuit(system_dim=self.system_dim_list)]
    )
    while self.num_slots < n_s:
        self.num_slots = self.V_circuit_list.__len__()
        for V_circuit in self.V_circuit_list:
            V_circuit.requires_grad_(False)
        self.V_circuit_list[-1].extend(deepcopy(param_swap_gate))
        self.V_circuit_list.append(deepcopy(param_swap_gate))
        if is_save_data:
            # Insert SWAP and calculate initial fidelity
            fidelity_train_swap_start = _average_fidelity(
                self, "train", projector
            ).item()
            fidelity_test_swap_start = _average_fidelity(self, "test", projector).item()

        # Train only SWAP gate
        if verbose:
            print("Training only on parameterized SWAP gates.")
        start_time_swap_only = time.time()
        _train(
            self,
            projector,
            eval_func,
            base_lr,
            max_epochs,
            is_save_data=False,
            is_auto_stop=is_auto_stop,
            verbose=verbose,
        )
        time_swap_only = time.time() - start_time_swap_only

        if is_save_data:
            # Calculate fidelity after SWAP-only training
            fidelity_train_swap_only = _average_fidelity(
                self, "train", projector
            ).item()
            fidelity_test_swap_only = _average_fidelity(self, "test", projector).item()

        # Allow all gates to be trained
        for V_circuit in self.V_circuit_list:
            V_circuit.requires_grad_(True)

        # Train all gates
        if verbose:
            print("Training on all gates.")
        start_time_all = time.time()
        _train(
            self,
            projector,
            eval_func,
            base_lr,
            max_epochs,
            is_save_data=is_save_data,
            is_auto_stop=is_auto_stop,
            verbose=verbose,
        )

        if is_save_data:
            time_all = time.time() - start_time_all

            # Calculate fidelity after training all gates
            fidelity_train_all = eval_func(self, "train", projector).item()
            fidelity_test_all = eval_func(self, "test", projector).item()

            if not os.path.exists(self.data_directory_name):
                os.makedirs(self.data_directory_name)

            csv_file_name = os.path.join(
                self.data_directory_name,
                f"swap_fidelity_time_dataset={self.train_unitary_set.__len__()}_d={self.slot_dim}.csv",
            )
            if not os.path.exists(csv_file_name):
                with open(csv_file_name, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [
                            "seed",
                            "num_slots",
                            "ancilla_dim",
                            "train_mode",
                            "fidelity_train_swap_start",
                            "fidelity_test_swap_start",
                            "time_swap_only",
                            "fidelity_train_swap_only",
                            "fidelity_test_swap_only",
                            "time_all",
                            "fidelity_train_all",
                            "fidelity_test_all",
                            "time_train_swap",
                            "time_overall",
                            "swap_loss",
                        ]
                    )

            swap_start_only_all_fidelity_time_item = (
                self.seed,
                self.num_slots,
                self.ancilla_dim,
                self.train_mode,
                fidelity_train_swap_start,
                fidelity_test_swap_start,
                time_swap_only,
                fidelity_train_swap_only,
                fidelity_test_swap_only,
                time_all,
                fidelity_train_all,
                fidelity_test_all,
                time_train_swap,
                time.time() - start_time_overall,
                swap_loss,
            )

            with open(csv_file_name, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(swap_start_only_all_fidelity_time_item)

    if is_save_data:
        # Extract the highest fidelity for each combination of num_slots and ancilla_dim
        try:
            import pandas as pd
        except ImportError as e:
            raise ImportError(
                "The pandas library is required to run this function. Please install it using 'pip install pandas'."
            ) from e

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_name).round(4)

        # Pivot the table to have num_slots as rows and ancilla_dim as columns, with max fidelity_test_all as values
        pivot_table = df.pivot_table(
            index="num_slots",
            columns="ancilla_dim",
            values="fidelity_test_all",
            aggfunc="max",
        )

        # Save the pivot table to a new CSV file
        max_fidelity_filename = os.path.join(
            self.data_directory_name,
            f"max_fidelity_dataset={self.train_unitary_set.__len__()}_d={self.slot_dim}.csv",
        )
        pivot_table.to_csv(max_fidelity_filename)
        if verbose:
            print(f"Saved max fidelity table to {max_fidelity_filename}")

    return fidelity_train_swap_only


def _train(
    self: PQCombNet,
    projector: Optional[torch.Tensor] = None,
    eval_func: Callable[
        [PQCombNet, str, Optional[torch.Tensor]], torch.Tensor
    ] = _average_fidelity,
    base_lr: float = 0.1,
    max_epochs: int = 1000,
    is_save_data: bool = False,
    is_auto_stop: bool = True,
    verbose: bool = True,
    alpha: float = 1.0,
) -> torch.Tensor:
    r"""
    Train the model using the provided parameters.

    Args:
        projector: The projector tensor used for fidelity calculations. If `None`, a default projector is used.
        eval_func: Optional custom evaluation function to replace _average_fidelity.
            The function must accept the following keyword arguments:
                - self: PQCombNet instance
                - fid_type: str, "train" or "test"
                - projector: Optional[torch.Tensor]
                - alpha: float, weighting parameter for fidelity and probability of success
            and return a torch.Tensor.
        base_lr: The base learning rate for the optimizer.
        max_epochs: The maximum number of training epochs.
        is_save_data: If `True`, saves the training data and results to the specified directory.
        is_auto_stop: If `True`, enables early stopping based on convergence criteria.
        verbose: A flag to indicate whether to output training information.
        alpha: Weighting parameter for fidelity and probability of success in the evaluation function.
            alpha=1.0 means only fidelity is considered; alpha=0 means only probability of success.
            Custom eval_func must support this argument.
    Returns:
        Depending on the presence of projector and training outcome, returns loss, fidelity, and probability of success.
    """
    if not list(self._V_circuit_list.parameters()):
        loss = 1 - eval_func(self=self, fid_type="train", projector=projector, alpha=alpha).item()
        fidelity = eval_func(
            self=self, fid_type="test", projector=projector, alpha=1
        ).item()
        prob_success = eval_func(
            self=self, fid_type="test", projector=projector, alpha=0
        ).item()
        if verbose:
            print(
                f"[{self.task_name} | {self.train_mode} | {self.seed}] "
                f"Loss: {loss:.8f} | "
                f"Fidelity: {fidelity:.8f} | "
                f"Probability of Success: {prob_success:.8f}"
            )
        return loss, fidelity, prob_success

    opt = torch.optim.Adam(self._V_circuit_list.parameters(), lr=base_lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, "min", factor=0.1)

    time_list = []
    start_time = time.time()
    for itr in range(max_epochs):
        time_list.append(time.time() - start_time)
        _print_progress_bar(itr + 1, max_epochs, prefix="Progress", verbose=verbose)

        loss = 1 - eval_func(self=self, fid_type="train", projector=projector, alpha=alpha)
        # train_fidelity = eval_func(
        #     self=self, fid_type="train", projector=projector, alpha=1
        # ).item()
        # train_prob_success = eval_func(
        #     self=self, fid_type="train", projector=projector, alpha=0
        # ).item()
        # if verbose and (itr % 10 == 0 or itr == max_epochs - 1):
        #     print(
        #         f"[{self.task_name} | {self.train_mode} | {self.seed}] "
        #         f"Iteration: {itr + 1} | Loss: {loss:.8f} | "
        #         f"Train Fidelity: {train_fidelity:.8f} | "
        #         f"Train Probability of Success: {train_prob_success:.8f}"
        #     )

        if _log_progress(
            self=self,
            itr=itr,
            loss=loss,
            time_list=time_list,
            base_lr=base_lr,
            current_lr=scheduler.get_last_lr()[0],
            max_epochs=max_epochs,
            projector=projector,
            is_save_data=is_save_data,
            is_auto_stop=is_auto_stop,
            verbose=verbose,
        ):
            break

        opt.zero_grad()
        loss.backward()
        opt.step()
        scheduler.step(loss)
        start_time = time.time()

    fidelity = eval_func(
        self=self, fid_type="test", projector=projector, alpha=1
    ).item()
    prob_success = eval_func(
        self=self, fid_type="test", projector=projector, alpha=0
    ).item()

    if is_save_data:
        V_circuit_lists_dir = os.path.join(self.data_directory_name, "V_circuit_lists")
        os.makedirs(V_circuit_lists_dir, exist_ok=True)
        save_path = os.path.join(
            V_circuit_lists_dir,
            f"V_circuit_list_{self.train_mode}_sd{self.slot_dim}_ns{self.num_slots}_na{self.ancilla_dim}_itr{itr}"
            + (f"_fid{fidelity:.5f}.pt" if fidelity >= 0 else ".pt"),
        )
        torch.save(self.V_circuit_list, save_path)
    if verbose:
        print(
            f"[{self.task_name} | {self.train_mode} | {self.seed}] Finished training"
            + (f" with Fidelity: {fidelity:.8f}" if fidelity >= 0 else "")
            + (
                f" with Probability of Success: {prob_success:.8f}"
                if projector is not None
                else ""
            )
        )
    if fidelity < 0:
        return loss
    elif projector is None:
        return loss, fidelity
    else:
        return loss, fidelity, prob_success
