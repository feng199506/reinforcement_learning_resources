# 理论研究路线

面向需要样本复杂度、收敛与函数逼近反例的读者。经典论文在目录中单列为“五年前（经典补充）”。

## 1. MDP 与抽象 DP

- Sutton 第 3–4 章（直觉）。
- Bertsekas *Abstract Dynamic Programming* 第 1–2 章：压缩映射、值/策略迭代。
- Bertsekas & Tsitsiklis *Neuro-Dynamic Programming*：函数逼近下的反例。

## 2. 表格可学习性

必读（本库论文）：

- Jin et al. *Minimax Regret Bounds for Reinforcement Learning*（arXiv:1703.05449）。
- Jin et al. *Is Q-learning Provably Efficient*（arXiv:1807.03765）。

配套：Szepesvári 算法书附录中的折扣 MDP。

## 3. 函数逼近与结构

- Jin et al. 线性函数逼近（arXiv:1907.05388）。
- Du et al. Bilinear Classes（arXiv:2103.10897）。
- Agarwal–Jiang–Kakade–Sun 理论书：[`books/Agarwal_Jiang_Kakade_Sun_Brantley_RL_Theory_ABJKS_en.pdf`](../books/Agarwal_Jiang_Kakade_Sun_Brantley_RL_Theory_ABJKS_en.pdf)。

## 4. 策略优化理论

Agarwal et al. 策略梯度最优性与分布偏移（arXiv:1908.00261）。不要把 PPO 的裁剪系数当成 TRPO 的 KL 约束证明。

## 5. 探索理论

Lattimore–Szepesvári *Bandit Algorithms* 随机/对抗/贝叶斯三部分，再读 MDP 中的乐观原理（UCRL 类，见 Szepesvári 书）。

## 6. 离线与离策略评价

Levine 离线教程（arXiv:2005.01643）之后读 CQL/IQL。离策略评价偏差、覆盖不足与 OOD 动作必须分开写，不能用在线回报代替。

## 7. 随机逼近

Recht 导览（arXiv:1806.09460）给出控制视角。严格 SA 证明以 NDP 与 Borkar 传统文献为准；本轮未收录付费墙专著。

## 8. 读法

先读定理条件（覆盖、可实现性、Bellman 完备），再看算法。关键理论论文允许无代码。
