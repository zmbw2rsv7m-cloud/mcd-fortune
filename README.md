# 麦门赛博求签 (McMen Fortune)

> 基于麦当劳官方 MCP 的趣味点餐决策 Skill
> 面向**所有麦当劳用户**的趣味点餐决策：摇电子签筒，结合麦当劳**官方 MCP**（`https://mcp.mcd.cn`）实时数据，出签文 + 命定餐品 + 今日宜忌，可一键安全下单。

当前版本：V0.1.6（迭代记录见 `CHANGELOG.md`）。

## 特色（差异化）

现有参赛作品多为「省钱 / 控卡 / 下单」工具型。本 Skill 走 **人格化 + 趣味** 路线：
庙签的庄重 × 生活化俏皮话，把点餐变成一场人人能玩的赛博求签仪式（程序员梗仅作可选彩蛋）。
大赛在 1024 举办，但产品面向所有麦当劳用户；且所有结果均基于麦当劳官方 MCP 真实数据（菜单 / 营养 / 门店 / 活动 / 券 / 价格），可落地下单。

## 获取 Token（关键一步）

数据来自麦当劳官方 MCP，需要你自己的 Token（代表你的会员身份）。按官方文档 `https://open.mcd.cn/mcp/doc`：

1. 打开 `https://open.mcd.cn/mcp/doc`，点击右上角 **【登录】**。
2. 跳转到登录页，**用手机号登录**（首次需阅读并同意《使用条款》《麦当劳 MCP 服务规则》）。
3. 登录后点击右上角 **【控制台】**，在弹出的控制台窗口中点 **【激活】** 按钮，申请 MCP Token。
4. 申请成功后**复制 Token**（一长串字符，切勿分享给他人）。

> ⚠️ Token 代表你的麦当劳会员身份，请勿提交到 GitHub 或泄露给他人。

## 安装与配置

1. 把本目录放到用户级技能目录：

   ```
   ~/.workbuddy/skills/mcd-fortune/
   ```

2. 复制配置模板并填入 Token：

   ```bash
   cp config.example.json config.json
   # 编辑 config.json，把 mcp_token 换成你从控制台复制的真实 Token
   ```

   `config.json` 内容：

   ```json
   {
     "mcp_token": "你的麦当劳官方 MCP Token",
     "mcp_endpoint": "https://mcp.mcd.cn"
   }
   ```

   （`config.json` 已在 `.gitignore` 中，不会被提交。）

3. 在 WorkBuddy 对话中说：**「麦门永存」**（兼容「麦门求签」「摇个签」「今天吃啥求签」「麦门黄历」）。

## 连通性自测

无需下单，先验证 Token 与端点是否可用：

```bash
python scripts/mcp_client.py list
python scripts/mcp_client.py schema calculate-price   # 查看参数结构
```

能列出 35 个工具名即代表配置成功。

## 安全

- 下单 / 领券 / 抽奖前强制预览明细 + 用户确认，绝不静默扣费。
- 价格 / 库存 / 限购以下单接口返回为准。
- 限流：每 Token 每分钟最多 600 次，避免高频调用。

## 文件

- `SKILL.md` — 主指令（触发词、流程、安全红线、文案风格）
- `CHANGELOG.md` — 版本与迭代记录（V0.1.0 起）
- `config.example.json` — Token 配置模板（复制为 `config.json` 后填写）
- `scripts/mcp_client.py` — 官方 MCP 直连客户端（仅标准库，自动处理握手与鉴权）
- `references/tool_catalog.md` — 官方 MCP 工具清单与配置要点
- `references/fortune_logic.md` — 签等 → 餐品映射逻辑
- `references/sample_output.md` — 输出样例

## 参赛（2026 麦当劳程序员创意开发大赛）

- 赛事官方仓库：`https://github.com/M-China/mcd-developer-innovation-challenge`
- 麦当劳官方 MCP 使用指南：`https://github.com/M-China/mcd-mcp-server`
- 本仓库已按官方要求包含必需文件：`README.md`、`CONTEST_DECLARATION.md`（内容不可修改）、`MCP_INTEGRATION.md`、源代码（`SKILL.md` + `scripts/` + `references/`），并附带 `workbuddy.md`（WorkBuddy 联动奖励核验用）。
- 安全合规：仓库不含任何真实 Token（`config.json` 已被 `.gitignore` 忽略），领券 / 下单等写操作均经用户显式确认后执行。

