# 算法地图

把本库算法按问题类型而不是按年份排列。论文在各 `NN_*/papers/`，代码在 [`projects/`](../projects/)。

## 精确求解（模型已知、状态可枚举）

价值迭代 / 策略迭代 / 线性规划。教材：Sutton 第 4 章、Kochenderfer 第 7 章、MIT 6.231 课件包。

## 表格学习

| 方法 | 同/离策略 | bootstrap | 资料 |
|---|---|---|---|
| MC | 均可 | 否 | Sutton 第 5 章；Silver 第 4 讲 |
| TD(0)/TD(λ) | 预测 | 是 | Sutton 第 6、12 章 |
| SARSA | 同策略 | 是 | Sutton 第 6 章 |
| Q-learning | 离策略 | 是 | Sutton 第 6 章；论文 `1807.03765` |

## 价值函数逼近

DQN 及扩展在 [`03_value_based/papers/`](../03_value_based/papers/)：DQN、Double DQN、PER、Dueling、C51（分布式价值）。Rainbow / QR-DQN / IMPALA 的单文件或模块化实现见 CleanRL 与 SB3，不必把未入库论文当成已下载。

实现对照：

- 模块化：[`projects/DLR_RM_stable_baselines3_en/`](../projects/DLR_RM_stable_baselines3_en/)（DQN）。
- 单文件：[`projects/vwxyzjn_cleanrl_en/cleanrl/dqn.py`](../projects/vwxyzjn_cleanrl_en/cleanrl/dqn.py)。

## 策略梯度与 Actor–Critic

[`04_policy_actor_critic/papers/`](../04_policy_actor_critic/papers/)：REINFORCE/A3C、GAE、TRPO、PPO、DDPG、TD3、SAC。

实现：

- PPO/SAC：SB3 与 CleanRL（`cleanrl/ppo.py`、`cleanrl/sac_continuous_action.py`）。
- 教学对照：[`courses/OpenAI_SpinningUp_DeepRL_html_en/`](../courses/OpenAI_SpinningUp_DeepRL_html_en/)（git 快照本轮未计入）。
- 采集器/回放：[`projects/pytorch_rl_TorchRL_en/`](../projects/pytorch_rl_TorchRL_en/)。

自然梯度与信赖域：TRPO 论文 + Spinning Up TRPO 页。PPO 是工程上的信赖域替代，不是理论上的同一保证。

## 探索

Bandit 书 → ICM/RND/HER/Go-Explore，见 [`05_exploration/papers/`](../05_exploration/papers/)。目标条件策略用 HER，不要把稀疏奖励只交给 ε-greedy。

## 模型式

Dyna（Sutton 第 8 章）→ PETS/MBPO → PlaNet/Dreamer 族 → MuZero → TD-MPC。代码：[`projects/danijar_dreamerv3_en/`](../projects/danijar_dreamerv3_en/)、[`projects/google_brax_en/`](../projects/google_brax_en/)。

模型误差会在规划中被放大；Dreamer 成绩不能直接当成无模型 PPO 在同一环境的公平对照，除非预算与评测协议对齐。

## 离线与模仿

CQL/IQL/TD3+BC、GAIL/AIRL、Decision Transformer：[`07_offline_imitation/papers/`](../07_offline_imitation/papers/)。代码：[`projects/takuseno_d3rlpy_en/`](../projects/takuseno_d3rlpy_en/)、[`projects/tinkoff_ai_CORL_en/`](../projects/tinkoff_ai_CORL_en/)、[`projects/kzl_decision_transformer_en/`](../projects/kzl_decision_transformer_en/)。

## 部分可观测与分层

DRQN、Option-Critic、HIRO、FuN：[`08_partial_observability_hierarchy/papers/`](../08_partial_observability_hierarchy/papers/)。环境：[`projects/Farama_Minigrid_en/`](../projects/Farama_Minigrid_en/)。

## 多智能体

MADDPG/COMA/QMIX/MAPPO：[`09_multi_agent/papers/`](../09_multi_agent/papers/)。环境与算法：PettingZoo、OpenSpiel、EPyMARL。

## 安全

CPO 与 Safety-Gymnasium：[`10_safe_robust/papers/`](../10_safe_robust/papers/)、`projects/PKU_Alignment_safety_gymnasium_en/`。
