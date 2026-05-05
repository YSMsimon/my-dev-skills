---
name: api-designer
description: Design REST APIs including endpoints, URL structures, HTTP methods, request/response bodies, status codes, authentication, versioning, pagination, and error formats. Use this skill whenever the user wants to design an API, plan endpoints, structure a backend, decide on REST conventions, write an API spec, design request/response shapes, or asks "how should I structure this API?" Trigger on phrases like "design an API", "what endpoints do I need", "REST API for", "API structure", "request/response format", "status codes", or "API versioning".
---

# API Designer

Design REST APIs that are consistent, predictable, and easy to consume. Good API design is a contract — once clients depend on it, changing it is expensive. Get the structure right upfront.

---

## URL structure

URLs identify **resources** (nouns). The HTTP method expresses the action.

```
GET    /users                    list all users
GET    /users/{id}               get one user
POST   /users                    create a user
PATCH  /users/{id}               update a user partially
PUT    /users/{id}               replace a user entirely
DELETE /users/{id}               delete a user

GET    /users/{id}/posts         list posts by this user
POST   /users/{id}/posts         create a post for this user
```

**Rules:**
- Plural nouns for collections: `/users`, not `/user`
- Lowercase, hyphen-separated: `/user-profiles`, not `/userProfiles`
- Nested max 2 levels deep — flatten deeper with query params: `GET /comments?post_id=42`
- Never put verbs in URLs: `/createUser` is wrong, `POST /users` is right

---

## HTTP methods

| Method | Use | Body | Idempotent |
|---|---|---|---|
| `GET` | Fetch resource(s) | No | Yes |
| `POST` | Create new resource | Yes | No |
| `PUT` | Replace resource entirely | Yes | Yes |
| `PATCH` | Update fields partially | Yes | No |
| `DELETE` | Delete resource | No | Yes |

Use `PATCH` over `PUT` for most updates — `PUT` requires sending the full object.

---

## Status codes

### Success
| Code | When to use |
|---|---|
| `200 OK` | GET, PATCH, PUT succeeded |
| `201 Created` | POST succeeded; include `Location: /users/abc` header |
| `204 No Content` | DELETE succeeded (no body) |

### Client errors
| Code | When to use |
|---|---|
| `400 Bad Request` | Malformed JSON, missing required field |
| `401 Unauthorized` | Missing or invalid token |
| `403 Forbidden` | Valid token but insufficient permissions |
| `404 Not Found` | Resource ID doesn't exist |
| `409 Conflict` | Duplicate (email already taken) |
| `422 Unprocessable Entity` | Valid JSON but business rule violation |
| `429 Too Many Requests` | Rate limited; add `Retry-After` header |

### Server errors
| Code | When to use |
|---|---|
| `500 Internal Server Error` | Unhandled exception |
| `503 Service Unavailable` | DB down, maintenance; add `Retry-After` header |

---

## Error response format

One consistent error shape for the whole API:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "message": "must be a valid email address" }
    ]
  }
}
```

`code` is machine-readable. `message` is human-readable. `details` is optional for field-level errors.

---

## Filtering, sorting, pagination

```
GET /v1/posts?status=published
GET /v1/posts?sort=created_at&order=desc
GET /v1/posts?page=2&per_page=20
GET /v1/posts?after=post_cursor_abc&limit=20
```

Use cursor pagination for feeds where items are inserted while users paginate.

Always wrap list responses: `{ "data": [...], "pagination": {...} }` — lets you add metadata without breaking clients.

---

## Versioning

Version from day one. Use URL path versioning: `/v1/users`, `/v2/users`.

Deprecation: add `Deprecation: true` and `Sunset: 2026-01-01` headers to old routes, monitor traffic before removing.

---

## Authentication

```
Authorization: Bearer <jwt>     # user-facing APIs
X-API-Key: sk_live_abc123       # server-to-server
```

- `401` for missing/expired/invalid token
- `403` for valid token but wrong permissions
- Never reveal which specific check failed

---

## Output format

When designing an API, deliver:

1. **Resource model** — entities and relationships (plain English)
2. **Endpoint table** — method, path, description, auth required
3. **Request/response examples** — for create, list, get, update, delete
4. **Error format** — standard error shape
5. **Design decisions** — notes on non-obvious choices

---

## Additional resources

- For usage examples, see [examples.md](examples.md)
- For scripts, see [scripts/](scripts/)
- For templates, see [template/](template/)
