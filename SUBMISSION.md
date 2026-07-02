# Day 26 Submission - MCP/A2A Infrastructure

## Summary

This submission completes the Day 26 Track 02 Cohort 2 MCP/A2A infrastructure lab:

- 4-agent architecture: `orchestrator`, `search_agent`, `database_agent`, `synthesis_agent`
- MCP server over stdio with governed tools
- A2A specialists exposed on ports `8001`, `8002`, `8003`
- ADK Web orchestrator on port `8000`
- Semantic routing and fallback chain
- Governance policy, audit logging, SQL guard, keyword block, and trace metadata
- ADK Web capstone prompts W1-W5 recorded as passed in the notebook

## Rubric Checklist

| Requirement | Status | Evidence |
|---|---:|---|
| MCP server exposes research tools | DAT | `mcp_server/research_tools_server.py` |
| Added fourth MCP tool `count_words` | DAT | `mcp_server/research_tools_server.py`, `lab_utils/governance/policy.json` |
| A2A search specialist | DAT | `agents/search_agent/agent.py`, `http://localhost:8001/.well-known/agent-card.json` |
| A2A database specialist | DAT | `agents/database_agent/agent.py`, `http://localhost:8002/.well-known/agent-card.json` |
| A2A synthesis specialist | DAT | `agents/synthesis_agent/agent.py`, `http://localhost:8003/.well-known/agent-card.json` |
| Orchestrator consumes all specialists | DAT | `agents/orchestrator/agent.py` |
| Agent registry demo | DAT | `lab_utils/agent_registry.py`, notebook Module 3 |
| Semantic router + fallback chain | DAT | `lab_utils/semantic_router.py`, `lab_utils/routing_tool.py` |
| Governance policy and audit log | DAT | `lab_utils/governance/`, `logs/governance_audit.jsonl` generated locally |
| SQL read-only guard blocks DDL/DML | DAT | W5 result, `GovernanceGuard._validate_sql()` |
| HITL/trace policy demo | DAT | Notebook Module 5 |
| ADK Web W1 transfer to search_agent | DAT | `artifacts/screenshots/adk_web_w1_chat.png` |
| ADK Web W2 MCP multi-tool flow | DAT | `artifacts/screenshots/adk_web_w2_chat.png` |
| W3 synthesis_agent delegation | DAT | Notebook `adk_web_results` cell |
| W4 `suggest_routing` recommends database_agent | DAT | Notebook `adk_web_results` cell |
| W5 governance deny for `DROP TABLE agent_metrics` | DAT | Notebook `adk_web_results` cell |

## Screenshot Evidence

| Scenario | Screenshot |
|---|---|
| W1 chat: A2A transfer to `search_agent` | `artifacts/screenshots/adk_web_w1_chat.png` |
| W1 trace | `artifacts/screenshots/adk_web_w1_trace.png` |
| W2 chat: MCP `search_documents`, `sql_query`, `summarize_text` | `artifacts/screenshots/adk_web_w2_chat.png` |
| W2 trace | `artifacts/screenshots/adk_web_w2_trace.png` |

## Validation Commands

Commands run locally before submission:

```powershell
$env:PYTHONPATH=(Get-Location).Path
& 'C:\Users\vuxba\Miniconda3\envs\pii-env\python.exe' -m compileall agents lab_utils mcp_server
git diff --check
Invoke-RestMethod -Uri http://localhost:8001/.well-known/agent-card.json
Invoke-RestMethod -Uri http://localhost:8002/.well-known/agent-card.json
Invoke-RestMethod -Uri http://localhost:8003/.well-known/agent-card.json
(Invoke-WebRequest -Uri http://127.0.0.1:8000 -UseBasicParsing).StatusCode
```

## Notes

- Real API keys are not committed. `.env`, `.env.local`, and `.google_api_keys.local` are ignored.
- `GOOGLE_MODEL` is configurable so the lab can switch models when a free-tier model quota is exhausted.
- The final ADK Web screenshot run used `GOOGLE_MODEL=gemini-flash-lite-latest` in the local process because `gemini-2.5-flash` hit free-tier quota during validation.
