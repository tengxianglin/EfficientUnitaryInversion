# 先回答合作者到底可能想看什么

“多试几种每行、每列任意两项相乘得到第三项”的建议，最合理的解释不是再随机生成几个 \(U\) 看 fidelity，而是检验下面这个结构猜想：

> 只要九个 Pauli 生成元能排成这种 3×3 乘法网格，是否就会有相同的代数结构和相同的 \(U^T\)/\(U^\dagger\) 协议？

答案目前已经可以说是：**不会。** 行列规则只约束 phase-free 标签的加法关系。

## 规则的精确定义

把 \(n=3\) 的 Pauli 标签写成 \(v=(x|z)\in\mathbb F_2^6\)，并把忽略 \(\pm1,\pm i\) 的乘法记作 XOR。若四个角点是 \(a,b,c,d\)，所有满足规则的网格都具有形式

\[
\begin{pmatrix}
a&b&a+b\\
c&d&c+d\\
a+c&b+d&a+b+c+d
\end{pmatrix}.
\]

因此，规则本身最多只给出四个 GF(2) 独立标签；它不固定这些标签之间的 symplectic 交换关系，也不固定 \(Y\)-parity 或指数包络。

例如，历史 custom S1 是

\[
\begin{pmatrix}
XXI&IYX&XZX\\
ZZI&YII&XZI\\
YYI&YYX&IIX
\end{pmatrix},
\]

而后来找到的 structure-preserving grid 是

\[
\begin{pmatrix}
XXI&IYX&XZX\\
ZZZ&XXY&YYX\\
YYZ&XZZ&ZXI
\end{pmatrix}.
\]

二者都满足六条独立的行/列检查，但前者的 restricted symplectic rank 是 2，后者是 4。

## 精确对照结果

\(|T_L|\) 是由 \(H(\alpha)^k\), \(0\le k<8\) 的 Gaussian-integer 系数展开得到的 phase-free 坐标支持大小；不是随机样本估计。\(\lambda\) 只表示归一化 Pauli-conjugation LCU 类中的精确转置成本。

| 例子 | 六条行列规则 | \(\dim W\) | \(\operatorname{rank}\omega\) | radical | \(|T_L|\) | \(\lambda_T\) | \(p=1/\lambda^2\) | 作用 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| custom_S1 | PASS | 4 | 2 | 2 | 16 | 2 | 1/4 | 历史 custom support |
| new_structure_grid | PASS | 4 | 4 | 0 | 16 | 4 | 1/16 | 后来验证过的完整 grid |
| S2_frozen | PASS | 4 | 4 | 0 | 10 | 1 | 1 | 正式 S2；官方目标仍是 \(U^\dagger\) |
| S2_same_W_saturated | PASS | 4 | 4 | 0 | 16 | 4 | 1/16 | 与 S2 同一个 \(W\) 的饱和 grid |
| same_W_q4_partial | PASS | 4 | 4 | 0 | 10 | 1 | 1 | 与下一行保持相同粗粒度计数 |
| same_W_q4_saturated | PASS | 4 | 4 | 0 | 16 | 4 | 1/16 | 同 \(W\)、同 q-奇数数、同反对易边数 |
| frozen_S1_control | FAIL | 5 | 4 | 1 | 32 | 4 | 1/16 | 当前正式 frozen S1，列规则不全 |
| row_only_full_M8 | FAIL | 6 | 6 | 0 | 64 | 8 | 1/64 | 只满足行规则的 full-\(M_8\) 对照 |

完整机器可读记录在 grid_examples.json，可用下面的命令重新生成：

~~~bash
/opt/anaconda3/bin/python verify_grid_examples.py --output grid_examples.json
~~~

## 最有区分力的匹配对

same_W_q4_partial：

\[
\begin{pmatrix}
ZIZ&ZZI&IZZ\\
XIX&YXZ&ZXY\\
YIY&XYZ&ZYX
\end{pmatrix}
\]

same_W_q4_saturated：

\[
\begin{pmatrix}
ZIZ&ZZI&IZZ\\
YZX&ZYX&XXI\\
XZY&IXX&XYZ
\end{pmatrix}.
\]

脚本精确检查了这两张网格具有：

- 相同的 phase-free \(W\)；
- \(\dim W=4\)、restricted symplectic rank \(4\)；
- 生成元中 \(Y\)-奇数的数量都是 4；
- Pauli 反对易边数都是 18；
- 但指数包络为 10 对 16，转置 LCU 成本为 \(\lambda=1\) 对 4。

这正是“为什么要多试例子”的答案：即使几个粗粒度结构数字相同，目标相关的 exponential envelope 仍可能不同。

这次结论又由独立的全量 verifier 复核：见
`results/eui_grid_exact_20260905/independent_grid_certificates.json`。

## 目前可以、不能说什么

可以说：

1. 对 proper（九项互异且非恒等）3×3 grid，行列规则给出四角点的 GF(2) 完成公式，因此 \(\dim W\le4\)；
2. 规则不单独决定 symplectic rank、中心/块结构、\(U^T\) 的 LCU 成本或 \(U^\dagger\) 的并行协议；
3. 同一 \(W\) 内的匹配例子已经足以否定“规则 \(\Rightarrow\) 唯一协议/唯一成本”。

不能说：

- 这些八个例子已经完成所有三量子比特 grid 的分类；
- \(\lambda\) 是任意 quantum comb 的 query lower bound；
- 某个新 grid 自动是新 protocol mechanism；
- 数值 optimizer 或随机 fidelity 能替代 exact envelope/character 证明。

## 对后续工作的最小建议

先不要上 GPU。下一步只需做一个有限、可证伪的 atlas：

1. 固定一个 phase-free \(W\)，枚举四角点的独立基并去重；
2. 对每张 grid 记录 \((\operatorname{rank}\omega,\operatorname{rad},q\text{-pattern},\text{commutation graph},T_L,\lambda_T)\)；
3. 先找“相同前四项、不同 \(T_L\) 或 \(\lambda\)”的最小匹配对；
4. 只有出现明确的 representation/intertwiner 触发条件时，才进入 \(U^\dagger\) 或 sequential/parallel protocol 搜索。
