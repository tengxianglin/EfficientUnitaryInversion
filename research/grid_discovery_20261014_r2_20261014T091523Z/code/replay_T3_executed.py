import json, hashlib
from pathlib import Path
import numpy as np
root=Path("results")
enc=root/"T3_transport_verified"
cir=root/"T3_circuits_streamed"
records=[json.loads(p.read_text()) for p in enc.glob("B*.json")]
assert len(records)==37
errs=[]
for rec in records:
 p=enc/rec["raw_arrays"]
 assert hashlib.sha256(p.read_bytes()).hexdigest()==rec["raw_sha256"]
 with np.load(p,allow_pickle=False) as raw:
  C=raw["C"]
  errs.append(float(np.linalg.norm(C.conj().T@C-np.eye(8))))
  assert raw["central_projectors"].shape[0]==(4 if rec["rank"]==2 else 1)
  assert raw["sector_isometries"].shape==(4,8,2) if rec["rank"]==2 else raw["sector_isometries"].shape==(1,8,8)
  for F in raw["matrix_units"]:
   V=C.conj().T@F@C
   errs.append(float(np.linalg.norm(F.T-C.conj()@V.T@C.T)))
samples=0
for p in cir.glob("B*.json"):
 rec=json.loads(p.read_text())
 for target in ("star","dagger"):
  gates=rec[target]["ordered_gates"]
  assert sum(g["gate"]=="ORACLE_FWD" for g in gates)==1
  assert not any(g["gate"]=="CY" for g in gates)
  assert sum(len(g["qubits"])==2 for g in gates if g["gate"]!="ORACLE_FWD")==rec[target]["cost"]["two_qubit"]
 for f in rec["raw_files"]:
  assert hashlib.sha256((cir/f["path"]).read_bytes()).hexdigest()==f["sha256"]
 for sample in rec["samples"]:
  n=sample["sample"]
  prefix=p.stem+"_sample"+str(n)
  with np.load(cir/(prefix+"_raw.npz"),allow_pickle=False) as raw:
   assert raw["coefficients"].tolist()==sample["coefficients"]
   K=raw["dagger_success_block"].copy()
   U=raw["oracle"].copy()
   errs.extend([float(np.linalg.norm(K-U.conj().T/2)),float(np.linalg.norm(raw["star_unitary"]-U.conj()))])
  circuit=np.load(cir/(prefix+"_dagger_circuit.npy"),allow_pickle=False)
  errs.append(float(np.linalg.norm(circuit[:8,:8]-K)))
  del circuit
  samples+=1
assert samples==90 and max(errs)<1e-10
summary={"status":"VERIFIED_SAVED_ARTIFACT_REPLAY","encodings":len(records),"circuit_samples":samples,"nontrivial_center_permutations":sum(rec["transpose_sector_permutation"]!=list(range(len(rec["sectors"]))) for rec in records),"max_replay_residual":max(errs),"artifacts_sha256_checked":True,"authoritative_transport":"results/T3_transport_verified","authoritative_circuits":"results/T3_circuits_streamed"}
with (root/"T3_saved_artifact_audit.json").open("x") as f:json.dump(summary,f,indent=2)
print(json.dumps(summary))