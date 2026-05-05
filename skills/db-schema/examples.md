# Database Schema — Examples

## Users table

```sql
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    email       TEXT NOT NULL,
    name        TEXT NOT NULL,
    role        TEXT NOT NULL DEFAULT 'member'
                    CHECK (role IN ('member', 'admin', 'moderator')),
    password_hash TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at  TIMESTAMPTZ DEFAULT NULL,
    CONSTRAINT uq_users_email UNIQUE (email)
);

CREATE INDEX idx_users_email   ON users(email);
CREATE INDEX idx_users_active  ON users(id) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_created ON users(created_at DESC);
```

---

## Posts with foreign key

```sql
CREATE TABLE posts (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    body        TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'draft'
                    CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMPTZ DEFAULT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_posts_user_id   ON posts(user_id);
CREATE INDEX idx_posts_status    ON posts(status);
CREATE INDEX idx_posts_published ON posts(published_at DESC) WHERE status = 'published';
```

---

## Many-to-many junction table

```sql
CREATE TABLE post_tags (
    post_id  BIGINT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    tag_id   BIGINT NOT NULL REFERENCES tags(id)  ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (post_id, tag_id)
);

CREATE INDEX idx_post_tags_tag_id ON post_tags(tag_id);
```

---

## Agent memory with pgvector

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE llm_memory (
    id           BIGSERIAL PRIMARY KEY,
    user_id      TEXT NOT NULL,
    role         TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'tool', 'system')),
    content      TEXT NOT NULL,
    embedding    vector(1024),
    tool_call_id TEXT DEFAULT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_llm_memory_created   ON llm_memory(user_id, created_at DESC);
CREATE INDEX idx_llm_memory_embedding ON llm_memory
    USING hnsw (embedding vector_cosine_ops)
    WHERE embedding IS NOT NULL;
```

---

## Common issues

### Missing index on foreign key
```sql
-- Symptom: slow JOINs or slow ON DELETE CASCADE
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 42;
-- "Seq Scan" on a large table → add an index
CREATE INDEX idx_posts_user_id ON posts(user_id);
```

### FLOAT for money
```sql
price FLOAT         -- BAD: floating point imprecision
price NUMERIC(10,2) -- GOOD: exact decimal
```

### TIMESTAMP without timezone
```sql
created_at TIMESTAMP     -- BAD: ambiguous, no timezone
created_at TIMESTAMPTZ   -- GOOD: stored as UTC
```

### Checking query performance
```sql
EXPLAIN ANALYZE
SELECT * FROM llm_memory
WHERE user_id = 'user_1'
ORDER BY created_at DESC
LIMIT 10;
-- "Seq Scan" on large table = missing index
-- High actual vs estimated time = stale statistics (run ANALYZE)
```
