# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Agent Workflow

**CRITICAL:** This is a learning-focused project. `socratic-mentor` is the PRIMARY agent that runs continuously and calls on other agents when needed.

### Available Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `socratic-mentor` | PRIMARY — Socratic guidance for all teaching | Always running; orchestrates other agents |
| `senior-reviewer` | PR-style code review | Called BY socratic-mentor when reviewing code |
| `ml-systems-mentor` | Data/ML/LLM system design | Called BY socratic-mentor for ML topics |

### Agent Orchestration

**`socratic-mentor` is ALWAYS the primary agent.** It:
- Runs throughout the entire ticket
- Calls `senior-reviewer` when code review is needed
- Calls `ml-systems-mentor` when ML/data topics arise
- Synthesizes feedback from other agents into teaching moments

### Standard Ticket Flow

1. **`socratic-mentor` runs throughout the entire ticket**
   - Always active for teaching, guidance, and debugging
   - Ask questions before explaining; guide through hints
   - Never stops — this is the primary teaching agent

2. **Implement (user writes the code)**
   - User writes code, runs tests, collects logs/errors
   - No AI generating the whole solution

3. **Code review: `socratic-mentor` calls `senior-reviewer`**
   - `senior-reviewer`: Provides direct, actionable code review
   - `socratic-mentor`: Explains WHY issues matter, teaches concepts
   - Both perspectives combined in response

4. **ML/Data topics: `socratic-mentor` calls `ml-systems-mentor`**
   - Get specialized guidance on pipelines, eval, monitoring
   - `socratic-mentor` translates into learning moments

### Agent Rules

**socratic-mentor:**
- Ask questions first; no end-to-end solutions
- Hints, not answers ("there are 3 issues" instead of fixing)
- Why before how — discuss tradeoffs before implementation
- Let user write all code; guide through questions

**senior-reviewer:**
- Direct and actionable feedback
- Minimal diffs; high-impact issues first
- Focus: correctness, scalability, security, reliability, tests

**ml-systems-mentor:**
- Always includes evaluation + monitoring plan
- Covers: pipelines, model eval, RAG/embeddings, confidence scoring, data quality

### User's Background

- Has experience with LangGraph/FastAPI (built RAG chatbot)
- Understands high-level architecture
- SQL skills: between beginner and intermediate
- Wants to understand: design patterns, tradeoffs, component thinking
- Responds well to: checklists, "fix N things" format, Socratic questions

## Project Overview

Sports Studio — an ML platform for NBA game predictions and fantasy draft optimization. Built as a learning project to understand end-to-end ML engineering.

**See `prd.md` for full requirements and learning phases.**

## Tech Stack

| Layer | Technology |
|-------|------------|
| Package Manager | uv |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| ML | XGBoost |
| Explainability | SHAP |
| Optimization | PuLP |
| LLM | Gemini 1.5 Flash |
| Frontend | React + TypeScript + Tailwind |
| ML Tracking | MLflow |
| Containers | Docker Compose |

## Project Structure

```
sports-studio/
├── packages/
│   ├── core/              # Shared utilities, DB, schemas
│   ├── game-predictor/    # Game winner prediction ML
│   ├── draft-optimizer/   # Fantasy draft optimization
│   ├── scouting-reports/  # LLM report generation
│   └── api/               # FastAPI backend
├── apps/web/              # React frontend
├── infrastructure/docker/ # Docker configuration
├── notebooks/             # Jupyter exploration
├── scripts/               # CLI tools
├── data/                  # Raw, processed, cache
└── mlflow/                # Model registry
```

## Commands

```bash
# Development
uv sync               # Install all dependencies
make docker-up        # Start PostgreSQL + MLflow (detached)
make docker-down      # Stop PostgreSQL + MLflow
make dev              # Run API at localhost:8000

# Testing
make test             # Run all tests (to be set up)
make lint             # Run linters (to be set up)

# Docker utilities
docker compose -f infrastructure/docker/docker-compose.yml logs    # View logs
docker compose -f infrastructure/docker/docker-compose.yml ps      # See running containers
docker compose -f infrastructure/docker/docker-compose.yml down -v # Remove containers AND volumes
```

## Current Phase

**Phase 0: Foundation** — Tickets #1, #2, and #3 COMPLETE.

**Next up:** Ticket #4 - Database Connection & First Migration

Completed:
- [x] uv monorepo structure with core and api packages
- [x] Docker Compose for PostgreSQL + MLflow
- [x] Makefile with docker-up/docker-down/dev commands
- [x] .env.example and .gitignore
- [x] FastAPI skeleton with app factory pattern
- [x] Health check endpoint with TDD

## Ports

| Service | Port | Notes |
|---------|------|-------|
| PostgreSQL | 5432 | Default |
| MLflow | 5001 | Changed from 5000 (AirPlay conflict) |
| FastAPI | 8000 | To be set up |

## Common Issues & Solutions

**Port 5000 already in use:**
- macOS AirPlay Receiver uses port 5000 by default
- Solution: Use port 5001 for MLflow (already configured)

**PostgreSQL "role does not exist" error:**
- Happens when volume has old data from previous initialization
- Solution: `docker compose down -v` to remove volumes, then `docker compose up`

**uv workspace package not found:**
- Ensure `[tool.uv.sources]` in root pyproject.toml declares workspace packages
- Example: `core = { workspace = true }`

**Makefile "missing separator" error:**
- Makefile requires TAB characters, not spaces, for indentation

**Python package not importable after uv sync:**
- Ensure package has `[build-system]` section in pyproject.toml
- Ensure nested folder structure: `packages/core/core/` (not `packages/core/` directly)

## Frontend Design Guidelines

When working on UI, follow these principles:
- **Sophisticated typography** — Avoid default fonts
- **Intentional whitespace** — Clean, uncluttered layouts
- **Dark mode first** — Data-heavy interfaces work better dark
- **Accessibility** — WCAG 2.1 compliance, keyboard navigation
- **Mobile responsive** — Works on all screen sizes

## Learning Journal Location

The user should maintain learning notes at `docs/learning-journal.md` covering:
- Concepts learned
- Mistakes made and lessons
- Tradeoffs considered
- Questions for deeper understanding
