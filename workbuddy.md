# WorkBuddy 开发记录 (workbuddy.md)

> 本文件为本 Skill 使用 WorkBuddy 辅助开发的对话上下文导出，用于核验是否符合「WorkBuddy 联动活动奖励」条件。
> 本作品全程使用 WorkBuddy（对话式）完成构思、MCP 接入调试、文案迭代与一键推送参赛。

## 一、开发脉络（WorkBuddy 对话式推进）

- **定方向**：以「麦当劳 × WorkBuddy 大赛」为目标，先与 WorkBuddy 确认用户范围——**面向所有麦当劳用户**（1024 只是由头，非程序员专属），走「人格化 + 趣味」路线，与多数「省钱 / 控卡」工具型作品差异化。
- **定方案**：Skill 直连官方 MCP（`https://mcp.mcd.cn`），Token 存 Skill 目录 `config.json`（模板 `config.example.json`，已被 `.gitignore` 忽略），触发词「麦门永存」。
- **接入调试**：用 `scripts/mcp_client.py`（仅 Python 标准库）实测 35 个工具 schema 与三类响应格式（JSON / 纯文本 markdown / 门店数组），定位并解决：价格单位（分 → 元）、外送 `beCode` 必传约束、JSON 尾部脏数据（`json.JSONDecoder().raw_decode` 取首段）等坑。
- **迭代（V0.1.0 → V0.1.6）**：按反馈逐步加入「多地址脱敏询问（绝不默认第一个）」「先领券再给到店 + 外送双套餐」「签诗热梗运行时化（WebSearch 当季热梗，不写死，搜索失败兜底）」，并对全文件精简（SKILL.md 5700 → 3592 字符，功能不减）。
- **全链路实测**：说「麦门永存」跑通 时辰 → 热梗 → 多地址询问 → 摇签 → 领券 → 双套餐真实出价，全程只读未下单，隐私仅显城市区。

## 二、贯穿开发的安全红线

- 领券 / 下单等**写操作**，必须经你明确确认，绝不静默扣费；
- 不提交任何真实 Token（`config.json` 已被 `.gitignore` 忽略）；
- 不泄露 `fullAddress` / `phone`，多地址仅列脱敏标签询问你选哪个。

## 三、WorkBuddy 带来的效率

- 对话式即可完成 MCP 端点探测、工具 schema 梳理、脚本调试与文案多轮迭代；
- 一键按官方要求补齐参赛必需文件（`CONTEST_DECLARATION.md` / `MCP_INTEGRATION.md` / `workbuddy.md`）并推送到 GitHub、提交报名 Issue；
- 显著加速「创意 → 可运行 Skill → 参赛」的闭环。

## 四、结论

本作品符合大赛「创意 + 实用」导向，且全部结果基于麦当劳官方 MCP 真实数据、可安全落地下单。WorkBuddy 的对话式开发是其能快速成型并参赛的关键。
