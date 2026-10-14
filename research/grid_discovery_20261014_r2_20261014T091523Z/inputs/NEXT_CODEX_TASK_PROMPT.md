# NEXT CODEX TASK PROMPT — independent audit, then bounded extensions

状态：**CODEX_RUN_READY（可开始 preflight；不代表外部工具已连通或研究结论已由 Codex 验证）**。

你收到的是已实际执行的 Pro 研究及其未提交补丁，不是要求用户手写代码的任务清单。先完整阅读 `THEORY.md`，严格区分该文的解析证明、精确有限枚举、finite-support 浮点旁证及未决问题。优先完成 T1/T2 的独立反证审查；T3 是实际电路转移；T4 才是新族探索。全部输出到新的 `research/grid_discovery_20261014_r2_<unique>/`，不得覆盖 r1 或 frozen 输入。

## 0. 输入、GitHub 与有界 Luna preflight

仓库：https://github.com/tengxianglin/EfficientUnitaryInversion
目标分支：`codex/eui-grid-pro-20261014`
Pro 读取的基准提交：`62fa763aff42e4bedf82b5de19bc9f05c5ed83b2`
已有 draft PR：https://github.com/tengxianglin/EfficientUnitaryInversion/pull/2
Pro 未创建新远端提交。`github_delivery.json` 中 push=false 不能改写成成功。

冻结路径：`research/pro_handoff_20261014/`。原输入 ZIP SHA256：
`bf8c6941078ac7d7f8086d83299eeac68a8a7cb169f3422c5389044576c0fb0d`
NEXT_PRO_PROMPT.md SHA256：
`90794f527ec34639451c51036653f3123c8f29981cf39fad2790a7b5abb4d3b0`
八例 JSON SHA256：
`ec33ce9f9f8f66b08ea0345016c8e6a3c11d0be8c68a7f4928258ff1040bd386`
原 abstract JSON SHA256：
`fd7d62aeeed96f72bdf740c9f9aeed45bf00f5f9c78fc4417bdada5e44c9cf74`
其他源和新代码 hash 以 delivery manifest 为准。

先做一次**有界 Luna 在线工具发现**：上限5分钟、最多两轮发现调用，只确认工具入口、身份/项目与可用CPU资源，不提交计算作业、不枚举私人目录或读取凭据、不假设旧工具仍可用。未知必填字段从工具schema读，不猜参数。工具发现失败应记录原错误及时间，仍可做无网络CPU独立实验；不要将“找不到Luna”当作科学结论。任何GPU探测若发生，第一次失败后至少等待60秒再复探，才记录为不可用；本任务默认 GPU=0，不需要为CPU整数任务主动占GPU。

本项目是QuAIR；禁止使用QudeLeap专用a6k/a6k2。任何可选GPU必须现场显式绑定可用设备，留至少20%显存余量；无授权不得开付费VM。下述正式任务全部CPU即可，最大并发1、总上限30 CPU-min、磁盘上限300MiB。每任务单独限时，超限写timeout，不静默缩小覆盖后还叫正式完成。外部shell命令先检查工作树，不能覆盖用户未发布改动。

GitHub preflight：读取当前ref与PR状态；若tip变化，检查frozen内容hash及新增目录冲突，不reset、不force-push。在目标分支或从其最新已审查tip派生的codex/分支应用 `grid_discovery_20261014_r1.patch`。先 `git apply --check`，确认所有路径只在r1目录。运行冻结verifier、r1 pytest和一次fresh复现后再commit/push，沿用draft PR2或新建draft PR。记录实际新commit并回读远端ref/关键文件验证。若仍无写能力，继续独立科研并输出第二轮补丁；不要求用户补代码或拼命令。

## T1 — 独立物理嵌入与 cubic law 审查

绑定 H1/H2/H3，目标是主动推翻973/37、phase defect或H³闭合中的任一项。**不要导入 r1 的 rank/bil/qval/mul_tag/embed_condition/power_support。** 可读取其输出作为最后的对照，但先独立计算。

负责新文件：`code/audit_rref.py`，接口：

```bash
python code/audit_rref.py --n 3 --all-ordered-bases \
  --source /path/to/r1/results --output /fresh/T1
```

实现路线：枚举F2⁶所有四维子空间的RREF（应为651个）；各子空间独立枚举GL(4,2)的20160组有序基。分别用 x,z 点积计算q0与omega，统计(B,q)，避免复制r1的四层物理基枚举。内层可用独立C++实现，Python仅协调。若纯Python超过预算，不悄悄少跑；先完成651个canonical基诊断，再将正式枚举标timeout/partial并保留coverage。

最便宜kill：Bmask1,qmask3；证明其radical全奇异、商Gauss sum−8，要求枚举计数0；四量子比特给定grid应通过。随后n2全空间20160基必须给280类型。只有kill/control均过后，才跑n3。

包络独立核验：对64个B各取一个明确四量子比特lift，用**稀疏整数矩阵或独立单字母表**计算所有H²单项式及所有H³完全对称三项系数；不要以Jordan closure直接代替。检查每个Δ1点的三对分解，六点张成W；逐行验证七情况H³证书，不从已有T值反推结果。六线相位以实际Pauli矩阵乘积计算，并独立重建完整Gram。72群仅用于对照轨道数，不先按r1 orbit代表筛输入。

范围与预算：CPU≤1核、≤8 CPU-min；RAM≤1GiB；磁盘≤80MiB；seed无（完全枚举）。n3目标13,124,160有序基、973类型、37个quadratic轨道；这些是待反证预期，不是硬编码筛选条件。首个矛盾立即保存最小(B,q)/grid、两种计算路径和输入hash，停止相关定理升级，不删除已完成数据。

原始产物：RREF列表、每基型计数、每允许类型至少一个物理witness、每禁止类型的判据、完整64型H²/H³系数/phase、轨道canonicalizer及测试、机器ledger。支持范围仅proper独立网格；不推断一般coeff子空间。

## T2 — 最关键：多Kraus振幅/真实span/comb归约独立审查

绑定 H4/H5。不要只重复LCU矩阵成功。负责：`proofs/one_query_audit.md`、`code/audit_comb_indices.py`、`results/T2/`。这是有限维解析审查加低维整数证书，不需要CVXPY。

分三步给逐条通过/失败结论：

1. 从一次查询 `L_mu(U)=sum A U B` 和目标Choi rank1推导标量函数。对单射线以本征投影trace取出a(t)的有限频率集合，分别验证T的∩(S−λ)={0}及†/*的∩(S+λ)。检查简并、a(0)=0、多Kraus、参数相位、不同射线共享I。反例控制S={1,-3}与{9,-3,-15}必须保留非零相位；负控制S={7,-5,-3,1}必须得到空交集。不能用只要求固定c的线性系统替代这一步。
2. 独立证明混合偏导使span{U(alpha)}等于Pauli坐标包络（九独立变量）。从所有成功L_mu在whole algebra上的延拓，明确写出一个任意逻辑V的**一次**原oracle模拟与目标C*/C^T解码。rank2的四中心扇区不得只取一个扇区而丢掉coherence。†的SU2下界应由反对易线子族获得；不能误用普遍U(8) no-go。
3. 在**不同于r1的tensor顺序**（推荐 i,b,a,o）重新实现comb trace/reshuffle，转换后核对三个整数primal/dual证书。生成每个矩阵单位的目标线性map；核对trace规范、Q²=dQ、Tr_aQ=I、上界p≤1/d²。用错误次序作为必须失败的negative test。adjugate2要核对等式 YU^TY=Tr(U)I−U。

命令：
```bash
python code/audit_comb_indices.py --dims 2 4 --targets transpose adjugate2 \
  --certificates /path/to/r1/results/comb_certificates.json --output /fresh/T2
```

预算：单核≤5 CPU-min、RAM≤1GiB、磁盘≤30MiB；无需GPU或solver。最便宜kill是d2 tensor索引和相位正控制。若解析步骤不能成立，精确指出失败量词并标`PRO_FOLLOWUP_REQUIRED`；即使数值仍准确也不能保留“全物理最优”标签。若证明与整数证书通过，停止无价值的大d8 SDP；该问题已经有精确上界和达到它的构造。

可选solver旁证仅在预先存在合法依赖时运行逻辑d2，PSD变量16×16，wall≤60秒；不安装未授权付费solver，不把状态optimal当作全参数证书。不是正式T2前提。

## T3 — 目标感知的实际编码、中心与电路成本

绑定 H5/H6。输入r1 `results/validation/all_anti_grids.json`（30例）、`results/exact/embedding1024.json`（选37物理quadratic轨道各一例），以及单量子比特S门错误公式控制。负责 `code/audit_transport.py` 与 `code/compile_all_anti.py`。

算法：每个选中physical W做辛Gram–Schmidt，显式求中心projector及二维/四维块。用Pauli方程构造等距编码，不能只返回抽象isomorphic。对rank2，输出所有四扇区和转置下其置换；对rank4，输出M4⊗I2重数。代码可用精确二次代数数或浮点加逐矩阵单位校验，记录使用哪一种。

最便宜kill：C=diag(1,i)的naive T迁移必须失败，C*/C^T版本必须通过。随后验证30例star witness和两辅助位逆电路，并输出实际有序门列表。SELECT用controlled-A、controlled-D分解，记录known one/two-qubit门数、A、总workspace、K=P=Q=1、后选及成功率。不得将multi-controlled已知门或硬件SWAP成本省略后叫门最优。验证成功块及带参考系统的Choi，不只单态fidelity。

命令：
```bash
python code/audit_transport.py --representatives quadratic37 \
  --input /path/to/r1/results --output /fresh/T3_transport
python code/compile_all_anti.py --input /path/to/r1/results/validation/all_anti_grids.json \
  --seed 20261015 --samples-per-grid 3 --output /fresh/T3_circuits
```

预算：单核≤7 CPU-min、RAM≤2GiB、磁盘≤80MiB，GPU0；同时仅一个≤128×128电路矩阵。float路线complex128/tol1e−10，失败后仅对同一例用高精度复核，记录两次结果。超过预算时先做star/dagger30例这一独立子任务，37例编码标partial，不把缺编码的轨道说成完成。产出grid、basis、center permutation、参数sign map、input/output target编码、门列表、raw系数和残差、逻辑/物理查询合同。

这可支持成本可迁移性与构造正确，不证明辅助位或已知门最少。

## T4 — 真正的新边界：绑定系数会破坏哪一步？

绑定H3/H4/H5的最小假设审计。输入四个grid：matched q4 partial与saturated；r1的B4,q0二次失败例；B55,q0全反对易例。先用r1输入中的九参数独立族作阳性控制，再研究下面明确的C矩阵：

- row-tied：C_{3r+c,s}=δ_{r,s}，C为9×3。
- column-tied：C_{3r+c,s}=δ_{c,s}，C为9×3。
- uniform：C为9×1全1。

H(beta)=Σ_j (C beta)_j P_j，beta全实域。负责 `code/tied_coeff_span.py`，不得只把九参数的coordinate T裁剪。

实现：完整span先精确展开k=0…7的所有独立beta单项式；每个单项式系数作为64维Pauli**向量**保存，用Gaussian-rational消元求实际span和转置线性限制。8×8 Cayley–Hamilton保证完整span可用k≤7覆盖，但不能据此断言奇偶分级也已闭合。若计算分级，对H²另用Cayley–Hamilton，even取H⁰,H²,…,H¹⁴，odd取H¹,H³,…,H¹⁵；绑定族至多3变量，这个预算可行。九参数control只取本轮已证明的三次完整span，未证明的额外graded闭合不作假设。不要把union support大小当span秩。然后计算每个低维family中一个预先规定整数射线集合 beta∈{-1,0,1}^m\{0} 的精确谱对称性；可取特征多项式的monic square-free part f，degree=D，候选γ=-2[x^(D-1)]f/D，再精确检查f(γ-x)=(-1)^D f(x)，避免昂贵根式且正确忽略重数。只找phase-aware kill，不将所有有限射线通过称为全域可行。

先检验绑定对易三项均匀系数谱{3,-1}与独立系数(1,2,4)谱{7,-5,-3,1}的差异；没有这个控制就停止。对于没有找到kill的族，解固定线性map是诊断而不是通道证书；给出具体未闭合振幅条件。

命令：
```bash
python code/tied_coeff_span.py --grids matched_q4 B4q0 B55q0 \
  --constraints independent row column uniform --span-max-degree 7 --graded-max-degree 15 \
  --rays ternary --output /fresh/T4
```

预算：单核≤8 CPU-min、RAM≤2GiB、磁盘≤100MiB；最大并发1；seed无（固定有限射线）。independent控制可用k≤3检验本轮定理，再逐绑定族完整span到k≤7、graded到k≤15。首个support≠span的例子保留原系数矩阵与rank证书；首个谱kill保存精确特征多项式与射线。未完成时按grid×constraint coverage报告，不猜缺项。T4无统一成功率目标；有限不反证不能升级为已存在物理仪器。

## 交付与停止规则

返回理论审查结论、实际实验（含失败）、原始fresh输出、hash/manifest、GitHub实际commit/PR与远端回读、下一轮Pro指令。每个claim使用`analytic-checked`、`exact-finite`、`finite-support`、`falsified`、`not_run`或`PRO_FOLLOWUP_REQUIRED`之一并解释范围。原有35个嵌入反例、H²反例、S门反例和两个参数相位正例都必须保留。

T1/T2若通过，停止重复大规模随机网格搜索及d8盲目SDP；研究增量转向T3的真实编码或T4的系数子空间。遇到已知文献完整覆盖时说明归属并停止包装成新颖结果；遇到真正反例则缩小定理，不改历史证据。不得重做已解决的49方向扫描并将其当新贡献。
