import time
from rich.console import Console
from rich.table import Table
from llm_lens.core import track, get_records

console = Console()

@track
def fake_openai_call(prompt: str) -> str:
    time.sleep(0.12)
    return f"response to: {prompt}"

@track
def failing_call():
    time.sleep(0.05)
    raise ConnectionError("API unreachable")

def main():
    console.print("[bold green]llm-lens[/bold green] is running!\n")

    fake_openai_call("what is 2+2?")
    fake_openai_call("explain recursion")
    try:
        failing_call()
    except ConnectionError:
        pass

    records = get_records()

    table = Table(title="Tracked Calls")
    table.add_column("Function", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Error")
    table.add_column("Timestamp", style="dim")

    for r in records:
        color = "green" if r["status"] == "ok" else "red"
        table.add_row(
            r["func"],
            f"[{color}]{r['status']}[/{color}]",
            str(r["latency_ms"]),
            r["error"] or "-",
            r["timestamp"]
        )

    console.print(table)
    console.print(f"\n[bold]Total calls:[/bold] {len(records)}")

