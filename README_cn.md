# 强化学习资源库

独立目录：`/root/reinforcement_learning_resources/`。覆盖本科入门、研究生理论、现代方法、完整参考代码、应用案例、评测与工程集成。检索日 **2026-10-30**；论文五年窗口 **2021-10-30 至 2026-10-30**，必要经典单列。

本轮只收集整理：不安装依赖、不运行实验、不训练、不连接设备、不部署、不上传 GitHub、不删除资料。不下载大型数据集、模型权重、仿真二进制或安装包。

## 已核验数量（只计完整通过项）

| 类型 | 已核验 | 类别目标 | 失败未计入 |
|---|---:|---|---|
| 完整教材/专著 | 14 | 10–20 | B-06 MARL 书 403；B-16 SOC 1978 标题核验失败 |
| 大学课程/系统教程 | 12 | 10–15 | — |
| 论文/综述/教程 | 150 | 100–150 | 见失败表；拒收的跑题 PDF 不计 |
| 官方软件文档集 | 11 | 8–12 | S-12 Isaac Lab 页面过短 |
| 算法/应用项目 | 19 | 15–25 | P-14 Safety-Gymnasium 551 MiB；P-17 CityLearn 272 MiB；P-22 Spinning Up git 缺 README |

合计目录条目 **206**（[`catalog_cn.csv`](catalog_cn.csv)）。本轮新下载 **206**；已有资料库复用 **0**（磁盘上未找到可核验的 MDP/MC/控制/机器人/无人机/大模型兄弟库目录，仅有缓存名，未移动原件、未重复计数）。

论文时间：近五年 **68**；窗口前经典补充 **82**。检索候选全库 **865** 条 arXiv 命中（含未入选）。

## 子方向

| 目录 | 内容 |
|---|---|
| [`01_foundations/`](01_foundations/) | MDP、价值函数、Bellman、动态规划、概率、优化、随机逼近 |
| [`02_tabular_methods/`](02_tabular_methods/) | MC、TD、SARSA、Q-learning、资格迹、探索与表格收敛 |
| [`03_value_based/`](03_value_based/) | 函数逼近、DQN 及扩展、分布式价值、离策略稳定性 |
| [`04_policy_actor_critic/`](04_policy_actor_critic/) | 策略梯度、GAE、TRPO/PPO、DDPG/TD3/SAC |
| [`05_exploration/`](05_exploration/) | Bandit、内在奖励、稀疏奖励、目标条件、课程与信用分配 |
| [`06_model_based/`](06_model_based/) | 动力学、规划、Dyna/MPC、世界模型、模型误差 |
| [`07_offline_imitation/`](07_offline_imitation/) | 离线 RL、行为克隆、逆 RL、模仿、离策略评价 |
| [`08_partial_observability_hierarchy/`](08_partial_observability_hierarchy/) | POMDP、记忆策略、分层与技能、长时域 |
| [`09_multi_agent/`](09_multi_agent/) | 马尔可夫博弈、CTDE、非平稳、协调 |
| [`10_safe_robust/`](10_safe_robust/) | 约束 MDP、风险敏感、鲁棒与安全探索 |
| [`11_generalization_transfer/`](11_generalization_transfer/) | 多任务、迁移、元学习、域随机化、sim-to-real |
| [`12_llm_reasoning_agents/`](12_llm_reasoning_agents/) | 后训练：SFT / 奖励模型 / PPO-RLHF / DPO / GRPO，不可混称 |
| [`13_applications/`](13_applications/) | 机器人、控制、调度、能源、交通、推荐、资源分配 |
| [`14_evaluation/`](14_evaluation/) | 基线、种子、统计、离线评价、复现与失效 |
| [`15_software_engineering/`](15_software_engineering/) | 环境接口、并行采样、回放、检查点、推理与监控 |

论文在各目录 `papers/`。教材、课程、软件文档、项目分别在 [`books/`](books/)、[`courses/`](courses/)、[`software_docs/`](software_docs/)、[`projects/`](projects/)。

## 登记文件

- [`catalog_cn.csv`](catalog_cn.csv) 已核验条目
- [`code_availability_cn.csv`](code_availability_cn.csv) 论文代码归属（官方完整 / 官方部分 / 无代码 / 待核实）
- [`evaluation_audit_cn.csv`](evaluation_audit_cn.csv) 评测字段（本轮多为待全文核实，不把单次最高回报当优越性）
- [`project_readiness_cn.csv`](project_readiness_cn.csv) 代码 **L0/L1**
- [`progress_cn.csv`](progress_cn.csv) 分方向进度
- [`download_failures_cn.csv`](download_failures_cn.csv) 失败、拒收、跨类去重
- [`search_log_cn.md`](search_log_cn.md) 检索、筛选、编号纠错与复用说明
- [`guides/`](guides/) 中文路线
- [`datasets_catalog_cn.csv`](datasets_catalog_cn.csv) 本轮无独立数据集清单（大型数据不下载）

独立自建文件在扩展名前标 `_cn` 或 `_en`。上游源码与离线 HTML 内部路径保持原样，外层目录加 `_en`。

## 指南

- [`guides/foundations_path_cn.md`](guides/foundations_path_cn.md) 本科到研究生先修
- [`guides/algorithms_map_cn.md`](guides/algorithms_map_cn.md) 算法地图
- [`guides/theory_path_cn.md`](guides/theory_path_cn.md) 理论研究
- [`guides/implementation_path_cn.md`](guides/implementation_path_cn.md) 实现与陷阱
- [`guides/offline_and_evaluation_cn.md`](guides/offline_and_evaluation_cn.md) 离线学习与评测
- [`guides/llm_rl_path_cn.md`](guides/llm_rl_path_cn.md) 语言模型 RL（与 SFT/DPO 区分）
- [`guides/applications_deployment_cn.md`](guides/applications_deployment_cn.md) 机器人 / 工业 / 推荐，管线不混用
- [`guides/core_reading_list_cn.md`](guides/core_reading_list_cn.md) 最小阅读集

## 代码与官方实现比例

- 种子标注「官方完整/部分」：**105 / 150 = 70.0%**。
- 其中摘要或种子给出可访问 GitHub 地址：**52 / 150 = 34.7%**。
- 标注「无代码」**39** 篇，多为理论/综述，允许无实现。
- 「待全文核实」**6** 篇。
- 本轮**未**为每篇论文克隆附属仓库；可运行对照见 [`projects/`](projects/) 的 Gymnasium、SB3、CleanRL、TorchRL、Tianshou、OpenSpiel、PettingZoo、Brax、d3rlpy、CORL、DreamerV3、Decision Transformer、TRL、veRL 等。
- 代码等级只到 L0/L1。19 个已核验项目均有 `SNAPSHOT_en.txt`（含 commit）。**不声称运行、复现或生产验证通过。**

## 完整性规则（摘要）

只计核验通过的完整资料。PDF 须 `%PDF` 头、pypdf 可解析、页数与字符足够、标题/作者匹配、可见参考文献。摘要、试读、目录、仅链接、残缺不计。课程按完整资料包计一次。HTML 保存为离线子集并写 `PAGES_en.txt`。源码保留结构、许可证与快照。不绕过访问限制。Workshop / 预印本不标为主会论文。

## 主要缺口（续跑对象）

- MARL 教材（Albrecht et al.）站点 403。
- Bertsekas–Shreve *Stochastic Optimal Control* 扫描件标题核验失败。
- Isaac Lab 文档为脚本渲染短页。
- Safety-Gymnasium、CityLearn 仓库超过体积上限（不下载仿真资源）。
- Spinning Up **git** 缺根 README；HTML 教程已另存于 [`courses/`](courses/)。
- 工业调度/能源完整流程案例偏论文、缺超限仓库。

## 断点续跑

```bash
cd /root/reinforcement_learning_resources
python3 -I scripts/run_en.py status
python3 -I scripts/run_en.py books --retry-failed
python3 -I scripts/run_en.py courses --retry-failed
python3 -I scripts/run_en.py software --retry-failed
python3 -I scripts/run_en.py projects --retry-failed
python3 -I scripts/run_en.py papers 13 --retry-failed
python3 -I scripts/run_en.py catalog
```

已核验条目不会覆盖。工作缓存：`/root/.cache/rl_lit/`。arXiv 与本机其他文献库共享 `/root/.cache/ipm_lit/locks/arxiv.org`。
