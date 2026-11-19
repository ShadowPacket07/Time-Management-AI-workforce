
# AI Workforce - Project Rules

## 1. Project Mission
Build an autonomous AI Workforce specialized in personal time management.

The system must:
- Collect and understand the user's schedule, tasks, deadlines, goals, and availability.
- Analyze information and generate feasible schedules.
- Detect scheduling conflicts and automatically resolve them when permitted.
- Track task progress and update schedules.
- Coordinate multiple AI agents without requiring the user to relay information.
- Ask the user only when a situation is outside established rules or cannot be safely resolved.

## 2. Technology Stack
- Python 3.14 (64-bit)
- LangGraph for workflow orchestration.
- Pydantic for data validation.
- SQLAlchemy and SQLite for initial data storage.
- python-dotenv for environment configuration.
- pytest for automated testing.
- Gemini API for information extraction.
- OpenAI API for schedule planning.
- Claude API for independent review.
- Google Calendar API for calendar synchronization.

Do not downgrade Python unless a confirmed compatibility issue makes it necessary.

## 3. AI Agent Responsibilities
- Gemini Agent: Extract and normalize information from user documents.
- Planner Agent (OpenAI): Generate schedules based on user rules and constraints.
- Reviewer Agent (Claude): Independently evaluate schedule quality and feasibility.
- Python Orchestrator: Coordinate agents, manage state, retries, and workflow execution.

Never allow an AI agent to bypass deterministic validation.

## 4. Autonomy Rules

The system may automatically:
- Schedule flexible tasks.
- Move flexible study sessions.
- Adjust the duration of unstarted flexible tasks.
- Resolve scheduling conflicts within user-defined rules.
- Create and update system-owned calendar events.

The system must never automatically:
- Change fixed university classes.
- Delete calendar events not owned by this system.
- Remove important deadlines.
- Guess critical missing information.
- Violate user-defined working hours or rest constraints.
- Perform actions outside granted permissions.

Ask the user only when:
- Important rules conflict.
- Critical information is missing or ambiguous.
- No feasible schedule can be generated.
- An action is outside the system's authorization.

## 5. Reliability and Error Handling
- Validate all structured data with Pydantic.
- Use deterministic Python logic for time calculations and conflict detection.
- Limit automatic planning retries to 3 attempts.
- Avoid infinite loops.
- Log important operations and errors.
- Never log API keys or sensitive credentials.
- Preserve operation history.
- Do not silently ignore validation errors.

## 6. Architecture Rules
- Keep AI integrations separate from business logic.
- Keep orchestration separate from individual agents.
- Keep database operations separate from scheduling logic.
- Use modular, maintainable code.
- Add type hints to Python functions.
- Use clear and consistent naming.
- Write tests for important business rules.

## 7. Security Rules
- Store API keys in environment variables.
- Never hardcode secrets.
- Never commit .env to Git.
- Provide .env.example containing placeholder values only.
- Request only the permissions necessary for each integration.

## 8. Development Rules
- Build incrementally, one phase at a time.
- Do not implement future phases prematurely.
- Do not install unnecessary dependencies.
- Do not create fake integrations or claim an integration works before testing it.
- Run relevant tests after modifying important code.
- Explain significant architectural decisions.
- Report errors and unresolved issues honestly.

## 9. Initial Development Scope
Current phase: Foundation only.

Focus on:
- Project structure.
- Environment configuration.
- Application settings.
- Scheduling rules configuration.
- Database foundation.
- Initial validation and tests.
- Documentation.

Do not connect Gemini, OpenAI, Claude, or Google Calendar APIs yet.

Do not build a frontend yet.
