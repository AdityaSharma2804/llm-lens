# llm-lens

Automatic observability for OpenAI and Anthropic API calls.  
Tracks latency, token usage, cost, and errors — with a live web dashboard.

<<<<<<< HEAD
[![PyPI version](https://img.shields.io/pypi/v/llm-lens-py)](https://pypi.org/project/llm-lens-py/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

llm-lens is an open-source Python SDK that automatically intercepts every OpenAI and Anthropic API call in your application — tracking latency, token usage, cost, model, and errors — with zero code changes. Just add one import.

> **Install:** `pip install llm-lens-py` | **Article:** [Medium](https://medium.com/@adityas2804/i-built-my-own-llm-observability-tool-heres-why-and-how-6ea060562b98)
=======
![llm-lens dashboard](https://raw.githubusercontent.com/AdityaSharma2804/llm-lens/main/docs/dashboard.png)
>>>>>>> f17402a (SEO optimized README)

---

## What it does

Add one import to your project. llm-lens silently intercepts every OpenAI and Anthropic API call and logs:

- Latency (ms)
- Input and output tokens
- Cost in USD
- Model used
- Errors and status

No SDK changes. No account setup. No config files.

---

## Installation

```bash
pip install llm-lens-py
```

---

## Usage

```python
import llm_lens        # patches OpenAI and Anthropic automatically
import openai

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "hello"}]
)
# this call was silently tracked
```

---

## CLI

```bash
# show a table of all tracked calls
llm-lens

# show aggregated stats: total calls, error rate, avg latency, total cost
llm-lens stats

# start the live dashboard at http://localhost:8000
llm-lens serve

# set a cost alert threshold
llm-lens config set cost_alert_usd 0.10
```

---

## Dashboard

Run `llm-lens serve` and open `http://localhost:8000`.

- Live stats: total calls, error rate, avg latency, total cost
- Latency per call chart
- Error per call chart
- Red alert banner when cost threshold is breached
- Auto-refreshes every 5 seconds

---

## Docker

```bash
docker build -t llm-lens .
docker run -p 8000:8000 llm-lens
```

---

## Supported models

| Provider  | Models                                          |
|-----------|-------------------------------------------------|
| OpenAI    | gpt-4o, gpt-4o-mini, gpt-4-turbo               |
| Anthropic | claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus |

---

## Data storage

All data is stored locally at `~/.llm_lens/calls.db` (SQLite). Nothing leaves your machine unless you deploy the server yourself.

---

## Stack

Python · FastAPI · SQLite · Vanilla JS · Chart.js · Docker · Render

---

## Status

<<<<<<< HEAD
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
- **Medium Article:** [How I built an LLM observability tool](https://medium.com/@adityas2804/i-built-my-own-llm-observability-tool-heres-why-and-how-6ea060562b98)
- **Dev.to Article:** [dev.to/adityasharma2804](https://dev.to/adityasharma2804/i-built-my-own-llm-observability-tool-heres-why-and-how-3619)

---

## Contributing

Feedback and PRs are welcome. Open an issue for bugs or feature requests.

---

## License

MIT © Aditya Sharma
=======
Active development. Feedback and PRs welcome.
>>>>>>> f17402a (SEO optimized README)
