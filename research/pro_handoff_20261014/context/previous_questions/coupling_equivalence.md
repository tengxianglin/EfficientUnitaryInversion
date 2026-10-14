# 大问题二：耦合子空间、目标作用与表示分块怎样决定反演电路等价

请先读README_FIRST.md、Background/MATH.md和Results/SUMMARY.md。附件给出实际运行的反例、矩阵与有限检查；这些结果的文献新颖性尚未核验。请研究同一个科学问题：如何在保留未知参数族和物理资源的条件下，判定两个结构化Hamiltonian族能否共用或转移反演电路？

对象：已知图G=(V,E)，B_e=XiXj+YiYj+ZiZj或声明的XZ边算符，H(J)=sum_e J_e B_e。耦合J属于已知实线性子空间 C⊆R^E，实际J未知。转移条件必须保留 C，而不只是Pauli支持集或生成代数。目标可分别为U†、Uᵀ、U*，一次只讨论一个；本文优先U†。同维变换需给参数映射和明确unitary/Clifford intertwiner，异维变换需给isometry及center/multiplicity数据。

主问题：能否给出有用的、可计算的判据，分类共享同一固定反演门的耦合子空间，并判断何时两族之间存在资源可追踪的电路转移？先把固定unitary sandwich V exp(-iH(J)) V†=exp(+iH(J))这一层做清楚，再说明Pauli/Clifford字典或一般comb会改变什么。不要无边界地承诺对任意规模实现完整canonicalizer。

已解决的小例子与约束：

- 三角形各向同性耦合的共享fixed-unitary线性子空间已限定为均匀轴或sum J=0平面的子空间，两类分别有显式V/W；请查归属或独立核对，但不要把同一分类当成新的待发现成果。
- 同一V_uniform在九个Pauli系数中的反对易核只有全1方向。generator algebra不包含这些系数信息。
- 前轮uniform XYZ/XZ三角形生成相同Pauli代数却有不同fixed-c反演性质；删项不能定义target-aware family equivalence。
- N3 open-chain已有C把六项变成M4 tensor I2，XZ逻辑门能提升；N4已有四个rank4中心sector。把logical/spectator分开描述不代表原物理oracle已变成小维oracle。
- 包一所讨论的参数相关相位和通道层变换不能偷换成这里固定sandwich的结论。若你扩大操作类，单独标明。

请交付：

1. 最近邻工作与归属：weighted Heisenberg graphs、chiral/sublattice symmetry、spin chirality、Schur-Weyl/Wedderburn decomposition、Clifford/symplectic equivalence。给原始引用和支持的准确statement；没有文献核验就不要声称新Open Problem。
2. 一个可以反驳的精确定义：对象至少包含参数线性空间/系数映射、目标作用及物理表示。说明commutation graph、binary span、生成代数、exponential envelope各自丢失什么；dagger的graded条件必须保留。
3. 选择最小尚未覆盖的延伸，例如四自旋开放链/四环上的非平凡耦合子空间，或明确的异维sector转移，给固定V存在的必要充分条件或一个严格有限范围分类。不要把full independent XYZ的一条旧切片障碍重命名成新分类。
4. 若提出canonicalizer，先给最小算法及失败证书：输入/输出、exact arithmetic、复杂度、参数映射、phase convention、center-sector匹配，及如何构造而非只声称存在的intertwiner。明确哪些步骤只是候选算法。
5. 给可复现正例和反例，验证整个参数族而非发现样本，列出query、原oracle维数、workspace、后选和成功率如何在转移后变化；已知门数与未知oracle调用数分开。
6. 最后给一个最强可支持命题和一个下一步：它必须解决附件尚未覆盖的条件，或用最小精确反例否证推广。已有定理足够时说明已知并停止，不制造“新机制”。

验收以原始文献、完整证明、显式矩阵/算法和可运行证书为准。模型自信、通用建议或更多问题清单不算完成。
