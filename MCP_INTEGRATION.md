# MCP 接入说明 (MCP_INTEGRATION.md)

> 本文件说明「麦门赛博求签」实际使用的麦当劳官方 MCP Server、调用的工具、调用流程与业务价值，供大赛审核与社区复现。

## 一、实际使用的麦当劳 MCP Server

- **服务地址**：`https://mcp.mcd.cn`（Streamable HTTP / JSON-RPC）
- **鉴权方式**：`Authorization: Bearer <你的 MCP Token>`
  - Token 从官方控制台申请：`https://open.mcd.cn/mcp/doc` → 登录（手机号）→ 控制台 → 激活
  - 本仓库将 Token 存于 `config.json`，**已被 `.gitignore` 忽略**；仅提交模板 `config.example.json`，不含任何真实凭证
- **官方使用指南**：`https://github.com/M-China/mcd-mcp-server`
- **限流**：600 次 / 分钟 / Token

## 二、实际调用的工具（核心链路）

本 Skill 在「只读求签 → 安全下单」全流程中调用以下工具（以 `python scripts/mcp_client.py list` 实测为准，工具集随版本可能变化）：

| 工具 | 用途 |
|---|---|
| `now-time-info` | 定时辰（早 / 午 / 晚 / 夜） |
| `delivery-query-addresses` | 取用户已存配送地址（多地址脱敏询问） |
| `delivery-query-stores` | 按地址查可麦乐送外送门店（拿 `storeCode` + 外送 `beCode`） |
| `query-nearby-stores` | 查最近到店门店（beType=1，无需 beCode） |
| `auto-bind-coupons` | 一键领券（免费，写操作需确认） |
| `available-coupons` | 可领券列表（麦门提醒） |
| `campaign-calendar` | 今日活动 / 大促提醒 |
| `query-meals` | 拉取门店真实菜单 |
| `calculate-price` | 计算到店 / 外送到手价（单位换算：分 → 元） |
| `list-nutrition-foods` | 营养数据（热量 / 蛋白 / 脂肪等） |

> 说明：`query-promotions` 为团餐专用（beType=6），默认路径不调用；其余写操作（领券 / 下单）均在你显式确认后执行。

## 三、调用流程（核心链路）

1. **定时辰**：`now-time-info` 取当前时间 → 映射签等基准（早 / 午 / 晚 / 夜）
2. **查当季热梗**：`WebSearch "<年><月> 网络热梗 流行语"` 取 2-3 个当季梗揉进签诗（**运行时实查，不写死**；搜索失败退回通用俏皮话兜底）
3. **定庙址**：`delivery-query-addresses` 检测多地址 → 仅列脱敏标签询问你选哪个 → `delivery-query-stores`（外送）/ `query-nearby-stores`（到店）
4. **摇签**：按签等映射命定餐品（经典双牛堡 / 豪华 / 单品等）
5. **领券**：`auto-bind-coupons` 免费领券（写操作，需确认）
6. **取真数据**：`query-meals` + `calculate-price` 算「到店自取 + 麦乐送外送」双套餐到手价
7. **麦门提醒**：`campaign-calendar` / `available-coupons` 汇总今日活动与已领券
8. **出签**：签文（含当季热梗）+ 命定餐品 + 今日宜忌 + 营养 + 麦门提醒
9. **安全下单**：仅当你说「就按这个下单」并复核明细确认后，才创建订单（`beType` 约束：到店 beType=1 无需 beCode；外送 beType=2 必传 beCode）

## 四、业务价值

- **全民向**：面向所有麦当劳用户（1024 只是由头，非程序员专属），把点餐变成人人可玩的赛博求签仪式
- **真数据**：所有结果基于麦当劳官方 MCP 实时数据（菜单 / 营养 / 门店 / 活动 / 券 / 价格），可落地下单
- **安全合规**：领券 / 下单等写操作均在你明确确认后执行，绝不静默扣费；不泄露 `fullAddress` / `phone`；仓库不含任何真实 Token
- **梗常新**：签诗热梗运行时按当季实查，不随文件发布日过期，永远新鲜

## 五、最小可运行示例

```bash
# 1) 填入你的 Token（不提交）
cp config.example.json config.json   # 编辑 config.json 粘贴 Token

# 2) 列工具 / 看单个工具入参
python scripts/mcp_client.py list
python scripts/mcp_client.py schema query-meals

# 3) 走核心链路（示例：查当前时间 + 外送门店 + 算价）
python scripts/mcp_client.py now-time-info '{}'
python scripts/mcp_client.py delivery-query-stores '{"addressId":"<你的地址ID>","beType":2}'
python scripts/mcp_client.py calculate-price '{"storeCode":"<storeCode>","orderType":2,"beType":2,"beCode":"<beCode>","items":[{"productCode":"<productCode>","quantity":1}]}'
```
