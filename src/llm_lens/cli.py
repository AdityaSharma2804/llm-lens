import time
from rich.console import Console
from llm_lens.core import track, track_latency

console = Console()

@track
def fake_openai_call(prompt: str) -> str:
    """Simulates an API call with artificial delay."""
    time.sleep(0.12)
    return f"response to: {prompt}"

@track
def failing_call():
    """Simulates a failed API call."""
    time.sleep(0.05)
    raise ConnectionError("API unreachable")

def main():
    console.print("[bold green]llm-lens[/bold green] is running!")

    console.print("\n--- decorator demo ---")
    result = fake_openai_call("what is 2+2?")
    console.print(f"got: {result}")

    try:
        failing_call()
    except ConnectionError:
        pass

    console.print("\n--- context manager demo ---")
    with track_latency("manual block"):
        time.sleep(0.08)
        console.print("did some work inside the block")
        