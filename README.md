# Hindsight Code Review Agent

An AI-powered code review agent that uses Hindsight
persistent memory to remember project-specific
engineering decisions and apply them during future
code reviews.

## Problem

Generic AI code reviewers often give recommendations
based only on general best practices.

However, every codebase has its own architectural
decisions and engineering conventions.

For example, a project may intentionally use synchronous
HTTP requests. A generic reviewer may recommend migrating
to async even when there is no requirement for it.

## Solution

This project combines an LLM-based code reviewer with
Hindsight persistent memory.

Developers can teach the agent project-specific decisions.
Those decisions are retained and recalled during future
reviews.

Workflow:

Code
  ↓
Code Review Agent
  ↓
Hindsight Recall
  ↓
LLM Reasoning
  ↓
Review
  ↓
Developer Feedback
  ↓
Hindsight Retain
  ↓
Future Reviews

## Before vs After

Without project memory:

Generic code
→ Generic recommendation

With Hindsight:

Generic code
+ Project-specific memory
→ Context-aware recommendation

Example:

Developer:
"Keep the project synchronous unless there is a concrete
requirement for async behavior."

The agent retains this decision and can use it during
future reviews.

## Tech Stack

- Python
- FastAPI
- Groq
- Hindsight
- Pydantic

## Features

- AI-powered code review
- Persistent project memory
- Developer feedback retention
- Project-specific recommendations
- Memory recall during future reviews

## Project Status

MVP / Open Source
