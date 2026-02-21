# Nova Demo

An agentic AI backend for Revit automation, powered by **FastAPI**, **LangGraph** (ReAct agent), and **OpenAI GPT-4o**.  
Designed to be called from a Revit plugin; every request must carry an **Auth0 JWT** that includes a Revit-provider claim.

---

## Architecture

```
Revit Plugin
  │  HTTP POST /api/v1/chat/stream
  │  Authorization: Bearer <Auth0 JWT>
  ▼
Nova FastAPI Backend
  ├── JWT Validation (Auth0 RS256 + provider claim check)
  ├── LangGraph ReAct Agent
  │     └── OpenAI GPT-4o (streaming)
  │           └── Tool calls ──► Revit Tools (11 tools)
  │                               ↕ JSON RPC
  │                              Revit Plugin (local bridge)
  └── SSE Stream → Revit Plugin UI
```

### Tool set (v0.1)

| Tool | Description |
|------|-------------|
| `get_elements_by_category` | List elements by Revit category |
| `get_element_by_id` | Fetch a single element by ID |
| `get_element_parameters` | Read all parameters of an element |
| `set_element_parameter` | Write a parameter value |
| `list_views` | List views (with optional type filter) |
| `get_active_view` | Return the currently active view |
| `list_levels` | Return all levels |
| `list_grids` | Return all grid lines |
| `get_model_info` | High-level document info |
| `list_warnings` | Model integrity warnings |
| `get_rooms_summary` | Room/space inventory |

---

## Quick Start

### 1. Prerequisites

- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/) installed (`pip install uv` or `brew install uv`)
- An Auth0 tenant with an API audience configured

### 2. Install dependencies

```bash
cd nova_demo
uv venv
uv pip install -e ".[dev]"
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your Auth0 domain, audience, and OpenAI API key
```

### 4. Run the server

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

---

## Auth0 Setup

1. Create an **API** in Auth0 with audience `https://nova-demo-api`.
2. In your Revit plugin's Auth0 application, add a custom claim to the access token (via Auth0 Actions or Rules):

```js
// Auth0 Action – add-revit-provider-claim
exports.onExecutePostLogin = async (event, api) => {
  api.accessToken.setCustomClaim("https://nova-demo/provider", "revit-plugin");
};
```

3. The backend validates:
   - Signature (RS256 via JWKS)
   - Audience & Issuer
   - `https://nova-demo/provider == "revit-plugin"`

---

## Consuming the SSE Stream (Revit Plugin)

```csharp
// Pseudo-code – C# Revit plugin
using var client = new HttpClient();
client.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", accessToken);

var request = new { message = "List all walls on Level 1", context = new { } };
using var response = await client.PostAsJsonAsync(
    "http://localhost:8000/api/v1/chat/stream", request);

await foreach (var sseEvent in response.ReadServerSentEventsAsync())
{
    var chunk = JsonSerializer.Deserialize<StreamChunk>(sseEvent.Data);
    switch (chunk.Type)
    {
        case "token":       AppendToUI(chunk.Content); break;
        case "tool_call":   ShowToolSpinner(chunk.Data["tool"]); break;
        case "tool_result": HideToolSpinner(); break;
        case "done":        FinaliseUI(chunk.Content); break;
        case "error":       ShowError(chunk.Content); break;
    }
}
```

---

## Extending with New Revit Tools

1. Add a new `@tool` function in `app/tools/your_module.py`.
2. Import and append it to `ALL_REVIT_TOOLS` in `app/tools/__init__.py`.
3. The agent picks it up automatically on next restart.

---

## Project Structure

```
nova_demo/
├── app/
│   ├── main.py                  # FastAPI app, CORS, lifespan
│   ├── config.py                # Pydantic Settings (env vars)
│   ├── auth/
│   │   ├── jwt_validator.py     # Auth0 RS256 + provider claim validation
│   │   └── dependencies.py     # get_current_user FastAPI dependency
│   ├── agents/
│   │   ├── revit_agent.py       # LangGraph ReAct agent + SSE streaming
│   │   └── prompts.py           # System prompt
│   ├── tools/
│   │   ├── __init__.py          # ALL_REVIT_TOOLS registry
│   │   ├── elements.py
│   │   ├── parameters.py
│   │   ├── views.py
│   │   ├── levels.py
│   │   └── model_info.py
│   ├── api/
│   │   └── routes.py            # /chat/stream, /tools, /health
│   └── models/
│       └── schemas.py           # Pydantic request/response models
├── pyproject.toml
├── .env.example
└── README.md
```

---

## Roadmap

- [ ] Real Revit plugin RPC bridge (WebSocket / named pipe)
- [ ] Multi-agent supervisor for complex multi-step Revit workflows
- [ ] Session memory / conversation history (Redis or in-memory)
- [ ] Element geometry & BIM data tools
- [ ] Transaction management (undo/redo support)
- [ ] Auth0 user-level RBAC (read-only vs. write permissions)
