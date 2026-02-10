# Sports Studio — Tickets

**Last Updated:** 2026-02-06

This document tracks all implementation tickets. Each ticket includes learning objectives and uses TDD where applicable.

---

## Phase 0: Foundation (Weeks 1-2)

### Ticket #1: Project Structure & uv Workspace Setup
**Status:** COMPLETE
**Completed:** 2026-02-06
**Estimated Time:** 2-3 hours

**Learning Objectives:**
- Understand what a monorepo is and why we use one
- Learn how `uv` workspaces differ from pip/poetry
- Understand pyproject.toml structure

**Description:**
Set up the monorepo structure with uv workspaces. Create the base directory structure and configure package dependencies.

**Acceptance Criteria:**
- [x] Root `pyproject.toml` with workspace configuration
- [x] `packages/core/` with its own `pyproject.toml`
- [x] `packages/api/` with dependency on `core`
- [x] `uv sync` successfully installs all packages
- [x] Can import `core` from `api` package
- [x] `.gitignore` configured properly

**Key Learnings:**
- Monorepos enable atomic commits and shared code without publishing packages
- uv workspaces: `members` defines packages, `sources` tells uv where to find them
- Python packaging requires nested structure: `packages/core/core/` (package dir vs importable module)
- `[build-system]` with hatchling is required for packages to be installable
- Lock files (uv.lock) should be committed for reproducibility

**Discussion Points:**
- Why separate packages instead of one big package?
- What's the difference between a workspace dependency and a regular dependency?
- How does uv resolve version conflicts?

---

### Ticket #2: Docker Compose for Local Development
**Status:** COMPLETE
**Completed:** 2026-02-06
**Estimated Time:** 2-3 hours
**Depends On:** #1

**Learning Objectives:**
- Understand Docker images vs containers
- Learn docker-compose for multi-service apps
- Understand volumes for data persistence

**Description:**
Create Docker Compose configuration to run PostgreSQL and MLflow locally.

**Acceptance Criteria:**
- [x] `docker-compose.yml` in `infrastructure/docker/`
- [x] PostgreSQL 16 container with persistent volume
- [x] MLflow container accessible at localhost:5001 (changed from 5000 due to AirPlay conflict)
- [x] `make docker-up` and `make docker-down` commands work
- [x] Data persists across container restarts
- [x] `.env.example` with required variables

**Key Learnings:**
- Images = blueprints (like classes), Containers = running instances (like objects)
- Volumes persist data outside containers - critical for databases
- Port mapping: `host:container` format (e.g., `5001:5000`)
- macOS AirPlay uses port 5000 - common conflict for developers
- PostgreSQL only creates users from env vars on FIRST initialization (empty data dir)
- Use `docker compose down -v` to remove volumes and start fresh
- Makefiles require TAB characters (not spaces) for indentation
- `.PHONY` declares targets that aren't actual files

---

### Ticket #3: FastAPI Skeleton with Health Check
**Status:** COMPLETE
**Completed:** 2026-02-06
**Estimated Time:** 2-3 hours
**Depends On:** #1

**Learning Objectives:**
- Understand FastAPI application factory pattern
- Learn about routers and how to organize endpoints
- Understand dependency injection basics

**Description:**
Create the basic FastAPI application structure with a health check endpoint.

**Acceptance Criteria:**
- [x] `packages/api/api/main.py` with app factory
- [x] `/api/v1/health` endpoint returns `{"status": "healthy"}`
- [x] OpenAPI docs available at `/docs`
- [x] `make dev` runs the API at localhost:8000
- [x] Tests for health endpoint (TDD: write test first!)

**TDD Approach:**
1. Write test: `test_health_returns_200()`
2. Run test (should fail)
3. Implement endpoint
4. Run test (should pass)

**Key Learnings:**
- App factory pattern: create app inside a function to control instantiation timing (critical for testing with different configs)
- TDD workflow: Red (failing test) → Green (make it pass) → Refactor
- TestClient from starlette.testclient lets you test endpoints without running a real server
- uv dependency groups: dev dependencies go in `[dependency-groups]` section
- Uvicorn `--factory` flag tells it that the import path points to a factory function, not an app instance
- pytest auto-discovers test functions starting with `test_` — no main block needed

**Discussion Points:**
- Why use an app factory instead of a global `app` object?
- What is a router and why separate endpoints into routers?
- What does "dependency injection" mean?

---

### Ticket #4: Database Connection & First Migration
**Status:** COMPLETE
**Completed:** 2026-02-07
**Estimated Time:** 3-4 hours
**Depends On:** #2, #3

**Learning Objectives:**
- Understand SQLAlchemy engine and session management
- Learn Alembic migrations and why they matter
- Understand connection pooling basics

**Description:**
Set up SQLAlchemy connection to PostgreSQL and create the first migration (users table).

**Acceptance Criteria:**
- [x] `packages/core/core/db/connection.py` with engine setup
- [x] `packages/core/core/db/models.py` with User model
- [x] Alembic initialized with first migration
- [x] `make migrate` applies migrations
- [x] Can create a user in the database via Python
- [x] Tests for database connection

**TDD Approach:**
1. Write test: `test_can_create_user()`
2. Implement User model and connection
3. Create migration
4. Test passes

**Key Learnings:**
- **Fail-Fast with Clear Errors**: Add null checks with clear error messages (e.g., `raise ValueError("DATABASE_URL not set")`). Don't let bad state propagate deep into library code.
- **Configuration from Environment (12-Factor App)**: Load DATABASE_URL from `.env`, never hardcode credentials. Same code should be deployable anywhere.
- **Schema as Code (Database Migrations)**: Alembic tracks schema changes in versioned files. Database structure should be version-controlled like code. Never make manual schema changes.
- **Separation of Concerns**: Engine (connection pool, created once) vs Session (unit of work, per-request). Different responsibilities belong in different components.
- **Idempotency / Test Cleanup**: Tests should delete what they create so they can run repeatedly. Operations should be repeatable.
- **Import Order Matters**: Load environment variables (`load_dotenv()`) before importing modules that read from environment at import time.
- **Workspace Dev Dependencies**: In uv workspaces, shared dev tools like pytest should go in root `pyproject.toml` to be available across all packages.

**Discussion Points:**
- What is a database migration? Why not just `CREATE TABLE` manually?
- What is a session? Why not just use the engine directly?
- What happens if two requests try to use the same connection?

---

### Ticket #5: Makefile & Developer Experience
**Status:** COMPLETE
**Completed:** 2026-02-07
**Estimated Time:** 1-2 hours
**Depends On:** #1, #2, #3

**Learning Objectives:**
- Understand why developer experience matters
- Learn Makefile basics for task automation

**Description:**
Create a Makefile with common development commands.

**Acceptance Criteria:**
- [ ] `make install` - Install all dependencies
- [ ] `make dev` - Run API server
- [ ] `make docker-up` / `make docker-down` - Manage containers
- [ ] `make migrate` - Apply database migrations
- [ ] `make test` - Run all tests
- [ ] `make lint` - Run linters (ruff)
- [ ] `make help` - Show available commands

**Key Learnings:**
- **Convention Over Configuration**: Standard targets (`make dev`, `make test`) work across projects - devs don't need to learn new commands
- **Single Source of Truth / DRY**: `## description` comments live next to targets - one place to update
- **Self-Documenting Systems**: `make help` uses grep/awk to extract docs automatically
- **Defensive Defaults**: `.PHONY` protects against file name conflicts (e.g., a file named `test` would break `make test`)
- **Safe Defaults**: `help` as the default target - running `make` alone is informative, not destructive
- Makefiles provide reproducibility, discoverability, and fast onboarding

**Discussion Points:**
- Why use a Makefile instead of just documenting commands?
- What makes good developer experience?

---

## Phase 1: Data Layer (Weeks 3-4)

### Ticket #6: NBA API Data Loader with Caching
**Status:** COMPLETE
**Completed:** 2026-02-10
**Estimated Time:** 4-5 hours
**Depends On:** #4

**Learning Objectives:**
- Understand API rate limiting and why it matters
- Learn caching strategies (TTL, cache invalidation)
- Understand error handling for external APIs

**Description:**
Create a data loader that fetches NBA data with rate limiting and disk caching.

**Acceptance Criteria:**
- [ ] `packages/core/core/utils/data_loader.py` with NBADataLoader class
- [ ] Rate limiting: max 1 request per second
- [ ] Disk cache with 24-hour TTL (using `diskcache`)
- [ ] Methods: `get_games(season)`, `get_player_stats(season)`
- [ ] Graceful error handling when API fails
- [ ] Tests with mocked API responses

**TDD Approach:**
1. Write test: `test_caches_response()`
2. Write test: `test_respects_rate_limit()`
3. Implement data loader
4. Tests pass

**Key Learnings:**
- **Mocking External APIs**: Use `patch()` and `side_effect` to fake API calls in tests
- **Exception Translation**: Catch low-level exceptions (Exception), raise high-level custom exceptions (NBADataLoaderError)
- **Dependency Injection**: Pass cache into class instead of creating internally - enables testing with temp directories
- **TDD Workflow**: Red (failing test) → Green (make it pass) → Refactor
- **Testing Time-Based Features**: Use short TTL (seconds) in tests vs production (24 hours)
- **Rate Limiting Pattern**: Check elapsed time BEFORE request, sleep remaining time if needed, update timestamp AFTER request
- **Endpoint Selection**: Choose bulk endpoints (LeagueDashPlayerStats) over per-item endpoints to minimize API calls

**Discussion Points:**
- Why cache API responses? What are the tradeoffs of TTL length?
- What happens if the NBA API is down? How should we handle it?
- Why use disk cache instead of in-memory cache?

---

### Ticket #7: Database Schema - Players & Games
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #4

**Learning Objectives:**
- Understand database normalization (1NF, 2NF, 3NF)
- Learn about primary keys, foreign keys, and indexes
- Understand when to denormalize

**Description:**
Design and implement the core database schema for players and games.

**Acceptance Criteria:**
- [ ] `players` table with proper constraints
- [ ] `games` table with home/away teams
- [ ] `player_game_stats` table with foreign keys
- [ ] Appropriate indexes for common queries
- [ ] Alembic migration for all tables
- [ ] SQLAlchemy models with relationships

**Schema Design Session:**
Before implementing, we'll discuss:
- Why separate `players` and `player_game_stats`?
- Should `team` be a separate table or a string column?
- What indexes do we need and why?

**Discussion Points:**
- What is normalization? When is it bad?
- Why use foreign keys instead of just storing IDs?
- How do you decide what to index?

---

### Ticket #8: Data Ingestion Service
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** #6, #7

**Learning Objectives:**
- Understand ETL (Extract, Transform, Load) patterns
- Learn Pydantic validation for data pipelines
- Understand idempotent operations

**Description:**
Create a service that ingests NBA data into the database with validation.

**Acceptance Criteria:**
- [ ] `packages/core/core/services/ingestion_service.py`
- [ ] Pydantic schemas for validating incoming data
- [ ] Upsert logic (insert or update existing records)
- [ ] CLI command: `python -m core.cli.ingest --seasons 2023-24,2024-25`
- [ ] Progress logging during ingestion
- [ ] Tests for validation and upsert logic

**TDD Approach:**
1. Write test: `test_validates_player_data()`
2. Write test: `test_upserts_existing_player()`
3. Implement service
4. Tests pass

**Discussion Points:**
- What is idempotency? Why does it matter for data pipelines?
- Where should validation happen - at API level, service level, or database level?
- How do you handle partial failures (some records succeed, some fail)?

---

### Ticket #9: Data Layer Unit Tests
**Status:** Not Started
**Estimated Time:** 2-3 hours
**Depends On:** #6, #7, #8

**Learning Objectives:**
- Understand test fixtures and factories
- Learn database testing patterns (transactions, rollback)
- Understand mocking external services

**Description:**
Comprehensive test suite for the data layer.

**Acceptance Criteria:**
- [ ] Pytest fixtures for database sessions
- [ ] Factory functions for test data
- [ ] Tests use transactions that rollback (clean state)
- [ ] All data loader methods tested with mocked API
- [ ] All ingestion service methods tested
- [ ] >80% code coverage for data layer

**Discussion Points:**
- Why rollback transactions in tests?
- When should you mock vs use real services?
- What makes a good test fixture?

---

## Phase 2: Game Predictor ML (Weeks 5-7)

### Ticket #10: Feature Engineering - Core Features
**Status:** Not Started
**Estimated Time:** 5-6 hours
**Depends On:** #8

**Learning Objectives:**
- Understand what makes a good ML feature
- Learn about feature leakage and how to avoid it
- Understand feature transformations (scaling, encoding)

**Description:**
Build the initial 8-10 core features for game prediction.

**Core Features to Implement:**
1. `home_team_win_pct_last_10` - Recent form
2. `away_team_win_pct_last_10` - Recent form
3. `home_team_net_rating` - Offensive rating - Defensive rating
4. `away_team_net_rating` - Offensive rating - Defensive rating
5. `home_team_rest_days` - Days since last game
6. `away_team_rest_days` - Days since last game
7. `home_team_streak` - Current win/loss streak
8. `away_team_streak` - Current win/loss streak
9. `is_back_to_back_home` - Playing consecutive days
10. `is_back_to_back_away` - Playing consecutive days

**Acceptance Criteria:**
- [ ] `packages/game-predictor/game_predictor/features/team_features.py`
- [ ] Each feature has unit tests
- [ ] Features computed without data leakage
- [ ] Notebook exploring feature distributions
- [ ] Documentation explaining each feature

**Discussion Points:**
- What is feature leakage? Why is it dangerous?
- Why use "last 10 games" instead of season average?
- How do we handle the start of a season when there's no history?

---

### Ticket #11: Train/Test Split for Time Series
**Status:** Not Started
**Estimated Time:** 2-3 hours
**Depends On:** #10

**Learning Objectives:**
- Understand why random splits are wrong for time series
- Learn temporal train/validation/test splits
- Understand walk-forward validation

**Description:**
Implement proper temporal splitting for training data.

**Acceptance Criteria:**
- [ ] `packages/game-predictor/game_predictor/training/splitter.py`
- [ ] Train on seasons 2022-23, 2023-24
- [ ] Validate on first half of 2024-25
- [ ] Test on second half of 2024-25
- [ ] No future data leakage in any split
- [ ] Tests verify temporal ordering

**Discussion Points:**
- Why can't we randomly shuffle games for train/test?
- What is walk-forward validation?
- How much data do we need for training vs testing?

---

### Ticket #12: XGBoost Model Training
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** #10, #11

**Learning Objectives:**
- Understand gradient boosting conceptually
- Learn key XGBoost hyperparameters
- Understand binary classification setup

**Description:**
Train the initial XGBoost game prediction model.

**Acceptance Criteria:**
- [ ] `packages/game-predictor/game_predictor/models/xgboost_model.py`
- [ ] Training script: `scripts/train_game_predictor.py`
- [ ] Model achieves >60% accuracy on validation set
- [ ] Hyperparameters documented and justified
- [ ] Model saved to `models/game_predictor/`
- [ ] Training notebook with analysis

**Key Hyperparameters to Discuss:**
- `n_estimators` - Number of trees
- `max_depth` - Tree depth
- `learning_rate` - Step size
- `subsample` - Row sampling

**Discussion Points:**
- What is gradient boosting at a high level?
- Why does max_depth matter? What happens if too high/low?
- How do we know if we're overfitting?

---

### Ticket #13: Model Evaluation & Metrics
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #12

**Learning Objectives:**
- Understand classification metrics (accuracy, AUC, Brier score)
- Learn about calibration and why it matters
- Understand baseline comparisons

**Description:**
Comprehensive model evaluation with multiple metrics.

**Acceptance Criteria:**
- [ ] Accuracy, AUC-ROC, and Brier score computed
- [ ] Comparison to baseline (always predict home team)
- [ ] Confusion matrix visualization
- [ ] Calibration plot (predicted probability vs actual)
- [ ] Evaluation notebook with insights
- [ ] Model exceeds baseline by >5%

**Discussion Points:**
- Why isn't accuracy enough? When does it mislead?
- What does AUC-ROC actually measure?
- What is a Brier score? Why care about calibration?

---

### Ticket #14: SHAP Explainability
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** #12

**Learning Objectives:**
- Understand SHAP values conceptually
- Learn to interpret feature importance
- Understand local vs global explanations

**Description:**
Add SHAP explainability with dual display modes.

**Acceptance Criteria:**
- [ ] `packages/game-predictor/game_predictor/models/explainer.py`
- [ ] Technical mode: raw SHAP values for each feature
- [ ] Human mode: plain English explanations
- [ ] SHAP waterfall plot generation
- [ ] Tests for explainer
- [ ] Notebook demonstrating SHAP on sample predictions

**Discussion Points:**
- What does a SHAP value actually mean?
- How is SHAP different from feature importance?
- Why have two display modes?

---

### Ticket #15: MLflow Experiment Tracking
**Status:** Not Started
**Estimated Time:** 2-3 hours
**Depends On:** #12

**Learning Objectives:**
- Understand why experiment tracking matters
- Learn MLflow concepts (experiments, runs, artifacts)
- Understand model versioning

**Description:**
Set up MLflow for tracking experiments and registering models.

**Acceptance Criteria:**
- [ ] MLflow experiments created for game predictor
- [ ] Training logs parameters, metrics, and artifacts
- [ ] Model registered in MLflow model registry
- [ ] Can load model from registry for inference
- [ ] MLflow UI accessible at localhost:5000

**Discussion Points:**
- Why track experiments instead of just saving the final model?
- What should you log? What's overkill?
- How do you decide which model version to deploy?

---

## Phase 3: Draft Optimizer (Weeks 8-10)

### Ticket #16: Fantasy Scoring System
**Status:** Not Started
**Estimated Time:** 2-3 hours
**Depends On:** #7

**Learning Objectives:**
- Understand fantasy sports scoring
- Learn to translate business rules into code
- Understand configuration-driven design

**Description:**
Implement the 9-category fantasy scoring system.

**Acceptance Criteria:**
- [ ] `packages/draft-optimizer/draft_optimizer/scoring.py`
- [ ] 9-cat scoring formula implemented
- [ ] Configurable scoring weights
- [ ] Fantasy points calculated for historical games
- [ ] Tests with known expected values

**9-Cat Scoring:**
```python
fantasy_points = (
    points * 1.0 +
    rebounds * 1.2 +
    assists * 1.5 +
    steals * 3.0 +
    blocks * 3.0 +
    turnovers * -1.0 +
    (fg_pct_bonus) +
    (ft_pct_bonus) +
    (three_made * 0.5)
)
```

**Discussion Points:**
- Why are steals/blocks weighted higher than points?
- How do percentage-based stats (FG%, FT%) affect scoring?
- How would you make scoring configurable for different leagues?

---

### Ticket #17: Player Projection Features
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** #16

**Learning Objectives:**
- Understand regression vs classification features
- Learn rolling statistics and momentum features
- Understand player-level vs team-level features

**Description:**
Build features for player projection model.

**Core Features:**
1. `avg_fantasy_points_last_5` - Recent performance
2. `avg_fantasy_points_last_10` - Medium-term performance
3. `season_fantasy_avg` - Season baseline
4. `minutes_avg` - Playing time
5. `usage_rate` - Ball handling share
6. `opponent_def_rating` - Matchup difficulty
7. `is_home` - Home/away
8. `days_rest` - Recovery time

**Acceptance Criteria:**
- [ ] `packages/draft-optimizer/draft_optimizer/features/player_features.py`
- [ ] Each feature tested
- [ ] Features computed without leakage
- [ ] Notebook exploring feature correlations

**Discussion Points:**
- Why is projecting player stats harder than game outcomes?
- What features capture "momentum" or "hot streaks"?
- How do we handle players who change teams mid-season?

---

### Ticket #18: Player Projection Model (XGBoost Regression)
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** #17

**Learning Objectives:**
- Understand regression vs classification
- Learn regression metrics (MAE, RMSE, R²)
- Understand multi-output regression

**Description:**
Train XGBoost regression model for player projections.

**Acceptance Criteria:**
- [ ] `packages/draft-optimizer/draft_optimizer/models/projection_model.py`
- [ ] Model predicts fantasy points per game
- [ ] MAE < 5.0 on validation set
- [ ] Training script with MLflow logging
- [ ] Comparison to simple baseline (season average)

**Discussion Points:**
- How is regression loss different from classification loss?
- What's the difference between MAE and RMSE? When prefer each?
- Why might a simple average be a strong baseline?

---

### Ticket #19: Linear Programming Optimizer (PuLP)
**Status:** Not Started
**Estimated Time:** 5-6 hours
**Depends On:** #18

**Learning Objectives:**
- Understand linear programming fundamentals
- Learn objective functions and constraints
- Understand feasibility and optimality

**Description:**
Build the roster optimization engine using PuLP.

**Constraints:**
- Budget: $200 total
- Roster size: 10 players
- Position requirements: 1-3 per position (PG, SG, SF, PF, C)

**Acceptance Criteria:**
- [ ] `packages/draft-optimizer/draft_optimizer/models/optimizer.py`
- [ ] AuctionOptimizer class with configurable constraints
- [ ] Solves in <500ms for 300 players
- [ ] Returns optimal roster with total cost and projected points
- [ ] Handles infeasible cases gracefully
- [ ] Tests for constraint satisfaction

**Discussion Points:**
- What makes a problem "linear"?
- What happens when constraints conflict (infeasible)?
- How do you add a new constraint?

---

### Ticket #20: Draft Optimizer Backtesting
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #19

**Learning Objectives:**
- Understand backtesting for optimization
- Learn to evaluate optimizer quality
- Understand simulation vs reality

**Description:**
Build a backtesting framework to evaluate optimizer performance.

**Acceptance Criteria:**
- [ ] `packages/draft-optimizer/draft_optimizer/backtesting.py`
- [ ] Simulate drafts using historical projections
- [ ] Compare optimized rosters to random drafts
- [ ] Measure: % of weeks in top 20% of possible lineups
- [ ] Report with visualizations

**Discussion Points:**
- What assumptions does backtesting make?
- How might real drafts differ from simulated ones?
- What would make the optimizer fail in practice?

---

## Phase 4: API & Backend (Weeks 11-12)

### Ticket #21: Prediction API Endpoints
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #14

**Learning Objectives:**
- Understand RESTful API design
- Learn request/response schemas with Pydantic
- Understand API versioning

**Description:**
Build API endpoints for game predictions.

**Endpoints:**
- `GET /api/v1/predictions/upcoming` - Predictions for upcoming games
- `GET /api/v1/predictions/game/{game_id}` - Single game prediction
- `GET /api/v1/predictions/game/{game_id}?include_shap=true` - With SHAP values

**Acceptance Criteria:**
- [ ] `packages/api/api/routers/predictions.py`
- [ ] Pydantic schemas for requests and responses
- [ ] Proper HTTP status codes (200, 404, 500)
- [ ] OpenAPI documentation generated
- [ ] Integration tests for all endpoints

**Discussion Points:**
- What makes an API "RESTful"?
- When would you use query params vs path params?
- How do you handle errors gracefully?

---

### Ticket #22: Draft Optimizer API Endpoints
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #19

**Learning Objectives:**
- Understand stateful vs stateless APIs
- Learn session management patterns
- Understand request validation

**Description:**
Build API endpoints for draft optimization.

**Endpoints:**
- `POST /api/v1/draft/optimize` - Get optimal roster
- `GET /api/v1/draft/players` - List available players with projections

**Acceptance Criteria:**
- [ ] `packages/api/api/routers/draft.py`
- [ ] Request schema with budget, constraints
- [ ] Response includes roster and reasoning
- [ ] Validation errors return helpful messages
- [ ] Integration tests

**Discussion Points:**
- Should optimization be sync or async? Why?
- How do you validate complex nested requests?
- What if optimization takes too long?

---

### Ticket #23: Google OAuth Authentication
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** #3

**Learning Objectives:**
- Understand OAuth 2.0 flow
- Learn JWT tokens and sessions
- Understand security considerations

**Description:**
Implement Google OAuth for user authentication.

**Acceptance Criteria:**
- [ ] `packages/api/api/auth/oauth.py`
- [ ] `packages/api/api/auth/jwt.py`
- [ ] `/api/v1/auth/google` - Initiate OAuth flow
- [ ] `/api/v1/auth/callback` - Handle OAuth callback
- [ ] `/api/v1/auth/me` - Get current user
- [ ] JWT stored in httpOnly cookie
- [ ] Protected endpoints require auth

**Discussion Points:**
- Why OAuth instead of username/password?
- What is a JWT? What goes inside it?
- Why httpOnly cookies instead of localStorage?

---

### Ticket #24: Streaming Endpoint for Reports
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #21

**Learning Objectives:**
- Understand Server-Sent Events (SSE)
- Learn streaming response patterns
- Understand when SSE vs WebSockets

**Description:**
Build streaming endpoint for scouting reports.

**Endpoint:**
- `GET /api/v1/reports/game/{game_id}/preview` - Stream report chunks

**Acceptance Criteria:**
- [ ] `packages/api/api/routers/reports.py`
- [ ] SSE format: `data: chunk\n\n`
- [ ] Final message: `data: [DONE]\n\n`
- [ ] Works with EventSource in browser
- [ ] Tests for streaming behavior

**Discussion Points:**
- What's the difference between SSE and WebSockets?
- When would you choose one over the other?
- How do you handle connection drops?

---

## Phase 5: LLM Integration (Week 13)

### Ticket #25: Gemini Client with Streaming
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #24

**Learning Objectives:**
- Understand LLM API patterns
- Learn async streaming
- Understand rate limiting for external APIs

**Description:**
Build Gemini API client with streaming support.

**Acceptance Criteria:**
- [ ] `packages/scouting-reports/scouting_reports/services/gemini_client.py`
- [ ] Async streaming generation
- [ ] Rate limiting (15 requests/minute for free tier)
- [ ] Error handling for API failures
- [ ] Tests with mocked responses

**Discussion Points:**
- How does streaming differ from batch generation?
- How do you handle rate limits gracefully?
- What happens if Gemini returns an error mid-stream?

---

### Ticket #26: Scouting Report Prompts
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #25

**Learning Objectives:**
- Understand prompt engineering
- Learn to structure data for LLMs
- Understand prompt iteration

**Description:**
Design and implement prompts for game preview reports.

**Acceptance Criteria:**
- [ ] `packages/scouting-reports/scouting_reports/prompts/game_preview.py`
- [ ] Prompt template with placeholders for game data
- [ ] SHAP factors formatted for LLM consumption
- [ ] Output is engaging sports journalism style
- [ ] Multiple prompt variations for A/B testing

**Discussion Points:**
- What makes a good prompt? How do you iterate?
- How much context should you give the LLM?
- How do you ensure consistent output format?

---

### Ticket #27: Report Generation Service
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #25, #26

**Learning Objectives:**
- Understand service orchestration
- Learn caching strategies for generated content
- Understand async generators in Python

**Description:**
Orchestrate report generation with caching.

**Acceptance Criteria:**
- [ ] `packages/scouting-reports/scouting_reports/services/report_service.py`
- [ ] Fetches prediction and SHAP data
- [ ] Builds prompt and streams response
- [ ] Caches generated reports (12-hour TTL)
- [ ] Serves cached reports instantly
- [ ] Tests for caching behavior

**Discussion Points:**
- When should you cache LLM responses? When not?
- How do you invalidate cache when data changes?
- What's the tradeoff of longer cache TTL?

---

## Phase 6: Frontend & Polish (Weeks 14-15)

### Ticket #28: React Project Setup
**Status:** Not Started
**Estimated Time:** 2-3 hours
**Depends On:** #21

**Learning Objectives:**
- Understand Vite and modern React setup
- Learn project structure patterns
- Understand TypeScript configuration

**Description:**
Set up React frontend with TypeScript, Tailwind, and shadcn/ui.

**Acceptance Criteria:**
- [ ] `apps/web/` with Vite + React + TypeScript
- [ ] Tailwind CSS configured
- [ ] shadcn/ui components installed
- [ ] Dark mode support
- [ ] API client setup with fetch

**Discussion Points:**
- Why Vite instead of Create React App?
- What is shadcn/ui and why use it?
- How does dark mode work with CSS variables?

---

### Ticket #29: Game Prediction UI Components
**Status:** Not Started
**Estimated Time:** 5-6 hours
**Depends On:** #28

**Learning Objectives:**
- Understand React component composition
- Learn TanStack Query for data fetching
- Understand state management patterns

**Description:**
Build UI components for game predictions.

**Components:**
- `MatchupCard` - Display two teams
- `PredictionDisplay` - Show prediction with probability
- `ShapWaterfall` - Technical SHAP visualization
- `ShapSimple` - Human-readable factors

**Acceptance Criteria:**
- [ ] Components in `apps/web/src/components/GamePredictor/`
- [ ] TanStack Query for data fetching
- [ ] Loading and error states
- [ ] Toggle between technical/simple SHAP views
- [ ] Responsive design

**Discussion Points:**
- How do you decide component boundaries?
- What state goes in components vs global?
- How does TanStack Query simplify data fetching?

---

### Ticket #30: Streaming Report UI
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** #27, #28

**Learning Objectives:**
- Understand EventSource in React
- Learn streaming text effects
- Understand custom hooks

**Description:**
Build streaming text component for scouting reports.

**Acceptance Criteria:**
- [ ] `apps/web/src/hooks/useStreamingReport.ts`
- [ ] `apps/web/src/components/ScoutingReport/StreamingText.tsx`
- [ ] Typewriter effect as text streams
- [ ] Loading state while waiting for first chunk
- [ ] Error handling for connection issues

**Discussion Points:**
- How do you handle EventSource in React?
- What state do you need for streaming?
- How do you clean up EventSource on unmount?

---

### Ticket #31: Draft Optimizer UI
**Status:** Not Started
**Estimated Time:** 5-6 hours
**Depends On:** #22, #28

**Learning Objectives:**
- Understand complex form state
- Learn data table patterns
- Understand optimistic updates

**Description:**
Build UI for draft optimization.

**Components:**
- `PlayerTable` - Sortable, filterable player list
- `BudgetSlider` - Adjust budget constraint
- `RosterBuilder` - Selected players display
- `OptimalLineup` - Optimization results

**Acceptance Criteria:**
- [ ] Components in `apps/web/src/components/DraftOptimizer/`
- [ ] Player table with sorting and filtering
- [ ] Budget and constraint controls
- [ ] Submit for optimization
- [ ] Display optimal roster

---

### Ticket #32: Authentication UI
**Status:** Not Started
**Estimated Time:** 3-4 hours
**Depends On:** #23, #28

**Learning Objectives:**
- Understand OAuth flow from frontend
- Learn auth state management
- Understand protected routes

**Description:**
Build authentication flow in React.

**Acceptance Criteria:**
- [ ] `apps/web/src/hooks/useAuth.ts`
- [ ] Google sign-in button
- [ ] Auth state persistence
- [ ] Protected route wrapper
- [ ] User menu with logout

---

### Ticket #33: Admin Dashboard
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** #29, #31

**Learning Objectives:**
- Understand admin UI patterns
- Learn data visualization basics
- Understand monitoring concepts

**Description:**
Build admin dashboard for model monitoring.

**Components:**
- `ModelMetrics` - Accuracy over time
- `DataFreshness` - Last data update
- `PredictionStats` - Prediction distribution

**Acceptance Criteria:**
- [ ] Components in `apps/web/src/components/Admin/`
- [ ] Charts for key metrics
- [ ] Real-time data updates
- [ ] Admin-only access

---

### Ticket #34: End-to-End Testing
**Status:** Not Started
**Estimated Time:** 4-5 hours
**Depends On:** All previous tickets

**Learning Objectives:**
- Understand E2E testing vs unit testing
- Learn Playwright basics
- Understand test reliability

**Description:**
Set up end-to-end tests for critical flows.

**Critical Flows:**
1. View game predictions
2. Generate scouting report
3. Run draft optimization
4. Login/logout

**Acceptance Criteria:**
- [ ] Playwright configured
- [ ] Tests for all critical flows
- [ ] Tests run in CI
- [ ] Screenshots on failure

---

### Ticket #35: Documentation & README
**Status:** Not Started
**Estimated Time:** 2-3 hours
**Depends On:** All previous tickets

**Learning Objectives:**
- Understand good documentation practices
- Learn README conventions
- Understand documentation as code

**Description:**
Write comprehensive project documentation.

**Acceptance Criteria:**
- [ ] README with project overview
- [ ] Setup instructions
- [ ] API documentation
- [ ] Architecture diagram
- [ ] Learning journal summary

---

## Summary

| Phase | Tickets | Estimated Hours |
|-------|---------|-----------------|
| Phase 0: Foundation | #1-5 | 10-15 hours |
| Phase 1: Data Layer | #6-9 | 13-17 hours |
| Phase 2: Game Predictor | #10-15 | 20-26 hours |
| Phase 3: Draft Optimizer | #16-20 | 18-23 hours |
| Phase 4: API & Backend | #21-24 | 13-17 hours |
| Phase 5: LLM Integration | #25-27 | 9-12 hours |
| Phase 6: Frontend | #28-35 | 29-37 hours |
| **Total** | **35 tickets** | **112-147 hours** |

At ~10 hours/week, this is approximately 11-15 weeks of work, fitting the 3-4 month timeline.

---

*Each ticket is designed to be completed in 1-2 sessions with learning discussions.*
