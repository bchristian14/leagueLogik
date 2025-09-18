# Agent Coordination Strategy

## Human-Coordinated Agent Communication

Since agents cannot directly communicate with each other, **Claude acts as the coordinator** managing agent communication through structured documents and workflows.

## Coordination Process

### 1. **Forward Flow Coordination**
```markdown
1. Claude invokes Architecture Agent
   ↓ receives output
2. Claude creates handoff document with Architecture Agent output
   ↓ provides context to next agent
3. Claude invokes Database Agent with handoff context
   ↓ receives output
4. Claude creates next handoff document
   ↓ continues workflow
```

### 2. **Feedback Flow Coordination**
```markdown
1. Claude invokes Code Review Agent with Database Agent output
   ↓ receives feedback/issues
2. If issues found:
   - Claude creates feedback document
   - Claude invokes Database Agent again with feedback context
   - Claude tracks iteration count
3. If no issues:
   - Claude creates handoff to next agent
   - Workflow continues
```

### 3. **Multi-Agent Feedback Coordination**
```markdown
1. Integration Agent finds issues affecting multiple agents
   ↓ Claude receives comprehensive feedback
2. Claude creates individual feedback documents for each affected agent
3. Claude coordinates parallel agent invocations to fix issues
4. Claude manages re-integration after all fixes complete
```

## Practical Example: T111 with Feedback Loop

### Initial Forward Flow
```markdown
Step 1: Architecture Agent Review
- Claude invokes Architecture Agent to review T111 requirements
- Output: Validated requirements and technical approach

Step 2: Database Agent Implementation
- Claude creates handoff document with Architecture Agent guidance
- Claude invokes Database Agent with clear requirements
- Output: PostgreSQL setup, models, migrations

Step 3: Code Review Agent Validation
- Claude invokes Code Review Agent with Database Agent output
- Code Review finds issues: "Missing error handling in database connection"
```

### Feedback Loop Handling
```markdown
Step 4: Feedback Communication
- Claude creates feedback document with specific issues
- Claude invokes Database Agent again with feedback context
- Database Agent fixes issues based on specific feedback

Step 5: Re-validation
- Claude invokes Code Review Agent again with updated output
- Code Review Agent validates fixes and approves
- Claude proceeds to next workflow step
```

## Communication Document Management

### Document Lifecycle
1. **Creation**: Claude creates communication documents as needed
2. **Population**: Agents receive context from documents
3. **Updates**: Claude updates documents with agent outputs
4. **Archival**: Completed documents preserved for reference

### Document Templates (for Claude to use)

#### Handoff Document Template
```markdown
# [Source Agent] to [Target Agent] Handoff - [Task ID]
*Created: [timestamp]*

## Previous Agent Output
[Complete output from previous agent]

## Context for Next Agent
**Task**: [Specific deliverable for target agent]
**Patterns to Follow**: [Reference to existing code/patterns]
**Quality Criteria**: [Success measures]
**Integration Points**: [How this connects to other components]

## Files to Reference
- [List of files the target agent should read]
- [List of patterns to follow]

## Previous Agent Notes
[Any specific guidance or context from previous agent]
```

#### Feedback Document Template
```markdown
# [Reviewer Agent] Feedback for [Implementation Agent] - [Task ID]
*Created: [timestamp]*

## Work Reviewed
[Description of what was reviewed]

## Issues Found
### Critical (Must Fix)
- **Issue**: [Description]
- **File**: [filename:line]
- **Solution**: [Specific fix needed]
- **Impact**: [Why this matters]

### Improvements (Should Fix)
- **Suggestion**: [Description]
- **Benefit**: [Why this would help]

## Validation Requirements
After fixes:
- [ ] [Specific validation step]
- [ ] [Re-run specific tests]

## Context for Implementation Agent
**Original Requirements**: [Link to original context]
**Patterns to Maintain**: [What should not change]
**Integration Constraints**: [What must be preserved]
```

## Iteration Management by Claude

### Iteration Tracking
Claude maintains iteration state and prevents infinite loops:

```markdown
Current Task: T111
Iteration Count: 2
Agents Involved: Database Agent ↔ Code Review Agent
Issues Remaining: 1 critical, 2 improvements
Max Iterations: 3
Status: Within limits, continue iteration
```

### Escalation Triggers
- **Max Iterations Reached**: 3 iterations per task
- **Conflicting Feedback**: Agents provide contradictory guidance
- **Scope Creep**: Feedback requests exceed task boundaries
- **Technical Blockers**: Issues require architectural changes

## Benefits of Human Coordination

✅ **Context Preservation**: Claude maintains full context across agent invocations
✅ **Quality Control**: Claude ensures feedback is actionable and appropriate
✅ **Workflow Management**: Claude manages complex multi-agent scenarios
✅ **Iteration Control**: Claude prevents infinite loops and manages escalation
✅ **Documentation**: Claude maintains complete audit trail
✅ **Efficiency**: Claude optimizes agent invocations and reduces redundant work

## Example Coordination Workflow

### Task T111: PostgreSQL Setup with Feedback Loop

```markdown
1. Claude: Invoke Architecture Agent for T111 review
   → Architecture Agent: Validates requirements, provides database setup guidance

2. Claude: Create handoff document with Architecture Agent output
   → Document contains: Technical approach, patterns to follow, success criteria

3. Claude: Invoke Database Agent with handoff context
   → Database Agent: Creates database setup, models, migrations

4. Claude: Invoke Code Review Agent with Database Agent output
   → Code Review Agent: Finds issues with error handling and connection patterns

5. Claude: Create feedback document with specific issues
   → Document contains: Specific files to fix, exact changes needed

6. Claude: Invoke Database Agent with feedback context (Iteration 2)
   → Database Agent: Fixes specific issues identified in feedback

7. Claude: Invoke Code Review Agent for re-validation
   → Code Review Agent: Validates fixes, approves quality

8. Claude: Create handoff to API Agent for next phase
   → Ready for F120 authentication implementation
```

This approach provides robust agent communication while leveraging Claude's ability to maintain context and coordinate complex workflows.

---

*This coordination strategy enables sophisticated agent collaboration through human-managed communication protocols.*