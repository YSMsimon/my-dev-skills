# API Designer — Examples

## Create resource (POST /users)

**Request:**
```http
POST /v1/users
Content-Type: application/json
Authorization: Bearer <token>

{
  "email": "alice@example.com",
  "name": "Alice Chen",
  "role": "member"
}
```

**Response:**
```http
HTTP/1.1 201 Created
Location: /v1/users/usr_abc123
Content-Type: application/json

{
  "id": "usr_abc123",
  "email": "alice@example.com",
  "name": "Alice Chen",
  "role": "member",
  "created_at": "2025-05-02T10:00:00Z",
  "updated_at": "2025-05-02T10:00:00Z"
}
```

Always return the created resource — the client shouldn't need a second GET.

---

## List resources (GET /users)

```http
HTTP/1.1 200 OK

{
  "data": [
    {"id": "usr_abc123", "email": "alice@example.com", "name": "Alice"},
    {"id": "usr_def456", "email": "bob@example.com",   "name": "Bob"}
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 84,
    "next": "/v1/users?page=2&per_page=20",
    "prev": null
  }
}
```

---

## Partial update (PATCH /users/{id})

```http
PATCH /v1/users/usr_abc123
Content-Type: application/json

{ "name": "Alice Smith" }
```

Only include fields being changed. Return the full updated resource with `200`.

---

## Delete (DELETE /users/{id})

```http
DELETE /v1/users/usr_abc123
Authorization: Bearer <token>
```

```http
HTTP/1.1 204 No Content
```

If already deleted, still return `204` (idempotent).

---

## Error responses

```http
HTTP/1.1 409 Conflict

{
  "error": {
    "code": "EMAIL_ALREADY_EXISTS",
    "message": "An account with this email already exists"
  }
}
```

```http
HTTP/1.1 401 Unauthorized

{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "The provided token is expired or invalid"
  }
}
```

---

## Common mistakes

### Verbs in URLs
```
# Wrong
POST /api/sendEmail
POST /api/users/123/activate

# Right
POST /v1/emails
POST /v1/users/123/activations
```

### Returning 200 for errors
```python
# Wrong
return {"status": "error", "message": "user not found"}, 200

# Right
raise HTTPException(status_code=404, detail={"error": {...}})
```

### No pagination on list endpoints
```python
# Wrong — returns all rows
def list_posts(db):
    return db.get_all_posts()

# Right
def list_posts(page: int = 1, per_page: int = 20, db = Depends(get_db)):
    per_page = min(per_page, 100)
    return db.get_posts(offset=(page-1)*per_page, limit=per_page)
```
