#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦门赛博求签 - 麦当劳官方 MCP 直连客户端 (Streamable HTTP / JSON-RPC)

读取技能目录下的 config.json 获取 Token，通过官方端点调用麦当劳 MCP。
仅依赖 Python 标准库（urllib），无需 pip install。

用法：
  python mcp_client.py list                       # 列出全部工具名（连通性 + 鉴权测试）
  python mcp_client.py schema <tool_name>         # 查看某工具的 inputSchema（调用前必读）
  python mcp_client.py init                       # 仅 initialize（测试连通性）
  python mcp_client.py <tool_name> '<json_args>'  # 调用某工具，例如：
  python mcp_client.py now-time-info '{}'
  python mcp_client.py query-nearby-stores '{"searchType":2,"city":"<用户城市>","keyword":"<附近位置/地标>","beType":1}'   # city+keyword 取自用户真实地址，勿套用示例
"""

import json
import os
import sys
import urllib.request
import urllib.error

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.stderr.write(
            "未找到 config.json。请复制 config.example.json 为 config.json 并填入 mcp_token。\n"
            "获取方式见 README.md「获取 Token」章节。\n"
        )
        sys.exit(2)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    token = cfg.get("mcp_token") or os.environ.get("MCD_MCP_TOKEN")
    if not token or str(token).startswith("在此"):
        sys.stderr.write("config.json 的 mcp_token 未填写真实 Token，请先填入。\n")
        sys.exit(2)
    endpoint = cfg.get("mcp_endpoint") or "https://mcp.mcd.cn"
    return endpoint, token


def rpc(endpoint, token, method, params=None, session_id=None, msg_id=1):
    is_notify = method.startswith("notifications/")
    body = {"jsonrpc": "2.0", "method": method}
    if not is_notify:
        body["id"] = msg_id
    if params is not None:
        body["params"] = params
    data = json.dumps(body).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": "Bearer " + token,
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        sys.stderr.write("HTTP %s: %s\n" % (e.code, e.read().decode("utf-8", "replace")))
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write("请求失败: %s\n" % e)
        sys.exit(1)
    sid = resp.headers.get("Mcp-Session-Id") or resp.headers.get("mcp-session-id")
    ctype = resp.headers.get("Content-Type", "")
    raw = resp.read().decode("utf-8", "replace")
    if is_notify:
        return sid, None
    result = None
    if "text/event-stream" in ctype:
        for line in raw.splitlines():
            if line.startswith("data:"):
                payload = line[5:].strip()
                if payload:
                    try:
                        obj = json.loads(payload)
                        if obj.get("id") == msg_id and "result" in obj:
                            result = obj["result"]
                    except Exception:  # noqa: BLE001
                        pass
    else:
        try:
            obj = json.loads(raw)
            result = obj.get("result")
        except Exception:  # noqa: BLE001
            pass
    return sid, result


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("用法: python mcp_client.py <tool_name|list|init> [json_args]\n")
        sys.exit(2)
    endpoint, token = load_config()
    cmd = sys.argv[1]

    # 1) initialize（建立会话）
    sid, init_res = rpc(
        endpoint,
        token,
        "initialize",
        {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcd-fortune", "version": "0.1.6"},
        },
    )
    if cmd == "init":
        print(json.dumps(init_res, ensure_ascii=False, indent=2))
        return

    # 2) 发送 initialized 通知
    rpc(endpoint, token, "notifications/initialized", None, sid, msg_id=0)

    if cmd == "list":
        _s, tools = rpc(endpoint, token, "tools/list", {}, sid, msg_id=2)
        names = [t["name"] for t in (tools or {}).get("tools", [])]
        print(json.dumps(names, ensure_ascii=False, indent=2))
        return

    if cmd == "schema":
        tool = sys.argv[2] if len(sys.argv) > 2 else ""
        _s, tools = rpc(endpoint, token, "tools/list", {}, sid, msg_id=2)
        for t in (tools or {}).get("tools", []):
            if t["name"] == tool:
                print(json.dumps(t, ensure_ascii=False, indent=2))
                return
        sys.stderr.write("未找到工具: " + tool + "\n")
        sys.exit(1)

    # 3) tools/call
    tool_name = cmd
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    _s, call_res = rpc(
        endpoint, token, "tools/call", {"name": tool_name, "arguments": args}, sid, msg_id=3
    )
    if call_res and "content" in call_res:
        for item in call_res["content"]:
            if item.get("type") == "text":
                sys.stdout.write(item["text"])
            else:
                print(json.dumps(item, ensure_ascii=False))
    else:
        print(json.dumps(call_res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
