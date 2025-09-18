# Agent Registry

*Last Updated: 2025-09-18*

This registry tracks all available agents, their status, and usage patterns.

## Core Production Agents

| Agent | Status | Purpose | Dependencies | Last Used |
|-------|--------|---------|--------------|-----------|
| Database Agent | ✅ Defined | Schema design, migrations, SQLAlchemy models | None | Not yet used |
| API Agent | ✅ Defined | FastAPI endpoints, business logic, Pydantic models | Database Agent | Not yet used |
| Frontend Agent | ✅ Defined | React components, TypeScript interfaces, UI/UX | API Agent | Not yet used |
| Code Review Agent | ✅ Defined | Code quality, pattern consistency, best practices | Any code-producing agent | Not yet used |
| Architecture Agent | ✅ Defined | Design validation, dependency management | None (guides others) | Not yet used |
| Security Agent | 🚧 Planned | Authentication, authorization, security best practices | All agents | Not defined |
| Testing Agent | 🚧 Planned | Unit tests, integration tests, test automation | Code-producing agents | Not defined |
| Integration Agent | 🚧 Planned | End-to-end coordination, cross-layer validation | All feature agents | Not defined |

## Specialized Agents

| Agent | Status | Purpose | Dependencies | Last Used |
|-------|--------|---------|--------------|-----------|
| Documentation Agent | 🚧 Planned | API docs, component docs, inline documentation | Conditional | Not defined |
| Performance Agent | 🚧 Planned | Optimization, profiling, performance analysis | Functional codebase | Not defined |
| Migration Agent | 🚧 Planned | Data migration, schema changes, refactoring | Database/API agents | Not defined |

## Agent Workflow Patterns

### Feature Development Workflow
```
P###: Phase Start
├── Architecture Agent (design validation)
├── F###.1: Database Agent → Code Review Agent
├── F###.2: API Agent → Code Review Agent
├── F###.3: Frontend Agent → Code Review Agent
├── Security Agent (cross-cutting review)
├── Integration Agent (end-to-end validation)
└── Testing Agent (comprehensive testing)
```

### Current Development Status
- **Active Phase**: P100 - Core Infrastructure & Authentication
- **Next Task**: T111 - PostgreSQL Setup and Configuration
- **Recommended Agent**: Database Agent
- **Workflow Position**: Starting F110 (Database Foundation)

## Usage Statistics

| Agent | Times Used | Success Rate | Average Task Duration | Notes |
|-------|------------|--------------|---------------------|-------|
| *No usage data yet* | - | - | - | System just established |

## Agent Coordination Rules

### Sequential Dependencies
1. **Architecture Agent** → All other agents (provides design guidance)
2. **Database Agent** → API Agent → Frontend Agent
3. **Code Review Agent** → After any code-producing agent
4. **Security Agent** → Cross-cutting, can run with any agent
5. **Integration Agent** → After all feature agents
6. **Testing Agent** → After integration

### Parallel Opportunities
- Database + API agents can work on different features simultaneously
- Code Review agent can review multiple outputs in parallel
- Security agent can review any completed work

### Quality Gates
- **Code Review Agent**: Required before integration
- **Security Agent**: Required for authentication/authorization tasks
- **Testing Agent**: Required before feature completion
- **Integration Agent**: Required before marking feature complete

---

## Modification Log

| Date | Change | Agent(s) Affected | Reason |
|------|--------|------------------|--------|
| 2025-09-18 | Initial registry creation | All | System establishment |

---

*This registry is automatically updated when agents are created, modified, or used.*