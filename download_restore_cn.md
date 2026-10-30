# 强化学习资源库全文包：下载与离线阅读说明（2026-10-30）

## 下载哪些文件

Release `rl-full-20261030` 附件：

| 附件 | 内容 |
|---|---|
| `reinforcement_learning_resources_20261030_batch001_cn_en.tar` | 首页、目录与登记表、中文指南、脚本、15 个子方向的论文、教材、课程、官方软件文档离线网页、参考项目源码（前半） |
| `reinforcement_learning_resources_20261030_batch002_cn_en.tar` | 参考项目源码（后半）、官方软件文档离线网页 |
| `reinforcement_learning_resources_20261030_books_restricted_cn_en.tar` | 9 本版权页注明“保留全部权利”的教材（Boyd 1 本、Bertsekas 7 本、Powell 1 本），按仓库所有者决定随包提供，单独成包，见 `release_restricted_books_cn.csv` |
| `archive_index_cn.csv` | 每个文件在哪个 tar 包里、大小、改动说明 |
| `windows_rename_map_cn.csv` | 为 Windows 改名、为离线阅读改内容/新增文件的全部明细 |
| `release_restricted_books_cn.csv` | 上述 9 本书的清单与作者站点 |
| `upload_report_cn.md` | 上传状态 |

各 tar 包互相独立，可以只下需要的。tar 包不压缩，每个不超过 1.5 GiB。

## Windows 解压

1. 把所有 tar 包下载到**同一个较短的目录**，例如 `D:\RL\`（路径越短越好，包内最长相对路径 168 个字符）。
2. 解压到同一个文件夹（三个包解压后自然合并成一个资料库目录）：
   - Windows 10/11 自带命令（在该目录打开“终端/命令提示符”）：
     `tar -xf reinforcement_learning_resources_20261030_batch001_cn_en.tar`，其余两个包同样执行。
   - 或用 7-Zip：选中全部 tar →“解压到当前文件夹”。
3. 打开 `index_cn.html`（双击，用 Edge/Chrome/Firefox）即可离线浏览。

## 离线阅读说明

- `index_cn.html`：离线首页，列出中文指南、登记表和全部 206 条目录，每条直接链接到本地 PDF / 网页 / 源码目录。
- `README_cn.html`、`guides/*.html`：Markdown 说明的网页版，路径都是可点击的相对链接；公式用包内 MathJax（`_offline_libs/`）渲染，无需联网。
- 课程网页（`courses/*_html_en/`）与官方软件文档（`software_docs/*/`）：已补下原站的样式表、脚本、字体、图片，改为包内相对路径；已保存页面之间的链接离线跳转。**只保存了部分页面**，指向未保存页面的链接已改为原站完整网址（联网时可打开）。统计、评论、广告、Read the Docs 在线插件等脚本不随包提供，离线时不影响正文显示。
- MIT OCW 三门课是官方离线网站压缩包（`courses/*.zip`），解压后打开其中的 `index.html`。6.041SC 包内 124 个过长文件名已截短（并同步改了包内引用），以免 Windows 解压超出 260 字符。
- 参考项目源码（`projects/`）保持上游原样，每个目录有 `SNAPSHOT_en.txt` 记录来源与提交。
- 改名/改内容明细：`windows_rename_map_cn.csv`。资料库原件未改动。

## 校验

`archive_index_cn.csv` 列出每个文件的字节数；解压后可对照。`tar -tf <包名>` 可列出包内文件。
