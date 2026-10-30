# 检索与核验日志

检索日：2026-10-30。五年窗口：2021-10-30 至 2026-10-30。工作目录：`/root/reinforcement_learning_resources/`。缓存：`/root/.cache/rl_lit/`。

本轮只收集整理。不安装依赖、不运行代码、不训练、不部署、不绕过访问限制。

## 1. 查重与复用

在 `/root` 下查找 MDP、Monte Carlo、控制、机器人、无人机、大模型等已有资料库目录。实际存在的兄弟库为空气质量与信号处理等，**没有**可核验复制的 RL/MDP/MC/机器人/UAV/LLM 资料树。`papers_en.py` 中的 SIBLINGS 路径未命中已核验 PDF，复用计数 **0**。未移动任何原件。

## 2. 教材

优先作者或出版社授权的完整 PDF：

| 编号 | 来源 | 结果 |
|---|---|---|
| B-01 | Sutton & Barto *RL: An Introduction* 2ed，incompleteideas.net 2020 印刷本 | 通过 |
| B-02 | Agarwal et al. *RL: Theory and Algorithms* 工作草稿 | 通过 |
| B-03 | Szepesvári *Algorithms for Reinforcement Learning* | 通过 |
| B-04 | Lattimore & Szepesvári *Bandit Algorithms* | 通过 |
| B-05 | Kochenderfer et al. *Algorithms for Decision Making*，Drive 直链 | 通过（700 页级） |
| B-06 | Albrecht et al. MARL 书 marl-book.com | **HTTP 403** |
| B-07 | Powell *Sequential Decision Analytics* 2ed | 通过 |
| B-08–B-14 | Bertsekas 作者站点 DP/RL/NDP/AlphaZero/Rollout | 通过 |
| B-15 | Boyd & Vandenberghe *Convex Optimization* | 通过（优化先修，非 RL 算法书） |
| B-16 | Bertsekas & Shreve SOC 1978 | **标题短语核验失败**（扫描件） |

合法来源均来自作者站点或 CC 教材页。不使用盗版聚合站。

## 3. 课程

12 套均核验：MIT 6.231 OCW 包、Silver UCL 讲义、CS285、CS885 Winter 2025、Spinning Up HTML、Hugging Face Deep RL HTML、CMU 10-703、Stanford CS234 索引页、MIT 6.041SC、ORF 411 HTML、MIT 16.410、CS188 fa24 HTML。视频不下载。CS234 部分附件 404，按索引页完整资料包计一次。Spinning Up 站点全站 wget 易挂起，改为指定 HTML 子集。

## 4. 软件文档

离线 HTML 子集（范围见各目录 `PAGES_en.txt`）：Gymnasium、SB3、CleanRL、TorchRL、RLlib、OpenSpiel、PettingZoo、MuJoCo、Brax、d3rlpy、Hugging Face TRL。Isaac Lab（S-12）脚本渲染页面过短，未计入。Gymnasium 迁移指南 URL 曾 404，改为 `/introduction/` 下有效页。

## 5. 项目快照

git 浅克隆，上限内剔除权重/大仿真资源，写 `SNAPSHOT_en.txt`。已核验 19：Gymnasium、SB3、SB3-Zoo、CleanRL、TorchRL、Tianshou、OpenSpiel、PettingZoo、Brax、Minari、MiniGrid、HighwayEnv、d3rlpy、CORL、DreamerV3、Decision Transformer、epymarl、TRL、veRL。

失败：Safety-Gymnasium 551 MiB、CityLearn 272 MiB、Spinning Up git 根目录无 README。RLlib 随 Ray 文档收录，未再克隆整棵 Ray。Isaac Lab 仿真资源不下载。

## 6. 论文检索

arXiv Atom API，26 条分方向查询（见 [`scripts/select_papers_en.py`](scripts/select_papers_en.py) 的 `QUERIES`），窗口用 `submittedDate`。候选 **865**。另有 MUST 列表覆盖 DQN/PPO/SAC/TD3/CQL/Dreamer 等代表作。

筛选：标题/摘要须含强化学习核心用语；Workshop 注释不得标为主会；预印本渠道记 arXiv，不以 ICML/NeurIPS/ICLR 主会冒充。

下载核验：HTTP 200、`%PDF`、pypdf、≥4 页、≥12k 字符、标题词匹配、第一作者姓氏、参考文献节。

### 近年集 / 经典集 / 全库

| 集合 | 数量 | 说明 |
|---|---:|---|
| 近五年已核验 | 68 | 首次公开 ≥ 2021-10-30 |
| 窗口前经典补充 | 82 | 必要教材级/算法代表作，单列 |
| 已核验论文合计 | 150 | 类别目标 100–150 |
| 检索候选全库 | 865 | 含未入选与后续拒收 ID |

### 编号纠错（重要）

MUST 中若干 arXiv ID 与拟收论文不符（例如把别的学科 PDF 当成 Bilinear Classes / Safety Gym / AlphaStar / NGU）。已人工拒收并按**标题检索**换入正确 ID，例如：

- Bilinear Classes → `2103.10897`（不是 `2106.08005`）
- Never Give Up → `2002.06038`（不是 `2004.12277`）
- DIAYN → `1802.06070`
- RCPO → `1805.11074`
- Recovery RL → `2010.15920`
- Procgen → `1912.01588`
- Learning to Drive in a Day → `1807.00412`
- How Many Random Seeds? → `1806.08295`
- Soft Actor-Critic → `1801.01290`（补入 04）

拒收 PDF 移至 `/root/.cache/rl_lit/rejected/`，不计入目录。AlphaStar/SMAC `1902.04043` 已在 09，13 记 `dup_elsewhere`，不重复计数。

仍保留的窗口前探索论文 `1606.01868` 实为 Bellemare 等 count-based 探索（与最初 VIME 编号设想不同），主题匹配，计入 05。`2004.10746` 芯片布局计入 13。

## 7. 官方代码比例

见 README。70% 为种子「官方完整/部分」标注率；可解析 GitHub 地址约 35%。理论篇允许无代码。本轮不为每篇论文克隆代码仓。

## 8. 评测与工程登记

[`evaluation_audit_cn.csv`](evaluation_audit_cn.csv) 列出 terminated/truncated、bootstrap、奖励缩放、归一化冻结、种子与区间等字段；论文行多为「待全文核实」。指南写明：单次最高回报 ≠ 稳定优越性；仿真 ≠ 实机/生产；训练奖励、评测指标、业务成效分列。LLM / 游戏 / 机器人 RL 管线不默认共用。

## 9. 续跑

状态在 [`scripts/state/`](scripts/state/)。`python3 -I scripts/run_en.py status|catalog` 或 `materials_en.py fetch … --retry-failed`。已 `ok`/`verified` 跳过。arXiv 速率限制与其他库共享锁，避免叠加。
