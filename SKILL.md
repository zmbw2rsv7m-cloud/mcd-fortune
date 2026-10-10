---
name: mcd-fortune
description: 麦门赛博求签——面向所有麦当劳用户的趣味点餐。说「麦门永存」即结合麦当劳官方 MCP 实时数据出签文+命定餐品(到店/外送双价)+今日宜忌+当季热梗，可一键安全下单。
version: 0.1.6
---

# 麦门赛博求签

用麦当劳官方 MCP（`https://mcp.mcd.cn`）真实数据，给每位顾客摇一支「今日麦运签」：签文 + 命定餐品（到店/外送双价）+ 今日宜忌 + 当季热梗。可一键安全下单。

## 触发词
主触发「麦门永存」；兼容「麦门求签」「摇个签」「今天吃啥求签」「麦门黄历」。

## 前置（必须）
- 技能目录 `config.json` 的 `mcp_token` 已填真实 Token（从 `config.example.json` 复制）。未配置则指引复制填写并停止，**不编造数据**。
- 任何写操作（下单/抽奖/建地址）前**必须**展示完整明细并等用户明确确认。
- 价格/库存/限购**以下单接口返回为准**，不从展示文本提取数值校验。

## 调用官方 MCP（直连，不依赖连接器）
随附 `scripts/mcp_client.py`（仅标准库）：
```bash
python <技能目录>/scripts/mcp_client.py list                 # 验连通+Token
python <技能目录>/scripts/mcp_client.py schema <tool>        # 读必填参数
python <技能目录>/scripts/mcp_client.py now-time-info '{}'
python <技能目录>/scripts/mcp_client.py delivery-query-addresses '{}'
python <技能目录>/scripts/mcp_client.py delivery-query-stores '{"addressId":"<id>","beType":2}'
```
脚本自动完成 JSON-RPC 握手 + Bearer 鉴权 + SSE 解析，读 `config.json`。`401/403`→Token 失效；`429`→限流 600 次/分钟。

**响应解析（agent 内部，不进用户卡）**：`content[0].text` 分三类——
1. JSON 类（`{"success"...}`/`## Original Response`）：`json.JSONDecoder().raw_decode` 解首段完整 JSON，忽略尾部。适用 now-time-info/query-meals/calculate-price/delivery-query-addresses/delivery-query-stores。⚠️ delivery-query-stores 的 `data` 直接是门店数组，取 `data[0].storeCode+beCode`。
2. 纯文本类：直接呈现，勿 JSON 解析。如 available-coupons 的 markdown 券列表。
3. 价格：`calculate-price` 单位「分」→÷100 转「元」；`query-meals.currentPrice` 已是「元」字符串，勿二次换算。

## 核心流程
目标：用户说「麦门永存」即全自动出签，尽量不打断；默认只读，除非用户主动要下单。

1. **定时辰** — `now-time-info` 取日期时间，定时段（早/午/下午茶/晚/夜宵）。
2. **查当季热梗（agent 内部，不写文件）** — `WebSearch "<当前年><当前月> 网络热梗 流行语"`，挑 2-3 个贴合点餐的梗（干饭/打工/摸鱼/省钱/躺平类），待注入签文。搜索失败则退回通用俏皮话，**绝不编造梗**。
3. **定庙址（多地址必问）** — 默认麦乐送外送：
   - `delivery-query-addresses`（无参）取已存地址。
   - 0 个：问「到店 or 外送？」外送→`delivery-create-address` 引导创建→`delivery-query-stores(beType=2)`；到店→问城市+位置→`query-nearby-stores(searchType=2,beType=1)`。
   - 1 个：直接用。
   - **多个：列脱敏标签（①家·城市·区 ②公司·城市·区，绝不含门牌与手机）问用户选哪个**；「换一个」重新问。
   - 取 `addressId`→`delivery-query-stores(addressId,beType=2)` 存 `storeCode`+`beCode`（外送必传）。
   - ⚠️ 隐私：仅显城市-区，不泄露 `fullAddress`/`phone`。
4. **摇签** — 时段主权重+轻微随机抖动作签等（上上/上/中/下/下下，见 fortune_logic）。用户附心愿仅轻度偏移。
5. **领券（自动免费）** — `auto-bind-coupons`（无参）领麦麦省券，记 `successCount`+券名；卡里注明「已领 N 张」。用户说「别领券」跳过；`successCount=0` 正常继续。
6. **取真数据+算双套餐** — 按签等从 `query-meals` 真菜单挑 1 个 `productCode`；为到店/外送各算一次价：
   - 外送：`query-meals(storeCode,orderType=2,beType=2,beCode)`→`calculate-price(storeCode,orderType=2,beType=2,beCode,items=[{productCode,quantity:1,couponId?}])`。
   - 到店：从地址解析 city/区→`query-nearby-stores(searchType=2,city,keyword,beType=1)` 取最近店 `storeCode`（无 beCode）→`query-meals(storeCode,orderType=1,beType=1)`→`calculate-price(...)`。
   - 两套餐都尝试带第 5 步券（`items[].couponId`）；券不适用则原价。营养取 `list-nutrition-foods`。
7. **麦门提醒** — `campaign-calendar`（活动）+`available-coupons`/`query-store-coupons`（可领/门店券，markdown 直接呈现）。⚠️ `query-promotions` 仅团餐(beType=6)专用，默认不调。
8. **出签** — 渲染签文卡（见 sample_output）：签等+签诗（含第 2 步热梗）+宜忌+命定餐品（到店/外送价+营养+所领券）+麦门提醒。
9. **安全下单（仅用户明确要求）** — 展示完整明细→等「确认」→`create-order`（外送必传 storeCode+beCode+beType=2）→回支付链接。未确认绝不下单。

## 安全红线
- ❌ 绝不静默调 `create-order`/`mall-create-order`/`draw-lottery`/`delivery-create-address`（建地址仅用户明确要外送且无地址时引导）。
- ✅ `auto-bind-coupons` 免费不改金额，已透明展示；「别领券」即跳。
- ❌ 不编菜单/价格/营养；MCP 不可用如实告知。❌ 不泄露 `fullAddress`/`phone`。
- ✅ 所有写操作前：预览→确认→执行→回传。⚠️ 限流 600 次/分钟。

## 文案风格
庙签庄重 × 生活化俏皮，全民向。**签诗玩梗且梗必须当季新鲜**——用第 2 步搜到的热梗，不写死任何梗到本文件。详见 `references/fortune_logic.md`；工具/字段见 `references/tool_catalog.md`；输出样例见 `references/sample_output.md`。
