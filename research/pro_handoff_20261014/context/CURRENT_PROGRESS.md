# 当前可核查进展与边界

截至 2026-10-14，本包收集的主要科学产物来自 2026-09-05、09-07、09-09。本轮新增的是当前证据核对与交接准备，没有新增科学实验或 Pro 推导。

## 3×3 网格

`evidence/grid/grid_examples.json` 和 `source/grid/verify_grid_examples.py` 给出八个精确对照：

| 名称 | 六条行列规则 | dim W | rank omega | 包络坐标数 | lambda_T |
|---|---|---:|---:|---:|---:|
| custom_S1 | 通过 | 4 | 2 | 16 | 2 |
| new_structure_grid | 通过 | 4 | 4 | 16 | 4 |
| S2_frozen | 通过 | 4 | 4 | 10 | 1 |
| S2_same_W_saturated | 通过 | 4 | 4 | 16 | 4 |
| same_W_q4_partial | 通过 | 4 | 4 | 10 | 1 |
| same_W_q4_saturated | 通过 | 4 | 4 | 16 | 4 |
| frozen_S1_control | 未通过 | 5 | 4 | 32 | 4 |
| row_only_full_M8 | 未通过 | 6 | 6 | 64 | 8 |

matched pair same_W_q4_* 还保持同一 phase-free W、odd-Y 数 4、反对易边数 18，成本仍不同。full commutation graph 并未因此自动相同。

lambda_T 只指归一化 Pauli-conjugation LCU 字典中的转置成本；standard postselection 的 p=1/lambda_T²。T_L 指 H(alpha)^k 的精确符号系数涉及的 Pauli 坐标，不能替换成任意生成代数。独立系数是这些网格数据的默认前提。

后续 `independent_grid_certificates.json` 枚举 64 个 alternating forms×16 个 quadratic refinements=1024 个抽象情形，按 72 阶 grid automorphism group 分为 44 类。16 个 rank-0 情形反驳不加条件的早期包络分类。原代码把余下 1008 个 rank-2/4 情形标记为 three_qubit_realizable_rank；该标记仅检查 symplectic rank。标准转置二次型和具体物理嵌入是否还需限制，是本轮请 Pro 核查的未决项，不能仅凭字段名认为已逐一构造嵌入。

原 census 支持的抽象精确规律是：在 rank-2/4 范围，六条线全 commuting 时包络为 10 且存在 restricted-character one-Pauli witness；其余饱和为 16，饱和情况下 lambda_T=2^(rank omega/2)。这是待独立核对并解释其机制的既有结果；不等于任意 quantum comb 最优性。

## 9 月 7 日理论检查

主证据：`evidence/theory/verification_results.json`；源码 `source/theory/verify_new_theory.py`。

- literal odd-X 符号变换为 F_X(M)=Z^tensor n M^T Z^tensor n，可与对应 star 变换组成 dagger；同一包络的 Pauli-LCU L1 成本不变。
- “对易乘积项总能删除并保持等价”已被精确反例否定：{XI,IX,XX,ZI,IZ} 删除 XX 后累计包络维数从 10 变 9，丢失 YY。生成代数相同也不足以保留 dagger 的奇偶幂约束。
- Heisenberg 开放链的 XX/ZZ 标签 Gram rank 随边数奇偶变化。N 为奇数时有旁观/重数自由度；N 为偶数时有两个中心 bits，不能无条件解释为相同的简单逻辑系统。
- 两两反对易 Hermitian involutions 的既有 identity：U†=(-U+sum Gamma_j U Gamma_j)/(m-1)。标准构造 p=((m-1)/(m+1))²；maximal 2n+1 frame 给 p=[n/(n+1)]²。独立 labels 可能已有单个共同反对易 Pauli、lambda=1；dependent odd relation 的字典最优性有不同分支。一般物理 one-query 最优性和文献新颖性仍未解决。七生成元个例在旧项目稿中出现过的记录属于文档事实，本包没有完整稿件，需查原文。

## 9 月 9 日 Heisenberg 补充

主证据在 `evidence/heisenberg/`；最终结果使用 `exact_extensions_v2.json`、`compilation_v2.json`。

- 系数共用一个未知振幅的 18 个配置：8 个精确确定性反演正例、10 个 fixed-nonzero-scalar 复线性范围内的负例。
- 三角形 H(J)=sum J_e(XX+YY+ZZ)_e 的谱为 S（4 重）、-S±2sqrt(D)（各 2 重），S=sum J，D=sum J_e²-sum_{e<f}J_eJ_f。均匀线 D=0 和零和平面 S=0 各有显式固定门 V/W，Q=1,A=0,p=1；两门适用族不同。
- 49 个 primitive 方向是有限校准，不是一般物理通道分类。独立边系数的 18 族有 7 个 XZ 二分图 Pauli 正例与 11 个限定负例。
- N3 链已有显式 M4 tensor I2 表示和 XZ 门提升；N4 已验证两个中心与四个 rank-4 sector。保留原三量子比特 oracle，不产生免费的低维 oracle。
- V/W 的既有 Qiskit 编译各 19 CX、depth 39；完整线路使用该已知门两次，未知 U 另计。编译门数非最优性结论；参数失配也非硬件噪声实验。
- 单边 XYZ 有 Q1/A2/p1 的编码器，输出 exp(2ia)U†、辅助位回到 00；J=(1,4,4) 有 Q1/A1/p1 构造，输出 exp(6ia)U†。因此 fixed-c 矩阵障碍不能外推成逆通道不可能。

## 较早背景与元数据限制

- frozen S1 的 transpose 有 Q1/A4/p1/16 LCU 证书；一般 ancilla-free deterministic 构造仍未解决。它与 custom_S1 不是同一支持。
- frozen S2 的 dagger 有 K1/P3/Q3/A0 固定并行构造。证书中的 P=3 最早出现结论限于其声明的 SU(4) representation-intertwiner 模型；一般 sequential/comb 最优性未证明。
- `evidence/background/` 只附历史证书与配置，未附完整旧训练和认证依赖。配置的 search resource 与 exact certificate 的 construction resource 是不同记录。S1 配置和旧证书的 support_hash 字符串不一致，支持文字相同；哈希规范的来源尚未在本轮重建，不能用两个哈希做静默等同连接。
- 旧 Type-2.2.2 高 fidelity/“universality”结果不纳入本轮科学证据，因其 target convention 问题尚不能被历史标题消除。

所有上述 exact/数值/限定负例需继续保持类别区别。文件完整性核对不是新数学证明；有限检查不是全域定理；已有构造不是资源最优性或新颖性证据。
