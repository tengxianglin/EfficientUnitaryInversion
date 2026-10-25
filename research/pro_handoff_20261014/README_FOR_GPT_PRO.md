# EfficientUnitaryInversion：优先发现 3×3 横竖规律

本轮要求你主导规律发现、理论延伸和实验设计。先读 `NEXT_PRO_PROMPT.md`，再读 `context/CURRENT_PROGRESS.md`、`context/GRID_PROBLEM.md` 和 `context/OTHER_OPEN_QUESTIONS.md`。已有结果是校准集，你应提出、检验和修正新的可证伪规律。

交接日期：2026-10-14。研究轮次：EUI_Pro_Grid_Theory_20261014。模式：HYBRID / manual_relay；当前仅为 prepared_for_manual_relay；新 Pro 回复 pending。本轮 Codex 没有新增科学实验。

## GitHub 工作位置

- 仓库：https://github.com/tengxianglin/EfficientUnitaryInversion
- 分支：`codex/eui-grid-pro-20261014`
- 本包在分支中的目录：`research/pro_handoff_20261014/`
- 用户已授权你在这个仓库修改本轮相关科研代码和文档。读取分支当前 tip 后，以新目录保存发现、脚本、实验结果和下一步方案；保留本包的冻结证据。
- GitHub 分支与 ZIP 的交付验证记录由 Codex 在包外提供。这里的 branch 名本身不证明远端已收到文件；先实际读取并校验清单。

## 输入与证据

`source/grid/` 是无第三方依赖的两个精确程序；`evidence/grid/` 含八个物理例子和全部 1024 个抽象 case。`source/heisenberg/` 已补齐本地 import 闭包。`REPRODUCE.md` 给出运行入口和版本事实；先写新输出目录。

完整来源和不包含的内容见 `context/SOURCE_MAP.json`。源代码和结果按字节复制，`BUILD_MANIFEST.json` 逐文件记录 SHA-256。执行 `python verify_bundle.py` 可验证文件清单；这只验证完整性，不证明数学结论。

特别注意：旧 census 的 `three_qubit_realizable_rank` 标记直接取 `rank in (2,4)`；它的统计是抽象模型事实。请独立核查标准计算基转置下，二次型、相位及表示嵌入是否还带来条件。不要把这一核查要求写成已发现的反例。

输出应包含理论推导、云端实际实验、下一步 Codex 可执行方案、未决项、GitHub 实际修改及其可核查交付记录。用户只负责传递文件和开始下一轮。
