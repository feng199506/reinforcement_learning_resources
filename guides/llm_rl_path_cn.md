# 语言模型强化学习路线

必须先区分训练方法，不能把所有后训练都叫 RL。

| 方法 | 是否强化学习 | 本库入口 |
|---|---|---|
| SFT | 否，监督 | TRL `sft_trainer` 文档与 [`projects/huggingface_trl_en/`](../projects/huggingface_trl_en/) |
| 奖励模型 | 监督学习（偏好对） | TRL `reward_trainer` |
| PPO-RLHF | 是，在线 RL（策略对奖励模型） | InstructGPT 论文；TRL `ppo_trainer` |
| DPO | 否，偏好对上的分类/回归目标 | arXiv:2305.18290；TRL `dpo_trainer` |
| GRPO / 可验证奖励 | 是，组相对策略梯度 | DeepSeekMath arXiv:2402.03300 |
| RLAIF | 用模型偏好代替人类 | 见 [`12_llm_reasoning_agents/papers/`](../12_llm_reasoning_agents/papers/) |

## 阅读顺序

1. Ziegler / Stiennon / InstructGPT / Bai HH：RLHF 流程。
2. DPO：明确它**替代** PPO，不是 PPO 的实现细节。
3. Let's Verify Step by Step、GSM8K：过程奖励与可验证奖励。
4. DeepSeek-R1：推理 RL；注意哪些阶段是 SFT、哪些是 RL。
5. 奖励投机：奖励模型被策略钻空，与真实目标不一致。

## 代码

- TRL：通用后训练。
- veRL：[`projects/volcengine_verl_en/`](../projects/volcengine_verl_en/)，分布式 LLM RL，与游戏/机器人管线不通用。

## 工程隔离

不默认 LLM RL、游戏 RL、机器人 RL 共用训练管线。观测是 token，动作是 token 或工具调用，奖励常来自模型或校验器，终止是 EOS/步数，与 MuJoCo 的 terminated/truncated 不是同一套语义。

权重与大型语料本轮不下载。
