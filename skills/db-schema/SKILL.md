---
name: db-schema
description: Design, review, and improve PostgreSQL database schemas including tables, columns, data types, indexes, constraints, foreign keys, relationships, migrations, and query optimisation. Use this skill whenever the user wants to model data, design a database, write a migration, optimise queries with indexes, normalise a schema, add pgvector support, or asks "how should I structure this in the database?" Trigger on mentions of tables, schemas, migrations, ERDs, relationships, PostgreSQL, pgvector, or database design questions.
---

# Database Schema Design

Design clear, correct, and performant PostgreSQL schemas. Model the domain accurately, enforce integrity at the database level, and support the application's query patterns.

---

## Naming conventions

| Thing | Convention | Example |
|---|---|---|
| Tables | `snake_case`, plural | `user_profiles`, `order_items` |
| Columns | `snake_case` | `created_at`, `user_id` |
| Primary key | `id` | `id BIGSERIAL PRIMARY KEY` |
| Foreign keys | `<table_singular>_id` | `user_id`, `order_id` |
| Indexes | `idx_<table>_<columns>` | `idx_posts_user_id` |
| Unique constraints | `uq_<table>_<columns>` | `uq_users_email` |
| Check constraints | `ck_<table>_<rule>` | `ck_orders_positive_total` |

---

## Data types — choose the most specific type

| Data | Type | Notes |
|---|---|---|
| Auto-increment ID (small table) | `SERIAL` | 4-byte int |
| Auto-increment ID (large table) | `BIGSERIAL` | 8-byte int |
| Distributed/external ID | `UUID` | `DEFAULT gen_random_uuid()` |
| Short text | `VARCHAR(n)` | When max length matters |
| Unlimited text | `TEXT` | No perf difference from VARCHAR in PG |
| Money / precise decimal | `NUMERIC(10, 2)` | Never use `FLOAT` for money |
| Timestamp with tz | `TIMESTAMPTZ` | **Always** use this over `TIMESTAMP` |
| Flexible data | `JSONB` | Binary, indexable — prefer over `JSON` |
| Vector embeddings | `vector(1024)` | Via pgvector extension |
| Enum | `TEXT` + `CHECK` | Easier to extend than PG ENUM |

---

## Primary keys

```sql
id BIGSERIAL PRIMARY KEY         -- most tables

id UUID PRIMARY KEY DEFAULT gen_random_uuid()  -- distributed / external-facing
```

Use UUID when IDs are exposed to clients (harder to enumerate) or created across multiple services.

---

## Indexes — when and why

```sql
-- Always index foreign keys (PG does NOT do this automatically)
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Composite — order matters: most selective column first
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial — only index the rows you always filter on
CREATE INDEX idx_sessions_active ON sessions(user_id, expires_at)
    WHERE revoked = false;

-- Vector similarity (pgvector)
CREATE INDEX idx_knowledge_embedding ON knowledge_base
    USING hnsw (embedding vector_cosine_ops)
    WHERE embedding IS NOT NULL;
```

**Always index:** every foreign key, columns in `WHERE`/`ORDER BY`/`JOIN ON`, `UNIQUE` constraint columns.

**Do NOT index:** low-cardinality columns (boolean, 2-value status), tables under 1000 rows.

---

## Relationships and ON DELETE

```sql
ON DELETE CASCADE   -- delete children when parent deleted (posts → comments)
ON DELETE RESTRICT  -- block parent deletion if children exist (orders → products)
ON DELETE SET NULL  -- orphan the child (optional audit trail)
```

---

## Migrations

- Never modify an applied migration — add a new one
- Always write both up and down
- For large tables: use `NOT VALID` to add constraints without a full table scan
- `NOT NULL` columns with defaults are safe on Postgres 11+ (no table rewrite)

---

## Output format

When designing a schema, deliver:

1. **Entity summary** — plain English: what the entities are and how they relate
2. **CREATE TABLE statements** — complete, runnable SQL with all constraints and defaults
3. **Index statements** — each with a comment explaining why it exists
4. **Design decisions** — notes on non-obvious choices
5. **Common queries** — 2–3 example queries the schema is designed to serve
6. **Migration** — up/down pair if modifying an existing schema

---

## Additional resources

- For usage examples, see [examples.md](examples.md)
- For templates, see [template/](template/)
