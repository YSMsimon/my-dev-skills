---
name: code-review
description: Perform a structured, thorough code review on a file, function, snippet, or entire module. Use this skill whenever the user asks to review code, check code quality, audit a function, look for bugs, find security issues, assess readability, or wants feedback on their implementation. Trigger even if the user phrases it casually like "what do you think of this?", "is this good?", or "any issues here?" when code is present.
---

# Code Review

Perform a multi-dimensional code review. Think like a senior engineer doing a pull request review: honest, specific, and constructive. The goal is actionable, prioritised feedback — not a list of nitpicks.

---

## Review dimensions

Work through all of these. Skip a dimension only if it genuinely doesn't apply.

### 1. Correctness
- Does the code do what it claims?
- Are edge cases handled: empty input, `None`/`null`, zero, negative, very large values?
- Are exceptions caught at the right level, or swallowed silently?
- Are there off-by-one errors or logic that fails on boundary values?

### 2. Security
- Is user input validated before use?
- SQL injection risk? (Always parameterised queries — never f-strings in SQL)
- Command injection? (`subprocess.run(cmd, shell=True)` with user input is dangerous)
- Secrets hardcoded or logged?
- File paths from user input validated (path traversal)?

### 3. Readability & naming
- Are names self-explanatory?
- Are functions short enough to hold in your head? (~30–40 lines)
- Magic numbers or strings that should be named constants?

### 4. Design & structure
- Does each function do one thing?
- Duplicated logic that should be extracted?
- Are side effects obvious and expected?

### 5. Performance
- N+1 queries (querying in a loop)?
- Unbounded operations (no limit on results, no recursion depth cap)?
- Expensive I/O that could be batched?

### 6. Error handling
- Exceptions too broad (`except Exception`)?
- Error messages useful for debugging?
- Does one error crash the whole session?

### 7. Tests (if provided)
- Happy path, error path, and edge cases covered?
- Do tests verify behaviour, not just that code runs?

---

## Adapting scope

- **Single function:** go deep on all 7 dimensions
- **Full file:** focus on structure and design first, drill into the riskiest parts
- **Diff / PR:** review only what changed, flag if changes interact badly with surrounding code
- **"Is this fine?" quick check:** lead with summary + critical only, offer to go deeper

---

## Tone

Be direct. "This function will panic on empty input" is better than "you might want to consider handling empty input." Explain *why* something is a problem. Prioritise — 3 critical issues is more useful than 15 medium ones. If the code is good, say so.

---

## Additional resources

- For usage examples, see [examples.md](examples.md)
- For review output template, see [template/review.md](template/review.md)
