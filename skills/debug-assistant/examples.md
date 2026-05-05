# Debug Assistant — Examples

## TypeError: missing argument

```
TypeError: Agent._save_turn() missing 1 required positional argument: 'assistance_content'
```

Cause: function signature changed but call sites weren't updated.
Fix: update the call site, or make the parameter optional with a default.

---

## TypeError: NoneType

```
AttributeError: 'NoneType' object has no attribute 'get'
TypeError: 'NoneType' object is not subscriptable
```

Cause: variable is None when you expected a value.

```python
print(type(my_var), my_var)   # print type AND value
```

Common culprits: `dict.get("key")` returns None on missing key, function missing a `return`, DB query returned no rows, `os.getenv("MISSING")` returns None.

---

## KeyError

```
KeyError: 'embedding'
```

```python
print(my_dict.keys())           # what keys actually exist?
embedding = my_dict.get('embedding')   # use .get() with a default
```

---

## JSONDecodeError

```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

```python
print(repr(text))   # repr shows hidden characters, newlines, etc.
```

Common causes: LLM returned markdown with ` ```json ``` ` fences (strip them), empty string, partial generation.

---

## RecursionError

```
RecursionError: maximum recursion depth exceeded
```

In the agent loop — `_execute()` calls itself with no depth limit:

```python
def _execute(self, messages, depth=0):
    if depth > 10:
        return messages + [{'role': 'assistant', 'content': 'Max tool depth reached.'}]
    ...
    return self._execute(messages, depth + 1)
```

---

## psycopg2.OperationalError: connection refused

```bash
docker compose ps        # check if container is running
docker compose up -d     # start it
docker compose logs db   # look for "ready to accept connections"
```

- Inside docker-compose: use service name `db`, not `localhost`
- From host machine: use `localhost` with the mapped port (e.g. 5433)

---

## psycopg2.errors.UndefinedTable

```bash
docker compose down -v   # remove volumes (clears DB)
docker compose up -d     # re-runs init.sql on fresh DB
```

---

## ollama._types.ResponseError: model not found

```bash
ollama list                   # see what's available
ollama pull nomic-embed-text  # pull missing model
```

---

## ollama._types.ResponseError: Internal Server Error

Cause: context window exceeded. The message history (including large tool results like HTML pages) grew too large for the model.

Fix: truncate large tool results before appending to messages, or add a depth limit to `_execute`.

---

## Debugging the agent loop

### Conversation not responding
```python
def _execute(self, messages):
    print(f"[_execute] messages: {len(messages)}", file=sys.stderr)
    ...
    print(f"[_execute] content length: {len(full_content)}", file=sys.stderr)
```

### Tool not being called
```python
for chunk in response:
    if chunk.message.tool_calls:
        print(f"[tool_calls] {chunk.message.tool_calls}", file=sys.stderr)
```

### Embedding dimension mismatch
```python
embedding = self.get_embedding("test")
print(f"[embed] dims: {len(embedding)}")   # must match vector(N) in schema
```
