# Memory: Go High Level (GHL) MCP

## Connection Details
- **MCP Server Name:** `prod-ghl-mcp`
- **Config File Location:** `C:\Users\baysh\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json`
- **API Endpoint:** `https://services.leadconnectorhq.com/mcp/`
- **Location ID:** `g7bSwjUBNtBynj8BfqfP`
- **Bearer Token:** `pit-f82601e8-d7b7-4eb1-b8b0-0270a41c50a3`

## Working Config (mcpServers section)
```json
"mcpServers": {
  "prod-ghl-mcp": {
    "command": "C:\\PROGRA~1\\nodejs\\nodejs\\npx.cmd",
    "args": ["mcp-remote","https://services.leadconnectorhq.com/mcp/","--header","Authorization: Bearer pit-f82601e8-d7b7-4eb1-b8b0-0270a41c50a3","--header","locationId: g7bSwjUBNtBynj8BfqfP"]
  }
}
```

## Root Cause of Connection Issue
Node.js is at `C:\Program Files\nodejs\nodejs\` (space in path). Claude desktop resolves `"command": "npx"` to the full path and wraps it in `cmd.exe /C C:\Program Files\nodejs\nodejs\npx.cmd ...` — the unquoted space causes the error: `'C:\Program' is not recognized as an internal or external command`

## The Fix
Use Windows 8.3 short path: `"command": "C:\\PROGRA~1\\nodejs\\nodejs\\npx.cmd"`
`PROGRA~1` = short name for `Program Files` — no spaces, always works.

## Mistakes to Avoid
1. Do NOT use `Set-Content -Encoding UTF8` in PowerShell 5.x — adds BOM, breaks JSON. Use `[System.IO.File]::WriteAllText($path, $json)`.
2. Do NOT use `ConvertTo-Json | Set-Content` to update one property — if parse fails, whole config gets wiped.
3. Config is NOT at `%APPDATA%\Claude\claude_desktop_config.json` — real path is `C:\Users\baysh\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json`.
4. `~/.claude/settings.json` does NOT contain MCP servers — only has `autoUpdatesChannel` and `effortLevel`.
5. Always fully quit Claude from the system tray before testing config changes.

## Verify Fix
```powershell
Get-Content "C:\Users\baysh\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\logs\mcp-server-prod-ghl-mcp.log" -Tail 20
```
Success = `Server started and connected successfully` with no `'C:\Program' is not recognized` error after it.

## GHL Account Info
- **2 Pipelines:** Demo Pipeline (3 stages), Marketing Pipeline (6 stages)
- **Total Contacts:** 326
- **Duplicates found (May 2026):** coronda willis x2, jessica teague x2, nina caculitan/hartman (same phone)