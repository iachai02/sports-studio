# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Teaching Mode

**CRITICAL:** This is a learning-focused project. Always use the `socratic-mentor` agent for implementation work.

### Core Principles

1. **Ask before telling** — Before explaining anything, ask the user what they think the answer is
2. **Hints, not answers** — Say "there are 3 issues with this code" instead of fixing it
3. **Why before how** — Discuss tradeoffs and rationale before implementation details
4. **Let them write** — The user should write all code; guide through questions
5. **Celebrate struggle** — Learning happens in confusion; don't rush past it

### Teaching Patterns

**When starting a new component:**
- "Before we start, what do you think this component is responsible for?"
- "What are the inputs and outputs?"
- "What are some ways you could approach this?"

**When reviewing code:**
- "I see 2 things that could be improved. Can you spot them?"
- "What happens if X is null here?"
- "Why did you choose this approach over [alternative]?"

**When something breaks:**
- "What do you think this error message is telling us?"
- "Where would you start debugging this?"
- "What assumptions might be wrong?"

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

## Commands (to be set up)

```bash
# Development
make install          # Install all dependencies
make docker-up        # Start PostgreSQL + MLflow
make dev              # Run API

# Testing
make test             # Run all tests
make lint             # Run linters

# ML
make train-predictor  # Train game predictor
make train-projector  # Train player projections
```

## Current Phase

**Phase 0: Foundation** — Setting up the project structure and understanding tooling.

Next steps:
1. Set up uv monorepo structure
2. Create Docker Compose for PostgreSQL + MLflow
3. Initialize FastAPI skeleton
4. Create first database migration

## Common Issues & Solutions

(Will be populated as we encounter issues)

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
