# Workflow Checklist Template

## Task: [Task Name]

### Step 1: Plan Re-evaluation  MANDATORY
- [ ] **Plan Re-evaluation Completed**: Used `/docs/templates/plan_reevaluation.md`
- [ ] **Goals still aligned**: Task still meets project objectives
- [ ] **Dependencies validated**: All dependencies still valid
- [ ] **Scope confirmed**: Task scope appropriate and realistic
- [ ] **Ready for evaluation**: Proceed to Pre-Task Evaluation

### Step 2: Pre-Task Evaluation  MANDATORY
- [ ] **Pre-Task Evaluation Completed**: Used `/docs/templates/pre_task_evaluation.md`
- [ ] **Requirements clarified**: All requirements clear and unambiguous
- [ ] **Implementation planned**: Detailed implementation approach defined
- [ ] **Testing strategy defined**: Clear testing approach established
- [ ] **Ready for implementation**: Proceed to Implementation

### Step 3: Implementation
- [ ] **Implementation started**: Development work begun
- [ ] **Code written**: Core functionality implemented
- [ ] **Tests written**: Unit and integration tests created
- [ ] **Manual testing**: Functionality manually verified
- [ ] **Ready for validation**: Proceed to Post-Task Validation

### Step 4: Post-Task Validation  MANDATORY
- [ ] **Post-Task Validation Completed**: Used `/docs/templates/post_task_validation.md`
- [ ] **Testing complete**: All tests passing
- [ ] **Code quality verified**: Linting and type checking passed
- [ ] **Documentation updated**: All docs updated appropriately
- [ ] **Roadmap updated**: Task marked complete in development roadmap
- [ ] **Ready for next task**: Task fully complete

## Additional Steps (As Appropriate)

### Architecture Review (For New Features/Significant Changes)
- [ ] **Architecture review completed**: Used `architecture-validator` agent
- [ ] **Design decisions validated**: Architecture choices confirmed
- [ ] **Integration points verified**: System integration validated

### Code Review (After Development)
- [ ] **Code review completed**: Used `code-reviewer` agent
- [ ] **Code quality confirmed**: Patterns and standards followed
- [ ] **Security verified**: No security issues identified

### Linting/Type Checking (MANDATORY per CLAUDE.md)
- [ ] **Backend linting**: `poetry run black .` passed
- [ ] **Backend import sorting**: `poetry run isort .` passed
- [ ] **Backend type checking**: `poetry run mypy .` passed
- [ ] **Frontend linting**: `npm run lint` passed
- [ ] **Frontend type checking**: `npm run typecheck` passed

### Commits (When Explicitly Requested)
- [ ] **Changes staged**: Relevant files added to git staging
- [ ] **Commit message drafted**: Following project commit standards
- [ ] **Commit created**: Changes committed with proper message

---

## Workflow Validation
- [ ] **All mandatory steps completed**: Steps 1, 2, and 4 done
- [ ] **All appropriate steps completed**: Additional steps as needed
- [ ] **Task fully validated**: Ready to proceed to next task
- [ ] **Documentation current**: All templates and roadmap updated

**Task Status:**  COMPLETE / ó IN-PROGRESS / L INCOMPLETE