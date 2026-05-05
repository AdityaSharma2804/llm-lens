import time
from llm_lens.core import _insert_record

def _wrap(original_func, label):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = original_func(*args, **kwargs)
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            _insert_record(label, elapsed, "ok", None)
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
