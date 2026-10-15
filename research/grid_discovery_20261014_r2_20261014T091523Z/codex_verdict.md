# Codex 独立审查结论（2026-10-14，R2）

四项正式任务均完成。未发现推翻 R1 独立九参数 proper 网格分类的数学反例。新增结果主要是独立验证其证明接口、真实中心编码与电路成本，以及系数绑定后真实张成空间的精确变化。原始输入、先前反例、失败及修复记录均保留。

- **T1 — exact-finite / analytic-checked：** 651个RREF子空间×20,160组基，完整13,124,160组；973物理类型、37二次轨道。n2控制280类型。64型H²/H³、六线相位、完整Gram、七情况证书和1024型对照全部通过。保留B1q3及35个rank-only误接受，B4q0仍需三次。
- **T2 — analytic-checked / exact-finite：** 多Kraus、简并、a(0)=0、参数相位和shared-I量词通过审查；span来自实际混合偏导；逻辑归约保留四中心相干。不同ibao顺序的3组整数comb证书通过，故意错误顺序失败；两个非零相位正控制保留。最优性仅适用于所述独立参数和一次forward查询合同。
- **T3 — finite-support：** 37/37显式编码，592代数矩阵单位和2368完整输入单位通过，最大残差6.68e-16；13例中心置换非平凡。30网格×3样本的实际primitive电路与参考Choi通过，最大残差7.16e-15。dagger用2辅助位、workspace5、p1/4，已知一/二比特门8–16/5–7；star用0辅助位、workspace3、p1，已知单比特门2–4。均K=P=Q=1。无门数或辅助位最优性声明。
- **T4 — exact-finite / analytic-checked：** 16/16任务行（4独立控制+12绑定族）完成；所有绑定族均support>span。B55行/列/统一绑定的full/even/odd分别6/2/4、6/2/4、4/2/2。216条固定射线中82条谱不对称，为其余9绑定族给出全域dagger/star obstruction。B55的54条通过仅是有限必要条件；star p1和dagger p1/4的存在性另由已验证父族构造继承，绑定后的更优概率仍未决。

一次独立T4核验因SymPy未展开表达式的结构比较失败；精确展开差为零。修复后416个稠密整数矩阵幂核验及独立有理秩全部通过，失败日志与源版本保留，未修改科学容差或预算。T1初次源JSON对照schema及T3初次内存驻留问题也保留并以fresh输出修正。T2的一次源版本复原哈希检查因额外换行失败，修正后两份执行源与记录哈希一致；未将该工程失败计为数学反例。

R1冻结verifier、77项pytest及一次fresh完整复现通过。所有科学执行串行、CPU-only，计费于本轮的子进程CPU合计33.313253秒（上限1800秒）；编辑、打包、网络不计作科学CPU时间。详细分组见resource_accounting.json。未运行可选solver、d8 SDP或重复大规模随机搜索。

主证据入口见README、proofs/、claim_ledger.json、consistency_report.json及各最终results目录。GitHub实际交付以外层GITHUB_DELIVERY.json的远端ref/文件回读为准；本报告不把本地commit或补丁视为远端成功。对Pro的ZIP状态为prepared_for_manual_relay，下一条回复pending，未自动发送。
