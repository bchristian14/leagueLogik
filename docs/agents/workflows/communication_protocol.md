# Agent Communication Protocol

## Overview

Agents communicate through structured documents and feedback loops, enabling iterative development and quality improvement.

## Communication Methods

### 1. **Forward Handoffs** (Agent A → Agent B)
**Purpose**: Pass validated work and context to next agent
**Mechanism**: Handoff documents in `/docs/agents/communication/handoffs/`
**Format**:
```markdown
# [Source Agent] to [Target Agent] Handoff

## Completed Work
- [List of deliverables]
- [Files created/modified]
- [Validation status]

## Context for Next Agent
- [Specific guidance]
- [Patterns to follow]
- [Integration requirements]

## Quality Validation
- [ ] All success criteria met
- [ ] Ready for next agent
- [ ] No blocking issues

## Next Agent Guidance
[Specific instructions and context for the receiving agent]
```

### 2. **Feedback Loops** (Agent B → Agent A)
**Purpose**: Request changes, report issues, or provide improvement suggestions
**Mechanism**: Feedback documents in `/docs/agents/communication/feedback/`
**Format**:
```markdown
# [Reviewing Agent] Feedback for [Implementation Agent]

## Issues Identified
### Critical Issues (Must Fix)
- [ ] Issue 1: [Description and impact]
- [ ] Issue 2: [Description and impact]

### Improvements (Should Fix)
- [ ] Improvement 1: [Description and benefit]
- [ ] Improvement 2: [Description and benefit]

### Suggestions (Could Fix)
- [ ] Suggestion 1: [Description]
- [ ] Suggestion 2: [Description]

## Specific Changes Requested
### File: [filename]
- **Problem**: [What's wrong]
- **Solution**: [What should be changed]
- **Rationale**: [Why this change is needed]

## Re-validation Requirements
After changes are made:
- [ ] [Specific validation step 1]
- [ ] [Specific validation step 2]

## Context Preserved
- Original requirements: [Link to original context]
- Previous iterations: [Links to previous feedback]
```

### 3. **Iteration Management**
**Purpose**: Track iteration cycles and prevent infinite loops
**Mechanism**: Iteration documents in `/docs/agents/communication/iterations/`
**Format**:
```markdown
# Task [T###] - Iteration [N]

## Iteration Summary
- **Trigger**: [What caused this iteration]
- **Agents Involved**: [Which agents participated]
- **Changes Made**: [Summary of changes]

## Previous Iteration Issues
- [Issues from previous iteration]
- [How they were addressed]

## Current Status
- **Completion**: [Percentage complete]
- **Blocking Issues**: [Any remaining blockers]
- **Next Steps**: [What happens next]

## Iteration Limit Check
- **Current Iteration**: [N]
- **Max Iterations**: 3 per task
- **Escalation Required**: [Yes/No - if approaching limit]
```

## Communication Workflows

### 1. **Successful Forward Flow**
```
Architecture Agent → Database Agent → API Agent → Code Review Agent → Testing Agent → Integration Agent
     ↓ handoff         ↓ handoff       ↓ handoff        ↓ handoff         ↓ handoff         ↓
   [handoff doc]    [handoff doc]   [handoff doc]    [handoff doc]     [handoff doc]   [complete]
```

### 2. **Feedback and Iteration Flow**
```
Database Agent → Code Review Agent
     ↓ handoff           ↓ finds issues
   [handoff doc]    [feedback doc] ← Creates feedback
     ↑ iteration         ↓
Database Agent ← [iteration doc] ← Human coordinates iteration
     ↓ fixes issues      ↓
   [updated work] → Code Review Agent (re-validation)
```

### 3. **Multi-Agent Feedback Flow**
```
Integration Agent finds issues affecting multiple agents:
     ↓
   [feedback doc] → Database Agent (schema issues)
     ↓
   [feedback doc] → API Agent (endpoint issues)
     ↓
   [feedback doc] → Frontend Agent (UI issues)
     ↓
   [iteration doc] → Coordinates parallel fixes
```

## Iteration Management Rules

### Maximum Iterations
- **Per Task**: 3 iterations maximum
- **Per Agent Pair**: 2 feedback cycles maximum
- **Escalation**: If limits exceeded, human intervention required

### Iteration Triggers
- Code Review Agent finds critical issues
- Testing Agent discovers functionality gaps
- Integration Agent identifies compatibility problems
- Security Agent finds security vulnerabilities

### Communication Responsibilities

#### Sending Agent (Implementation)
- Read all handoff context before starting
- Create complete handoff documentation
- Respond to feedback within iteration scope
- Update iteration tracking

#### Receiving Agent (Review/Quality)
- Validate handoff completeness before proceeding
- Provide specific, actionable feedback
- Re-validate after iterations
- Confirm quality gates before final approval

#### Human Coordinator (Claude)
- Monitor iteration counts
- Escalate when limits approached
- Coordinate multi-agent feedback cycles
- Maintain communication artifact hygiene

## Communication Templates

### Standard Handoff Template
```markdown
**From**: [Agent Name]
**To**: [Agent Name]
**Task**: [T### or F###]
**Iteration**: [Number]

**Deliverables Completed**:
- [List all files and functionality delivered]

**Quality Validation**:
- [All validation criteria met]

**Context for Next Agent**:
- [Specific patterns used]
- [Integration points prepared]
- [Special considerations]

**Ready for**: [Next agent work or specific validation]
```

### Standard Feedback Template
```markdown
**From**: [Reviewing Agent]
**To**: [Implementation Agent]
**Task**: [T### or F###]
**Issue Severity**: [Critical/Important/Suggestion]

**Issue**: [Clear description of problem]
**Impact**: [How this affects functionality/quality]
**Solution**: [Specific changes requested]
**Validation**: [How to verify fix]

**Files Affected**: [List of files needing changes]
**Integration Impact**: [Effect on other components]
```

## Benefits of This System

✅ **Iterative Quality**: Agents can improve work based on feedback
✅ **Context Preservation**: Communication history maintained
✅ **Controlled Iterations**: Limits prevent infinite loops
✅ **Specific Feedback**: Clear, actionable improvement requests
✅ **Multi-Agent Coordination**: Complex feedback scenarios handled
✅ **Audit Trail**: Complete record of decisions and changes

---

*This communication protocol enables robust, iterative agent collaboration while maintaining quality and preventing endless revision cycles.*