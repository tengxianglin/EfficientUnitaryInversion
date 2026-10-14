你的回复必须依次完成两项交付：
1. 理论推导：明确假设、对象、等价关系和资源合同，提出并推导可核查的规律；保留失败猜想及其最小反例，给出修正版命题或明确的未决缺口。
2. Codex 的下一份可执行实验方案：把你的推导连接到独立且有界的实验任务，写清输入、实现、对照、预算、停止规则，以及哪些结果能支持或否定哪条猜想。

这是 EfficientUnitaryInversion 的新一轮研究。请你主导发现规律和理论延伸，在你当前可用的 ChatGPT 计算环境实际做小规模实验；更多资源的实验再交 Codex。Codex 执行后会返回原始结果、证据包和下一份 Pro 指令，你再继续推导与规划。用户只转递文件和启动各轮。一般性点评或未来工作列表不足以完成这轮。

一、先读取与核验

阅读 README_FOR_GPT_PRO.md、context/GRID_PROBLEM.md、context/CURRENT_PROGRESS.md、context/OTHER_OPEN_QUESTIONS.md。通过 verify_bundle.py 和 BUILD_MANIFEST.json 检查完整性，按 context/SOURCE_MAP.json 核对来源和缺失项。所有文件路径相对包根。GitHub 中包根是 research/pro_handoff_20261014/。

二、在理论和实验选型前做聚焦的在线文献检索

查阅原始论文，比较有限几何与 Pauli 网格、symplectic/quadratic forms、stabilizer/contextuality、operator/Jordan/Clifford algebras、representation intertwiners、unitary inversion/supermaps 和 LCU/Fourier 方法的最近邻工作。检索范围随有用线索调整，不必把每个领域都综述一遍。记录检索日期、真实链接或 DOI、全文/摘要访问范围、相关定理/公式/页码，并说明原文结论与本轮推断的区别。检索改变方法时说明原因。没有找到直接命中不能证明新颖性；无法浏览时保留文献判断为未决。文献综述不能替代理论推导。

三、第一优先级：发现 3×3 横竖规律

原始任务是多找九个三量子比特 Pauli 组成的 proper 3×3 网格，每行每列任意两项相乘，忽略整体相位后得到第三项；进一步分析横竖的对易/反对易、相位和全局一致性。现有“乘法规则不足以唯一决定成本”的反例是出发点，请继续寻找正确的更强规律。

请把同一个对象放到多种表示空间中比较，主动选择能暴露遗漏信息的表示。可考虑下列候选视角；它们只是探索方向，不是要求成立的命题或固定路线：
- F2 标签、四生成子块、张量/rank-one 描述与有限射影几何；核查与 Segre/quadric 等对象是否确有对应及其适用范围。
- 完整 9×9 commutation Gram、带符号图、行列 incidence hypergraph、谱与 automorphism/orbit invariants；六条局部线与跨线关系分开。
- Z4 相位 cocycle、quadratic refinement、Y-parity、行列乘积符号与可能的 contextuality constraints。
- 真实 H(alpha)^k 的符号系数、graded exponential envelope、Jordan/associative/Lie closure、中心及 Wedderburn/表示重数分解。
- Walsh/Fourier character、LP primal/dual certificates；向量化、Liouville/Choi、较高阶张量或 polynomial features，用来揭示粗粒度统计丢失的结构。

不要求把高维表示都用一遍。每种被采用的表示要解释：保留或丢掉什么信息、允许什么等价变换、对哪个目标有用，以及为什么可能形成更简单的规律。可做降维/聚类/符号回归辅助发现，但新规律需要独立检验或证明。

先提出若干非等价的可证伪猜想，目标为 3–6 条有实质区别的候选；如果实际只支持更少，解释原因即可。候选可以关于：横竖模式的允许集合/约束、最小完整不变量、包络何时饱和、成本何时下降、物理嵌入条件、某一更一般 family 或电路构造。每条写清量词、假设、预测、最小失败例子、已有校准对和 cheapest falsification test。不要先把尚未检验的猜想写成定理。

对已有数据先做独立、小成本校准。八个物理例子中有两个不是完整网格的控制，不要混入 proper population；当前 frozen S1 与 custom_S1 要分开。matched pair same_W_q4_* 在相同 W、rank、odd-Y 计数、反对易边数下仍有不同包络和 lambda，是强制反例校准。若使用学习/统计发现，预先按非等价类划分发现与检验集合，避免等价重排泄漏；预测 lambda/T_L 时不能把答案自身或其直接编码喂入输入特征。

原始 abstract census 的 1024 cases/44 classes 不应被直接称为已穷尽物理表示。源码的 three_qubit_realizable_rank 只检查 rank∈{2,4}。请核查标准计算基转置下 q、相位 lift 和具体 Pauli 表示是否还限制嵌入；若有差异，给出精确条件和明确 witness/counterexample，若没有则证明充分性。这一问题目前未决，不预设 census 有错。也要明确 72 阶 grid group、物理 Clifford 等价和 target-preserving 等价是否为同一关系。

四、你在 ChatGPT 自身计算环境中实际运行小实验

先探测并报告你真实拥有的代码执行、CPU/RAM/超时、网络与 GitHub 工具。使用实际可用的内置计算环境；没有代码执行能力就明确标 not_run 并给 Codex 可执行任务，不能虚构云端实验、日志或资源。

先运行廉价 sanity/counterexample gate；优先精确 F2、Gaussian-integer、有理数或符号检查，再以明确 dtype/tolerance 的数值旁证辅助。初始云端探索总预算建议不超过 30 CPU-min；单批受实际工具超时和内存约束，必要时分批并保存断点。没有已授权的外部付费资源时不新开付费 VM。超过可用环境或本轮小实验预算的任务说明复杂度、内存和预计成本，移交 Codex。

把本轮每个实际尝试写进 machine-readable hypothesis/experiment ledger：假设、表示、输入 hash、命令、软件版本、seed、已知对照、输出、终态、反例、证明状态及局限。小规模通过标 finite-support，不升级为全域定理；失败也保存并分析最弱修正。source/grid/ 两个脚本可作为参考，但独立 checker 应避免复制同一个核心错误。每次写 fresh output，保留原包文件。

五、GitHub 修改和交付

用户已授权你直接在 https://github.com/tengxianglin/EfficientUnitaryInversion 修改本轮相关研究代码与文档。先读分支 codex/eui-grid-pro-20261014 的当前 tip，确认写入工具确实可用。这个分支从远端 main 起步，并增加本包，避免混入本地其它未发布提交。

请在该分支或从其当前 tip 派生的新 codex/ 分支中，建立新的 research/grid_discovery_<unique-round>/ 目录。提交理论报告、假设台账、独立 checker、原始云端实验与复现命令、相关测试及你撰写的后续 Codex 方案。保持 research/pro_handoff_20261014/ 原样作为冻结输入；需要修正时写新文件并解释差异。沿用/更新该 draft PR，或为新分支建立 draft PR。不要用改变历史结果来消除反例。

实际 push 后给出 repository/branch/commit/PR URL，并重新读取远端 ref 或关键文件确认交付。工具若只能读仓库或不能 commit，提供可应用 patch/ZIP，明确 GitHub 修改尚未交付；不要把计划、生成文本或本地文件称为已提交。不要要求用户手工写代码、拼命令、补实验设计。

六、第二优先级：推进关联理论疑难点

从 context/OTHER_OPEN_QUESTIONS.md 选择与网格规律联系最强的一至两个问题。优先 target-aware 等价与高低维电路转移，或允许参数相关全局相位后的 one-query 物理可行性/最优成功率。三角形均匀线、零和平面和 N3/N4 具体实例已完成，不重复包装为未解决创新。普遍最优性、任意多 Kraus 情形、一般图和新颖性仍未解决。

U^T、U*、U† 始终分开；固定系数还是独立未知系数必须明示；矩阵等式、允许全局相位的通道等式、postselection 成功分支分别判断。固定非零标量线性 no-go 不能排除参数相关振幅/相位通道。记录 K/P/Q、用户辅助位、总 workspace、后选、p(theta)/p_min 及已知门成本；representation compression 保留原物理 oracle 的查询成本。

七、你撰写交给 Codex 的实验方案

每份独立任务必须绑定你本轮的一个推导/猜想/反例修正，包含：精确目标与假设、GitHub commit 和输入 hash、负责文件及接口、可实现算法、匹配对照、preflight、最便宜 kill gate、命令/步骤、fresh 输出、seed/覆盖范围、CPU/GPU/RAM/时间/磁盘/并发预算、成功/失败/停止规则、原始产物、独立复核和禁止外推的结论。资源不足应给出明确可缩小的诊断范围，不静默替代正式实验。前置条件齐全才标 CODEX_RUN_READY；无需进一步实验时给出有理由的 stop。

Codex 下一轮先做有界 Luna 在线工具发现，再执行有充分条件的任务。资源使用需现场检查；本项目为 QuAIR 项目，不能使用 QudeLeap 专用 a6k/a6k2。GPU 需显式绑定并留 20% 余量；一次探测失败不足以转 CPU，按既有规则至少 60 秒复探。你无需猜测本地空闲 GPU 型号，可给出设备无关的资源上限与最低要求，由 Codex 现场核实。

请返回自包含报告和一个 ZIP（附 SHA-256、manifest 和 GitHub 交付记录）。报告至少覆盖 Related Work / Method Choice、Derived Conclusions、Cloud Experiments Actually Run、Experimental Consequences、Next Codex Task Prompt、Unsupported / Unresolved。这些是你回复的交付要求，不是 Codex 已替你完成的内容。若推导或可执行方案缺关键前提，精确指出缺口并标 PRO_FOLLOWUP_REQUIRED；保留已完成部分和真实失败，继续可独立推进的工作。
