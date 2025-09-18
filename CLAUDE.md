# CLAUDE.md - Golf League Management System

This file provides guidance to Claude Code when working with this repository.

## Project Overview

Golf League Management Web Application for a 100-member league designed to replace manual signup processes with automated online management. Built with FastAPI backend, React frontend, and PostgreSQL database.

**Key Context:** Solo development with GCP free tier deployment, methodical development approach with thorough testing and validation at each step.

## Architecture

**Technology Stack:**
- Backend: FastAPI (Python 3.11+), SQLAlchemy 2.x, PostgreSQL 15+, Alembic migrations
- Frontend: React 18+ with Vite, TypeScript, Tailwind CSS, Shadcn/ui components
- Development: Poetry (backend), npm (frontend), PostgreSQL on WSL2/Ubuntu
- Production: nginx reverse proxy, single GCP compute instance

## Development vs Production: API URL Handling

### Development (Current)
- Frontend dev server (Vite): `localhost:5173`
- Backend dev server: `localhost:8000`
- API calls: `localhost:5173` → `localhost:8000/api/v1`

### Production (Target)
- Single domain with nginx reverse proxy on GCP compute instance
- Static frontend served by nginx: `yourdomain.com`
- API proxied by nginx: `yourdomain.com/api/*` → FastAPI backend
- Database: PostgreSQL on same instance

## Development Commands - CRITICAL

**MANDATORY: ALWAYS start with directory awareness:**
```bash
pwd                     # Confirm current directory
ls -la                  # See current directory contents
# THEN proceed with intended commands
```

**ALWAYS verify servers aren't running before starting new ones:**
```bash
# Check for running processes
ps aux | grep uvicorn
ps aux | grep vite
# Kill if needed: kill -9 <PID>
```

**CRITICAL RULE: Never assume current working directory**
- Always check `pwd` before running commands
- Verify you're in the correct directory for the task
- Use absolute paths when uncertain

**Backend Commands (ALWAYS use Poetry in backend/ directory):**
```bash
cd backend
poetry install                           # Install dependencies
poetry run alembic upgrade head         # Run database migrations
poetry run uvicorn app.main:app --reload --host 0.0.0.0  # Start dev server
poetry run pytest                       # Run tests
poetry run black .                      # Code formatting
poetry run isort .                      # Import sorting
poetry run mypy .                       # Type checking

# NEVER use python directly - ALWAYS use `poetry run python`
# NEVER use pip - ALWAYS use `poetry add package_name`
```

**Frontend Commands (in frontend/ directory):**
```bash
cd frontend
npm install                              # Install dependencies
npm run dev -- --host 0.0.0.0          # Start dev server (with network access)
npm run build                           # Build for production (creates dist/)
npm run test                            # Run tests
npm run lint                            # ESLint
npm run typecheck                       # TypeScript checking
```

**Database Operations:**
```bash
cd backend
poetry run alembic revision --autogenerate -m "description"
poetry run alembic upgrade head
```

**CRITICAL: Port Management**
- Backend runs on port 8000
- Frontend runs on port 5173
- Always check for conflicts before starting servers
- Use --host 0.0.0.0 for network access (mobile testing)

## Development Workflow

### Step 1: Plan Re-evaluation (MANDATORY)
Before starting any task, re-evaluate the current plan:

```markdown
## Plan Re-evaluation: [Task Name]

### Current Plan Validation
- [ ] **Goal Alignment**: Does this task still align with overall project goals?
- [ ] **Dependency Changes**: Have dependencies changed since plan creation?
- [ ] **New Requirements**: Are there new requirements or insights from previous tasks?
- [ ] **Scope Appropriateness**: Does the scope need adjustment based on learning?
- [ ] **Technical Feasibility**: Technical constraints discovered that affect this task?
- [ ] **Timeline Realism**: Is the estimated timeline still realistic?

### Plan Updates Required
- [ ] **Task Scope**: Modifications needed?
- [ ] **Dependencies**: Added/removed/changed?
- [ ] **Timeline**: Adjustments needed?
- [ ] **Integration**: Changes to integration points?

### Updated Task Definition
[Revised task description if changes needed]

### Impact Assessment
- Affects other tasks: [list]
- Timeline impact: [estimated]
- Resource impact: [estimated]
```

### Step 2: Pre-Task Evaluation (MANDATORY)
After plan re-evaluation, create detailed task evaluation:

```markdown
## Task: [Task Name]

### Pre-Task Evaluation
- [ ] **Requirements Clarity**: Any ambiguity that must be clarified?
- [ ] **Architectural Impact**: New endpoints/components/database tables needed?
- [ ] **Dependencies**: What existing code will be modified?
- [ ] **Testing Strategy**: Unit tests + integration tests + user acceptance criteria
- [ ] **Success Criteria**: Specific, measurable outcomes

### Implementation Plan
1. Database changes (if any)
2. Backend API changes
3. Frontend component changes
4. Testing approach
5. Documentation updates

### Risk Assessment
- Breaking changes to existing functionality?
- Migration considerations?
- Dependencies on external services?
```

### Step 3: Implementation
Execute the task using the updated plan and evaluation.

### Step 4: Post-Task Validation (MANDATORY)
After completing any task, validate with this checklist:

```markdown
## Task Completion: [Task Name]

### Post-Task Validation
- [ ] **Components Affected**: List all new/modified files
- [ ] **Testing Completed**: Unit tests passing + manual testing done
- [ ] **Success Criteria Met**: All requirements satisfied
- [ ] **Documentation Updated**: API docs, component docs, README updates
- [ ] **Code Quality**: Lint/type checks passing
- [ ] **Database Migration**: Applied and tested if schema changes
- [ ] **No Breaking Changes**: Existing functionality preserved
- [ ] **Ready for Commit**: All validation complete

### Test Results
- Unit tests: [PASS/FAIL]
- Integration tests: [PASS/FAIL]
- Manual testing: [PASS/FAIL]
- Linting: [PASS/FAIL]
- Type checking: [PASS/FAIL]

### Next Steps
- Follow-up tasks identified?
- Documentation updates needed?
- Future enhancements noted?

### Plan Updates for Future Tasks
- [ ] **Lessons Learned**: What should inform future tasks?
- [ ] **Plan Adjustments**: Do subsequent tasks need updating?
- [ ] **New Dependencies**: Have new dependencies been created?
- [ ] **Timeline Impact**: Does this affect future task estimates?
```

## Subagent Usage Guidelines

### When to Use Subagents
- Complex multi-domain tasks (database + API + frontend)
- Large refactoring efforts across multiple files
- Specialized tasks requiring domain expertise
- Code review and validation

### Best Practices for Subagents
1. **Provide Complete Context**: Include existing patterns, file structures, conventions
2. **Sequential Dependencies**: Database → API → Frontend
3. **Specify Deliverables**: Exactly what should be returned
4. **Include Validation**: Testing requirements and success criteria
5. **Reference Documentation**: Point to existing examples and patterns

### Subagent Task Template
```markdown
**Context**: [Current project state, existing patterns]
**Task**: [Specific deliverable with clear boundaries]
**Dependencies**: [Required files, existing code to reference]
**Constraints**: [Technology choices, patterns to follow]
**Deliverables**: [Exactly what should be returned]
**Testing**: [How to validate the work]
```

## Project Structure

```
leagueLogik/
├── README.md                    # Project overview
├── CLAUDE.md                    # This guidance file
├── docs/                        # Documentation
│   ├── templates/              # Task and validation templates
│   ├── workflow/               # Development workflow docs
│   └── architecture/           # Technical architecture
├── backend/                     # FastAPI application
│   ├── app/                    # Application code
│   ├── alembic/                # Database migrations
│   ├── tests/                  # Backend tests
│   └── pyproject.toml          # Poetry configuration
├── frontend/                    # React application
│   ├── src/                    # Source code
│   ├── public/                 # Static assets
│   ├── tests/                  # Frontend tests
│   └── package.json            # npm configuration
├── deploy/                      # Deployment configuration
│   ├── nginx.conf              # nginx configuration
│   ├── systemd/                # systemd service files
│   └── scripts/                # Deployment scripts
└── .vscode/                     # VS Code configuration
```

## API Structure

```
/api/v1/
├── auth/                       # JWT authentication
├── users/                      # User management
├── seasons/                    # Season management
├── rounds/                     # Round scheduling
├── courses/                    # Course data
├── transactions/               # Financial transactions
├── scores/                     # Score entry and results
└── admin/                      # Administrative functions
```

## Database Design Principles

1. **Start Simple**: Core entities first, complexity later
2. **Referential Integrity**: Foreign keys and constraints
3. **Audit Trail**: Created/updated timestamps, user tracking
4. **Soft Deletes**: Preserve data integrity
5. **Performance**: Indexes on commonly queried fields

## Testing Requirements

### Backend Testing
- Unit tests for business logic
- Integration tests for API endpoints
- Database transaction testing
- Authentication/authorization testing

### Frontend Testing
- Component unit tests
- User interaction testing
- API integration testing
- Responsive design testing

### Manual Testing Checklist
- [ ] All forms validate correctly
- [ ] Authentication works (login/logout)
- [ ] Mobile responsive design
- [ ] Error handling displays properly
- [ ] Loading states work correctly

## Code Quality Standards

### Backend
- Type hints required for all functions
- Pydantic models for API validation
- SQLAlchemy models with proper relationships
- Error handling with appropriate HTTP status codes

### Frontend
- TypeScript strict mode enabled
- Component prop types defined
- Error boundaries for error handling
- Accessibility standards followed

## Commit Standards

### Commit Message Format
```
type: brief description

Detailed explanation of changes made.

Testing completed:
- Unit tests: PASS
- Integration tests: PASS
- Manual testing: PASS

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Commit Types
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance tasks

## Deployment Architecture

**Development Environment:**
- WSL2 Ubuntu
- Poetry for Python dependencies
- npm for frontend dependencies
- PostgreSQL local database
- Vite dev server for frontend
- uvicorn for backend

**Production Target:**
- GCP Compute Engine (micro instance - free tier)
- Single server architecture:
  - nginx reverse proxy (serves static files + API proxy)
  - FastAPI backend (systemd service)
  - PostgreSQL database (local instance)
  - React frontend (built static files in nginx)
- $0/month cost using free tier

**nginx Configuration Pattern:**
```nginx
# Static frontend files
location / {
    root /var/www/leaguelogik/dist;
    try_files $uri $uri/ /index.html;
}

# API proxy to FastAPI backend
location /api/ {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Security Guidelines

- JWT tokens with proper expiration
- Password hashing with bcrypt
- Input validation on all endpoints
- CORS configuration for production
- Environment variables for secrets
- No secrets in code or commits
- nginx security headers

## Performance Guidelines

- Database queries optimized with proper indexes
- API pagination for large datasets
- Frontend code splitting and lazy loading
- Image optimization and caching
- Minimize bundle sizes
- nginx gzip compression
- Static file caching

## Documentation Requirements

Each new feature must include:
- API endpoint documentation (automatically generated)
- Component documentation with props/usage
- Database schema updates documented
- README updates for new functionality
- CLAUDE.md updates for new patterns

## Common Pitfalls to Avoid

1. **Directory Confusion**: ALWAYS run `pwd` and `ls -la` before executing commands
2. **Command Errors**: Always use poetry run for Python commands
3. **Port Conflicts**: Check for running processes before starting servers
4. **Missing Migrations**: Run alembic upgrade after schema changes
5. **Authentication Issues**: Verify JWT tokens are properly configured
6. **API Endpoint Conflicts**: Check existing routes before adding new ones
7. **Database Transaction Issues**: Use proper session management
8. **Frontend State Management**: Follow established patterns for state updates
9. **Import/Export Issues**: Use consistent import patterns throughout codebase
10. **Production Build Issues**: Test npm run build before deployment
11. **nginx Configuration**: Ensure API paths match between frontend and nginx
12. **Assuming Working Directory**: Never assume where you are - always verify with pwd

## Emergency Debugging

### Backend Issues
```bash
cd backend
poetry run python -c "from app.database import engine; print(engine.url)"
poetry run alembic current
poetry run alembic history
```

### Frontend Issues
```bash
cd frontend
npm run build  # Check for build errors
npm run typecheck  # Check TypeScript issues
```

### Database Issues
```bash
# Connect to database directly
psql -U username -d database_name
# Check table structure
\dt
\d table_name
```

### Production Issues
```bash
# Check nginx status
sudo systemctl status nginx
sudo nginx -t  # Test configuration

# Check FastAPI service
sudo systemctl status leaguelogik-backend
sudo journalctl -u leaguelogik-backend -f  # Follow logs
```

This guidance ensures consistent, high-quality development with proper testing and validation at each step.