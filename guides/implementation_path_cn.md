# 算法实现路线

本轮代码等级只到 **L0/L1**（已下载并静态见到入口）。不声称运行或复现通过。

## 环境接口

先读 Gymnasium 文档 [`software_docs/Gymnasium_docs_html_en/`](../software_docs/Gymnasium_docs_html_en/)：

- `reset` / `step` 的五元组。
- **terminated**（任务结束）与 **truncated**（时间截断）必须分开；bootstrap 只能在 truncated 时对下一状态做，terminated 时目标为 0。
- 向量环境与 wrappers。

代码：[`projects/Farama_Gymnasium_en/`](../projects/Farama_Gymnasium_en/)。

## 三条实现对照

同一算法看三种风格，避免只抄一种库的默认超参：

1. **教学**：Spinning Up HTML 教程 [`courses/OpenAI_SpinningUp_DeepRL_html_en/`](../courses/OpenAI_SpinningUp_DeepRL_html_en/)（官方 git 仓库本轮因缺少根目录 README 未计入 [`projects/`](../projects/)，见 [`download_failures_cn.csv`](../download_failures_cn.csv) P-22）。
2. **单文件**：CleanRL [`projects/vwxyzjn_cleanrl_en/`](../projects/vwxyzjn_cleanrl_en/)（`ppo.py`、`dqn.py`、`sac_continuous_action.py`）。
3. **模块化**：SB3 [`projects/DLR_RM_stable_baselines3_en/`](../projects/DLR_RM_stable_baselines3_en/)、Tianshou [`projects/thu_ml_tianshou_en/`](../projects/thu_ml_tianshou_en/)。

连续控制再加 TorchRL 采集器：[`projects/pytorch_rl_TorchRL_en/`](../projects/pytorch_rl_TorchRL_en/)。

## 必须静态核对的入口

每个项目根目录有 `SNAPSHOT_en.txt`（commit）。另查：

- 训练脚本：`train.py` / `cleanrl/*.py` / `spinup/algos/...`
- 评测：`enjoy.py`、`eval` 选项、确定性动作开关。
- 配置：SB3-Zoo [`projects/DLR_RM_rl_baselines3_zoo_en/hyperparams/`](../projects/DLR_RM_rl_baselines3_zoo_en/hyperparams/)。
- 依赖：`pyproject.toml` / `requirements.txt` / `setup.py`。
- 许可证文件。

## 实现陷阱（对应评测表）

- 奖励缩放、观测归一化：统计量必须只在训练集或滚动窗口上更新，评测时冻结。
- 探索噪声在评测时应关闭或单独报告。
- 记录环境步数、梯度更新次数与墙钟时间，不要只报 episode return。
- 多种子；聚合用中位数与区间（见 rliable 论文），禁止把单次最高回报当优越性。

## 下一步（本轮不做）

隔离环境按 SNAPSHOT 安装依赖，先在 `CartPole` / `Pendulum` 跑通一步，再谈 MuJoCo。不把上游 README 曲线当作本机复现。
