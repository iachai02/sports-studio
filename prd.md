# Sports Studio — Product Requirements Document

**Version:** 1.0
**Last Updated:** 2026-02-06
**Status:** Learning Project — Active Development
**Goal:** Build a production-grade ML platform while deeply understanding every component

---

## Executive Summary

Sports Studio is a **learning-focused ML platform** for NBA analytics, built to understand end-to-end machine learning engineering through hands-on implementation. The project emphasizes understanding the **why** behind every decision, not just the **what**.

This project covers:
- **ML/Feature Engineering**: XGBoost models for player projections and game predictions
- **Mathematical Optimization**: Linear Programming for fantasy draft optimization
- **Explainable AI**: SHAP for model interpretability with dual technical/human-readable modes
- **LLM Integration**: Gemini API with streaming responses for scouting reports
- **Full-Stack Development**: FastAPI + React + PostgreSQL
- **MLOps**: Docker, MLflow, CI/CD pipelines

**Learning Philosophy:** Every step uses the Socratic method. Before implementing, you articulate your understanding. We discuss tradeoffs, inputs/outputs, and design patterns. Code is written by you, with guidance through questions.

---

## Learning Approach

### The Socratic Method

For every major component, we follow this cycle:

1. **Understand the problem** — What are we solving? What are the inputs and outputs?
2. **Explore tradeoffs** — What are the options? Why would we pick A over B?
3. **Design first** — Sketch the solution before writing code
4. **Implement** — You write the code with hints, not answers
5. **Review** — What did we learn? What would we do differently?

### What "Teaching Mode" Means

- I will ask you to explain your thinking FIRST before giving guidance
- I'll give hints like "there are 3 issues with this code" instead of fixing it for you
- When you're stuck, I'll ask guiding questions rather than provide solutions
- We'll discuss WHY certain patterns exist, not just how to use them

---

## Scope Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Sport** | NBA only | Faster iteration, focused learning |
| **Fantasy Format** | Yahoo/ESPN Standard (9-cat) | Most common, clear rules to learn |
| **Prediction Target** | Game winner | Clear evaluation, good for learning classification |
| **Differentiator** | LLM scouting reports | Leverages streaming, prompt engineering |
| **Training Data** | Last 3 seasons (~3,600 games) | Sufficient for learning without data overload |
| **Cost Constraint** | Free tier only | Gemini free, local Docker, no cloud costs |
| **Timeline** | 3-4 months | Learning-focused but with progress |
| **Data Source** | nba_api only | Accept flakiness, learn error handling |
| **Initial Features** | 8-10 core features | Learn deeply on fewer, add more later |
| **Testing** | TDD approach | Write tests first for better design |
| **Docker Depth** | Practical usage | Learn enough to use, not internals |
| **User Personas** | All three | Fantasy player, data analyst, casual fan |

## Teaching Workflow

Based on your preferences, we'll use a **Design + Real-time Guidance** approach:

1. **Design Phase**: Discuss architecture, pseudocode, and tradeoffs together
2. **Implementation Phase**: Work through code together with guiding questions
3. **Review Phase**: Reflect on what was learned, what could be better

For **frontend work**: Learn React patterns initially (state management, hooks, animations), then I can help write more of it once you're comfortable. We'll reference sports-intelligence-hub for UI patterns.

---

## Project Phases

The project is divided into **building blocks** that stack on each other. Each phase builds understanding before adding complexity.

### Phase 0: Foundation (Weeks 1-2)
**Goal:** Understand the tooling and project structure before writing any business logic.

**Learning Topics:**
- Why monorepos? What problems do they solve?
- What is `uv` and how does it differ from pip/poetry?
- Docker fundamentals: images, containers, volumes, networks
- PostgreSQL basics: schemas, tables, relationships
- FastAPI structure: routers, dependencies, middleware

**Deliverables:**
- [ ] Monorepo structure set up with `uv`
- [ ] Docker Compose running PostgreSQL + MLflow locally
- [ ] Basic FastAPI app with health check endpoint
- [ ] First database table created and migrated
- [ ] Understanding documented: "What I learned about X"

---

### Phase 1: Data Layer (Weeks 3-4)
**Goal:** Build a robust data pipeline that fetches, validates, and stores NBA data.

**Learning Topics:**
- API rate limiting and caching strategies
- Database schema design for sports data
- Data validation with Pydantic and Pandera
- SQLAlchemy ORM patterns vs raw SQL
- Why separation of concerns matters (services vs models vs routers)

**Key Questions to Answer:**
- Why do we cache API responses? What are the tradeoffs of TTL?
- How do we design tables to avoid data duplication?
- What's the difference between validation at the API level vs database level?
- Why use an ORM instead of raw SQL (or vice versa)?

**Deliverables:**
- [ ] NBA API integration with rate limiting and caching
- [ ] Database schema: players, games, player_game_stats
- [ ] Data loader service with validation
- [ ] Unit tests for data layer
- [ ] Documentation: schema decisions and why

---

### Phase 2: Game Predictor ML (Weeks 5-7)
**Goal:** Build a classification model to predict NBA game winners.

**Learning Topics:**
- Feature engineering: what makes a good feature?
- Train/validation/test splits for time series data
- XGBoost fundamentals: gradient boosting, hyperparameters
- Model evaluation: accuracy, AUC-ROC, calibration
- SHAP explainability: how does it work?

**Key Questions to Answer:**
- Why is random train/test split wrong for time-series prediction?
- What's the difference between leakage and valid features?
- How do we know our model is better than just guessing "home team wins"?
- What does a SHAP value actually mean?

**Deliverables:**
- [ ] Feature engineering pipeline with 20+ features
- [ ] Trained XGBoost model with >65% accuracy
- [ ] SHAP integration with dual display modes
- [ ] MLflow experiment tracking setup
- [ ] Model evaluation notebook with analysis

---

### Phase 3: Draft Optimizer (Weeks 8-10)
**Goal:** Build player projection model + linear programming optimization.

**Learning Topics:**
- Regression vs classification: different targets, different metrics
- Linear programming fundamentals: objective, constraints, feasibility
- Fantasy scoring systems and how to model them
- How to combine ML predictions with optimization

**Key Questions to Answer:**
- Why is projecting player stats harder than predicting game winners?
- What makes an optimization problem "linear"?
- How do constraints affect the solution space?
- What happens when the problem is infeasible?

**Deliverables:**
- [ ] Player projection model (XGBoost regression)
- [ ] PuLP-based roster optimizer
- [ ] Draft optimizer API endpoints
- [ ] Backtesting framework to evaluate optimizer
- [ ] Understanding document: LP concepts

---

### Phase 4: API & Backend (Weeks 11-12)
**Goal:** Build production-quality API with auth and streaming.

**Learning Topics:**
- REST API design principles
- Authentication: OAuth flows, JWT tokens
- Streaming responses: SSE vs WebSockets
- Error handling and validation patterns
- API documentation with OpenAPI

**Key Questions to Answer:**
- Why OAuth instead of username/password?
- When would you use SSE vs WebSockets?
- How do you version an API?
- What makes an API "RESTful"?

**Deliverables:**
- [ ] Full API with all endpoints
- [ ] Google OAuth authentication
- [ ] Streaming endpoint for reports
- [ ] OpenAPI documentation
- [ ] Integration tests

---

### Phase 5: LLM Integration (Week 13)
**Goal:** Generate scouting reports with Gemini streaming.

**Learning Topics:**
- LLM prompt engineering
- Streaming API patterns
- Rate limiting and cost management
- Caching strategies for generated content

**Key Questions to Answer:**
- What makes a good prompt? How do you iterate on prompts?
- How do you handle LLM rate limits gracefully?
- When should you cache LLM responses?

**Deliverables:**
- [ ] Gemini client with streaming
- [ ] Scouting report generation
- [ ] React streaming text component
- [ ] Caching layer for reports

---

### Phase 6: Frontend & Polish (Weeks 14-15)
**Goal:** Build the React frontend and finalize the project.

**Learning Topics:**
- React component architecture
- State management with TanStack Query
- Streaming data in React
- Responsive design with Tailwind

**Deliverables:**
- [ ] Full React application
- [ ] Admin dashboard
- [ ] Mobile responsive design
- [ ] End-to-end testing
- [ ] Project documentation

---

## Tech Stack

| Layer | Technology | Why This Choice |
|-------|------------|-----------------|
| **Package Manager** | uv | Fast, modern, handles workspaces well |
| **Backend** | FastAPI | Async, auto-docs, Pydantic integration |
| **Database** | PostgreSQL | Production-standard, rich features to learn |
| **ORM** | SQLAlchemy 2.0 | Industry standard, async support |
| **Migrations** | Alembic | Pairs with SQLAlchemy, handles schema changes |
| **ML** | XGBoost | Production-proven, excellent with tabular data |
| **Explainability** | SHAP | Industry standard for tree models |
| **Optimization** | PuLP | Simple API, good for learning LP |
| **LLM** | Gemini 1.5 Flash | Free tier, streaming support |
| **Frontend** | React + TypeScript | Industry standard, great ecosystem |
| **Styling** | Tailwind + shadcn/ui | Fast development, consistent design |
| **ML Tracking** | MLflow | Standard for experiment tracking |
| **Containers** | Docker Compose | Local dev, reproducibility |

---

## Directory Structure

```
sports-studio/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Lint, test, type-check
│       └── ml-pipeline.yml           # Model training triggers
│
├── packages/
│   ├── core/                         # Shared utilities & schemas
│   │   ├── core/
│   │   │   ├── schemas/              # Pydantic models
│   │   │   ├── db/                   # SQLAlchemy models, connection
│   │   │   ├── services/             # Business logic
│   │   │   └── utils/                # Data loading, caching
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   ├── game-predictor/               # Game winner prediction
│   │   ├── game_predictor/
│   │   │   ├── features/             # Feature engineering
│   │   │   ├── models/               # XGBoost, SHAP explainer
│   │   │   └── training/             # Pipeline, hyperopt
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   ├── draft-optimizer/              # Fantasy draft optimization
│   │   ├── draft_optimizer/
│   │   │   ├── features/             # Player features
│   │   │   ├── models/               # Projection model, LP solver
│   │   │   └── services/             # Optimizer service
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   ├── scouting-reports/             # LLM report generation
│   │   ├── scouting_reports/
│   │   │   ├── prompts/              # Prompt templates
│   │   │   └── services/             # Gemini client
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   └── api/                          # FastAPI backend
│       ├── api/
│       │   ├── routers/              # REST endpoints
│       │   ├── middleware/           # Logging, error handling
│       │   └── auth/                 # OAuth, JWT
│       ├── tests/
│       └── pyproject.toml
│
├── apps/
│   └── web/                          # React frontend
│       ├── src/
│       │   ├── components/           # UI components
│       │   ├── hooks/                # Custom hooks
│       │   └── lib/                  # API client, utils
│       ├── package.json
│       └── vite.config.ts
│
├── infrastructure/
│   └── docker/
│       ├── Dockerfile.api
│       ├── Dockerfile.ml
│       └── docker-compose.yml
│
├── notebooks/                        # Jupyter exploration
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_game_prediction.ipynb
│   └── 04_shap_explainability.ipynb
│
├── scripts/                          # CLI tools
│   ├── fetch_nba_data.py
│   ├── train_game_predictor.py
│   └── train_projections.py
│
├── data/
│   ├── raw/                          # Immutable source data
│   ├── processed/                    # Feature-engineered data
│   └── cache/                        # API response cache
│
├── mlflow/                           # Model registry
├── pyproject.toml                    # Root workspace config
├── uv.lock
├── Makefile
├── CLAUDE.md                         # Claude Code guidance
└── README.md
```

---

## Database Schema (Initial Design)

This will evolve as we build. We'll discuss each table design decision.

```sql
-- Core data tables
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    nba_player_id VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    team VARCHAR(50),
    position VARCHAR(10),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    nba_game_id VARCHAR(20) UNIQUE NOT NULL,
    season VARCHAR(10) NOT NULL,
    game_date DATE NOT NULL,
    home_team VARCHAR(50) NOT NULL,
    away_team VARCHAR(50) NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    winner VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE player_game_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    game_id INTEGER REFERENCES games(id),
    minutes FLOAT,
    points INTEGER,
    rebounds INTEGER,
    assists INTEGER,
    steals INTEGER,
    blocks INTEGER,
    turnovers INTEGER,
    fg_pct FLOAT,
    ft_pct FLOAT,
    three_pct FLOAT,
    UNIQUE(player_id, game_id)
);

-- ML & predictions
CREATE TABLE game_predictions (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    model_version VARCHAR(50) NOT NULL,
    predicted_winner VARCHAR(50) NOT NULL,
    win_probability FLOAT NOT NULL,
    shap_values JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Auth
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    oauth_provider VARCHAR(20) NOT NULL,
    oauth_id VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Evaluation Metrics

### Game Predictor
| Metric | Target | Baseline |
|--------|--------|----------|
| Accuracy | >65% | ~58% (home team always wins) |
| AUC-ROC | >0.70 | 0.50 (random) |
| Brier Score | <0.22 | 0.25 (home team bias) |

### Player Projections
| Metric | Target | What It Measures |
|--------|--------|------------------|
| MAE | <5.0 fantasy pts | Average prediction error |
| RMSE | <7.0 fantasy pts | Penalizes large misses |

### Optimizer
| Metric | Target | What It Measures |
|--------|--------|------------------|
| Runtime | <500ms | Speed for 300+ players |
| Backtest | Top 20% in >60% of weeks | Quality of optimized lineups |

---

## Success Criteria

By project completion:

- [ ] End-to-end pipeline: data → ML → API → frontend
- [ ] Game predictor with >65% accuracy
- [ ] SHAP explanations in dual modes
- [ ] Streaming scouting reports
- [ ] OAuth authentication working
- [ ] Docker Compose single-command deployment
- [ ] All tests passing
- [ ] **Most importantly:** Deep understanding of WHY each component works

---

## Learning Journal

Throughout the project, maintain notes on:

1. **Concepts learned** — What was new?
2. **Mistakes made** — What went wrong and why?
3. **Tradeoffs considered** — What alternatives existed?
4. **Questions to revisit** — What needs deeper understanding?

This becomes your portfolio documentation and interview prep material.

---

*This PRD establishes the learning-focused foundation for Sports Studio. Every phase will begin with understanding the problem before writing code.*
