# llm-lens

**Automatically track OpenAI and Anthropic API costs, latency, and token usage in Python — zero code changes required.**

[![PyPI version](https://img.shields.io/pypi/v/llm-lens-py)](https://pypi.org/project/llm-lens-py/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Dashboard](https://img.shields.io/badge/demo-live-brightgreen)](https://llm-lens.onrender.com)

llm-lens is an open-source Python SDK that automatically intercepts every OpenAI and Anthropic API call in your application — tracking latency, token usage, cost, model, and errors — with zero code changes. Just add one import.

> **Install:** `pip install llm-lens-py` | **Demo:** [llm-lens.onrender.com](https://llm-lens.onrender.com) | **Article:** [Medium](https://medium.com/@adityas2804/i-built-my-own-llm-observability-tool-heres-why-and-how-6ea060562b98)

---

## Why llm-lens?

When you build Python applications on top of OpenAI or Anthropic APIs, you have no built-in visibility into:

- **How much you're spending** — cost can spiral fast across gpt-4o, claude-3-5-sonnet, etc.
- **How fast your calls are** — latency affects UX but is invisible by default
- **How often they fail** — silent errors are hard to catch without instrumentation

Commercial LLM observability tools like LangSmith and Helicone solve this, but require account setup, SDK changes, and monthly fees. **llm-lens gives you the same visibility with a single import and no configuration.**

---

## Quickstart

```bash
pip install llm-lens-py
```

```python
import llm_lens        # patches OpenAI and Anthropic automatically
import openai

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "hello"}]
)
# this call was silently tracked — latency, tokens, cost, model, status
```

That's it. No decorators. No wrappers. No config files. No account signup.

---

## How It Works

llm-lens uses **Python monkey-patching** to intercept LLM API calls at runtime without modifying your code. On `import llm_lens`, it replaces the `create()` method on both OpenAI and Anthropic SDK clients with a wrapper that:

1. Starts a timer with `time.perf_counter()`
2. Calls the original OpenAI / Anthropic SDK
3. Extracts `input_tokens`, `output_tokens`, `model` from the response
4. Calculates cost in USD from a built-in pricing table
5. Writes a record to `~/.llm_lens/calls.db` (SQLite)
6. Returns the **original response untouched**

Your existing code gets the exact same response. The only difference is that every call is now tracked locally.

---

## Features

### Zero-configuration instrumentation
No SDK changes. No account. No config. Just `import llm_lens` at the top of your file.

### CLI — instant terminal visibility
```bash
llm-lens                              # rich table of all tracked calls
llm-lens stats                        # total calls, error rate, avg latency, total cost
llm-lens serve                        # live dashboard at localhost:8000
llm-lens config set cost_alert_usd 0.10  # set a cost alert threshold
```

### Live web dashboard
Run `llm-lens serve` and open `http://localhost:8000`:
- Stats bar: total calls, error rate, avg latency, total cost
- Latency per call line chart (Chart.js)
- Error per call bar chart with red/green color coding
- Red alert banner when cost threshold is breached
- Auto-refreshes every 5 seconds

![llm-lens dashboard](docs/dashboard.png)

### Cost tracking
- Pricing table for `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `claude-3-5-sonnet`, `claude-3-5-haiku`, `claude-3-opus`
- Fuzzy model matching handles version suffixes (e.g. `gpt-4o-2024-08-06`)
- Cost stored per call in USD with 8 decimal precision
- Configurable cost alert threshold in `~/.llm_lens/config.json`

### Error tracking
- All exceptions caught and logged with full error message
- Per-call `status`: `ok` or `error`
- Error rate calculated in SQL aggregation

### Privacy-first
All data stored locally at `~/.llm_lens/calls.db`. Nothing leaves your machine unless you deploy the server yourself.

---

## Supported Models

| Provider  | Models |
|-----------|--------|
| OpenAI    | gpt-4o, gpt-4o-mini, gpt-4-turbo |
| Anthropic | claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus |

---

## Data Stored Per Call

| Column | Description |
|--------|-------------|
| `latency_ms` | End-to-end response time in milliseconds |
| `input_tokens` | Prompt tokens from the usage object |
| `output_tokens` | Completion tokens from the usage object |
| `cost_usd` | Calculated cost in USD (8 decimal places) |
| `model` | Model string returned by the API |
| `status` | `ok` or `error` |
| `error` | Exception message if the call failed |
| `timestamp` | UTC datetime of the call |

SQLite database location: `~/.llm_lens/calls.db`

---

## REST API

Start the server with `llm-lens serve` to access:

| Endpoint | Description |
|----------|-------------|
| `GET /` | Live dashboard |
| `GET /calls` | All call records as JSON |
| `GET /stats` | Aggregated stats: total, errors, avg latency, total cost |
| `GET /alert` | Alert object if cost threshold breached |
| `GET /health` | `{status: ok}` for uptime monitoring |

---

## Docker

```bash
docker build -t llm-lens .
docker run -p 8000:8000 llm-lens
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Instrumentation | Python monkey-patching |
| Storage | SQLite (stdlib `sqlite3`) |
| Backend | FastAPI + uvicorn |
| Frontend | Vanilla JS + Chart.js |
| Packaging | hatchling + pyproject.toml |
| Container | Docker (python:3.12-slim) |
| Deployment | Render (free tier) |

---

## Comparison

| Tool | Zero code changes | Local storage | Free | Open source |
|------|:-----------------:|:-------------:|:----:|:-----------:|
| **llm-lens** | ✅ | ✅ | ✅ | ✅ |
| LangSmith | ❌ | ❌ | ❌ | ❌ |
| Helicone | ❌ | ❌ | ❌ | ❌ |
| Langfuse | ❌ | ❌ | ✅ | ✅ |

---

## Installation & Requirements

```bash
pip install llm-lens-py
```

- Python >= 3.10
- Works with `openai` and `anthropic` Python SDKs
- No external database required

---

## Roadmap

- [ ] Async / asyncio support
- [ ] Streaming response tracking
- [ ] Per-model cost breakdown in dashboard
- [ ] Export to CSV
- [ ] Slack / email alerts
- [ ] ClickHouse migration for high-volume use
- [ ] GitHub Actions CI (ruff lint + tests)

---

## Links

- **PyPI:** [pypi.org/project/llm-lens-py](https://pypi.org/project/llm-lens-py/)
- **Live Dashboard:** [llm-lens.onrender.com](https://llm-lens.onrender.com)
- **Medium Article:** [How I built an LLM observability tool](https://medium.com/@adityas2804/i-built-my-own-llm-observability-tool-heres-why-and-how-6ea060562b98)
- **Dev.to Article:** [dev.to/adityasharma2804](https://dev.to/adityasharma2804/i-built-my-own-llm-observability-tool-heres-why-and-how-3619)

---

## Contributing

Feedback and PRs are welcome. Open an issue for bugs or feature requests.

---

## License

MIT © Aditya Sharma
