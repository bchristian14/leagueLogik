# Agent Usage Guide

## How to Use the Agent System

### 1. **Agent Invocation Pattern**

Agents are invoked using Claude Code's Task tool with this pattern:

```typescript
Task tool with:
- subagent_type: "general-purpose"
- description: "[Agent Type]: [Brief task description]"
- prompt: "[Complete agent prompt from template]"
```

### 2. **Step-by-Step Agent Usage**

#### Step 1: Choose the Right Agent
- Review `/docs/agents/registry.md` to find the appropriate agent
- Check dependencies to ensure prerequisites are met
- Verify the agent fits the current workflow position

#### Step 2: Prepare Agent Context
- Gather all required context (existing code, requirements, patterns)
- Read the agent definition in `/docs/agents/core/[agent_name].md`
- Use the agent's task prompt template

#### Step 3: Invoke the Agent
```markdown
**Agent**: [Agent Name from registry]
**Context**: [Project state and background]
**Task**: [Specific deliverable with clear boundaries]
**Existing Patterns**: [Reference to similar implementations]
**Technical Constraints**: [Technology requirements]
**Dependencies**: [Required files and prerequisites]
**Deliverables**: [Exactly what should be returned]
**Quality Criteria**: [Success measures]
**Integration Points**: [Connections to other components]
```

#### Step 4: Validate Output
- Check deliverables against quality criteria
- Verify integration points are ready
- Run validation checklist from agent definition
- Confirm handoff requirements are met

#### Step 5: Coordinate Next Steps
- Update agent registry usage statistics
- Invoke next agent in workflow sequence
- Document any lessons learned or pattern updates

### 3. **Practical Example: T111 (PostgreSQL Setup)**

For our next task T111, here's how to use the Database Agent:

#### Context Preparation
```markdown
Current State:
- Fresh project with basic FastAPI structure
- No database models or migrations yet
- Poetry environment configured
- Need to establish PostgreSQL connection and Alembic setup

Business Requirements:
- User authentication system
- Member management with financial transactions
- Course and round scheduling
- Score tracking and results
```

#### Agent Invocation
```markdown
**Agent**: Database Agent
**Context**: LeagueLogik Golf League Management System - Initial database setup phase

**Current Database State**: No database models exist yet. Need initial setup.
**Business Requirements**: Establish PostgreSQL connection, configure Alembic, create base model patterns
**Existing Patterns**: None yet - this establishes the patterns

**Task**: T111 - PostgreSQL Setup and Configuration
- Create database connection configuration
- Set up Alembic migration system
- Establish base model patterns (UUID, timestamps, soft deletes)
- Create initial database and test connection

**Technical Constraints**:
- Technology: PostgreSQL 15+, SQLAlchemy 2.x, Alembic migrations
- Location: Database config in `/backend/app/database.py`, models in `/backend/app/models/`
- Environment: Use environment variables for database connection
- Development: Local PostgreSQL instance for development

**Dependencies**: Poetry environment configured, PostgreSQL installed locally

**Deliverables**:
- [ ] Database connection configuration in `/backend/app/database.py`
- [ ] Alembic configuration and initial migration
- [ ] Base model class with UUID, timestamps, soft delete patterns
- [ ] Environment variable configuration for database connection
- [ ] Database creation and connection testing
- [ ] Documentation for database setup process

**Quality Criteria**:
- [ ] Database connection works in development environment
- [ ] Alembic migrations functional (upgrade/downgrade)
- [ ] Base patterns established for future models
- [ ] Environment variables properly configured
- [ ] No hardcoded connection strings

**Integration Points**: Foundation for all future database models and API endpoints
```

### 4. **Agent Coordination Example**

For Feature F110 (Database Foundation), the workflow would be:

```markdown
1. Architecture Agent: Review T111 requirements and resolve ambiguities → Output: Clear, validated requirements
2. Database Agent (T111): PostgreSQL Setup → Output: Working database connection
3. Database Agent (T112): Users Table → Output: User model and migration
4. Database Agent (T113): Admin User Seeding → Output: Seeding functionality
5. Code Review Agent: Review all database work → Output: Quality validated code
6. Ready for API Agent (F120)
```

### 5. **Quality Gates**

Each agent has specific quality gates that must be passed:

- **Database Agent**: Migration scripts work, relationships valid, patterns consistent
- **Code Review Agent**: Code quality, pattern adherence, best practices
- **Architecture Agent**: Design alignment, scalability, dependency management

### 6. **Troubleshooting**

#### Common Issues:
- **Missing Context**: Agent doesn't have enough information → Provide more detailed context
- **Unclear Requirements**: Agent produces wrong output → Refine task description and deliverables
- **Integration Problems**: Agent output doesn't fit → Review integration points and handoff requirements

#### Best Practices:
- Always provide existing code patterns as references
- Be specific about deliverables and quality criteria
- Include integration points so agent knows how their work fits
- Validate output before proceeding to next agent

---

*This guide ensures consistent, high-quality agent usage throughout the development process.*