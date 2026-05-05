# API Endpoints — [Resource Name]

## Resource model

[Describe the entities and their relationships in plain English.]

## Endpoints

| Method | Path | Description | Auth |
|---|---|---|---|
| `GET` | `/v1/[resources]` | List [resources] (paginated) | [auth level] |
| `POST` | `/v1/[resources]` | Create [resource] | [auth level] |
| `GET` | `/v1/[resources]/{id}` | Get [resource] by ID | [auth level] |
| `PATCH` | `/v1/[resources]/{id}` | Update [resource] fields | [auth level] |
| `DELETE` | `/v1/[resources]/{id}` | Delete [resource] | [auth level] |

## Design decisions

[Notes on non-obvious choices: UUID vs integer ID, soft delete, nested vs flat routes, etc.]
