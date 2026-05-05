# Test Writer — Examples

## Testing database code

```python
def test_add_message_stores_content(db):
    db.add_message("user1", "user", "hello world", embedding=None, tool_call_id=None)
    history, _ = db.get_recent_history("user1", limit=10)
    assert len(history) == 1
    assert history[0]["content"] == "hello world"
    assert history[0]["role"] == "user"

def test_get_recent_history_respects_limit(db):
    for i in range(15):
        db.add_message("user1", "user", f"message {i}", embedding=None, tool_call_id=None)
    history, _ = db.get_recent_history("user1", limit=5)
    assert len(history) == 5

def test_get_recent_history_isolates_by_user(db):
    db.add_message("user1", "user", "alice message", embedding=None, tool_call_id=None)
    db.add_message("user2", "user", "bob message",   embedding=None, tool_call_id=None)
    history, _ = db.get_recent_history("user1", limit=100)
    contents = [m["content"] for m in history]
    assert "alice message" in contents
    assert "bob message" not in contents
```

---

## Mocking Ollama

```python
from unittest.mock import patch, MagicMock

def test_agent_run_calls_chat_with_system_prompt(mock_config):
    with patch("my_agent_loop.Client") as MockClient:
        mock_client = MagicMock()
        MockClient.return_value = mock_client

        mock_chunk = MagicMock()
        mock_chunk.message.content = "Hello!"
        mock_chunk.message.tool_calls = None
        mock_client.chat.return_value = [mock_chunk]

        agent = Agent(cfg=mock_config, db=MagicMock())
        agent.run("hi")

        assert mock_client.chat.called
        call_kwargs = mock_client.chat.call_args[1]
        assert call_kwargs["model"] == mock_config.model
```

---

## Mocking web search

```python
def test_web_search_returns_empty_on_no_results():
    with patch("crawl.DDGS") as MockDDGS:
        MockDDGS.return_value.__enter__.return_value.text.return_value = []
        from crawl import web_search
        result = web_search("xkq92jfkwq2")
        assert result == []
```

---

## Testing threaded code

```python
import threading

def test_update_profile_runs_in_background(agent):
    update_finished = threading.Event()
    original = agent._update_profile

    def tracked(*args, **kwargs):
        original(*args, **kwargs)
        update_finished.set()

    with patch.object(agent, "_update_profile", side_effect=tracked):
        agent._save_turn({"role": "user", "content": "I am Alice"})
        agent._save_turn({"role": "assistant", "content": "Hello Alice!"})

        assert not update_finished.is_set()   # call returned immediately
        update_finished.wait(timeout=5)
        assert update_finished.is_set()        # background thread finished
```
