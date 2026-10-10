# 版本记录 (CHANGELOG)

> 本 Skill 的迭代依据。版本号遵循语义化版本（主.次.修订）。

## V0.1.6 (2026-10-10) — 热梗运行时化 + 全文件精简

- **热梗运行时化（用户要求）**：签诗/宜忌不再写死任何梗。`fortune_logic.md` §4 删除硬编码签诗，改为「出签前用 `WebSearch '<年><月> 网络热梗 流行语'` 取 2-3 个当季梗，按签等基调揉进签诗；搜索失败退回通用俏皮话兜底，绝不编造梗」。SKILL 核心流程新增第 2 步「查当季热梗」（仅 agent 内部，不写文件），保证梗永远新鲜。
- **全文件精简（用户要求）**：SKILL.md 由约 5700 字符压到约 3800 字符，删除与 tool_catalog 重复的「响应解析」长段；tool_catalog.md 删去重复响应格式小节、压到约 50 行；fortune_logic.md 去硬编码、只留结构与生成规则。功能不减，仅去冗余。
- 升级版本至 0.1.6。

## V0.1.5 (2026-10-10) — 多地址询问 + 领券双套餐 + 玩梗 + 去敏

- **多地址必须询问（用户要求）**：`delivery-query-addresses` 返回多个地址时，列出脱敏标签（①家·城市·区 ②公司·城市·区）询问用户选哪个，绝不直接默认第一个；用户说「换另一个」重新询问。仅 1 个地址时直接使用。
- **领券后给「到店 + 外送」双套餐（用户要求）**：核心流程新增第 4 步 `auto-bind-coupons` 自动领券（免费、不改金额、透明展示，用户说「别领券」可跳过）；第 5 步为同一命定餐品分别算「到店自取价」与「麦乐送到手价」，均尝试带上所领券（items[].couponId），让用户自己选取餐方式。
- **签文更玩梗（用户要求）**：fortune_logic 第 4、5 节签诗与宜忌重写，更生活化、有记忆点；程序员梗保留为可选彩蛋。
- **价格换算说明不进用户卡（用户要求）**：`calculate-price` 单位为「分」需 ÷100 的说明仅保留在 SKILL「响应解析」与 fortune_logic 的 agent 内部注释，**不写入给用户看的签文卡**；sample_output 展示已换算的「元」价，不出现分/元换算提示。
- **去除个人真实查询数据（用户要求）**：sample_output / CHANGELOG / tool_catalog 中所有来自某次真实 Token 查询的具体数据（城市、门店名、餐品名、价格、券名、脱敏手机等）全部改为占位符或泛化描述，确保 Skill 可安全上传 GitHub 供所有人使用。
- 升级版本至 0.1.5。

## V0.1.4 (2026-10-10) — 实测全链路 + 响应格式与工具边界校准

- 真实跑通「麦门永存」只读全链路：Token 有效、数据真实。
- **响应解析三类格式**（写进 SKILL「响应解析」小节）：JSON 类用 `raw_decode` 取首段完整 JSON 忽略尾部；纯文本类（如 available-coupons 的 markdown 券列表）直接呈现；`delivery-query-stores` 的 `data` 直接是门店数组，取 `data[0]` 的 storeCode+beCode。
- **工具边界校准**：`query-promotions` 仅企业团餐（beType=6）专用，默认路径不调用；「麦门提醒」以 `available-coupons`（无参、markdown）+ `campaign-calendar` 为主。
- **价格单位**：`calculate-price` 返回单位为「分」需 ÷100 转「元」；`query-meals` 的 currentPrice 已是「元」字符串，勿二次换算。
- **隐私**：`delivery-query-addresses` 的 `phone` 官方已脱敏（格式如 `1xx****xxxx`），可展示；`fullAddress` 完整门牌按红线脱敏（仅显示到城市-区）。
- 升级版本至 0.1.4。

## V0.1.3 (2026-10-10) — 全自动定庙址（麦乐送外送优先）

- 按用户要求把「麦门永存」做成全自动体验：用户装好 skill + 填 token 后，说一句即出结果，中间不打断。
- 核心流程「定庙址」重写为自动路径：默认走麦乐送外送，`delivery-query-addresses`（无入参）取已存地址 → 取 `addressId` → `delivery-query-stores(addressId, beType=2)` 补门店；仅当用户无配送地址时才轻问到店 / 外送。
- 补充**外送 beCode 约束**：`delivery-query-stores` 返回 `storeCode`+`beCode`，后续 `query-meals`/`calculate-price`/`create-order` 外送场景必传 `beCode`；到店 `beType=1` 无需。
- 新增**隐私红线**：`delivery-query-addresses` 的 `fullAddress`/`phone` 不得泄露，展示仅用标签/城市-区。
- 工具清单 `tool_catalog.md` 将 `delivery-query-addresses`/`delivery-query-stores` 升为求签主链路（✅），`delivery-create-address` 注明仅兜底。
- 升级版本至 0.1.3。

## V0.1.2 (2026-10-10) — 修正门店地址参数

- 修正 `query-nearby-stores` 调用示例与说明：地址 = 用户所在 `city` + 附近 `keyword`（位置关键词），`searchType=2` 时必填；移除写死的测试城市，改为占位符，并明确「绝不使用示例城市/位置」。
- 核心流程「定庙址」补充：触发「麦门永存」未提供位置时必须主动询问用户真实城市+位置；另注 `searchType=1` 可查用户收藏餐厅。
- 升级版本至 0.1.2。

## V0.1.1 (2026-10-10) — 文档与参数对齐官方 MCP

- 修正 `query-nearby-stores` 调用示例（补齐必填 beType，searchType=2 时 city+keyword）。
- 核心流程「定庙址」补充：触发「麦门永存」时若未提供城市/位置需主动询问，默认 beType=1 到店自取（无需 beCode）。
- 明确价格单位：`calculate-price` 返回为「分」需 ÷100 转「元」；`query-meals.currentPrice` 已是「元」字符串，勿二次换算。
- 工具数更新为实测 35 个；`mcp_client.py` 同步修正示例与 clientInfo 版本号。
- 升级版本至 0.1.1。

## V0.1.0 (2026-10-10) — 初始版本

- **核心玩法**：麦门赛博求签。用户说「麦门永存」触发，结合麦当劳官方 MCP 实时数据出签文 + 命定餐品 + 今日宜忌，可一键安全下单。
- **连接方式**：直连官方 MCP（`https://mcp.mcd.cn`，Streamable HTTP / JSON-RPC），`Authorization: Bearer <Token>` 鉴权；Token 存技能目录 `config.json`（模板 `config.example.json`，已被 `.gitignore` 忽略）。
- **随附脚本**：`scripts/mcp_client.py`，仅标准库，自动完成 JSON-RPC 握手与 SSE 解析；支持 `list` / `schema <tool>` / `init` / `<tool> <args>`。
- **求签逻辑**：时段主权重 + 轻微随机抖动，心愿仅作可选微调（见 `references/fortune_logic.md`）。
- **安全红线**：下单 / 领券 / 抽奖前强制预览明细 + 用户确认，绝不静默扣费；价格 / 库存 / 限购以下单接口返回为准。
- **文案风格**：庙签庄重 × 生活化俏皮话，面向所有麦当劳用户；程序员梗仅作可选彩蛋。
- **已知限制**：工具集随官方 MCP 版本可能变化，调用前以 `python scripts/mcp_client.py list` 实测为准；限流每 Token 600 次/分钟。
