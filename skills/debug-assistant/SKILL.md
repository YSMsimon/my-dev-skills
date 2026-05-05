---
name: debug-assistant
description: Systematically debug errors, exceptions, unexpected behaviour, and failing tests. Use this skill whenever the user shows an error message, stack trace, wrong output, or describes something that isn't working. Trigger on phrases like "I'm getting an error", "this isn't working", "why is this failing", "I don't understand this traceback", "help me debug", "getting a TypeError/ValueError/KeyError/AttributeError", or when any stack trace or error message is present in the conversation.
---

# Debug Assistant

Work through bugs systematically. The goal is to understand *why* the code is failing, not just silence the error.

---

## Debugging process

### Step 1: Read the full traceback — bottom to top

The last line is the error. The frames above show the call chain. Find the last frame pointing to *your* code (not a library) — that's where to look.

### Step 2: Inspect state at the failure point

Add temporary prints to see what values are present:

```python
print(f"[DEBUG] role={msg.get('role')}, content={str(msg.get('content'))[:80]}")
```

Or use `breakpoint()` to drop into pdb:
- `p variable` — print a value
- `n` — next line (step over)
- `s` — step into function
- `c` — continue
- `where` — show full stack

### Step 3: Trace the root cause backwards

Ask: why does this variable have this value? Follow it backwards — where is it assigned, what conditions lead to it?

### Step 4: Form a hypothesis, then verify

Write: "I think X is happening because Y." Add a print or assertion to prove it **before** writing any fix.

### Step 5: Apply the minimal fix

Change only what addresses the root cause. Don't clean up surrounding code at the same time.

---

## Output format

1. **What the error means** — plain English
2. **Root cause** — the specific condition, with reference to the relevant line/function
3. **Fix** — exact code change with before/after
4. **How to verify** — the test or command to confirm it's fixed
5. **Watch out for** — related risks or deeper structural issues

If not enough information: ask for the full traceback, the relevant function, and what input triggered the error.

---

## Additional resources

- For common error types and fixes, see [examples.md](examples.md)
- For logging setup script, see [scripts/logging_setup.py](scripts/logging_setup.py)
