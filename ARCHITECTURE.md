# Code Review Agent — Architecture

## 1. System Goal

The system is an AI-powered code review agent that uses Hindsight as persistent memory.

The agent should become increasingly aware of:

- Project conventions
- Developer preferences
- Previous review decisions
- Accepted and rejected suggestions
- Recurring issues
- Architectural decisions

Memory must influence future code-review behavior.

---

## 2. High-Level Architecture

```text
                    Developer
                        |
                        v
                +---------------+
                |   FastAPI API  |
                +-------+-------+
                        |
                        v
                +---------------+
                | Code Review    |
                | Agent          |
                +-------+-------+
                        |
             +----------+----------+
             |                     |
             v                     v
      Hindsight Recall         LLM Review
             |                     |
             |                     |
             +----------+----------+
                        |
                        v
                Structured Review
                        |
                        v
                Developer Feedback
                        |
                        v
                Memory Extraction
                        |
                        v
                Hindsight Retain
```

---

## 3. Hindsight Memory Bank

The application uses one Hindsight memory bank:

```text
code-review-agent
```

The bank represents the accumulated knowledge of the project and developer.

We are intentionally using one bank for the MVP.

---

## 4. Memory Types

The application recognizes the following logical memory categories.

### 4.1 Project Convention

Rules or conventions specific to the codebase.

Examples:

- HTTP library conventions
- Naming conventions
- Error-handling conventions
- Testing conventions
- Framework-specific practices

Example memory:

> This project uses requests for HTTP calls. Do not recommend replacing requests with httpx unless there is a concrete requirement for async HTTP.

---

### 4.2 Developer Preference

A preference expressed by the developer that should influence future reviews.

Example:

> The developer prefers explicit error handling instead of broad exception handling.

---

### 4.3 Review Decision

An important decision made during a previous code review.

Example:

> The authentication abstraction was intentionally retained because multiple services depend on it.

---

### 4.4 Accepted Suggestion

A recommendation from the agent that the developer accepted or implemented.

Example:

> The developer accepted the recommendation to add input validation to the API endpoint.

---

### 4.5 Rejected Suggestion

A recommendation that the developer explicitly rejected, together with the reason when available.

Example:

> The developer rejected replacing requests with httpx because the project does not require asynchronous HTTP.

Rejected suggestions are particularly important because they prevent the agent from repeatedly making the same unwanted recommendation.

---

### 4.6 Recurring Issue

A problem that appears repeatedly across reviews.

Example:

> Authentication handlers repeatedly omit rate limiting.

Recurring issues can influence future review prioritization.

---

### 4.7 Architectural Decision

A project-level technical decision that future reviews should respect.

Example:

> Database access must go through the repository layer rather than directly from API handlers.

---

## 5. Tags

When supported by the Hindsight client, retained knowledge should use tags to describe its logical category.

Example:

```text
project_convention
developer_preference
review_decision
accepted_suggestion
rejected_suggestion
recurring_issue
architectural_decision
```

The application should keep the tag vocabulary small and predictable.

Tags are for retrieval/filtering and debugging; the actual memory content remains natural-language knowledge.

Hindsight supports tag filtering during recall. 

---

## 6. Retain Strategy

The application should retain information primarily when meaningful learning occurs.

Potential retain events:

1. Developer establishes a project convention.
2. Developer states a preference.
3. Developer accepts an important recommendation.
4. Developer rejects a recommendation and explains why.
5. Developer identifies a recurring issue.
6. Developer explains an architectural decision.

The application should avoid retaining:

- Every generated review
- Temporary conversational text
- Duplicate information
- Generic programming knowledge
- Irrelevant code snippets
- Low-value LLM reasoning

---

## 7. Recall Strategy

Before generating a review, the agent should query Hindsight using the code-review context.

Example query:

```text
What project conventions, developer preferences,
previous review decisions, and relevant lessons should
be considered when reviewing this code?
```

The query should also include relevant code context.

Example:

```text
Reviewing Python authentication code.

What previous project conventions, decisions,
developer preferences, and recurring issues are relevant
to authentication code?
```

Hindsight returns relevant memories.

Those memories are then passed explicitly into the LLM review context.

---

## 8. Memory → Review Flow

The critical behavior is:

```text
Code
  |
  v
Build memory query
  |
  v
Hindsight Recall
  |
  v
Relevant memories
  |
  v
Review prompt
  |
  v
LLM
  |
  v
Review findings
```

The agent must not merely retrieve memories and display them.

The memories must influence the review.

---

## 9. Feedback → Memory Flow

After a review:

```text
Review
  |
  v
Developer feedback
  |
  v
Determine whether meaningful knowledge exists
  |
  v
Create concise memory statement
  |
  v
Assign logical memory category
  |
  v
Hindsight Retain
```

Example:

```text
Agent:
"Consider replacing requests with httpx."

Developer:
"No. We intentionally use requests across this project."

Retained memory:

"This project intentionally uses requests for HTTP calls.
Do not recommend replacing requests with httpx unless a
concrete async requirement exists."
```

---

## 10. Memory Safety

The agent must not automatically treat every developer statement as a permanent project rule.

Before retaining information, the application should distinguish between:

- Explicit project decisions
- Explicit developer preferences
- Temporary instructions
- Questions
- Hypothetical statements
- Casual conversation

Only meaningful knowledge should become persistent memory.

---

## 11. MVP Retrieval Policy

The first implementation will use:

```text
Hindsight Recall
```

rather than Hindsight Reflect.

Reason:

The application should explicitly control how retrieved memories are injected into the review prompt.

This makes the relationship between:

```text
Memory
→ Review Context
→ Review Behavior
```

easy to inspect and demonstrate.

---

## 12. Memory-Aware Review

Every review should conceptually have two modes:

### Memory OFF

```text
Code
→ LLM
→ Generic review
```

### Memory ON

```text
Code
→ Hindsight Recall
→ Relevant project knowledge
→ LLM
→ Project-aware review
```

The final demo should be able to demonstrate the difference.

---

## 13. Core Product Loop

The complete learning loop is:

```text
                +------------------+
                |  Submit Code     |
                +--------+---------+
                         |
                         v
                +------------------+
                | Hindsight Recall |
                +--------+---------+
                         |
                         v
                +------------------+
                |   LLM Review     |
                +--------+---------+
                         |
                         v
                +------------------+
                | Review Findings  |
                +--------+---------+
                         |
                         v
                +------------------+
                | Developer        |
                | Feedback         |
                +--------+---------+
                         |
                         v
                +------------------+
                | Hindsight Retain |
                +--------+---------+
                         |
                         +--------------------+
                                              |
                                              v
                                      Future Reviews
```

This loop is the core differentiator of the product.