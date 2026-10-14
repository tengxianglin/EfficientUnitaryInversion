# Heisenberg 补充实验与 Pro 交接

本轮完成了上一轮留下的可执行检查：各边独立耦合、三角形固定门的适用系数域、基本门编译、系数失配、显式低维映射与中心分块。另补了一个允许参数相关全局相位的确定性反演例子。全部在 quair01 CPU 上运行，GPU 用量为 0。

## 已完成的结果

| 检查 | 结果 | 主证据 |
|---|---|---|
| 49 个 primitive 整数耦合方向，系数在 [-2,2]、识别整体正负号 | 7 个有固定门，42 个有固定振幅线性障碍 | exact_extensions_v2.json：triangle.rays |
| 三角形符号谱 | 特征多项式精确等于 `(x-S)^4*((x+S)^2-4D)^2` | triangle.symbolic_charpoly_exact_match |
| 原均匀门 V 的9项系数域 | 反对易方程的核只有 `(1,1,1,1,1,1,1,1,1)` 一维 | triangle.uniform_V_allowed_9_term_coefficient_kernel |
| 零和耦合平面 | 同一个 W 反演全部 `J12+J23+J13=0` 实耦合，Q=1,A=0,p=1 | triangle.zero_sum_W_exact_checks |
| 18 个独立边系数参数族 | 7 个 XZ 二分图有单 Pauli 门；11 个有声明范围内的切片反证 | edge_families.cases |
| N3 open-chain 电路转移 | 六个 XYZ 项逐一映为 `M4 tensor I2`，XZ 的 `YIY` 反演门可提升回原系统 | transfer |
| N4 中心分块 | XXXX、ZZZZ 与各边项对易；四个正交完备投影各 rank4 | transfer.N4_* |
| 两个3-qubit门 V/W 的12个编译配置 | 每次已知门均19 CX、depth39；不含未知U本身成本，不是最优性证明 | compilation_v2.json |
| 编译后的均匀族35例、零和族35例 | 最大矩阵残差分别约8.66e-14、2.93e-14；含无反演门基线 | uniform_family、zero_sum_W_trials |
| 15个耦合失配格 | epsilon=0.1,t=1时过程保真度0.9605304970；仅为理想参数失配诊断 | frozen_coupling_imbalance_diagnostic |
| 单边XYZ的相位协变通道对照 | 两个workspace qubits、一次forward U、p=1；输出 `exp(2ia)U†`，workspace回到00 | phase_covariant.json |
| 相同49方向的仿射谱检查 | 13个关于某中心反射对称，36个不对称；仅声明有限域谱性质 | affine_controls.json：rays |
| 新方向 J=(1,4,4) 的编码对照 | Q1/A1/p1，输出 `exp(6ia)U†`，workspace回0；17个数值样本通过 | affine_controls.json：representative |

## 三角形中已解决的分类

令 `B12=XXI+YYI+ZZI`、`B23=IXX+IYY+IZZ`、`B13=XIX+YIY+ZIZ`，`H(J)=sum J_e B_e`。定义

`S=J12+J23+J13`，`D=sum J_e^2 - sum_{e<f} J_e J_f`。

精确谱为 S（四重）、−S±2sqrt(D)（各两重）。实耦合下 `D=1/2 sum_{e<f}(J_e-J_f)^2`。其不同本征值集合关于0对称，当且仅当 `S=0` 或 `D=0`；后者就是三边耦合相同。

证明需区分退化：D=0直接给±S；S=0给0、±2sqrt(D)。若D>0且S不为0，三特征值互异时，对称的三点集合必须含0，但令一个非S本征值为0后另两点是S、−2S，不能互为相反数。碰撞D=S²不为0时只剩S、−3S，也不对称。这补上了49方向扫描之外的一般代数论证。

对已知方向J、未知全体实振幅a，固定复线性关系 `L(exp(-iaH(J)))=c exp(+iaH(J))`、c固定非零，要求本征值集合关于0对称。可从不同指数频率的线性无关性直接推出。两类充分性分别由显式V和W证书给出。

零和平面的门为 `W=Psym+i/sqrt(3)[P12,P23]`，其中Pij是SWAP，`Psym=(H_uniform+3I)/6`。同一个W覆盖整平面；它与均匀H对易，不能替代均匀反演门V。零和平面需要有正有负的耦合；若限定所有J_e非负，仅剩原点。一般线性耦合子空间若可由一个固定门反演，必须包含在上述平面或均匀直线之一；子空间不能跨两类任取向量。

上述结论没有解决任意一次查询量子通道。单边XYZ已经给出反例：尽管 `H²-3I=-2H` 排除了固定c，固定编码器却可把成功块做成 `exp(2ia)U†`，从而确定性实现同一目标通道。输出的参数相关全局相位在密度矩阵上消失。这个例子不能反过来推广成所有独立XYZ系数都可反演。

另一个校准例取J=(1,4,4)，其能量-15（2重）、-3（2重）、9（4重）关于-3对称。通过一个workspace qubit的显式编码，一次查询的输出为exp(6ia)U†且workspace返回0。这个方向在原[-2,2]扫描外，单列为构造对照。相同49方向另有13个仿射谱对称例；这组谱检查不作为任意multi-Kraus通道的必要充分性结论。

文献新颖性均未审查。三角形谱来自spin-trimer/S3表示，固定门存在不等于新机制或查询优势。

## 执行与复核

Python 3.12.7，NumPy1.26.4、SciPy1.13.1、SymPy1.13.2；Qiskit2.2.3仅安装到本次远端isolatedvenv。每进程单CPU线程。最终两份主脚本walltime分别3.1848秒、3.1149秒；准备、安装、分析和打包耗时不计入这个计算时间。GPU·h=0。

`source/`保留第一版；`source_v2/`增加了N4逐项中心性断言和N3逻辑矩阵输出，输入参数与阈值不变。第一版结果保留，最终以`exact_extensions_v2.json`、`compilation_v2.json`为准。`source_phase/`和`phase_covariant.json`是追加的单边相位对照。所有结果为未提交工作区证据，不能以仓库HEAD代替源码快照。

根代理用独立Kronecker构造核对W、49个最小多项式及旧18配置的边界。独立审查另核对了三角形一般谱分类和电路转移。门编译结果保存operations与global_phase并重建Operator核对。Qiskit wire(2,1,0)对应原Pauli的sites(0,1,2)，U和已知门始终使用同一矩阵排序。

`FINAL.sha256`保留远端工作目录的basename布局，核对本地副本时Python将.py映射到source_v2/。它不是直接在本地根目录运行`sha256sum -c`的清单。最终本地统一清单为`MANIFEST.sha256`；两个交接包各有可直接使用的`CHECKSUMS.sha256`和独立验证脚本。

## 剩余大问题

1. 允许参数相关全局相位/振幅和任意多Kraus通道后，一次查询的可行性、最优成功率和辅助空间应如何判定？单边相位对照及两类p=1三角形作为校准例。
2. 一般加权Heisenberg图的哪些耦合子空间共享固定反演门？怎样把系数约束、目标作用、中心和表示重数一起纳入电路等价与转移？三角形分类和N3/N4实例已解决，不再把它们当待证猜想。

这两个方向分别打包。包内只含科研定义、结果和可运行脚本，不含原音频、私人通信、完整Obsidian笔记、凭据或运行日志。全局文献Open Problem身份尚未核验，Pro须先查最近邻工作。
