# Code Review — Examples

## Correctness: swallowed exception

```python
# Bug — error is lost silently
try:
    self.db.update_user_profile(self.user_id, json.loads(text))
except json.JSONDecodeError:
    pass

# Better
except json.JSONDecodeError as e:
    print(f"[profile] JSON parse failed: {e}", file=sys.stderr)
```

---

## Security: SQL injection

```python
# DANGEROUS
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# Safe — parameterised
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

---

## Security: command injection

```python
# Risky — user can pass "ls; rm -rf /"
def run_bash(command: str) -> str:
    result = subprocess.run(command, shell=True, ...)
```

For internal tools this is acceptable; for externally-exposed APIs it isn't.

---

## Readability: magic number

```python
# Unclear
if depth > 10:

# Named constant
MAX_TOOL_DEPTH = 10
if depth > MAX_TOOL_DEPTH:
```

---

## Design: function doing too many things

```python
# _build_messages fetches history, computes embeddings,
# semantic searches, AND saves to DB — hard to test, hard to change
def _build_messages(self, user_message: str) -> List[Dict]:
    history, recent_ids = self.db.get_recent_history(...)  # I/O
    embedding = self.get_embedding(user_message)           # I/O
    memories = self.db.semantic_search(...)                # I/O
    self._save_turn(...)                                   # side effect!
```

Side effects inside "build" functions are surprising — consider separating persistence from construction.

---

## Performance: unbounded recursion

```python
# No depth limit — if tools keep firing, this stack-overflows
def _execute(self, messages):
    ...
    return self._execute(messages)

# Fix
def _execute(self, messages, depth=0):
    if depth > MAX_TOOL_DEPTH:
        return messages
    ...
    return self._execute(messages, depth + 1)
```

---

## Error handling: too broad

```python
# Masks ALL errors including programmer mistakes
try:
    result = tool_handler[name](**args)
except Exception:
    pass

# Better — specific, with logging
except KeyError:
    print(f"[tool] unknown tool: {name}", file=sys.stderr)
    result = f"Error: no tool named '{name}'"
except TypeError as e:
    print(f"[tool] wrong args for {name}: {e}", file=sys.stderr)
    result = f"Error: {e}"
```
