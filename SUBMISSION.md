# Bài nộp Ngày 26 - Hạ tầng MCP/A2A

## Thông tin sinh viên

- **Mã học viên:** 2A202600610
- **Họ và tên:** Vũ Quang Bảo
- **Bài lab:** Day 26 - Track 02 - Cohort 2 - MCP/A2A Infrastructure
- **Kho mã nguồn:** `BaoVu2k4/Day26-Track02-Cohort2-MCP-A2A-Infrastructure`

## Tóm tắt bài làm

Bài nộp hoàn thiện lab hạ tầng MCP/A2A với các thành phần chính:

- Kiến trúc 4 agent: `orchestrator`, `search_agent`, `database_agent`, `synthesis_agent`.
- MCP server chạy qua `stdio`, có governance guard cho từng tool.
- Ba A2A specialist chạy trên các cổng `8001`, `8002`, `8003`.
- ADK Web orchestrator chạy trên cổng `8000`.
- Định tuyến ngữ nghĩa và chuỗi fallback.
- Quản trị dữ liệu: ma trận capability, audit log, SQL read-only guard, chặn từ khóa nhạy cảm, trace metadata.
- Capstone W1-W5 đã được ghi kết quả `ĐẠT` trong notebook.

## Bảng đối chiếu rubric

| Yêu cầu | Trạng thái | Minh chứng |
|---|---:|---|
| MCP server cung cấp công cụ nghiên cứu | ĐẠT | `mcp_server/research_tools_server.py` |
| Thêm MCP tool thứ tư `count_words` | ĐẠT | `mcp_server/research_tools_server.py`, `lab_utils/governance/policy.json` |
| Search agent chuyên trách qua A2A | ĐẠT | `agents/search_agent/agent.py`, `http://localhost:8001/.well-known/agent-card.json` |
| Database agent chuyên trách qua A2A | ĐẠT | `agents/database_agent/agent.py`, `http://localhost:8002/.well-known/agent-card.json` |
| Synthesis agent chuyên trách qua A2A | ĐẠT | `agents/synthesis_agent/agent.py`, `http://localhost:8003/.well-known/agent-card.json` |
| Orchestrator gọi được cả ba agent chuyên trách | ĐẠT | `agents/orchestrator/agent.py` |
| Demo agent registry | ĐẠT | `lab_utils/agent_registry.py`, notebook Module 3 |
| Bộ định tuyến ngữ nghĩa và chuỗi fallback | ĐẠT | `lab_utils/semantic_router.py`, `lab_utils/routing_tool.py` |
| Chính sách governance và audit log | ĐẠT | `lab_utils/governance/`, audit log sinh cục bộ tại `logs/governance_audit.jsonl` |
| SQL read-only guard chặn DDL/DML | ĐẠT | Kết quả W5, `GovernanceGuard._validate_sql()` |
| Demo HITL/trace policy | ĐẠT | Notebook Module 5 |
| ADK Web W1 transfer sang `search_agent` | ĐẠT | `artifacts/screenshots/adk_web_w1_chat.png` |
| ADK Web W2 gọi MCP multi-tool flow | ĐẠT | `artifacts/screenshots/adk_web_w2_chat.png` |
| W3 ủy quyền `synthesis_agent` | ĐẠT | Cell `adk_web_results` trong notebook |
| W4 `suggest_routing` gợi ý `database_agent` | ĐẠT | Cell `adk_web_results` trong notebook |
| W5 governance deny với `DROP TABLE agent_metrics` | ĐẠT | Cell `adk_web_results` trong notebook |

## Ảnh minh chứng

| Kịch bản | Ảnh minh chứng |
|---|---|
| W1 chat: A2A transfer sang `search_agent` | `artifacts/screenshots/adk_web_w1_chat.png` |
| W1 trace | `artifacts/screenshots/adk_web_w1_trace.png` |
| W2 chat: MCP `search_documents`, `sql_query`, `summarize_text` | `artifacts/screenshots/adk_web_w2_chat.png` |
| W2 trace | `artifacts/screenshots/adk_web_w2_trace.png` |

## Lệnh kiểm tra đã chạy

Các lệnh đã chạy cục bộ trước khi nộp:

```powershell
$env:PYTHONPATH=(Get-Location).Path
& 'C:\Users\vuxba\Miniconda3\envs\pii-env\python.exe' -m compileall agents lab_utils mcp_server
git diff --check
Invoke-RestMethod -Uri http://localhost:8001/.well-known/agent-card.json
Invoke-RestMethod -Uri http://localhost:8002/.well-known/agent-card.json
Invoke-RestMethod -Uri http://localhost:8003/.well-known/agent-card.json
(Invoke-WebRequest -Uri http://127.0.0.1:8000 -UseBasicParsing).StatusCode
```

## Ghi chú bảo mật

- Không commit API key thật.
- Các file `.env`, `.env.local`, `.google_api_keys.local`, `logs/`, `node_modules/` đều được ignore.
- Có thể cấu hình `GOOGLE_MODEL` để chuyển model khi một model free-tier bị hết quota.
- Lần chụp minh chứng cuối dùng `GOOGLE_MODEL=gemini-flash-lite-latest` trong process cục bộ vì `gemini-2.5-flash` bị hết quota free-tier trong lúc kiểm thử.
