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

## Development Roadmap Integration

**CRITICAL: Always check current roadmap status before starting work**
- Primary roadmap: `/docs/development_roadmap.md`
- Current phase tracking in roadmap header
- Use Plan Re-evaluation template before major changes: `/docs/templates/plan_reevaluation.md`

**Before any development task:**
1. **Check Current Phase**: Review roadmap to identify current phase (P###) and status
2. **Identify Next Task**: Follow sequential task numbering (T###) within current phase
3. **Follow Success Criteria**: Each task has specific success criteria that must be met
4. **Update Progress**: Mark tasks complete in roadmap and update phase status
5. **Validate Dependencies**: Ensure prerequisite tasks/phases are complete before proceeding

**Task Numbering System:**
- Major Phases: P100, P200, P300... (insert P150 for new phase between P100-P200)
- Features: F110, F120, F130... (insert F115 for new feature between F110-F120)
- Tasks: T111, T112, T113... (insert T111.5 for new task between T111-T112)

**Never skip phases or tasks** - the roadmap ensures proper dependency management and systematic progress.

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
npm run test:watch                      # Run tests in watch mode
npm run test:coverage                   # Run tests with coverage report
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

**Streamlined 8-Step Process for Task Execution:**

### Step 1: Foundation Check
**Purpose**: Ensure prerequisites are met before starting implementation
- Use `architecture-validator` agent to validate dependencies and infrastructure
- Confirm required services, databases, and tooling are available
- User engagement if blockers are found that require decisions
- **Output**: Clear go/no-go decision to proceed with implementation

### Step 2: Implementation with Testing
**Purpose**: Build the feature with comprehensive automated validation
- Use domain-specific agents: `fastapi-backend-specialist`, `frontend-react-specialist`, `database-architect`
- Implement production code following established patterns
- Write automated tests during implementation (TDD where beneficial)
- Ensure proper test coverage for business logic and API contracts
- **Output**: Working feature with passing automated tests

### Step 3: Code Review
**Purpose**: Ensure consistency with established patterns and quality standards
- Use `code-reviewer` agent to validate implementation
- Check adherence to project conventions and coding standards
- Verify security best practices and performance considerations
- Identify any deviations from established patterns
- **Output**: Validated code ready for user exploration

### Step 4: User Exploration
**Purpose**: Real-world validation through direct user interaction
- User explores the implemented feature directly (no demos)
- Test feature functionality in realistic scenarios
- Identify any usability issues or missing requirements
- **Output**: User feedback on functionality and experience

### Step 5: Iterative Fixes (if needed)
**Purpose**: Address any issues discovered during user exploration
- Use same domain-specific agents to implement fixes
- Update tests to reflect any changes
- Re-run code review for significant changes
- **Output**: Refined feature addressing user feedback

### Step 6: Documentation Updates
**Purpose**: Keep documentation current with minimal overhead
- Update only what changed (avoid unnecessary documentation churn)
- Prefer auto-generated API docs and inline component documentation
- Update architectural decisions if significant patterns changed
- **Output**: Current, minimal documentation

### Step 7: Roadmap Update
**Purpose**: Track completion and maintain project visibility
- Mark task as complete in development roadmap
- Update phase status if all tasks in a phase are done
- Note any new tasks discovered during implementation
- **Output**: Updated project tracking

### Step 8: Commit and Push (when requested)
**Purpose**: Persist changes with clear history
- Create descriptive commit messages following project standards
- Push changes to remote repository if requested
- **Output**: Code changes safely persisted

## Test-Driven Development (TDD) Guidelines

**Use TDD for:**
- Business logic (handicap calculations, scoring algorithms, balance calculations)
- API endpoints with clear input/output contracts
- Complex data transformations
- Financial transaction processing

**TDD Process:**
1. Write failing test that describes expected behavior
2. Implement minimal code to pass the test
3. Refactor with confidence knowing tests will catch regressions
4. Repeat for each piece of functionality

**Testing Strategy:**
- **Unit Tests**: Business logic, utility functions, data models
- **Integration Tests**: API endpoints, database operations
- **Component Tests**: React components, user interactions
- **Coverage Goal**: >90% for business logic, >80% overall

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

## Role-Based Access Control

For implementing endpoint permissions and role-based access patterns, see:
**Documentation**: `/docs/architecture/role_based_access_patterns.md`

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