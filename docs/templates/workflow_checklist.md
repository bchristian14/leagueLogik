# Streamlined Development Workflow Checklist

## Task: [Task Name]

### Step 1: Foundation Check ✅
**Agent**: `architecture-validator`
- [ ] Dependencies validated (infrastructure, services, tooling)
- [ ] No blockers preventing implementation
- [ ] **Decision**: GO / NO-GO to proceed

### Step 2: Implementation with Testing ✅
**Agent**: Domain-specific (`fastapi-backend-specialist`, `frontend-react-specialist`, `database-architect`)
- [ ] Production code implemented following established patterns
- [ ] Automated tests written (TDD where beneficial for business logic)
- [ ] All tests passing with adequate coverage
- [ ] **Output**: Working feature with comprehensive test validation

### Step 3: Code Review ✅
**Agent**: `code-reviewer`
- [ ] Code patterns and conventions validated
- [ ] Security and performance considerations reviewed
- [ ] Adherence to project standards confirmed
- [ ] **Output**: Code approved for user exploration

### Step 4: User Exploration 👤
**User Action**: Direct feature testing (no demos)
- [ ] Feature explored directly by user in realistic scenarios
- [ ] Usability and functionality validated
- [ ] User feedback collected
- [ ] **Decision**: ACCEPT / NEEDS_FIXES

### Step 5: Iterative Fixes (if needed) 🔄
**Agent**: Same domain-specific agent + code review for significant changes
- [ ] User feedback addressed
- [ ] Tests updated to reflect changes
- [ ] Code re-reviewed if significant modifications made
- [ ] **Return to Step 4** until user accepts

### Step 6: Documentation Updates 📝
**Minimal, targeted updates only**
- [ ] Changed functionality documented (prefer auto-generated API docs)
- [ ] Inline component documentation updated
- [ ] Architectural decisions recorded if patterns changed

### Step 7: Roadmap Update 📊
**Project tracking maintenance**
- [ ] Task marked complete in development roadmap
- [ ] Phase status updated if all tasks in phase completed
- [ ] New tasks noted if discovered during implementation

### Step 8: Commit and Push (when requested) 💾
**Version control**
- [ ] Descriptive commit message following project standards
- [ ] Changes pushed to remote repository if requested

---

## Quality Gates (MANDATORY)

### Automated Testing
- [ ] **Unit tests**: Business logic and utility functions (>90% coverage goal)
- [ ] **Integration tests**: API endpoints and database operations
- [ ] **Component tests**: React components and user interactions
- [ ] **All tests passing**: No failing tests allowed

### Code Quality (MANDATORY per CLAUDE.md)
- [ ] **Backend linting**: `poetry run black .` passed
- [ ] **Backend import sorting**: `poetry run isort .` passed
- [ ] **Backend type checking**: `poetry run mypy .` passed
- [ ] **Frontend linting**: `npm run lint` passed
- [ ] **Frontend type checking**: `npm run typecheck` passed

---

## Success Criteria
- [ ] All automated tests passing
- [ ] Code review approved with no pattern violations
- [ ] User exploration completed successfully
- [ ] Documentation current and minimal
- [ ] Changes committed if requested

**Task Status**: 🟢 COMPLETE | 🟡 IN-PROGRESS | 🔴 BLOCKED

---

## TDD Guidelines
**Use Test-Driven Development for:**
- Business logic (handicap calculations, scoring algorithms, balance calculations)
- API endpoints with clear input/output contracts
- Complex data transformations
- Financial transaction processing

**TDD Process:** Write failing test → Implement minimal code → Refactor → Repeat