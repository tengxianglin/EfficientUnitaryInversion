# 3×3 Pauli 网格：相位补全、二次型嵌入与一次查询分类

研究轮次：grid_discovery_20261014_r1。日期：2026-10-14。

本报告按“理论推导 → 实际实验 → 下一轮可执行研究”组织。冻结输入未改动。GitHub 交付状态为 **未 push**；已读取的基准提交是 `62fa763aff42e4bedf82b5de19bc9f05c5ed83b2`，新增路径为 `research/grid_discovery_20261014_r1/`。完整补丁及交付记录随证据包提供。

**最重要的结论。** 六条线的反对易模式只给五比特，六条有序线乘积的总相位补上第六比特。三量子比特标准转置的物理嵌入还受二次型限制，1024 个抽象类型中恰有 973 个可以实现，而不是 rank-only 筛选得到的 1008 个。在九个系数独立的前提下，真实指数包络在三次幂前完成：全对易线型为 10 维，其他物理网格为 16 维。进一步得到下面的单查询目标分类；其一般物理上界来自本报告的振幅引理、线性张成论证及显式 comb 证书，不是由随机测试或 LCU 最优性冒充。

| 六线类型 | rank B | 抽象物理类型数 | 指数包络维数 | 最优 p(T) | 最优 p(*) | 最优 p(†) |
|---|---:|---:|---:|---:|---:|---:|
| 全对易 | 4 | 16 | 10 | 1 | 0 | 0 |
| 混合 | 2 | 495 | 16 | 1/4 | 0 | 0 |
| 混合 | 4 | 432 | 16 | 1/16 | 0 | 0 |
| 全反对易 | 2 | 30 | 16 | 1/4 | 1 | 1/4 |

这里的零表示整个承诺族上不存在非零成功的一次查询仪器；不是“只在某一点失败”的经验判断。表中所有正成功率均为常数，因而等于最坏情况成功率。973 是有序四生成子上的 (B,q) 类型数，不是实际 Pauli 网格总数、带符号 lift 总数或 Clifford 轨道总数。理论证明尚未经过第二位研究者独立审稿；下一轮优先审查第 7–9 节，而不是扩大随机样本。

## 1. 假设、约定与资源合同

每个条目是标准 Hermitian 三量子比特 Pauli 字符串，按 q0 q1 q2 排列；Y=[[0,-i],[i,0]]。网格 proper 表示九个非恒等条目两两不同，横竖每组三项 projective 相乘闭合。允许在讨论 family 等价时给条目加 ± 号，但必须同步改变其未知系数，不能在固定参数比较时丢弃这些符号。

本轮的主要承诺族是

\[
H(\alpha)=\sum_{g\in G}\alpha_gP_g,\qquad
U(\alpha)=e^{-iH(\alpha)},\qquad\alpha\in\mathbb R^9.
\]

九个系数**独立未知、全实域**。任意射线 tβ 均包含在承诺族内，且 α=0 时 U=I。对于系数绑定、只给离散参数、排除单位元或不同 oracle 时间合同，必须重新检查证明。不得把这里的独立九参数结论套到三条 Heisenberg 边仅各有一个系数的族。

物理合同：一次使用原始 8×8 forward U，不默认 controlled-U、U*、U† 或压缩维度的 oracle；允许任意参数无关的前后 CPTP 操作、有限辅助空间、仪器、多个成功 Kraus 分支，要求成功 CP map 对任意输入及其参考系统精确等于 p(α) 倍目标酉通道。允许各分支有参数相关复振幅。本文 K 表示串行查询层数、P 表示最大并行宽度、Q 表示总 forward 查询数；本轮构造均 K=P=Q=1。A 是原有三系统量子比特之外的干净用户辅助位；workspace=3+A，未把原系统中的中心标签或重数空间算作免费新增辅助位。

目标必须分开：T 是计算基转置，* 是逐元素复共轭，† 是伴随。概率、矩阵恒等式和通道恒等式在下文分别说明。

## 2. Related Work / Method Choice

2026-10-14 聚焦检索了原始论文；逐项真实链接、访问范围、页码/公式和未命中范围见 `RELATED_WORK.md`。方法选择先于本轮枚举。

Holweck–Saniga–Lévay 的有限几何处理确认了 Mermin 方阵与 Q⁺(3,2) 的联系，但不是每个 projective 网格的物理对易结构都等于该几何的极化。Hashagen 等对实 Clifford 群使用的 q=x·z 及 O⁺ 结构提示：rank-only 不是标准计算基转置问题的充分物理嵌入条件。Dehaene–De Moor 的 binary/quadratic Clifford 描述支持将 projective 辛结构、转置二次型和相位 cocycle 分层，而不是只保留 odd-Y 总数。

Kirby–Love 的 noncontextual Pauli Hamiltonian 工作是 closure/推断结构的邻近参考，不提供这里的真实 H(α)^k 包络等式。因此本轮直接计算 Gaussian-integer 单项式系数，不把 associative、Jordan 或 Lie closure 当作默认答案。Childs–Wiebe 的 LCU 架构解释概率下界；Quintino 等的 universal supermap 工作给出一查询逻辑转置的已知边界，促使本轮补上“承诺族如何合法归约到全逻辑代数”的证明，而不是直接引用 universal 下界套用结构化族。

方法链为：projective incidence → 六线及跨线 Gram → 实二次型嵌入 → Z4 lift → 精确多项式包络 → Walsh 有理证书 → 中心/矩阵块 → 多 Kraus 振幅及 comb 归一化。没有使用聚类、学习或把答案作为特征的回归。没有以检索未发现相同公式作为新颖性证明。

## 3. 四生成子、Segre 几何与相位补全

### 3.1 固定坐标

令 a,b,c,d 为左上 2×2 的四个种子，则九点为

```
a      b      a+b
c      d      c+d
a+c    b+d    a+b+c+d
```

四种子必须独立：它们张成至多四维；若至多三维，就只有七个非零向量，不可能容纳九个互异非零条目。取 W=F2⁴，a,b,c,d=e0,e1,e2,e3。代码采用整数标签

```
1   2   3
4   8  12
5  10  15
```

将 v 看成 [[v0,v1],[v2,v3]]，定义几何二次型 Δ(v)=v0v3+v1v2。九点 G 正好是 Δ=0 的非零点，即 rank-one 张量点；其三行三列是两个 ruling。J=polar(Δ)，在代码的六比特顺序 (01,02,03,12,13,23) 中 J 的 mask 为 12。**Δ 是几何二次型，不是一般情况下的物理转置 q。**

保持 incidence 的线性自同构群是 (GL(2,2)×GL(2,2))⋊C2，阶 72，对应行列排列及转置。它并不自动保持物理 B 或 q。

### 3.2 六线只能看到五比特

记

\[
p=B(a,b),\ t=B(a,c),\ u=B(a,d),\ v=B(b,c),\ w=B(b,d),\ z=B(c,d).
\]

下式中加法都在 F2。依次取三行、三列，其反对易指示量是

\[
\epsilon=(p,z,p+u+v+z,t,w,t+u+v+w).
\]

因此六条线中反对易线的条数必为偶数；所有 32 个偶校验模式都在三量子比特中出现。每条线的任意两项都具有相同的对易类型，因为 B(x,x+y)=B(x,y)。局部线只知道 u+v，看不到 u 与 v 各自的值。

按从左到右、从上到下定义有序三项乘积

\[
P_{g_1}P_{g_2}P_{g_3}=\tau_\ell I,
\quad \tau_\ell\in\{\pm1,\pm i\},\quad
\tau_\ell^2=(-1)^{\epsilon_\ell}.
\]

**相位补全公式：**

\[
\prod_{\ell=1}^{6}\tau_\ell=(-1)^\delta,
\qquad \delta=p+t+u+w+z.
\]

证明可逐个交换 Pauli 因子：行序九项与列序九项之间的交换符号为 κ=p+t+v+w+z，三列各自平方的符号和为 u+v，故六个标量乘积给 κ+(u+v)=δ。该公式还由标准字母乘法表独立核查全部 64 个 B。

于是 u=δ+p+t+w+z，v 再由任一第三条线恢复。六线模式加 δ 完全恢复四生成子的 B，进而恢复完整 9×9 Gram M_ij=B(g_i,g_j)。这比单纯统计反对易边数更强。

每个条目在六线中恰出现两次，故任意九个独立 ± 符号翻转都不改变总相位；单条线相位会改变。反对易线的方向变换则必须同步处理，不能把其有序 ±i 视为无方向的标量标签。

### 3.3 转置的十比特坐标与 Mermin 特例

物理 q 满足 q(x+y)=q(x)+q(y)+B(x,y)。九个 q(g) 给出四个种子的 q，以及六线所含五比特的 B。补上 δ 后，(q(g1),…,q(g9),δ) 是全部 1024 个有序抽象 (B,q) 的一一编码。另一证明：四变量无常数二次型的十维空间限制到九个 rank-one 点时，核恰为 span{Δ}；δ 区分相差 Δ 的两项。

这不是“最小电路成本特征”：只预测本轮 λ(T) 时，rank B 与“是否全线对易”已足够。十比特编码还保留了物理可嵌入性和具体目标作用所需的信息。它也不是 72 群商之后的最小轨道编码，更不记录固定系数 Hamiltonian 的全部参数语义。

若六线全对易，则 B 只能为 0 或 J。三量子比特中 rank0 的四维 W 无法嵌入，所以 B=J，δ=1，六线乘积为 −1。这恢复 Mermin 方阵的符号矛盾。含反对易线的网格不是六个可联合测量的 contexts，不能笼统称为同一种 contextuality 证明。

## 4. 三量子比特嵌入：必要且充分的修正

### 4.1 判据

标准物理空间 V=F2⁶ 带 q0(x,z)=x·z，是六维 hyperbolic 二次空间。设 R=rad(B)。四维 (W,q) 可等距嵌入 V 当且仅当：

- rank B=4；或
- rank B=2 且 q|R 非零；或
- rank B=2、q|R=0，且诱导在 W/R 上的二维非退化二次型为 hyperbolic，即 Arf=0。

rank0 不可嵌入。最后一项也可用精确 Gauss sum 检验：Σ_{x∈W}(-1)^{q(x)}=+8；值 −8 是禁止情形。

### 4.2 必要性与充分性

rank0 的 W 为四维辛各向同性子空间，但六维非退化辛空间的各向同性维数至多三。

rank4 时，给 W 加一个二维二次平面，其 Arf 与 W 相同，即得到 Arf0 的六维非退化空间，所以总能嵌入。最小量子比特数为 2 当且仅当 W 自身 Arf0；Arf1 需 3。

rank2、q|R=0 时，R 是二维全奇异子空间。若存在三量子比特嵌入，则 W⊂R⊥，且两者维数都为四，故 W=R⊥。由六维 hyperbolic 空间去掉两对 hyperbolic 方向，R⊥/R 是 hyperbolic 平面，不能是 anisotropic 平面。反过来，hyperbolic 平面加两条互相正交的 singular radical 方向显式嵌入六维 hyperbolic 空间。

rank2、q|R 非零时，选 radical 基 r1,r2 使 q(r1)=1,q(r2)=0。给非退化二维补空间的基向量分别加 r1，可以独立改变它们的 q 值而不改变 B；因而只剩一个此类退化等距型。三量子比特模型可取 radical={YII,IXI}，非退化补空间={IIX,IIZ}。这给出充分性。C++ 还给每个允许的有序 (B,q) 输出了实际 Pauli 四种子，不依赖该判据判断接受与否。

### 4.3 最小禁止例与精确计数

按整数 mask 字典序，首个 rank-only 反例是 B=1,q=3：仅 B(a,b)=1，q(a)=q(b)=1，q(c)=q(d)=0。其 q(v)=v0v1+v0+v1；R=span{c,d} 全奇异，而 W/R 为 anisotropic 平面，不能在三量子比特中出现。

明确的四量子比特 witness 是

```
YIII  XYII  ZYII
IIZI  IIIZ  IIZZ
YIZI  XYIZ  ZYZZ
```

它满足每条线的 projective 乘法，rankB=2、qmask=3，最小物理量子比特数为 4。禁止的是三量子比特标准 q 嵌入，不是抽象 Pauli 代数的存在性。

六比特 B 中 rank2 有 35 个，rank4 有 28 个。每个 rank2 B 的 16 个 q 中：12 个在 radical 非零，3 个商型为 plus，1 个商型为 minus。因此

\[
35\cdot15+28\cdot16=973.
\]

旧 rank-only 候选 1008 个多接受了 35 个。1024/44 的抽象枚举本身未被推翻；物理标签需改为 973/37。被排除的 51 个类型为 16 个 rank0 加 35 个 rank2-minus，分成七个旧轨道。rank2-minus 四个轨道大小 6,9,18,2。

二量子比特可实现 280 个类型；另外 693 个类型最少需 3 个量子比特；剩余 51 个最少需 4 个。所有 1024 个的四量子比特构造都存在：第 i 个种子在 i 位放 X 或 Y 以规定 qi，在 j<i 且 Bij=1 的位放 Z。四个 x 标签独立。

### 4.4 相位 lift 与等价关系

对全部 1024 个类型，本轮用实际三或四量子比特 Pauli 算出 16 个 projective 标签的 gauge，并精确核验 256 对乘法的 Z4 coboundary 等式。因此在上述嵌入成立后，没有观察到、也不需要再添加一个额外的相位 lift 存在性障碍：有具体矩阵 witness 就已给出了 lift。完整相位值仍依赖代表元，不能从 B,q 猜一个绝对符号表。

72 群只作用于抽象 incidence 坐标。保持 B 的子空间同构可以延拓为 ambient 辛变换，并由一般 Clifford 实现 projective Pauli 映射；它未必保持标准转置 q。保持 q 的同构对应更严格的 orthogonal/实 Clifford 结构。允许各项符号重参数化时，B 的物理网格轨道数为 8，而 (B,q) 的 72 群轨道数为 37。这里 37 指 quadratic/projective 分类，不等于任意固定参数约束下的精确电路等价分类；实现变换仍需输出符号、编码与目标两侧的门。

## 5. 真实指数包络：二次缺口与三次闭合

### 5.1 为什么可用单项式，而不能只用代数 closure

令 T_{≤k} 为 I,H,…,H^k 中所有非零符号单项式系数所含的 Pauli 标签。独立 α 确保每个单项式的所有排列都具有同一 XOR 标签；真正的问题是其 Gaussian-integer 系数是否抵消。代码保留这种精确抵消。

有限维中，span_C{U(α)} 等于全部非零单项式系数的线性张成：一方向由指数级数给出，另一方向由 α=0 处的混合偏导给出。每个非零单项式仅含一个 Pauli 标签，故这里的坐标包络就是实际线性空间，记为 E。这个“坐标支持=张成空间”只在本轮独立参数结构下成立；系数绑定时偏导系数一般是多个 Pauli 的组合。

### 5.2 二次缺失公式

设 C=B+J。则

\[
W\setminus T_{\le2}
=\{x\in W: \Delta(x)=1,\ x\in\operatorname{rad}(C)\}.
\]

证明：不在 {0}∪G 的 x 有 Δ(x)=1，恰有三个无序分解 x=g+h、g,h∈G。H² 的对应系数是反对易子，非零当且仅当 B(g,h)=0。由 Δ(g)=Δ(h)=0、Δ(x)=1 得 J(g,x)=1，故三个分解全部抵消当且仅当 C(g,x)=0 对六个参与的 g 都成立。这六个 g 张成 W。例如 x=9 的三对是 (1,8),(3,10),(12,5)；其余 x 由保持 Δ 的群传递作用得到。因此条件等价于 x∈rad(C)。

### 5.3 三次闭合的有限证明

若 B=J，定义 τ(Pv)=(-1)^{Δ(v)}Pv。因为 polarΔ=B，τ 是复线性 anti-automorphism。它固定九个生成子，故固定 H 和所有 H^k，任何 Δ=1 项都不出现。已有 I 加九点给出

\[
E=\operatorname{span}\{I,P_g:g\in G\},\quad\dim E=10.
\]

若 B≠J，对一个二次仍缺失的 x，有 x∈rad(C)、Δx=1，C 非零且 rank2。保持 Δ 的群可将 x 移为 9。条件 9∈rad(C) 对非零交替型 C 只剩七种。下表给出三个互异网格点之和为 9、且 C 在其两两之间均为 1 的 witness：

| C mask | B mask=C+J | 三点 | 本轮标准四量子比特 lift 的 H³ 系数 |
|---:|---:|---|---:|
| 8 | 4 | 2,4,15 | 6 |
| 17 | 29 | 1,2,10 | -2 |
| 25 | 21 | 1,2,10 | -2 |
| 34 | 46 | 1,4,12 | -2 |
| 42 | 38 | 1,4,12 | -2 |
| 51 | 63 | 1,2,10 | -2 |
| 59 | 55 | 1,2,10 | -2 |

三点上的 J 边和为 Δx=1，C 边和也为 1，故 B 的三条边中反对易条数为偶数。三算符完全对称乘积在零条反对易边时系数为 ±6，在两条时为 ±2，均非零。因此每个二次缺失标签都在 H³ 出现。

结论为 **B=J 时 T=10，否则 T=W=16，至多三次幂即可判定**，对任意实际实现该 proper 四生成子网格的 n 均成立。n≥4 时 B=0 也是“六线全对易”却 T=16 的反例；所以“全对易 iff T=10”需保留 n=3 假设，几何的 B=J 版本才是可推广版本。

### 5.4 失败猜想没有删除

较强的“非全对易网格在 H² 已饱和”是错的。首个可物理实现的 mask 反例是 B=4,q=0：

```
XII  IXI  XXI
IIX  ZII  ZIX
XIX  ZXI  YXX
```

累计维数为 1,10,15,16，H² 缺少标签9（此 lift 是 YII）。H³ 中 α_2 α_4 α_15 的系数为 ±6，补上它。64 个 B 中有 29 个确实需第三次幂；34 个到二次，唯一的 B=J 在一次后已完成。完整轨道表和证据见 JSON。

## 6. Walsh 转置证书与表示块

对饱和 E=span{Pv:v∈W}，转置乘子为 (-1)^{q(v)}。所有 W 上的线性 character 都可由某个原始 n 量子比特 Pauli 的共轭实现：ambient 辛空间非退化保证 restriction 到 W* 满射。

\[
c_\ell=\frac1{16}\sum_{v\in W}(-1)^{q(v)+\ell(v)},
\qquad U^T=\sum_\ell c_\ell Q_\ell UQ_\ell^\dagger.
\]

Walsh 解唯一；quadratic Gauss sum 给出 2^r 个非零系数、模长 2^{-r/2}，其中 r=rankB。因此 λ_T=Σ|c|=2^{r/2}。代码使用 Fraction 给出 primal/dual gap=0 的证书，不依赖浮点 LP。全对易物理情形 B=J 时，q+Δ 是线性，且 Δ 在 G 为零，故一个 Pauli character 已实现 T，λ=1。

LCU 构造成功 Kraus 为 U^T/λ：p=1/λ²。所需辅助位上界 A=r（rank2 用2位，rank4用4位），不是辅助位最优性声明。SELECT 只控制已知 Pauli；U 自身不受控。

Pauli 代数的中心来自 R=radB，复杂表示分解为

\[
\mathcal A\cong\bigoplus_{2^{4-r}} M_{2^{r/2}}(\mathbb C)\otimes I_m,
\quad m=2^{n-4+r/2}.
\]

三量子比特中：rank4 为 M4⊗I2；rank2 为四个 M2 中心扇区。后者不是简单“一个量子比特加两个可丢弃 spectator”：中心扇区可以带不同的未知 Hamiltonian，且 q|R 非零时转置会置换中心特征标。任何压缩必须保存中心、重数和目标编码。

## 7. 多 Kraus 的参数振幅：不能偷换为 fixed-c

任意一次 forward 查询成功 Kraus 都可写为固定的复线性矩阵映射 L_μ(U)。成功目标是酉通道，因而其 Choi 秩为1；在每个参数点，各成功 Kraus 必为

\[
L_\mu(U(\alpha))=a_\mu(\alpha)F(U(\alpha)).
\]

这不是先验令 a 为常数。固定射线 α=tβ，记 H(β) 的不同本征值集合为 S。利用每个目标本征投影的 trace 分量，a(t) 可写成有限指数多项式，其允许频率属于以下集合交：

- F=T：Γ_T=∩_{λ∈S}(S−λ)={0}。
- F=† 或 *：Γ_-=∩_{λ∈S}(S+λ)。

第一式由 S 的最小和最大元素即得：平移频率同时适用于所有 λ，只能为0。第二式非空当且仅当 S=γ−S，且有限非空 S 对应的 γ 至多一个。指数函数在全实轴线性独立，因此 T 的 a(t) 必为常数，†/* 的 a(t) 要么恒零，要么为 c exp(-itγ)。即使存在本征简并，该证明仍成立，只需对非零秩投影取归一化 trace。

由于所有射线交于 U(0)=I，对 T 有 a_μ(α)=a_μ(0)；对于 †/*，若某条射线强制 a_μ(0)=0，则其他任意射线的单频率振幅也为零。此论证覆盖参数相关成功概率、分支相关相位和任意有限 Kraus 分解。

**必过相位正例：** S={1,-3} 给 Γ_-={-2}，允许 exp(2it) 的分支相位；S={9,-3,-15} 给 Γ_-={-6}，允许 exp(6it)。本轮精确谱集合测试保留了这两个例子，没有用 fixed-c 障碍将其否定。此处只复核频率条件，不冒充重新构造了冻结资料中的两个编码器。

## 8. 一次查询转置的全物理最优性及精确 comb 证书

### 8.1 从承诺族到逻辑全矩阵代数

第7节令每个成功 Kraus 在原承诺族上为常数倍转置。第5节的混合偏导证明 E=span{U(α)}。若 E=𝒜 饱和，则线性性给 L_μ(X)=a_μ(0)X^T 对所有 X∈𝒜 成立。因此同一物理仪器也能以相同常数概率转置 𝒜 中所有酉元。

取已知表示编码，把一个任意 d×d 酉 V 同样作用于每个中心扇区的逻辑块，d=2^{r/2}。其物理实现只需一次 V⊗I 的调用加已知编码。输出的转置用共轭编码消去，即得到任意 V 的逻辑转置；没有假设能直接免费调用压缩 oracle。故结构化族成功率不能超过 universal 单查询 d 维转置的最优值 1/d²。

这个 known bound 与 Quintino 等的 Theorem2 在 k=1 时一致，但以下给出本轮独立核验的精确证书，避免只依赖外部归属。

### 8.2 不用 SDP solver 的 primal/dual

统一 tensor 次序为 (外部输出 o, oracle 输出 a, oracle 输入 b, 外部输入 i)，C-order 展平。转置的 Kraus 系数张量为

\[
t_{oabi}=\delta_{ob}\delta_{ai},\quad T=|t\rangle\langle t|,
\quad Q=\operatorname{Tr}_o T=I_b\otimes|I\rangle\langle I|_{ai}
\]

（最后一式按 a,b,i 次序重排理解）。成功 comb 为 pT。确定性 completion 满足 Cdet≥pT，Tr_o Cdet=I_a⊗C1，Tr_b C1=I_i。

Q≥0，Tr_a Q=I_bi，Tr(Q²)=d³。对 completion 的偏迹不等式用 Q 取 trace，得到

\[
d=\operatorname{Tr}(C1)\ge p\operatorname{Tr}(Q^2)=p d^3,
\quad p\le1/d^2.
\]

取 M=dI−Q，Q²=dQ，所以 M≥0。显式 primal 为

\[
C1=I_{bi}/d,\qquad
Cdet=\frac{dT+I_o\otimes M}{d^3},\qquad p=1/d^2.
\]

completion 和 causal trace 约束直接成立。`comb_certificate.py` 对 d=2,4 用 int64 验证这些整数恒等式、每个矩阵单位上的目标作用，以及 qubit adjugate 的同类证书。没有浮点求解器状态被当作最优性证明。

因此饱和网格的通用物理最优 p_T=2^{-r}，与 Walsh LCU 下界相等；全对易 B=J 情形已有 p=1。大辅助空间和多 Kraus 不再留下这个特定独立网格转置问题的概率缺口。辅助位最少数和已知门复杂度最优性仍未证明。

## 9. 复共轭与伴随：全反对易和混合线完全不同

### 9.1 任意一条对易线的 phase-aware kill gate

若网格含对易线，选择独立的两个 Pauli A,D，则第三项为 ±AD。独立系数允许合法选择

\[
H=A+2D+4AD.
\]

两个独立对易 Pauli 的联合本征值覆盖 ±1×±1，其不同谱为 S={7,-5,-3,1}（三量子比特时每个重数2）。该集合不是关于任何中心对称：min+max=2，但反射 λ↦2−λ 将 −3 送到缺失的5。因此 Γ_-=∅。

第7节说明每个成功 Kraus 在此射线上为0，进而在 I 为0，再沿任意其他射线仍只能为0。故任何含对易线的完整九参数 proper family 均不允许非零的一次查询 † 或 * 成功通道。943 个物理类型均含这样的 kill line。特别注意：若把 A、D、AD 的系数绑定相等，谱退化为 {3,-1}，上述 kill gate 就不属于该族；这正是不可丢失“独立系数”假设的原因。

### 9.2 全六线反对易：四个 SU(2) 扇区

全反对易约束给 p=t=w=z=1、u+v=1，即 Bmask=55 或59，rankB=2。九个网格标签全部避开 R=radB。故每个二维中心扇区中的 H 都是 traceless Hermitian 2×2，U 属于各扇区的 SU(2)。精确奇偶包络为 even=R（4个标签），odd=W\R（12个标签）。

取任一反对易种子 A=P_a,D=P_b，四个共轭 {I,A,D,AD} 的均匀 twirl 是投影到中心。每个 SU(2) 块满足 U^{-1}=Tr(U)I−U，因而在整个物理系统上

\[
U^\dagger=\frac{-U+AUA+DUD+(AD)U(AD)^\dagger}{2}.
\]

LCU 的 l1 范数2，给出 K=P=Q=1、A=2、workspace=5、p=1/4 的 heralded 构造，无 controlled-U。任意反对易线本身含有一整套逻辑 su(2)，限制其三个独立系数便得到 arbitrary SU(2) oracle 加 spectator。第7节给常数振幅，逻辑 adjugate/transpose comb 证书给 p≤1/4，故这是全物理最优概率。

复共轭更便宜。九点上的函数 f(g)=q(g)+1 是线性 character 的限制，当且仅当每条线都有 Σ_line q=1，即所有六线反对易；六条线关系张成全部五维关系空间。由 ambient 辛非退化性，存在原始三量子比特 Pauli Q0 满足

\[
Q0 P_g Q0=(-1)^{q(g)+1}P_g.
\]

所以 Q0 U Q0=U*，确定性 p=1，A=0、workspace=3。这是 *，并不是同一个门直接给出 †。

### 9.3 一个实际生成并模拟的例子

```
XII  ZII  YII
ZXI  YIY  XXY
YXI  XIY  ZXY
```

B=55,qseed=0；六条有序线乘积都为 −iI，总相位 −1；Q0=YIX 给 U*=YIX·U·YIX。逆变换用 {III,XII,ZII,YII} 的共轭，系数 (−1/2,1/2,1/2,1/2)。实际模拟了含两辅助位的 32×32 SELECT 电路，成功块为 U†/2。全部30个全反对易物理类型均输出了具体 grid 与 star witness。

已知门成本上界：令 w(A),w(D) 为 Pauli weight，SELECT 及其逆可用两次 controlled-A 和两次 controlled-D，外加 ancilla 上一个相对符号 Clifford（一个 CZ 加局部 Z）。因此至多 2(w(A)+w(D))+1≤13 个二量子比特 Clifford primitive；例子中 w(A)=w(D)=1，给5个的解析上界。另有辅助位 Hadamard/局部相位门及一次成功测量。这里是按 primitive 的构造上界，不是硬件路由后实测门数，也不是最优 gate synthesis 结果。

## 10. Target-aware 等价与高低维转移

若 U'=C U C†，则

\[
U'^\dagger=C U^\dagger C^\dagger,
\quad U'^T=C^*U^T C^T,
\quad U'^*=C^*U^* C^T.
\]

忽略 T/* 的共轭编码会产生真正错误。最小反例 C=S=diag(1,i)、U=e^{-0.37iX}：错误公式 C U^T C† 的 Frobenius 残差为 1.0228028964965088，而正确公式残差为0。

把一个 Qquery 协议迁移到 U' 时，每个原 oracle 调用可用 C† U' C 替代，外部目标编码按上式选取；总 forward 调用数仍 Q，但最多新添 2Q+2 个已知 C/C†/C*/C^T 因子（可相消，不计作最优门数）。维度降低只是表示分析，不是免费提供了更小的黑盒。必须明确中心扇区、multiplicity、输入/输出等距编码及其目标变体；中心扇区间的 coherent 输入不能被偷偷改成经典分支。

在辛等距 f 下，q2(fv)+q1(v) 是线性的，所以转置 Walsh 约束发生 character 平移，λ 保持。这解释一般 Clifford 可保持最优概率却不保持 naive 同侧共轭矩阵公式的区别。若有已知系数子空间，还需显式证明 α 的带符号重参数化保存该子空间；只比较相同 Pauli 代数或删除条目都不够。

## 11. Cloud Experiments Actually Run

环境为当前 ChatGPT 内置容器：Python3.13.5、NumPy2.3.5、SciPy1.17.0、SymPy1.14.0、pytest9.0.2；cgroup CPU配额4核、内存上限4GiB，可见5核。计算主要单线程；没有创建 VM、使用付费资源、GPU 或用户远程机器。本地 GitHub DNS 不通，gh 不存在；连接的 GitHub 工具可以读指定分支，但没有写入接口。具体探测见环境与交付 JSON。

冻结 ZIP 的 inventory 与 SHA256 验证通过，SOURCE_MAP 的30条文件 hash 均匹配；读取了所有指定 Markdown。本轮没有修改 frozen 目录。物理 sanity 对八例分别处理：六个 proper 网格；frozen_S1_control 和 row_only_full_M8 是非 proper 控制。custom_S1 没有被重命名为 frozen S1。

| 实验 | 实際范围 | 结果 | 证据范围 |
|---|---|---|---|
| 独立物理枚举 C++ | n2 的20,160组基；n3 的13,124,160组基 | 280 / 973类型，每个允许类型给具体种子 | 全部有序独立四种子，精确有限穷举 |
| 标准 Pauli 表多项式 checker | 64种B，九独立变量，H⁰…H⁷ | H²缺口公式、三次闭合、相位公式全通过 | 精确Gaussian integers；不限阶结论另有证明 |
| 二次型/轨道/Walsh | 1024种(B,q)，72群 | 973物理、37轨道、35额外排除、所有有理gap=0 | 精确有限枚举 |
| 相位 lift | 1024种，每种256对 | 262,144条cocycle等式通过 | 标准字母乘法与抽象cocycle独立核查 |
| 符号 gauge | 973种，每种512翻转 | 498,176种全线总相位不变 | 精确有限检验 |
| 原系统矩阵验证 | 973种，每种一组seed固定的九个整数系数 | transpose/概率/Choi全部通过 | complex128、tol=1e−11，finite-support |
| star / dagger 及完整SELECT | 全反对易30种 | Pauli star与32×32逆电路全部通过 | 同上；最优性不由样本得出 |
| 对易线phase-aware kill | 943种；另含两个相位正例 | 谱多项式、trace矩、Γ集合均通过 | 整数/SymPy精确部分与矩阵旁证分开 |
| comb primal/dual | d2,d4转置、d2 adjugate | 三个整数证书通过 | 无solver，整数恒等式+PSD解析证明 |
| pytest | 77项（最终测试集） | 全通过 | 首次测试有1个JSON schema读取错误，修复前日志保留 |

数值 seed=20261014，θ=0.137，系数从整数[-4,4]产生；每个类型只用一组，原向量全部保存。最大 Frobenius 残差：T算符1.2932e−15、成功概率算符1.0965e−15、成功Choi4.6087e−15、star1.0060e−15、dagger1.0770e−15、完整逆电路成功块8.6330e−16。

主要首次运行的内部 CPU 时间：物理n3枚举0.13秒；精确checker7.365秒；矩阵/cocycle验证7.070秒；comb证书0.0058秒。`/usr/bin/time` 另包含Python导入开销，分别记录在日志，不混称同一计时范围。已计时的核心实验与测试远低于30 CPU-min；不为未计时的文献阅读/编辑声称一个精确CPU总数。首次验证峰值RSS约149MiB。后续复现可能产生额外计时记录，以 ledger 为准。

八例复核结果：custom_S1 T16/λ2；new_structure_grid T16/λ4；S2_frozen T10/λ1；S2_same_W_saturated T16/λ4；same_W_q4_partial T10/λ1；same_W_q4_saturated T16/λ4。非proper frozen_S1_control T32 与 row_only_full_M8 T64 单独记录。本轮重新算了八例的包络和六个 proper 的有理LCU证书；两个非proper的 λ 字段仅保留 source 值，不称为重新证明。matched q4 pair 仍是同W/rank/odd-Y计数/反对易边数却不同包络与成本的对照。

## 12. 六条研究假设的生命周期

H1：六线加一比特总相位可补全 B；继而九q加δ编码(B,q)。保留并给公式证明，64/1024精确校验。

H2：rank2/4 足以物理实现。**反证**：B1,q3；修正为第4节二次型条件，35个额外排除；n3直接物理穷举独立确认。

H3：非特殊型在H²已饱和。**反证**：B4,q0累计1,10,15,16；修正为rad(B+J)缺口与H³闭合。

H4：独立 proper 网格的转置LCU概率可能就是一般物理最优。现有推导通过振幅刚性、span=代数、逻辑归约和comb双证书闭合该特定范围；仍安排独立检查，不推广到系数绑定族或辅助位最少数。

H5：全反对易网格可能具有统一star/逆构造。已给star p1、dagger p1/4，并以相位兼容谱kill证明其余线型无非零一次查询分支。两种参数相关相位正控制均保留。

H6：一般Clifford对三个目标都用同一种外侧共轭即可转移。**反证**：单量子比特S门；修正为第10节目标相关的C*/C^T编码。

每条量词、最便宜kill test、对照、反例和证据状态见 `hypothesis_ledger.json`。数值实验标finite-support；解析结论与有限枚举各自注明证明依据。

## 13. Experimental Consequences 与下一轮

最值得做的不是继续随机寻找更多同轨道网格。应独立验证三类可能共错的接口：物理q嵌入与抽象分类；独立参数的真实span与一查询多Kraus归约；target-aware编码的中心/复共轭约定。`NEXT_CODEX_TASK_PROMPT.md` 给出有界Luna preflight和四个具体任务，其中关键理论审查与低维精确证书优先，系数绑定探索最后。

复现脚本、原始结果、实际失败日志、输入/代码hash和严格fresh-output合同都随包提供。执行就绪指“输入与算法合同完备、可开始检查”；不表示研究预期已经由Codex完成，或外部设备/依赖已经探测成功。

## 14. Unsupported / Unresolved

本轮没有证明以上公式的新颖性，没有完成一般绑定系数族、一般Heisenberg图、任意结构化family或多查询全局最优性。没有把 frozen S1、S2 的旧协议包装成新发现；没有重新解决已有三角形均匀线/零和平面及N3/N4转移实例。

对独立 proper 3×3 family，本文给出的一查询概率分类有自包含解析论证和精确局部证书，但其振幅引理到逻辑oracle归约仍须独立研究代码/证明审阅；这比多跑浮点样本重要。最少辅助位、已知门最优、硬件连接/噪声、通用构造性Clifford canonicalizer、系数子空间等价算法仍未完成。SDP优化器未运行（本地无cvxpy/clarabel/scs），本轮以显式整数primal/dual替代证明，而非将缺失求解器写成成功实验。

GitHub远端没有本轮提交：read-only connector与本地网络/CLI限制真实存在。补丁只新增本轮目录；未编辑旧证据、原PR或远端历史。后续由有写权限的Codex依照交付计划应用、提交、push并回读验证。
