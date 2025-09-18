# Agent System Overview

The LeagueLogik agent system provides specialized, coordinated subagents for complex development tasks. Agents are implemented as structured prompt templates that use Claude Code's Task tool with the `general-purpose` subagent type.

## Agent Architecture

### Agent Components
1. **Agent Definition**: Specialized role, capabilities, and constraints
2. **Task Prompt Template**: Structured prompt format for consistent outputs
3. **Coordination Rules**: How the agent fits into workflows
4. **Validation Criteria**: Success measures and quality gates

### Agent Types

#### Core Production Agents
- **Database Agent**: Schema design, migrations, data modeling
- **API Agent**: FastAPI endpoints, business logic, validation
- **Frontend Agent**: React components, TypeScript interfaces, UI/UX
- **Code Review Agent**: Code quality, pattern consistency, best practices
- **Architecture Agent**: Design validation, dependency management, scalability
- **Security Agent**: Authentication, authorization, input validation, security best practices
- **Testing Agent**: Unit tests, integration tests, test automation
- **Integration Agent**: End-to-end feature coordination, cross-layer validation

#### Specialized Agents
- **Documentation Agent**: API docs, component docs, inline documentation
- **Performance Agent**: Optimization, profiling, performance analysis
- **Migration Agent**: Data migration, schema changes, refactoring

## Usage Patterns

### Feature-Level Workflow
```
Architecture Agent (requirement validation) → Database Agent → API Agent → Frontend Agent → Code Review Agent → Security Agent → Integration Agent → Testing Agent
```

### Task-Level Workflow with Feedback
```
Domain Agent → Code Review Agent → [Feedback Loop if needed] → Integration Ready
```

### Communication Pattern
```
Claude coordinates all agent communication through:
- Handoff documents (forward flow)
- Feedback documents (iteration requests)
- Iteration tracking (prevents infinite loops)
```

### Agent Invocation
```typescript
// Example agent invocation pattern
Task tool with:
- subagent_type: "general-purpose"
- description: "[Agent Type]: [Brief task description]"
- prompt: "[Agent-specific structured prompt from template]"
```

## Quality Gates

Each agent has specific quality criteria that must be met before handoff to the next agent in the workflow.

## Agent Registry

See `registry.md` for the complete list of available agents and their current status.

---

*This agent system ensures consistent, high-quality deliverables while maintaining the flexibility to adapt to project needs.*