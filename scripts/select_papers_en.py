#!/usr/bin/env python3
"""Search arXiv, merge curated MUST papers, write seed JSON.

  PYTHONUNBUFFERED=1 python3 -I scripts/select_papers_en.py search
  PYTHONUNBUFFERED=1 python3 -I scripts/select_papers_en.py write
"""
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import SEEDS, CATS, save, load, WINDOW_START, WINDOW_END, window_status
from papers_en import API, parse_entries, meta_file, get_meta, CAND_DIR, http

CODE_RE = re.compile(r"github\.com/[\w.\-]+/[\w.\-]+", re.I)

# Curated canonical papers. IDs must exist on arXiv.
MUST = [
    # 01 foundations / theory
    ("01", "1806.09460", "理论综述", "学术教程", "none",
     "连续控制视角的 RL 导览，连接 MDP、策略搜索与最优控制。",
     "连续控制视角综述，作为动态规划/优化基础读物。"),
    ("01", "1811.12560", "深度RL导论", "学术教程", "none",
     "深度 RL 导论：MDP、价值/策略方法与实现要点。",
     "深度 RL 入门综述。"),
    ("01", "1907.05388", "线性函数逼近理论", "原始研究论文", "none",
     "COLT：线性函数逼近下可证明高效 RL。",
     "线性 FA 可学习性经典结果。"),
    ("01", "1908.00261", "策略梯度理论", "原始研究论文", "none",
     "策略梯度最优性、逼近与分布偏移。",
     "策略梯度理论经典。"),
    ("01", "2106.08005", "结构类", "原始研究论文", "none",
     "Bilinear Classes：可证明泛化的结构框架。",
     "RL 可学习结构类。"),
    ("01", "2007.08101", "有限样本", "原始研究论文", "none",
     "若元数据确认则保留；否则 write 阶段会按标题核验。",
     "有限样本/理论候选，下载时以标题为准。"),
    ("01", "2205.10821", "理论综述", "综述", "none",
     "近年 RL 理论综述候选。",
     "近五年理论综述候选。"),
    ("01", "2301.08252", "理论", "原始研究论文", "none",
     "近年理论论文候选。",
     "近五年理论候选。"),
    # 02 tabular
    ("02", "1807.03765", "Q-learning收敛", "原始研究论文", "none",
     "Is Q-learning Provably Efficient：表格 Q-learning 样本复杂度。",
     "表格 Q-learning 可证明效率。"),
    ("02", "1611.04717", "极小极大遗憾", "原始研究论文", "none",
     "Azar–Osband–Munos：RL 极小极大遗憾界。",
     "表格方法遗憾界经典。"),
    ("02", "1703.05426", "PAC-MDP", "原始研究论文", "none",
     "Dann 等统一 PAC RL。",
     "表格 PAC 框架。"),
    ("02", "2007.08459", "UCBVI", "原始研究论文", "none",
     "表格探索与 UCB 型值迭代候选。",
     "表格探索算法。"),
    ("02", "2107.08346", "表格理论", "原始研究论文", "none",
     "近年表格/有限 MDP 理论候选。",
     "近五年表格理论。"),
    ("02", "2204.05928", "表格方法", "原始研究论文", "none",
     "近年表格方法候选。",
     "近五年表格方法。"),
    # 03 value-based
    ("03", "1312.5602", "DQN", "原始研究论文", "official_partial",
     "Playing Atari with Deep RL：DQN。",
     "深度 Q 网络经典。"),
    ("03", "1509.06461", "Double DQN", "原始研究论文", "official_partial",
     "Double Q-learning 深度化。",
     "Double DQN。"),
    ("03", "1511.05952", "PER", "原始研究论文", "official_partial",
     "优先经验回放。",
     "PER。"),
    ("03", "1511.06581", "Dueling", "原始研究论文", "official_partial",
     "Dueling 网络。",
     "Dueling DQN。"),
    ("03", "1707.06887", "C51", "原始研究论文", "official_partial",
     "分布式价值学习 C51。",
     "C51。"),
    ("03", "1710.02298", "Rainbow", "原始研究论文", "official_partial",
     "Rainbow 组合 DQN 扩展。",
     "Rainbow。"),
    ("03", "1710.10044", "QR-DQN", "原始研究论文", "official_partial",
     "分位数回归分布式 RL。",
     "QR-DQN。"),
    ("03", "1802.01561", "IMPALA", "原始研究论文", "official_partial",
     "IMPALA 重要性加权 Actor-Learner。",
     "离策略稳定的分布式学习。"),
    ("03", "2002.06038", "Agent57", "原始研究论文", "none",
     "Agent57 覆盖 Atari 57。",
     "价值方法扩展。"),
    ("03", "1907.07629", "R2D2", "原始研究论文", "official_partial",
     "Recurrent Replay Distributed DQN。",
     "循环价值学习。"),
    # 04 policy / actor-critic
    ("04", "1502.05477", "TRPO", "原始研究论文", "official_partial",
     "信赖域策略优化。",
     "TRPO。"),
    ("04", "1506.02438", "GAE", "原始研究论文", "official_partial",
     "广义优势估计。",
     "GAE。"),
    ("04", "1707.06347", "PPO", "原始研究论文", "official_full",
     "近端策略优化。",
     "PPO。"),
    ("04", "1509.02971", "DDPG", "原始研究论文", "official_partial",
     "深度确定性策略梯度。",
     "DDPG。"),
    ("04", "1802.09477", "TD3", "原始研究论文", "official_full",
     "Twin Delayed DDPG。",
     "TD3。"),
    ("04", "1801.01290", "SAC", "原始研究论文", "official_full",
     "Soft Actor-Critic。",
     "SAC。"),
    ("04", "1812.05905", "SAC应用", "原始研究论文", "official_full",
     "SAC 算法与应用扩展。",
     "SAC 后续。"),
    ("04", "1602.01783", "A3C", "原始研究论文", "official_partial",
     "异步优势 Actor-Critic。",
     "A3C。"),
    ("04", "2105.14039", "策略梯度", "原始研究论文", "none",
     "近年策略梯度/自然梯度候选。",
     "近五年策略方法。"),
    # 05 exploration
    ("05", "1705.05363", "ICM", "原始研究论文", "official_partial",
     "内在好奇心模块。",
     "ICM。"),
    ("05", "1810.12894", "RND", "原始研究论文", "official_partial",
     "随机网络蒸馏探索。",
     "RND。"),
    ("05", "1707.01495", "HER", "原始研究论文", "official_full",
     "后见经验回放，目标条件策略。",
     "HER。"),
    ("05", "1901.10995", "Go-Explore", "原始研究论文", "official_partial",
     "Go-Explore 稀疏奖励。",
     "Go-Explore。"),
    ("05", "2004.12277", "NeverGiveUp", "原始研究论文", "none",
     "Never Give Up 探索。",
     "NGU。"),
    ("05", "1606.01868", "VIME", "原始研究论文", "official_partial",
     "变分信息最大化探索。",
     "VIME。"),
    ("05", "2206.08853", "探索", "原始研究论文", "none",
     "近年探索方法候选。",
     "近五年探索。"),
    ("05", "2303.11103", "探索", "原始研究论文", "none",
     "近年探索方法候选。",
     "近五年探索。"),
    # 06 model-based
    ("06", "1805.12114", "PETS", "原始研究论文", "official_full",
     "概率集成 + Trajectory Sampling。",
     "PETS。"),
    ("06", "1811.04551", "PlaNet", "原始研究论文", "official_full",
     "潜空间规划 PlaNet。",
     "PlaNet。"),
    ("06", "1912.01603", "Dreamer", "原始研究论文", "official_full",
     "Dreamer 世界模型。",
     "Dreamer。"),
    ("06", "2010.02193", "DreamerV2", "原始研究论文", "official_full",
     "DreamerV2。",
     "DreamerV2。"),
    ("06", "2301.04104", "DreamerV3", "原始研究论文", "official_full",
     "DreamerV3 多样域世界模型。",
     "DreamerV3。"),
    ("06", "1911.08265", "MuZero", "原始研究论文", "none",
     "MuZero 隐式模型规划。",
     "MuZero。"),
    ("06", "1906.08253", "MBPO", "原始研究论文", "official_full",
     "Model-Based Policy Optimization。",
     "MBPO。"),
    ("06", "2006.16712", "模型式综述", "综述", "none",
     "Moerland 等模型式 RL 综述。",
     "模型式综述。"),
    ("06", "2203.04955", "TD-MPC", "原始研究论文", "official_full",
     "时序差分学习 + MPC。",
     "TD-MPC。"),
    ("06", "2310.16828", "TD-MPC2", "原始研究论文", "official_full",
     "TD-MPC2。",
     "TD-MPC2。"),
    # 07 offline / imitation
    ("07", "2005.01643", "离线RL教程", "学术教程", "none",
     "Levine 等离线 RL 教程。",
     "离线 RL 教程。"),
    ("07", "1812.02900", "BCQ", "原始研究论文", "official_full",
     "Batch-Constrained Q-learning。",
     "BCQ。"),
    ("07", "2006.04779", "CQL", "原始研究论文", "official_full",
     "Conservative Q-Learning。",
     "CQL。"),
    ("07", "2110.06169", "IQL", "原始研究论文", "official_full",
     "Implicit Q-Learning。",
     "IQL。"),
    ("07", "2106.06860", "TD3+BC", "原始研究论文", "official_full",
     "TD3+BC 离线连续控制。",
     "TD3+BC。"),
    ("07", "2004.07219", "D4RL", "基准与数据集", "official_partial",
     "D4RL 离线基准。",
     "D4RL。"),
    ("07", "2106.01345", "DecisionTransformer", "原始研究论文", "official_full",
     "Decision Transformer。",
     "DT。"),
    ("07", "1606.03476", "GAIL", "原始研究论文", "official_full",
     "生成对抗模仿学习。",
     "GAIL。"),
    ("07", "1811.06783", "AIRL", "原始研究论文", "official_partial",
     "对抗逆强化学习。",
     "AIRL。"),
    ("07", "2005.13239", "MOPO", "原始研究论文", "official_full",
     "Model-based Offline Policy Optimization。",
     "MOPO。"),
    ("07", "2005.05951", "MOReL", "原始研究论文", "official_full",
     "MOReL 离线模型式。",
     "MOReL。"),
    ("07", "2112.10751", "RvS", "原始研究论文", "official_full",
     "RvS：离线 RL 作为监督。",
     "RvS。"),
    ("07", "2210.07105", "CORL", "基准与数据集", "official_full",
     "CORL 离线实现与评测。",
     "CORL。"),
    # 08 POMDP / hierarchy
    ("08", "1507.06527", "DRQN", "原始研究论文", "official_partial",
     "Deep Recurrent Q-Network。",
     "DRQN。"),
    ("08", "1609.05140", "Option-Critic", "原始研究论文", "official_full",
     "Option-Critic 分层。",
     "Option-Critic。"),
    ("08", "1805.08296", "HIRO", "原始研究论文", "official_full",
     "HIRO 分层离策略。",
     "HIRO。"),
    ("08", "1703.01161", "FuN", "原始研究论文", "official_partial",
     "FeUdal Networks。",
     "FuN。"),
    ("08", "1910.00091", "OpenSpiel论文", "基准与数据集", "official_full",
     "若为 OpenSpiel 系统文则保留；否则 write 时按标题调整分类。",
     "MARL/博弈系统候选。"),
    ("08", "2205.10821", "分层", "原始研究论文", "none",
     "近年分层/记忆策略候选。",
     "近五年分层。"),
    ("08", "2301.00704", "POMDP", "原始研究论文", "none",
     "近年 POMDP/记忆候选。",
     "近五年 POMDP。"),
    # 09 multi-agent
    ("09", "1706.02275", "MADDPG", "原始研究论文", "official_full",
     "多智能体 DDPG，CTDE。",
     "MADDPG。"),
    ("09", "1803.11485", "QMIX", "原始研究论文", "official_full",
     "QMIX 值分解。",
     "QMIX。"),
    ("09", "1705.08926", "COMA", "原始研究论文", "official_partial",
     "Counterfactual Multi-Agent Policy Gradients。",
     "COMA。"),
    ("09", "2103.01955", "MAPPO", "原始研究论文", "official_full",
     "MAPPO。",
     "MAPPO。"),
    ("09", "1902.04043", "SMAC", "基准与数据集", "official_partial",
     "StarCraft Multi-Agent Challenge。",
     "SMAC。"),
    ("09", "1908.09453", "OpenSpiel", "基准与数据集", "official_full",
     "OpenSpiel：博弈 RL 框架论文。",
     "OpenSpiel。"),
    ("09", "2009.14471", "PettingZoo", "基准与数据集", "official_full",
     "PettingZoo 环境套件候选。",
     "PettingZoo。"),
    ("09", "2205.14953", "MARL", "原始研究论文", "none",
     "近年 MARL 候选。",
     "近五年 MARL。"),
    # 10 safe
    ("10", "1705.10528", "CPO", "原始研究论文", "official_partial",
     "Constrained Policy Optimization。",
     "CPO。"),
    ("10", "1910.12708", "SafetyGym", "基准与数据集", "official_partial",
     "Benchmarking Safe Exploration。",
     "Safety Gym。"),
    ("10", "1705.08417", "安全综述", "综述", "none",
     "安全 RL 综述候选。",
     "安全 RL 综述。"),
    ("10", "2001.09377", "约束RL", "原始研究论文", "none",
     "约束 MDP / 风险敏感候选。",
     "约束 RL。"),
    ("10", "2102.09079", "安全RL", "原始研究论文", "none",
     "近年安全 RL 候选。",
     "近五年安全 RL。"),
    ("10", "2205.10330", "鲁棒", "原始研究论文", "none",
     "鲁棒/约束候选。",
     "鲁棒 RL。"),
    ("10", "2303.03231", "安全", "原始研究论文", "none",
     "近年安全探索候选。",
     "近五年安全。"),
    ("10", "2404.04710", "安全", "原始研究论文", "none",
     "近年安全/鲁棒候选。",
     "近五年安全。"),
    # 11 transfer / foundation
    ("11", "1703.03400", "MAML", "原始研究论文", "official_full",
     "Model-Agnostic Meta-Learning。",
     "MAML。"),
    ("11", "1903.08254", "PEARL", "原始研究论文", "official_full",
     "PEARL 元 RL。",
     "PEARL。"),
    ("11", "1703.06907", "域随机化", "原始研究论文", "official_partial",
     "Domain randomization for sim-to-real。",
     "域随机化。"),
    ("11", "2205.06175", "Gato", "原始研究论文", "none",
     "Gato 通用智能体。",
     "Gato。"),
    ("11", "1910.07113", "sim2real", "原始研究论文", "none",
     "OpenAI Rubik 立方 sim-to-real 候选。",
     "sim-to-real。"),
    ("11", "2206.07568", "迁移", "原始研究论文", "none",
     "近年迁移/多任务候选。",
     "近五年迁移。"),
    ("11", "2312.05253", "基础模型", "原始研究论文", "none",
     "RL 基础模型候选。",
     "RL 基础模型。"),
    ("11", "2402.19402", "基础模型", "综述", "none",
     "近年基础模型/多任务候选。",
     "近五年基础模型。"),
    # 12 LLM RL
    ("12", "1909.08593", "RLHF早期", "原始研究论文", "official_partial",
     "Ziegler 等：从人类偏好微调语言模型。",
     "早期 RLHF。"),
    ("12", "2009.01325", "摘要RLHF", "原始研究论文", "official_partial",
     "Stiennon 等摘要 RLHF。",
     "摘要 RLHF。"),
    ("12", "2203.02155", "InstructGPT", "原始研究论文", "none",
     "InstructGPT：SFT + 奖励模型 + PPO。",
     "InstructGPT。"),
    ("12", "2204.05862", "HH-RLHF", "原始研究论文", "official_partial",
     "Bai 等有助且无害。",
     "HH-RLHF。"),
    ("12", "2305.18290", "DPO", "原始研究论文", "official_full",
     "Direct Preference Optimization：不是在线 RL。",
     "DPO，须与 PPO-RLHF 区分。"),
    ("12", "2402.03300", "GRPO", "原始研究论文", "official_partial",
     "DeepSeekMath：GRPO 可验证奖励。",
     "GRPO。"),
    ("12", "2501.12948", "DeepSeek-R1", "原始研究论文", "official_partial",
     "DeepSeek-R1 推理强化学习。",
     "DeepSeek-R1。"),
    ("12", "2305.20050", "过程奖励", "原始研究论文", "official_partial",
     "Let's Verify Step by Step。",
     "过程奖励。"),
    ("12", "2110.14168", "GSM8K", "基准与数据集", "official_partial",
     "GSM8K 可验证数学。",
     "GSM8K。"),
    ("12", "2310.01377", "RLAIF", "原始研究论文", "none",
     "RLAIF 候选。",
     "RLAIF。"),
    ("12", "2404.14715", "LLM-RL", "原始研究论文", "none",
     "近年 LLM RL 候选。",
     "近五年 LLM RL。"),
    ("12", "2409.12122", "推理RL", "原始研究论文", "none",
     "近年推理 RL 候选。",
     "近五年推理 RL。"),
    # 13 applications
    ("13", "1912.06680", "OpenAIFive", "原始研究论文", "none",
     "Dota 2 OpenAI Five。游戏 RL，不可直接当工业管线。",
     "游戏 RL 案例。"),
    ("13", "1902.01714", "AlphaStar", "原始研究论文", "none",
     "AlphaStar。",
     "游戏 RL 案例。"),
    ("13", "1712.01815", "AlphaZero", "原始研究论文", "none",
     "AlphaZero。",
     "规划+自对弈。"),
    ("13", "2011.09607", "FinRL", "原始研究论文", "official_full",
     "FinRL 金融决策。",
     "金融应用。"),
    ("13", "2103.11972", "工业应用", "原始研究论文", "none",
     "工业/调度应用候选。",
     "工业应用。"),
    ("13", "2006.06821", "能源", "原始研究论文", "none",
     "能源/需求响应候选。",
     "能源应用。"),
    ("13", "2107.07511", "交通", "原始研究论文", "none",
     "交通应用候选。",
     "交通应用。"),
    ("13", "2203.00310", "机器人", "原始研究论文", "none",
     "机器人控制应用候选。",
     "机器人应用。"),
    ("13", "2306.11700", "调度", "原始研究论文", "none",
     "调度/资源分配候选。",
     "调度应用。"),
    # 14 evaluation
    ("14", "1709.06560", "DeepRLThatMatters", "立场与方法论", "official_partial",
     "Deep Reinforcement Learning that Matters。",
     "评测失效经典。"),
    ("14", "1708.04133", "复现", "立场与方法论", "none",
     "Islam 等深度 RL 复现性。",
     "复现性。"),
    ("14", "2108.13264", "rliable", "立场与方法论", "official_full",
     "Deep RL at the Edge of the Statistical Precipice。",
     "rliable 多种子与区间。"),
    ("14", "2005.12729", "ImplementationMatters", "立场与方法论", "official_full",
     "Implementation Matters in Deep RL。",
     "实现细节敏感性。"),
    ("14", "2006.05990", "WhatMattersOnPolicy", "立场与方法论", "official_full",
     "What Matters In On-Policy Reinforcement Learning。",
     "同策略实现消融。"),
    ("14", "1812.11711", "多种子", "立场与方法论", "official_partial",
     "Colas 等种子与统计。",
     "种子与统计。"),
    ("14", "2112.12320", "评测", "立场与方法论", "none",
     "近年评测协议候选。",
     "评测协议。"),
    ("14", "2206.05281", "评测", "立场与方法论", "none",
     "近年评测候选。",
     "近五年评测。"),
    ("14", "2304.01315", "评测", "立场与方法论", "none",
     "近年评测候选。",
     "近五年评测。"),
    # 15 software / systems
    ("15", "2111.08819", "CleanRL", "原始研究论文", "official_full",
     "CleanRL 单文件实现。",
     "CleanRL。"),
    ("15", "1712.09381", "RLlib", "原始研究论文", "official_full",
     "RLlib 分布式 RL。",
     "RLlib。"),
    ("15", "2306.00577", "TorchRL", "原始研究论文", "official_full",
     "TorchRL。",
     "TorchRL。"),
    ("15", "2407.17032", "Gymnasium", "原始研究论文", "official_full",
     "Gymnasium 环境 API。",
     "Gymnasium。"),
    ("15", "1812.06110", "Dopamine", "原始研究论文", "official_full",
     "Dopamine 框架。",
     "Dopamine。"),
    ("15", "1912.10600", "Acme", "原始研究论文", "official_full",
     "Acme。",
     "Acme。"),
    ("15", "2107.14171", "Tianshou", "原始研究论文", "official_full",
     "Tianshou。",
     "Tianshou。"),
    ("15", "2209.10958", "工程", "原始研究论文", "none",
     "近年 RL 系统/工程候选。",
     "近五年系统。"),
]

QUERIES = [
    ("01", "MDP理论", 'ti:"Markov decision" AND (all:Bellman OR all:"value iteration" OR all:"policy iteration")'),
    ("01", "随机逼近", 'ti:"stochastic approximation" AND (all:reinforcement OR all:TD OR all:"Q-learning")'),
    ("01", "样本复杂度", 'ti:"reinforcement learning" AND (all:"sample complexity" OR all:"PAC" OR all:minimax) AND (cat:cs.LG OR cat:stat.ML)'),
    ("02", "表格Q", 'ti:"Q-learning" AND (all:tabular OR all:"finite MDP" OR all:convergence)'),
    ("02", "TD资格迹", '(ti:"temporal difference" OR ti:"eligibility trace" OR ti:SARSA) AND (all:tabular OR all:convergence)'),
    ("03", "DQN扩展", '(ti:DQN OR ti:"distributional reinforcement" OR ti:Rainbow) AND (cat:cs.LG OR cat:cs.AI)'),
    ("03", "离策略价值", 'ti:"off-policy" AND (all:"Q-learning" OR all:"value-based") AND (cat:cs.LG)'),
    ("04", "PPO-SAC", '(ti:PPO OR ti:"proximal policy" OR ti:"soft actor-critic" OR ti:TD3) AND (cat:cs.LG OR cat:cs.AI)'),
    ("04", "策略梯度", 'ti:"policy gradient" AND (all:baseline OR all:advantage OR all:"natural gradient")'),
    ("05", "内在奖励", '(ti:exploration OR ti:"intrinsic reward" OR ti:"curiosity") AND all:"reinforcement learning"'),
    ("05", "目标条件", '(ti:"goal-conditioned" OR ti:"hindsight" OR ti:"curriculum") AND all:"reinforcement learning"'),
    ("06", "世界模型", '(ti:"world model" OR ti:Dreamer OR ti:MuZero OR ti:"model-based reinforcement")'),
    ("06", "MPC规划", '(ti:MPC OR ti:"model predictive") AND all:"reinforcement learning"'),
    ("07", "离线RL", '(ti:"offline reinforcement" OR ti:"batch reinforcement" OR ti:CQL OR ti:"implicit Q")'),
    ("07", "模仿学习", '(ti:"imitation learning" OR ti:"inverse reinforcement" OR ti:"behavior cloning")'),
    ("08", "POMDP", '(ti:POMDP OR ti:"partially observable") AND (all:reinforcement OR all:planning)'),
    ("08", "分层", '(ti:"hierarchical reinforcement" OR ti:"option-critic" OR ti:"skill learning")'),
    ("09", "MARL", '(ti:"multi-agent reinforcement" OR ti:MAPPO OR ti:QMIX OR ti:MADDPG)'),
    ("10", "安全约束", '(ti:"safe reinforcement" OR ti:"constrained MDP" OR ti:"risk-sensitive")'),
    ("11", "迁移元学习", '(ti:"meta reinforcement" OR ti:"transfer reinforcement" OR ti:"sim-to-real") AND all:reinforcement'),
    ("12", "RLHF", '(ti:RLHF OR ti:"reinforcement learning from human feedback" OR ti:GRPO)'),
    ("12", "DPO对比", '(ti:"direct preference optimization" OR ti:DPO) AND (all:language OR all:LLM)'),
    ("13", "机器人控制", '(ti:"reinforcement learning") AND (all:robot OR all:manipulation OR all:locomotion) AND (cat:cs.RO OR cat:cs.LG)'),
    ("13", "工业调度", '(ti:"reinforcement learning") AND (all:scheduling OR all:maintenance OR all:"energy management" OR all:traffic)'),
    ("14", "评测复现", '(ti:"reinforcement learning") AND (all:reproducibility OR all:benchmark OR all:evaluation) AND (all:seed OR all:statistic)'),
    ("15", "软件系统", '(ti:Gymnasium OR ti:CleanRL OR ti:TorchRL OR ti:RLlib OR ti:Tianshou)'),
]


def search(per=40):
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    cands = load(CAND_DIR / "all_en.json", {})
    win = f"submittedDate:[{WINDOW_START.replace('-', '')}0000 TO {WINDOW_END.replace('-', '')}2359]"
    for cat, sub, q in QUERIES:
        qq = f"({q}) AND {win}"
        url = API + urllib.parse.urlencode({"search_query": qq, "start": 0, "max_results": per,
                                           "sortBy": "relevance", "sortOrder": "descending"})
        st, body, _, _ = http(url, accept="application/atom+xml", tries=4)
        if st != 200:
            print(f"  [{st}] {cat} {sub}: {q[:80]}", flush=True)
            continue
        ents = parse_entries(body)
        for rank, (aid, m) in enumerate(ents.items()):
            save(meta_file(aid), m)
            c = cands.setdefault(aid, {"hits": [], "cats": []})
            c["hits"].append({"cat": cat, "subtopic": sub, "q": q, "rank": rank})
            if cat not in c["cats"]:
                c["cats"].append(cat)
        print(f"  {len(ents):3d}  {cat} {sub}", flush=True)
        save(CAND_DIR / "all_en.json", cands)
    print("candidates", len(cands), flush=True)


RL_RE = re.compile(
    r"\b(reinforcement learning|markov decision|q-learning|policy gradient|actor-critic|"
    r"temporal difference|bellman|mdp\b|pomdp|offline rl|imitation learning|"
    r"multi-agent reinforcement|world model|proximal policy|soft actor)\b",
    re.I)
NOT_RE = re.compile(
    r"\b(quantum chemistry only|cryptocurrency pump)\b", re.I)


def classify(m, default="04"):
    blob = (m.get("title", "") + " " + m.get("abstract", "")).lower()
    rules = [
        ("12", r"rlhf|language model|llm|dpo\b|grpo|instructgpt|reward hacking|process reward"),
        ("10", r"safe reinforcement|constrained mdp|risk-sensitive|cpo\b|control barrier"),
        ("09", r"multi-agent|multiagent|mappo|qmix|maddpg|markov game"),
        ("08", r"pomdp|partially observable|hierarchical reinforcement|option-critic|skill learning"),
        ("07", r"offline reinforcement|batch rl|imitation learning|inverse reinforcement|behavior cloning|conservative q"),
        ("06", r"model-based reinforcement|world model|dreamer|muzero|model predictive"),
        ("05", r"exploration|intrinsic reward|curiosity|hindsight|goal-conditioned|curriculum"),
        ("03", r"\bdqn\b|distributional reinforcement|rainbow|dueling|prioritized replay"),
        ("04", r"policy gradient|actor-critic|ppo\b|soft actor|td3|trpo|gae\b"),
        ("02", r"tabular|q-learning|sarsa|eligibility trace|td\(\d"),
        ("14", r"reproducib|evaluation protocol|statistical|rliable|benchmarking deep rl"),
        ("15", r"gymnasium|cleanrl|torchrl|rllib|software|library"),
        ("13", r"robot|schedul|energy|traffic|maintenance|recommend"),
        ("11", r"transfer|meta-learning|sim-to-real|domain random|foundation model"),
        ("01", r"sample complexity|bellman|markov decision|stochastic approximation"),
    ]
    for cat, pat in rules:
        if re.search(pat, blob):
            return cat
    return default


def write_seeds(per_cat_max=10, recent_fill=6, classic_cap=5):
    cands = load(CAND_DIR / "all_en.json", {})
    must_ids = [aid for _, aid, *_ in MUST]
    metas = get_meta(list(dict.fromkeys(must_ids + list(cands))))
    buckets = {c: [] for c in CATS}
    used = set()

    def add(cat, item, aid=None):
        if aid and aid in used:
            return False
        classic = bool(item.get("classic_reason"))
        if classic and sum(1 for x in buckets[cat] if x.get("classic_reason")) >= classic_cap:
            if aid:
                used.add(aid)
            return False
        if len(buckets[cat]) >= per_cat_max:
            return False
        if aid:
            used.add(aid)
        buckets[cat].append(item)
        return True

    for cat, aid, sub, typ, code_kind, reason, classic in MUST:
        m = metas.get(aid)
        if not m:
            print(f"  MUST missing meta {aid} ({cat})", flush=True)
            continue
        abs_ = m.get("abstract") or ""
        comment = m.get("comment") or ""
        gh = CODE_RE.search(comment + " " + abs_)
        item = {
            "arxiv": aid,
            "subtopic": sub,
            "type": typ,
            "level": "硕士/博士",
            "difficulty": "中级",
            "reason": reason,
            "summary": (abs_[:400] + "…") if len(abs_) > 400 else abs_,
            "summary_basis": "arXiv 摘要（检索日）",
            "code_kind": code_kind,
            "task": sub,
        }
        if gh and not item.get("code_url"):
            item["code_url"] = "https://" + gh.group(0)
            if item["code_kind"] in ("none", "待全文核实"):
                item["code_kind"] = "official_partial"
        if window_status(m["v1_date"]) != "近五年":
            item["classic_reason"] = classic
        jr = (m.get("journal_ref") or "") + " " + comment
        if re.search(r"workshop", jr, re.I) and not re.search(r"proceedings of (icml|neurips|nips|iclr|colt)", jr, re.I):
            item["venue_note"] = "注释含 workshop：不得标为主会论文"
        add(cat, item, aid)

    scored = []
    for aid, c in cands.items():
        if aid in used:
            continue
        m = metas.get(aid)
        if not m:
            continue
        blob = (m.get("title", "") + " " + m.get("abstract", ""))
        if not RL_RE.search(blob) or NOT_RE.search(blob):
            continue
        if window_status(m["v1_date"]) != "近五年":
            continue
        gh = 1 if CODE_RE.search((m.get("comment") or "") + (m.get("abstract") or "")) else 0
        best = min((h["rank"] for h in c["hits"]), default=99)
        scored.append((gh, len(c["hits"]), -best, aid, m, c))
    scored.sort(reverse=True)

    for gh, n, nb, aid, m, c in scored:
        cat = classify(m)
        if len(buckets[cat]) >= per_cat_max:
            for h in c["hits"]:
                if len(buckets.get(h["cat"], [])) < per_cat_max:
                    cat = h["cat"]
                    break
            else:
                needy = min(buckets, key=lambda k: len(buckets[k]))
                if len(buckets[needy]) < recent_fill:
                    cat = needy
                else:
                    continue
        abs_ = m.get("abstract") or ""
        comment = m.get("comment") or ""
        ghm = CODE_RE.search(comment + " " + abs_)
        item = {
            "arxiv": aid,
            "subtopic": (c.get("hits") or [{"subtopic": CATS[cat][1]}])[0]["subtopic"],
            "type": "原始研究论文",
            "level": "硕士/博士",
            "difficulty": "中级",
            "reason": "近五年 arXiv 检索命中，标题/摘要含强化学习核心用语，且与该子方向匹配。",
            "summary": (abs_[:400] + "…") if len(abs_) > 400 else abs_,
            "summary_basis": "arXiv 摘要（检索日）",
            "code_kind": "official_partial" if ghm else "待全文核实",
            "task": CATS[cat][1],
        }
        if ghm:
            item["code_url"] = "https://" + ghm.group(0)
        jr = (m.get("journal_ref") or "") + " " + comment
        if re.search(r"workshop", jr, re.I):
            item["venue_note"] = "注释含 workshop：不得标为主会论文"
        add(cat, item, aid)

    outdir = SEEDS / "papers"
    outdir.mkdir(parents=True, exist_ok=True)
    total = 0
    n_recent = n_classic = 0
    for cat, (slug, *_rest) in CATS.items():
        items = buckets[cat]
        path = outdir / f"{cat}_{slug}_seed_cn.json"
        path.write_text(json.dumps(items, ensure_ascii=False, indent=1))
        total += len(items)
        for it in items:
            if it.get("classic_reason"):
                n_classic += 1
            else:
                n_recent += 1
        print(f"{cat} {slug}: {len(items)} seeds", flush=True)
    print(f"papers {total} (recent {n_recent}, classic {n_classic})", flush=True)


if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["search"])[0]
    if cmd == "search":
        search(int(sys.argv[2]) if len(sys.argv) > 2 else 40)
    elif cmd == "write":
        write_seeds()
    else:
        print(__doc__)
