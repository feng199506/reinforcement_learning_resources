# 离线学习与评测路线

## 离线 RL 与模仿

问题：不能交互，只有有限数据。覆盖不足时，任何高回报都可能是外推幻觉。

阅读顺序：

1. Levine 教程 arXiv:2005.01643（[`07_offline_imitation/papers/`](../07_offline_imitation/papers/)）。
2. BCQ → CQL → IQL → TD3+BC。
3. 模仿：行为克隆 vs GAIL vs AIRL；逆 RL 不是“有专家轨迹就等于 RL”。
4. 序列建模：Decision Transformer，须标明它更接近条件行为克隆。

代码：d3rlpy、CORL、Decision Transformer、Minari（**不下载**轨迹数据）。

## 离策略评价

训练策略与行为策略不同。重要性采样方差、拟合 Q 评价偏差、分布外动作要分列。不能用训练时的在线回报冒充实机效果。

## 评测清单（写入 [`evaluation_audit_cn.csv`](../evaluation_audit_cn.csv) 的字段）

- terminated / truncated / bootstrap。
- 奖励缩放、观测归一化、统计量冻结。
- 随机评测 vs 确定性评测。
- 环境步、更新次数、计算时间。
- 种子、置信区间、聚合方式。
- 模型选择与最终测试分离；超参搜索预算公平。
- 离线覆盖与 OOD。
- 仿真器漏洞与奖励投机。
- 策略更新后的能力/安全退化。
- 检查点权重 vs 可恢复训练状态（优化器、回放、归一化统计量、RNG）。

## 基准论文

Henderson *Deep RL that Matters*、Islam 复现性、Engstrom Implementation Matters、Andrychowicz What Matters、Agarwal rliable。均在 [`14_evaluation/papers/`](../14_evaluation/papers/)。

Zoo 配置：[`projects/DLR_RM_rl_baselines3_zoo_en/`](../projects/DLR_RM_rl_baselines3_zoo_en/)。文档：CleanRL 超参页、SB3 `rl_tips`。
