import time
from llm_lens.core import _insert_record

PRICING = {
    "gpt-4o":            {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":       {"input": 0.15,  "output": 0.60},
    "gpt-4-turbo":       {"input": 10.00, "output": 30.00},
    "claude-3-5-sonnet": {"input": 3.00,  "output": 15.00},
    "claude-3-5-haiku":  {"input": 0.80,  "output": 4.00},
    "claude-3-opus":     {"input": 15.00, "output": 75.00},
}

def _calculate_cost(model, input_tokens, output_tokens):
    for key in PRICING:
        if key in model:
            p = PRICING[key]
            return round(
                (input_tokens / 1_000_000 * p["input"]) +
                (output_tokens / 1_000_000 * p["output"]),
                8
            )
    return None

def _wrap(original_func, label):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = original_func(*args, **kwargs)
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            input_tokens = None
            output_tokens = None
            cost_usd = None
            model = None
            if hasattr(result, "usage") and result.usage is not None:
                usage = result.usage
                input_tokens = getattr(usage, "input_tokens",
                               getattr(usage, "prompt_tokens", None))
                output_tokens = getattr(usage, "output_tokens",
                                getattr(usage, "completion_tokens", None))
            if hasattr(result, "model"):
                model = result.model
            if input_tokens and output_tokens and model:
                cost_usd = _calculate_cost(model, input_tokens, output_tokens)
            _insert_record(label, elapsed, "ok", None,
                           input_tokens, output_tokens, cost_usd, model)
            return result
        except Exception as e:
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            _insert_record(label, elapsed, "error", str(e))
            raise
    return wrapper

def patch_openai():
    try:
        import openai
        target = openai.resources.chat.completions.Completions
        target.create = _wrap(target.create, "openai.chat.completions.create")
        print("[llm-lens] OpenAI patched")
    except ImportError:
        pass

def patch_anthropic():
    try:
        import anthropic
        target = anthropic.resources.messages.Messages
        target.create = _wrap(target.create, "anthropic.messages.create")
        print("[llm-lens] Anthropic patched")
    except ImportError:
        pass

def patch_all():
    patch_openai()
    patch_anthropic()

