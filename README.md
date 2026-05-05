[中文版](README_CN.md)

# dev-skills

A collection of reusable skills for AI coding agents. Each skill is a self-contained folder with instructions, examples, scripts, and templates.

## Skills

| Skill | Description |
|---|---|
| `api-designer` | Design REST APIs — endpoints, status codes, auth, versioning |
| `code-review` | Structured code review across correctness, security, performance, and more |
| `db-schema` | PostgreSQL schema design, indexes, migrations, pgvector |
| `debug-assistant` | Systematic debugging — tracebacks, common errors, root cause analysis |
| `dockerfile` | Dockerfiles and docker-compose for any stack |
| `git-workflow` | Commit messages, branching, PRs, rebasing, undoing mistakes |
| `test-writer` | pytest unit tests, fixtures, mocking, integration tests |

## Structure

Each skill folder contains:
- `SKILL.md` — main instructions loaded by the agent
- `examples.md` — usage examples
- `scripts/` — runnable code
- `template/` — boilerplate starting points

## Also available

These skills are also bundled inside the full agent at [github.com/YSMsimon/this-is-my-agent](https://github.com/YSMsimon/this-is-my-agent/tree/master/skills).
