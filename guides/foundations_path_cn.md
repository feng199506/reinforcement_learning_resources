# 基础学习路线

适用：本科入门到研究生先修。本路线只指向本库已收集资料，不替代课程学分。

## 1. 概率与优化先修

- 概率：[`courses/MIT_OCW_6_041SC_Probabilistic_Systems_en.zip`](../courses/MIT_OCW_6_041SC_Probabilistic_Systems_en.zip)（MIT 6.041SC）。
- 凸优化：[`books/Boyd_Vandenberghe_Convex_Optimization_en.pdf`](../books/Boyd_Vandenberghe_Convex_Optimization_en.pdf)。用于策略优化、信赖域与约束，不是 RL 算法书。

## 2. MDP、价值函数与 Bellman 方程

1. Sutton & Barto 第 3–4 章：[`books/Sutton_Barto_RL_Introduction_2ed_2020_en.pdf`](../books/Sutton_Barto_RL_Introduction_2ed_2020_en.pdf)。
2. David Silver 第 1–3 讲：[`courses/UCL_David_Silver_RL_Course_2015_en/`](../courses/UCL_David_Silver_RL_Course_2015_en/)。
3. Kochenderfer 等《Algorithms for Decision Making》第 7 章精确求解：[`books/Kochenderfer_Wheeler_Wray_Algorithms_Decision_Making_en.pdf`](../books/Kochenderfer_Wheeler_Wray_Algorithms_Decision_Making_en.pdf)。
4. 控制表述：Bertsekas 1976/1987 动态规划全书（`books/Bertsekas_*DP*_en.pdf`）。

完成标志：能手写有限 MDP 的价值迭代、策略迭代，并说明折扣、平均代价与随机最短路的差别。

## 3. 表格方法

Silver 第 4–5 讲 + Sutton 第 5–6、12 章。对应子目录 [`02_tabular_methods/papers/`](../02_tabular_methods/papers/)。

必须分清：

- Monte Carlo：完整回报，不 bootstrap。
- TD(0)/TD(λ)：bootstrap 与资格迹。
- SARSA：同策略；Q-learning：离策略。
- 探索：ε-greedy、UCB；收敛条件见 Szepesvári [`books/Szepesvari_Algorithms_for_RL_en.pdf`](../books/Szepesvari_Algorithms_for_RL_en.pdf)。

## 4. 探索的独立基础

Bandit 不是“小 MDP”，而是探索–利用的骨架：[`books/Lattimore_Szepesvari_Bandit_Algorithms_en.pdf`](../books/Lattimore_Szepesvari_Bandit_Algorithms_en.pdf)。

## 5. 函数逼近入口

Sutton 第 9–13 章，Silver 第 6–7 讲。理论侧：[`books/Agarwal_Jiang_Kakade_Sun_Brantley_RL_Theory_ABJKS_en.pdf`](../books/Agarwal_Jiang_Kakade_Sun_Brantley_RL_Theory_ABJKS_en.pdf) 与 [`books/Bertsekas_Tsitsiklis_Neuro_Dynamic_Programming_en.pdf`](../books/Bertsekas_Tsitsiklis_Neuro_Dynamic_Programming_en.pdf)（反例与收敛）。

## 6. 建议顺序

本科：Sutton → Silver → Spinning Up 文档 [`courses/OpenAI_SpinningUp_DeepRL_html_en/`](../courses/OpenAI_SpinningUp_DeepRL_html_en/) → CleanRL 代码。

研究生理论：Szepesvári → Agarwal et al. → Abstract DP [`books/Bertsekas_Abstract_Dynamic_Programming_3ed_en.pdf`](../books/Bertsekas_Abstract_Dynamic_Programming_3ed_en.pdf)。

控制/运筹：Bertsekas Course in RL [`books/Bertsekas_Course_in_Reinforcement_Learning_2ed_en.pdf`](../books/Bertsekas_Course_in_Reinforcement_Learning_2ed_en.pdf) 与 Powell [`books/Powell_Sequential_Decision_Analytics_Modeling_2ed_en.pdf`](../books/Powell_Sequential_Decision_Analytics_Modeling_2ed_en.pdf)。
