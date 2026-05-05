import sys
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from llm_lens.core import track, get_records, get_stats

console = Console()

@track
def fake_openai_call(prompt: str) -> str:
    time.sleep(0.12)
    return f"response to: {prompt}"

@track
def failing_call():
    time.sleep(0.05)
    raise ConnectionError("API unreachable")

def show_table():
    fake_openai_call("what is 2+2?")
    fake_openai_call("explain recursion")
    try:
        failing_call()
    except ConnectionError:
        pass

    records = get_records()

    table = Table(title="Tracked Calls")
    table.add_column("Function", style="cyan")
    table.add_column("Model", style="blue")
    table.add_column("Status", style="bold")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Input tok", justify="right")
    table.add_column("Output tok", justify="right")
    table.add_column("Cost (USD)", justify="right", style="yellow")
    table.add_column("Error")
    table.add_column("Timestamp", style="dim")

    for r in records:
        color = "green" if r["status"] == "ok" else "red"
        cost = f"{r['cost_usd']:.6f}" if r["cost_usd"] else "-"
        error = (r["error"] or "-")[:25]
        table.add_row(
            r["func"],
            r["model"] or "-",
            f"[{color}]{r['status']}[/{color}]",
            str(r["latency_ms"]),
            str(r["input_tokens"] or "-"),
            str(r["output_tokens"] or "-"),
            cost,
            error,
            r["timestamp"]
        )

    console.print(table)
    console.print(f"\n[bold]Total calls:[/bold] {len(records)}")

def show_stats():
    s = get_stats()
    total = s["total"] or 0
    errors = s["errors"] or 0
    avg_latency = s["avg_latency"] or 0.0
    total_cost = s["total_cost"] or 0.0

    error_rate = round((errors / total * 100), 1) if total > 0 else 0.0

    console.print(Panel.fit(
        f"[bold]Total calls:[/bold]  {total}\n"
        f"[bold]Errors:[/bold]       {errors} ({error_rate}%)\n"
        f"[bold]Avg latency:[/bold]  {avg_latency} ms\n"
        f"[bold]Total cost:[/bold]   ${total_cost:.6f}",
        title="[bold green]llm-lens stats[/bold green]"
    ))

def serve():
    import uvicorn
    uvicorn.run("llm_lens.server:app", host="127.0.0.1", port=8000, reload=True)

def main():
    console.print("[bold green]llm-lens[/bold green] is running!\n")

    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        show_stats()
    elif len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()
    else:
        show_table()
