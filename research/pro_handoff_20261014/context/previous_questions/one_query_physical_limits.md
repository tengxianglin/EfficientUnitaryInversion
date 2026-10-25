# 大问题一：结构化未知酉的一次查询通道可行性与最优成功率

请先读README_FIRST.md、Background/MATH.md、Results/SUMMARY.md，再核对精确数据和代码。不要假设你能访问我的本机路径，也不要把附件中的科学陈述当作已发表定理。目标是证明、反证或定位已有结果；允许结论是“已知”或“尚未解决”。

主问题：对承诺族 F={U(theta)=exp(-iH(theta))}，什么时候一个参数无关、只调用一次forward U的物理量子电路可以精确输出逆通道？如何给出最优最坏情况成功率与所需辅助空间？请重点研究三qubit的独立各向同性边耦合族 H(J)=sum J_e B_e，以及这些耦合构成的已知子空间。theta/J未知；固定门可以依赖已知promise，不能依赖未知实际系数。

操作合同：允许任意有限维已知ancilla、参数无关的前后CPTP操作、仪器与heralded成功标志；U只使用一次且不默认controlled-U。要求成功CP map对所有输入（包括与参考系统纠缠的输入）满足 E_theta^succ(rho)=p(theta) U(theta)† rho U(theta)。不得只检验一个态或平均fidelity。success branch的算符允许含参数相关的全局相位；多个Kraus算符可能分别带参数相关标量。最坏情况成功率定义p_min=inf_theta p(theta)，请区分p_min>0、逐点p(theta)>0、成功率恒定、确定性p=1。若你的结论需要紧参数域，先声明它，不静默把全实域改成有限网格。

附件已经解决的校准例必须全部通过：

- 均匀三角形和sum J=0平面分别有不同固定门，Q1/A0/p1。
- 对固定方向J，固定常数c的复线性矩阵反演只可能在S=0或D=0；这个statement不是任意channel的no-go。
- 单边XYZ已有Q1/A2/p1相位协变编码器，系统块exp(2ia)U†。因此不能再次提出“固定c障碍推出channel不可能”的猜想。
- 对各向同性边J全独立的整个三角形族，附件没有给出一般one-query channel的完整结论；某一单边切片的fixed-c反证不能代替这一结论。

请交付一个相互衔接的答案：

1. 先检索universal unitary inversion、probabilistic supermaps、representation matching、no-programming与phase-covariant transformations最近邻工作。给原始URL/DOI、正确作者标题、精确定理及其与当前promise的差别。不可联网则写文献状态未验证，不编引用。
2. 明确几层可行性之间的关系：固定c矩阵等式、参数相关相位/振幅、单clean block、一般multi-Kraus成功channel。给必要充分条件或明确缺口；可先解决已知Hamiltonian方向的一参数族，再解释哪些步骤能用于多参数非对易族。
3. 对完整三角形独立边族或一个严格说明的新子空间，给构造或严格no-go；有构造时给p(theta)、p_min、query/ancilla/测量资源。只有某个字典或固定架构内的最优时必须保留范围。
4. 若用SDP，请从Choi/comb归一化与oracle索引顺序推导约束，说明有限样本SDP如何得到全参数证书；提供可运行最小实例、primal/dual或Farkas证书。有限随机fidelity和求解器状态都不能单独作证明。
5. 给最强可支持proposition、已知结果归属、一个会否证你的推广的最小例子，以及下一项真正能区分剩余假设的实验。不要再建议重复附件的49方向扫描或已经完成的V/W存在性检查。

终止规则：若主问题已被现有定理完整覆盖，请明确归属并停止包装成创新；若证明卡住，列出具体引理与已验证范围，不用“显然可以推广”填补。

补充校准：Background末尾还有13/49仿射谱检查与J=(1,4,4)的Q1/A1/p1显式编码。请把已知单方向存在性排除出Open Problem。对一般multi-Kraus成功channel，固定参数时其目标Choi rank为1，所以每个成功Kraus只能是标量倍U†；请研究随参数变化的标量/环境向量兼容性，不能让它们具有不同系统作用。
