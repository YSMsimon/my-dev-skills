-- Migration: [description]
-- Date: [YYYY-MM-DD]

-- === UP ===

ALTER TABLE [table] ADD COLUMN [column] [type] [constraints];

CREATE INDEX idx_[table]_[column] ON [table]([column])
    WHERE [condition];   -- remove WHERE if not a partial index


-- === DOWN ===

DROP INDEX IF EXISTS idx_[table]_[column];

ALTER TABLE [table] DROP COLUMN [column];
