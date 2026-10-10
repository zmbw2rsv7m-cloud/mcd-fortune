# 麦当劳官方 MCP 工具清单

端点 `https://mcp.mcd.cn`（Streamable HTTP/JSON-RPC）；`Authorization: Bearer <Token>`，Token 从 `open.mcd.cn` 控制台申请。工具集随版本可能变，以 `python scripts/mcp_client.py list` 实测为准。✅ 本 Skill 用；❗ 写操作需确认。

## 配置
技能目录 `config.json`：`{"mcp_token":"...","mcp_endpoint":"https://mcp.mcd.cn"}`（模板见 config.example.json）。可选 WorkBuddy 连接器：在 `~/.workbuddy/mcp.json` 加 `mcpServers.mcd-mcp`（type streamablehttp, url, headers.Authorization）。本 Skill 不依赖连接器。

## 工具
**求签主链路（✅只读）**
- now-time-info 当前时间（定时辰）
- delivery-query-addresses 已存配送地址（无参；返回 addressId/fullAddress/phone，phone 已脱敏可显，fullAddress 按红线脱敏）
- delivery-query-stores 地址附近可配送店（addressId+beType=2；data 直接是门店数组，取 data[0].storeCode+beCode）
- query-nearby-stores 到店店（searchType=2 必填 city+keyword，beType=1）
- query-meals 门店菜单（必填 storeCode；外送加 beType+beCode）
- query-meal-detail 餐品详情
- list-nutrition-foods 营养
- campaign-calendar 活动日历
- available-coupons 可领券（**返回 markdown，无 JSON，直接呈现**，无参）
- query-store-coupons 门店券
- calculate-price 算到手价（外送必传 storeCode+beCode+beType=2；单位「分」）
- query-promotions ⚠️ 仅团餐(beType=6)专用，默认不调

**写操作（❗确认后/引导时）**
- create-order 下单（外送必传 storeCode+beCode+beType=2）
- cancel-order / auto-bind-coupons 领券 / draw-lottery 抽奖 / mall-create-order 积分兑换 / delivery-create-address 建地址（仅无地址且要外送时引导）/ party-order-create 派对

**会员/资产（✅只读，扩展用）**
- query-my-account / query-my-coupons / query-my-prizes / mall-points-products / mall-product-detail / mall-order-* / order-list / query-order

**其他（默认不用）**
- query-meal-assistance / query-survey-coupon / query-lottery-info / query-party-city / query-party-store / query-party-store-date / query-party-store-session

## 注意
- 定庙址默认麦乐送：`delivery-query-addresses`→addressId→`delivery-query-stores(addressId,beType=2)` 拿 storeCode+beCode；外送后续必传 beCode，到店(beType=1)无需。
- calculate-price 单位「分」→÷100「元」；query-meals.currentPrice 已是「元」。
- 响应三类解析见 SKILL.md「响应解析」。
- 隐私：fullAddress 仅显城市-区；phone 已脱敏可显。限流 600 次/分钟。
