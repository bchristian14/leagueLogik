# Golf League Management - Development Roadmap
*Version: 1.6 | Last Updated: 2025-09-19*

## Roadmap Structure & Modification Guide

This roadmap uses a flexible numbering system designed for easy modification:
- **Major Phases**: P100, P200, P300... (insert P150 for new phase between P100-P200)
- **Features**: F110, F120, F130... (insert F115 for new feature between F110-F120)
- **Tasks**: T111, T112, T113... (insert T111.5 for new task between T111-T112)

**To modify this roadmap:**
1. Use Plan Re-evaluation template for any changes
2. Update version number and last updated date
3. Add new items with appropriate numbering
4. Update dependencies in affected items
5. Commit changes with clear description

## Workflow Adherence

**Each task must follow the documented workflow from CLAUDE.md:**

Tasks include a **Workflow** section with mandatory steps:
- **Plan Re-evaluation** (mandatory) - Use `/docs/templates/plan_reevaluation.md`
- **Pre-Task Evaluation** (mandatory) - Use `/docs/templates/pre_task_evaluation.md`
- **Implementation** - Execute the development work
- **Code Review** (for significant features) - Use `code-reviewer` agent
- **Post-Task Validation** (mandatory) - Use `/docs/templates/post_task_validation.md`

**Workflow Templates Available:**
- `/docs/templates/plan_reevaluation.md` - Plan validation before starting
- `/docs/templates/pre_task_evaluation.md` - Detailed task planning
- `/docs/templates/post_task_validation.md` - Completion validation
- `/docs/templates/workflow_checklist.md` - Complete workflow tracking

**Do not mark tasks complete until all workflow steps are validated.**

---

## P000: Foundation Phase ✅ COMPLETE
**Status:** Complete | **Duration:** Setup phase
**Goal:** Establish development environment and workflow

### F010: Development Environment Setup ✅
- **Status:** Complete
- **Dependencies:** None
- **Deliverables:**
  - [x] T011: Project structure (backend/frontend separation)
  - [x] T012: Poetry + npm environment setup
  - [x] T013: CLAUDE.md with workflow guidelines
  - [x] T014: Documentation templates
  - [x] T015: Git repository initialization

---

## P100: Core Infrastructure & Authentication
**Status:** Planned | **Estimated Duration:** 1-2 weeks
**Goal:** Establish secure authentication and user management
**Dependencies:** P000 complete

### F110: Database Foundation
**Status:** Planned | **Priority:** Critical
**Goal:** Create database schema and user management system
**Dependencies:** None

#### T111: PostgreSQL Setup and Configuration ✅ COMPLETE
**Deliverable:** Functional database connection
- Create local development database
- Configure Alembic for migrations
- Establish database connection patterns
- Create environment configuration
**Success Criteria:**
- [x] PostgreSQL running locally
- [x] Alembic migrations functional
- [x] Database connection tested
- [x] Environment variables configured

#### T112: Users Table Implementation ✅ COMPLETE
**Deliverable:** Complete user data model
```sql
users table schema:
- member_id (primary key, UUID)
- email (unique, not null)
- password_hash (not null)
- first_name, last_name (not null)
- phone_number
- date_of_birth (optional; for forward & 75+ tee eligibility)
- member_status (active|inactive)
- member_type (candidate|full|lifetime)
- admin_roles (null|admin|treasurer|course_coordinator|tournament_coordinator)
- GHIN_id
- member_balance (decimal, default 0.00)
- signup_date (not null)
- AGA_membership_expiry
- created_at, updated_at (auto-managed)
```
**Success Criteria:**
- [x] Users table created with constraints
- [x] Model validation implemented
- [x] Database indexes optimized
- [x] Migration scripts tested

#### T113: Admin User Seeding ✅ COMPLETE
**Deliverable:** Initial admin account for testing
- Create database seeding functionality
- Generate secure initial admin user
- Verify admin account access
**Workflow:**
- [x] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [x] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [x] Implementation completed
- [x] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [x] Admin user created successfully
- [x] Admin login credentials functional
- [x] Admin permissions verified

---

### F120: Backend Authentication System
**Status:** Planned | **Priority:** Critical
**Goal:** Complete JWT authentication API
**Dependencies:** F110 complete

#### T121: JWT Authentication Endpoints ✅ COMPLETE
**Deliverable:** Working authentication API
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- POST /api/v1/auth/logout
- GET /api/v1/auth/me (current user info)
**Workflow:**
- [x] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [x] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [x] Implementation completed
- [x] Code Review completed (use `code-reviewer` agent)
- [x] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [x] Login returns valid JWT token
- [x] Token refresh working correctly
- [x] Logout invalidates tokens
- [x] User info endpoint secured

#### T122: Password Security Implementation ✅ COMPLETE
**Deliverable:** Secure password management
- bcrypt password hashing (12 rounds minimum)
- Password validation rules
- Password change functionality
- Account lockout after failed attempts
**Workflow:**
- [x] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [x] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [x] Implementation completed
- [x] Code Review completed (use `code-reviewer` agent)
- [x] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [x] Passwords properly hashed
- [x] Validation rules enforced
- [x] Password change working
- [x] Security measures active

#### T123: Core Role System Implementation ✅ COMPLETE
**Deliverable:** Flexible role-based permission foundation
- `get_user_roles(user)` function returning set of user's roles
- `require_roles(*roles)` dependency factory for endpoint protection
- Role inheritance logic (admin inherits all other roles)
- Core permission checking utilities
**Workflow:**
- [x] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [x] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [x] Implementation completed
- [x] Code Review completed (use `code-reviewer` agent)
- [x] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [x] `get_user_roles()` returns correct role sets for all user types
- [x] `require_roles()` dependency factory working for any role combination
- [x] Role inheritance logic functional (admin gets all permissions)
- [x] Comprehensive test coverage for all role scenarios

#### T123.5: Refactor Existing Auth Dependencies ✅ COMPLETE
**Deliverable:** Updated auth system using new role framework
- Replace `get_current_admin()` with role-based dependencies
- Update `User.is_admin` property to use new role system
- Apply new role system to existing auth endpoints
- Remove legacy boolean admin checking
**Workflow:**
- [x] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [x] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [x] Implementation completed
- [x] Code Review completed (use `code-reviewer` agent)
- [x] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [x] All existing endpoints using new role system
- [x] `get_current_admin()` replaced/removed
- [x] No legacy boolean admin logic remaining
- [x] All existing functionality preserved with enhanced role support

#### T123.7: Member Self-Access Patterns ✅ COMPLETE
**Deliverable:** Member data access control system
- [x] `require_member_self_or_admin(member_id)` dependency
- [x] Member accessing own data vs admin accessing any data logic
- [x] Permission utilities for member data access validation
- [x] Foundation ready for upcoming member management endpoints
**Workflow:**
- [x] Plan Re-evaluation completed (implemented directly)
- [x] Pre-Task Evaluation completed (implemented directly)
- [x] Implementation completed
- [x] Code Review completed (comprehensive testing validates implementation)
- [x] Post-Task Validation completed (all tests passing)
**Success Criteria:**
- [x] Member self-access pattern implemented and tested
- [x] Admin can access any member data, members only own data
- [x] Clear error messages for unauthorized access attempts
- [x] Ready for immediate use in T211 member CRUD endpoints

---

### F130: Frontend Authentication Interface
**Status:** Planned | **Priority:** High
**Goal:** User-friendly authentication interface
**Dependencies:** F120 complete

#### T131: Login Page Implementation ✅ COMPLETE
**Deliverable:** Professional login interface
- Responsive login form with validation
- Error handling and user feedback
- Loading states during authentication
- Password visibility toggle
**Workflow:**
- [x] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [x] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [x] Implementation completed
- [x] Code Review completed (use `code-reviewer` agent)
- [x] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [x] Login form functional and validated
- [x] Error messages clear and helpful
- [x] Loading states working
- [x] Mobile responsive design

#### T132: Authentication State Management
**Deliverable:** Persistent auth state
- React Query for authentication state
- Secure token storage strategy
- Auto-logout on token expiration
- Route protection implementation
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] Auth state persists on refresh
- [ ] Token expiration handled gracefully
- [ ] Protected routes working
- [ ] State management optimized

#### T132.5: Frontend Testing Framework Setup
**Deliverable:** Complete frontend testing infrastructure
- Configure Vitest as test runner for React/TypeScript
- Install and configure @testing-library/react for component testing
- Setup jsdom environment for DOM testing
- Configure test scripts in package.json (test, test:watch, test:coverage)
- Create test utilities and setup files
**Workflow:**
- [ ] Pre-Task Evaluation completed
- [ ] Implementation completed (use `frontend-react-specialist` agent)
- [ ] Post-Task Validation completed (coverage and test execution verified)
**Success Criteria:**
- [ ] Vitest running tests successfully
- [ ] @testing-library/react configured for component testing
- [ ] Test scripts working (npm run test, npm run test:watch)
- [ ] Coverage reporting functional with minimum 80% threshold
- [ ] Test utilities and setup files ready for use

#### T132.7: Backend Authentication API Tests
**Deliverable:** Comprehensive backend authentication test suite
- Unit tests for JWT token utilities (/app/utils/auth.py)
- Integration tests for authentication API endpoints (/app/api/v1/auth.py)
- Tests for API dependencies and role-based access (/app/api/dependencies.py)
- Password change and token refresh endpoint tests
- Account lockout and security feature tests
**Workflow:**
- [ ] Pre-Task Evaluation completed
- [ ] Implementation completed (use `fastapi-backend-specialist` agent)
- [ ] Post-Task Validation completed (coverage and test execution verified)
**Success Criteria:**
- [ ] >90% test coverage for authentication modules
- [ ] All authentication API endpoints tested (login, logout, refresh, me, change-password)
- [ ] JWT token lifecycle tests (creation, validation, expiration, refresh)
- [ ] Role-based access control tests for all permission patterns
- [ ] Security tests (account lockout, failed attempts, password validation)

#### T132.9: Frontend Authentication Tests
**Deliverable:** Complete frontend authentication test coverage
- Unit tests for useAuth hook (/frontend/src/hooks/useAuth.ts)
- Tests for token storage utilities (/frontend/src/lib/auth.ts)
- API client integration tests (/frontend/src/lib/api.ts)
- Component tests for LoginPage (/frontend/src/pages/LoginPage.tsx)
- Route protection tests (ProtectedRoute component)
**Workflow:**
- [ ] Pre-Task Evaluation completed
- [ ] Implementation completed (use `frontend-react-specialist` agent)
- [ ] Post-Task Validation completed (coverage and test execution verified)
**Success Criteria:**
- [ ] >85% test coverage for authentication modules
- [ ] useAuth hook tested (login, logout, state management, error handling)
- [ ] Token storage tested (get, set, remove, expiration validation)
- [ ] API client tested (token attachment, refresh interceptors, error mapping)
- [ ] LoginPage component tested (form validation, submission, error display)
- [ ] Route protection tested (authentication checks, role-based access, redirects)

#### T133: Admin Dashboard Shell
**Deliverable:** Basic admin interface
- Dashboard layout and navigation
- Placeholder sections for future features
- User profile display
- Logout functionality
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] Dashboard accessible after login
- [ ] Navigation structure clear
- [ ] User info displayed correctly
- [ ] Logout working properly

---

## P200: Member Management System
**Status:** Planned | **Estimated Duration:** 1-2 weeks
**Goal:** Complete member CRUD operations and management
**Dependencies:** P100 complete

### F210: Backend Member Management API
**Status:** Planned | **Priority:** High
**Goal:** Complete member management endpoints
**Dependencies:** F120 complete

#### T211: Member CRUD Endpoints
**Deliverable:** Full member API
- GET /api/v1/members (with filtering/pagination)
- POST /api/v1/members (admin creates member)
- PUT /api/v1/members/{id} (update member data)
- GET /api/v1/members/{id} (member details)
- DELETE /api/v1/members/{id} (soft delete)
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] All CRUD operations functional
- [ ] Filtering by status/type working
- [ ] Pagination implemented
- [ ] Admin permissions enforced

#### T212: Member Validation and Business Rules
**Deliverable:** Data integrity and business logic
- Email uniqueness validation
- GHIN ID format validation
- Member type progression rules
- Balance calculation logic
- Phone number formatting
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] All validation rules enforced
- [ ] Business logic implemented
- [ ] Error messages clear
- [ ] Data integrity maintained

---

### F220: Frontend Member Management Interface
**Status:** Planned | **Priority:** High
**Goal:** Admin member management UI
**Dependencies:** F210 complete

#### T221: Basic Member Roster Table
**Deliverable:** Core member list display
- Member table with essential columns
- Basic member data display
- Responsive table layout
- Loading states
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] Member list displays correctly
- [ ] All member data visible
- [ ] Table responsive on mobile
- [ ] Loading states working

#### T221.5: Member Table Search and Filtering
**Deliverable:** Search and filter functionality
- Search by name, email, GHIN
- Filter by member status and type
- Filter by balance ranges
- Clear filters functionality
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] Search returns accurate results
- [ ] Filtering working efficiently
- [ ] Multiple filters can be combined
- [ ] Clear filters resets properly

#### T221.7: Member Table Sorting and Export
**Deliverable:** Advanced table features
- Sortable columns (name, status, balance, etc.)
- Pagination controls
- Export to CSV functionality
- Column visibility controls
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] Table sorting functional
- [ ] Pagination working correctly
- [ ] CSV export contains correct data
- [ ] Column controls working

#### T222: Add/Edit Member Forms
**Deliverable:** Member data entry interface
- New member creation form
- Edit existing member form
- Form validation and error display
- Member type change workflow
- Balance adjustment interface
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] Forms validate correctly
- [ ] Data saves successfully
- [ ] Error handling working
- [ ] Member type changes tracked

#### T223: Member Detail View
**Deliverable:** Comprehensive member profile
- Complete member information display
- Balance and transaction history
- Member activity summary
- Edit and action buttons
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] All member data displayed
- [ ] Transaction history accurate
- [ ] Action buttons functional
- [ ] Profile updates working

---

## P300: Financial Transaction System
**Status:** Planned | **Estimated Duration:** 1-2 weeks
**Goal:** Track member balances and financial transactions
**Dependencies:** P200 complete

### F310: Transaction Database Schema
**Status:** Planned | **Priority:** Critical
**Goal:** Complete transaction tracking system
**Dependencies:** F210 complete

#### T311: Transactions Table Implementation
**Deliverable:** Financial transaction tracking
```sql
transactions table schema:
- transaction_id (primary key, UUID)
- member_id (foreign key, nullable for non-member transactions)
- transaction_type (enum: deposit|withdrawal|green_fee|admin_fee|side_game_entry|side_game_winnings|refund|adjustment|course_payment|other)
- amount (decimal, positive for credits, negative for debits)
- description (text, not null)
- reference_number (varchar, optional)
- admin_id (foreign key, who processed)
- round_id (foreign key, if round-related)
- vendor_payee (text, for non-member transactions like course payments)
- created_at (auto-managed)
```
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Transaction table created with constraints
- [ ] Foreign key relationships established
- [ ] Transaction types properly defined
- [ ] Audit trail functionality

#### T312: Balance Calculation Logic
**Deliverable:** Real-time balance system
- Balance calculation from transaction history
- Balance validation before transactions
- Transaction rollback capabilities
- Balance caching for performance
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Balance calculations accurate
- [ ] Negative balance prevention
- [ ] Rollback functionality working
- [ ] Performance optimized

---

### F320: Financial Management API & Interface
**Status:** Planned | **Priority:** High
**Goal:** Complete financial management system
**Dependencies:** F310 complete

#### T321: Transaction Management Endpoints
**Deliverable:** Transaction API
- POST /api/v1/transactions (create transaction)
- GET /api/v1/transactions (admin view all)
- GET /api/v1/members/{id}/transactions (member transactions)
- GET /api/v1/members/{id}/balance (current balance)
- PUT /api/v1/transactions/{id} (admin corrections)
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] All transaction endpoints working
- [ ] Admin-only access enforced
- [ ] Member transaction privacy maintained
- [ ] Balance endpoints accurate

#### T322: Admin Financial Management Interface
**Deliverable:** Admin financial tools
- Add deposit functionality
- Transaction history viewer with filters
- Financial reporting dashboard
- Bulk transaction processing
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Deposit functionality working
- [ ] Transaction history searchable
- [ ] Reports accurate and useful
- [ ] Bulk operations functional

#### T323: Member Financial Interface
**Deliverable:** Member financial view
- Member balance display component
- Personal transaction history
- Balance insufficient warnings
- Transaction detail views
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Balance displayed prominently
- [ ] Transaction history accessible
- [ ] Warnings appear appropriately
- [ ] Details clear and accurate

---

## P400: Season & Course Management
**Status:** Planned | **Estimated Duration:** 2-3 weeks
**Goal:** Season setup and course data management
**Dependencies:** P300 complete

### F410: Course Database & GHIN Integration
**Status:** Planned | **Priority:** Medium
**Goal:** Complete course data system
**Dependencies:** F310 complete

#### T411: Course Data Structure Implementation
**Deliverable:** Course database schema
```sql
venues table:
- venue_id (primary key, UUID)
- venue_name (not null)
- address (text)
- website (url)
- phone_number

courses table:
- course_id (primary key, UUID)
- venue_id (foreign key)
- course_name (not null)
- total_holes (default 18)

teeboxes table:
- teebox_id (primary key, UUID)
- course_id (foreign key)
- teebox_name (not null)
- gender (M|F|Unisex)
- slope_rating (decimal)
- course_rating (decimal)
- total_distance (integer)

holes table:
- hole_id (primary key, UUID)
- teebox_id (foreign key)
- hole_number (1-18)
- distance (integer)
- par (3|4|5)
- stroke_index (1-18)
```
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] All course tables created
- [ ] Relationships properly established
- [ ] Data validation rules applied
- [ ] Sample course data loaded

#### T412: GHIN Course Data Research
**Deliverable:** GHIN integration plan
- Research GHIN course database access
- Evaluate API availability and costs
- Create course import strategy
- Design manual course entry fallback
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] GHIN access options documented
- [ ] Integration approach defined
- [ ] Fallback plan established
- [ ] Cost/benefit analysis complete

---

### F420: Season Management System
**Status:** Planned | **Priority:** High
**Goal:** Complete season configuration system
**Dependencies:** F410 complete

#### T421: Season Data Structure Implementation
**Deliverable:** Season configuration schema
```sql
seasons table:
- season_id (primary key, UUID)
- season_name (not null)
- start_date, end_date (not null)
- active (boolean, default false)
- championship_prize_pool (decimal)
- eligibility_rules (JSON)
- point_schedules (JSON - regular, playoff, reset)
- payout_schedules (JSON)
- flight_rules (JSON - max_flight_size, etc.)
- side_game_defaults (JSON)
- created_at, updated_at
```
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Season table created with constraints
- [ ] JSON configurations validated
- [ ] Default values established
- [ ] Migration scripts tested

#### T422: Season Creation and Editing Forms
**Deliverable:** Basic season management
- Season creation form with validation
- Season editing interface
- Basic season information fields
- Form validation and error handling
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Season creation working
- [ ] Season editing functional
- [ ] Form validation effective
- [ ] Error handling clear

#### T422.5: Season Configuration System
**Deliverable:** Advanced season settings
- Point schedules configuration
- Payout schedules setup
- Flight rules configuration
- Side game defaults setup
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Point schedules configurable
- [ ] Payout schedules working
- [ ] Flight rules editable
- [ ] Side game defaults functional

#### T422.7: Season Management Operations
**Deliverable:** Season lifecycle management
- Season activation/deactivation
- Season copying functionality
- Season archive management
- Season status tracking
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Activation/deactivation working
- [ ] Copying functionality operational
- [ ] Archive system functional
- [ ] Status tracking accurate

---

## P500: Round Scheduling & Signup System
**Status:** Planned | **Estimated Duration:** 2-3 weeks
**Goal:** Event scheduling and member signup management
**Dependencies:** P400 complete

### F510: Round Management System
**Status:** Planned | **Priority:** Critical
**Goal:** Complete round scheduling system
**Dependencies:** F420 complete

#### T511: Round Data Structure Implementation
**Deliverable:** Round scheduling schema
```sql
rounds table:
- round_id (primary key, UUID)
- season_id (foreign key, not null)
- course_id (foreign key, not null)
- special_event_id (foreign key, optional)
- event_date, event_time (not null)
- registration_deadline (calculated)
- start_type (shotgun|tee_times|tbd)
- teebox_assignments (JSON by member type)
- fees (JSON - green, admin, championship, side games)
- max_participants (integer)
- round_status (scheduled|cancelled|completed)
- created_at, updated_at
```
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Round table created with constraints
- [ ] Course relationships established
- [ ] Fee structures flexible
- [ ] Status management working

#### T512: Round Creation and Editing Forms
**Deliverable:** Basic round management
- Round creation form with validation
- Round editing interface
- Basic round information (date, time, course)
- Form validation and error handling
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Round creation working
- [ ] Round editing functional
- [ ] Basic validation effective
- [ ] Error handling clear

#### T512.5: Course and Teebox Selection Interface
**Deliverable:** Course configuration for rounds
- Course selection dropdown
- Teebox assignment by member type
- Course information display
- Teebox validation rules
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Course selection working
- [ ] Teebox assignments functional
- [ ] Course info displayed correctly
- [ ] Validation rules enforced

#### T512.7: Round Scheduling and Status Management
**Deliverable:** Round operations management
- Round scheduling calendar view
- Round status management (scheduled/cancelled/completed)
- Fee configuration interface
- Round capacity management
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Calendar view functional
- [ ] Status changes working
- [ ] Fee configuration flexible
- [ ] Capacity limits enforced

---

### F520: Member Signup System
**Status:** Planned | **Priority:** Critical
**Goal:** Complete signup and registration system
**Dependencies:** F510 complete

#### T521: Signup Data Structure Implementation
**Deliverable:** Signup tracking schema
```sql
round_signups table:
- signup_id (primary key, UUID)
- round_id (foreign key, not null)
- member_id (foreign key, not null)
- signup_timestamp (auto-managed)
- pairing_request (member_id reference)
- tee_time_preference (early|late|no_preference)
- side_game_entries (JSON)
- total_fees_paid (calculated)
- signup_status (confirmed|cancelled|waitlist)
- created_at, updated_at
```
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Signup table with constraints
- [ ] Unique constraints on round/member
- [ ] Side game tracking flexible
- [ ] Status management complete

#### T522: Signup Business Logic Implementation
**Deliverable:** Signup processing system
- Automatic fee calculation
- Balance validation before signup
- Signup deadline enforcement
- Signup modification/cancellation
- Waitlist management
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Fee calculation accurate
- [ ] Balance validation working
- [ ] Deadline enforcement active
- [ ] Modification system functional

#### T523: Public Tournament Schedule Page
**Deliverable:** Public tournament viewing
- Public schedule display (no login required)
- Tournament information display
- Course and date information
- Registration status indicators
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Schedule page informative
- [ ] Tournament details clear
- [ ] Course information accurate
- [ ] Status indicators working

#### T523.5: Member Signup Page and Side Games
**Deliverable:** Core signup functionality
- Member signup form
- Side game selection interface
- Pairing and tee time preferences
- Signup validation and error handling
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Signup process intuitive
- [ ] Side game selection clear
- [ ] Preferences captured correctly
- [ ] Validation working properly

#### T523.7: Signup Management and Payment Integration
**Deliverable:** Signup operations and payment
- Signup modification/cancellation
- Payment confirmation workflow
- Balance deduction processing
- Signup status management
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Modification/cancellation working
- [ ] Payment integration functional
- [ ] Balance updates accurate
- [ ] Status management correct

---

## P600: Tournament Preparation Tools
**Status:** Planned | **Estimated Duration:** 2-3 weeks
**Goal:** Flight creation and tee sheet management
**Dependencies:** P500 complete

### F610: Flight Management System
**Status:** Planned | **Priority:** High
**Goal:** Automated flight creation system
**Dependencies:** F520 complete

#### T611: Flight Creation Algorithm
**Deliverable:** Automated flight generation
- Sort players by handicap index
- Apply season flight size rules
- Handle candidate members separately
- Flight balancing logic
- Manual override capabilities
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Flights generated automatically
- [ ] Handicap sorting accurate
- [ ] Flight sizes appropriate
- [ ] Manual adjustments possible

#### T612: Flight Management Interface
**Deliverable:** Flight administration tools
- View generated flights
- Manual flight adjustments
- Flight finalization process
- Flight printing/export
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Flight display clear
- [ ] Adjustments easy to make
- [ ] Finalization process clear
- [ ] Export functionality working

---

### F620: Tee Sheet Management
**Status:** Planned | **Priority:** High
**Goal:** Complete tee sheet creation and management
**Dependencies:** F610 complete

#### T621: Tee Sheet Generation System
**Deliverable:** Automated tee sheet creation
- Group players into 2-4 person groups
- Apply pairing requests from signups
- Generate tee times or shotgun assignments
- Tournament standings consideration
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Groupings appropriate
- [ ] Pairing requests honored
- [ ] Tee time assignments logical
- [ ] Standings consideration working

#### T622: Tee Sheet Management Interface
**Deliverable:** Tee sheet administration
- View proposed tee sheet
- Manual pairing adjustments
- Tee sheet finalization
- Printable format generation
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Tee sheet display clear
- [ ] Adjustments intuitive
- [ ] Finalization complete
- [ ] Print formats professional

---

## P700: Score Entry & Results System
**Status:** Planned | **Estimated Duration:** 3-4 weeks
**Goal:** Score entry, results calculation, and prize distribution
**Dependencies:** P600 complete

### F710: Scorecard & Score Entry System
**Status:** Planned | **Priority:** Critical
**Goal:** Complete score entry interface
**Dependencies:** F620 complete

#### T711: Scorecard Data Structure
**Deliverable:** Score tracking schema
```sql
scorecards table:
- scorecard_id (primary key, UUID)
- round_id (foreign key, not null)
- member_id (foreign key, not null)
- teebox_id (foreign key, not null)
- handicap_index (decimal, at time of round)
- playing_handicap (calculated)
- gross_scores (JSON array by hole)
- putts (JSON array by hole)
- fairways_hit (JSON array for par 4+)
- penalties (JSON by hole)
- dq_flag (boolean)
- dq_reason (text)
- created_at, updated_at
```
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Scorecard table complete
- [ ] Score validation rules
- [ ] Handicap calculations
- [ ] DQ tracking functional

#### T712: Basic Score Entry Interface
**Deliverable:** Core score input functionality
- Scorecard display by groups
- Basic score entry (hole-by-hole)
- Score validation (max score rules)
- Save and auto-save functionality
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Score entry intuitive
- [ ] Validation working correctly
- [ ] Auto-save functional
- [ ] Group display clear

#### T712.5: Advanced Score Tracking
**Deliverable:** Detailed score data
- Putt tracking per hole
- Fairway hit tracking (par 4+)
- Penalty tracking
- Real-time score calculations
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Putt tracking working
- [ ] Fairway tracking accurate
- [ ] Penalty recording functional
- [ ] Calculations real-time

#### T712.7: Bulk Score Entry and Management
**Deliverable:** Efficient score entry tools
- Bulk score entry options
- Score import functionality
- Score correction interface
- DQ flag and reason entry
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Bulk entry efficient
- [ ] Import functionality working
- [ ] Corrections easy to make
- [ ] DQ handling proper

---

### F720: Results Calculation Engine
**Status:** Planned | **Priority:** Critical
**Goal:** Complete results calculation and prize distribution
**Dependencies:** F710 complete

#### T721: Net Flight Results Calculation
**Deliverable:** Flight standings system
- Net score calculations
- Flight standings with playoffs
- Tie-breaking procedures (scorecard playoffs)
- Flight winner determination
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Net scores calculated correctly
- [ ] Flight standings accurate
- [ ] Tie-breaking working properly
- [ ] Winners determined correctly

#### T721.5: Side Game Results Calculation
**Deliverable:** Side game winners and payouts
- Skins calculations (gross and net)
- CTP (Closest to Pin) results
- Low putts calculations
- Deuces tracking and winners
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Skins calculated correctly
- [ ] CTP results accurate
- [ ] Low putts working properly
- [ ] Deuces tracking functional

#### T721.7: Points and Prize Distribution
**Deliverable:** Season points and prize money
- Season points allocation based on standings
- Prize money distribution calculations
- Payout schedule application
- Financial transaction generation
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Points allocation working
- [ ] Prize distribution accurate
- [ ] Payout schedules applied correctly
- [ ] Transactions generated properly

#### T722: Flight Results Display
**Deliverable:** Flight standings presentation
- Flight results and standings display
- Individual player scorecards
- Net score calculations shown
- Flight winner highlighting
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Flight results display clearly
- [ ] Scorecards readable and accurate
- [ ] Net scores shown correctly
- [ ] Winners highlighted properly

#### T722.5: Side Game Results Display
**Deliverable:** Side game winners presentation
- Side game winners display
- Skins results by hole
- CTP and other side game results
- Prize amounts for each game
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Side game winners clear
- [ ] Skins results detailed
- [ ] All side games covered
- [ ] Prize amounts accurate

#### T722.7: Season Standings and Publication
**Deliverable:** Season tracking and results publication
- Season standings updates
- Points leaderboard display
- Results publication system
- Historical results access
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Season standings accurate
- [ ] Points tracking working
- [ ] Publication system functional
- [ ] Historical data accessible

---

## P800: Special Events & Advanced Features
**Status:** Planned | **Estimated Duration:** 2-3 weeks
**Goal:** Multi-round tournaments and special competitions
**Dependencies:** P700 complete

### F810: Special Events Framework
**Status:** Planned | **Priority:** Medium
**Goal:** Multi-round tournament management
**Dependencies:** F720 complete

#### T811: Special Events Data Structure
**Deliverable:** Special event tracking
```sql
special_events table:
- event_id (primary key, UUID)
- event_name (not null)
- event_type (wigwam_warriors|ringers|tournament_of_champions|custom)
- season_id (foreign key)
- start_date, end_date
- entry_requirements (JSON)
- scoring_method (JSON)
- prize_structure (JSON)
- active (boolean)
```
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Special events schema complete
- [ ] Event types properly defined
- [ ] Scoring methods flexible
- [ ] Prize structures configurable

#### T812: WigWam Warriors Scoring System
**Deliverable:** 3-round aggregate scoring system
- Multi-round score aggregation logic
- Eligibility tracking (must play all 3 rounds)
- Net score calculation across rounds
- Leaderboard for 3-round aggregate
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] 3-round aggregation working correctly
- [ ] Eligibility rules enforced
- [ ] Net score calculations accurate
- [ ] Leaderboard displays properly

#### T813: Ringers Tournament System
**Deliverable:** Best-hole tracking system
- Ringers scorecard maintenance (best score per hole)
- Separate gross and net competitions
- Score updating logic (replace with better score)
- Final ringers scorecard calculation
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Best score per hole tracking working
- [ ] Gross/net competitions separate
- [ ] Score replacement logic correct
- [ ] Final scorecard accurate

#### T814: Tournament of Champions System
**Deliverable:** Qualification-based tournament
- Qualification tracking (net flight winners)
- Timeframe-based eligibility rules
- No entry fee system (admin funded)
- Special tournament designation
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Qualification tracking accurate
- [ ] Eligibility rules enforced
- [ ] Admin funding system working
- [ ] Tournament designation clear

#### T815: Custom Scoring Framework
**Deliverable:** Flexible scoring system for future events
- Configurable scoring algorithms
- Custom event type creation
- Flexible prize structure configuration
- Scoring rule engine
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Custom scoring configurable
- [ ] New event types can be created
- [ ] Prize structures flexible
- [ ] Rule engine extensible

---

### F820: Hole-in-One Pool System
**Status:** Planned | **Priority:** Low
**Goal:** Persistent hole-in-one pool management
**Dependencies:** F810 complete

#### T821: HIO Pool Implementation
**Deliverable:** Hole-in-one pool system
```sql
hio_pool table:
- pool_id (primary key, UUID)
- current_prize_amount (decimal)
- entry_fee (decimal)
- active (boolean)

hio_entries table:
- entry_id (primary key, UUID)
- pool_id (foreign key)
- member_id (foreign key)
- entry_date, amount_paid

hio_winners table:
- winner_id (primary key, UUID)
- pool_id (foreign key)
- member_id (foreign key)
- round_id (foreign key)
- hole_number, distance
- prize_amount, payout_date
```
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] HIO pool tracking complete
- [ ] Entry management working
- [ ] Winner verification system
- [ ] Prize payout functional

---

## P900: Deployment & Production
**Status:** Planned | **Estimated Duration:** 1-2 weeks
**Goal:** Production deployment on GCP compute instance
**Dependencies:** P800 complete

### F910: Production Configuration
**Status:** Planned | **Priority:** Critical
**Goal:** Production-ready application
**Dependencies:** All previous phases

#### T911: GCP Compute Instance Setup
**Deliverable:** Basic server infrastructure
- GCP compute instance configuration
- Basic server hardening and security
- Network and firewall configuration
- SSH access and user management
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] GCP instance operational
- [ ] Server security configured
- [ ] Network access working
- [ ] SSH access functional

#### T911.5: Web Server and SSL Configuration
**Deliverable:** Web server setup
- nginx installation and configuration
- SSL certificate installation
- HTTP to HTTPS redirection
- Security headers configuration
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] nginx configuration correct
- [ ] SSL certificates working
- [ ] HTTPS redirection functional
- [ ] Security headers active

#### T911.7: Application Service Configuration
**Deliverable:** Application deployment setup
- systemd service configuration for FastAPI
- Application process management
- Log file configuration
- Service auto-start configuration
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Services auto-starting
- [ ] Process management working
- [ ] Logs properly configured
- [ ] Service monitoring functional

#### T912: Deployment Automation
**Deliverable:** Automated deployment process
- Deployment scripts creation
- Environment configuration management
- Database migration automation
- Rollback procedures
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Deployment scripts working
- [ ] Environment management automated
- [ ] Migrations running correctly
- [ ] Rollback tested and functional

#### T913: Database Backup and Recovery
**Deliverable:** Data protection system
- Automated database backup procedures
- Backup verification and testing
- Recovery procedures documentation
- Backup retention policy
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Automated backups working
- [ ] Backup verification functional
- [ ] Recovery procedures tested
- [ ] Retention policy enforced

#### T913.5: Application Performance Monitoring
**Deliverable:** Performance tracking
- Application performance monitoring
- Resource usage tracking
- Performance alerts and thresholds
- Performance reporting dashboard
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Performance monitoring active
- [ ] Resource tracking working
- [ ] Alerts configured properly
- [ ] Dashboard functional

#### T913.5: Production Security Hardening
**Deliverable:** Production security configuration
- Remove default credentials from settings
- Configure secure environment variables
- Implement credential rotation policies
- Validate all security configurations
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:**
- [ ] No default credentials in production
- [ ] Environment variables properly configured
- [ ] Credential rotation procedures established
- [ ] Security configuration validated

#### T913.7: Security and Error Monitoring
**Deliverable:** Security and error tracking
- Security monitoring setup
- Error logging and alerting
- Failed login attempt tracking
- System health monitoring
**Workflow:**
- [ ] Plan Re-evaluation completed (`/docs/templates/plan_reevaluation.md`)
- [ ] Pre-Task Evaluation completed (`/docs/templates/pre_task_evaluation.md`)
- [ ] Implementation completed
- [ ] Architecture Review completed (use `architecture-validator` agent)
- [ ] Code Review completed (use `code-reviewer` agent)
- [ ] Post-Task Validation completed (`/docs/templates/post_task_validation.md`)
**Success Criteria:
- [ ] Security monitoring functional
- [ ] Error alerting working
- [ ] Login monitoring active
- [ ] Health checks operational

---

## Validation Framework

### Technical Validation Checklist
For each major feature (F###):
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing
- [ ] API endpoints documented
- [ ] Database migrations tested
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Mobile responsiveness verified

### User Acceptance Testing
For each phase (P###):
- [ ] Admin workflow testing completed
- [ ] Member workflow testing completed
- [ ] Error scenarios tested
- [ ] Edge cases handled
- [ ] Documentation updated
- [ ] Training materials prepared

### Production Readiness
For final deployment:
- [ ] Load testing completed (100+ concurrent users)
- [ ] Security audit passed
- [ ] Backup and recovery tested
- [ ] SSL and security headers configured
- [ ] Performance optimized
- [ ] Monitoring and alerting operational

---

## Modification History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-09-18 | Initial roadmap creation | Ben Christian |
| 1.1 | 2025-09-18 | Added date_of_birth to users table for tee eligibility; Made member_id nullable in transactions for non-member payments (e.g., course payments); Added course_payment transaction type and vendor_payee field | Ben Christian |
| 1.2 | 2025-09-18 | Split T812 Multi-Round Scoring Systems into focused tasks: T812 (WigWam Warriors), T813 (Ringers), T814 (Tournament of Champions), T815 (Custom Scoring Framework) | Ben Christian |
| 1.3 | 2025-09-18 | Major task complexity reduction: Split overly complex tasks into minimum testable deliverables across all phases. Split T221, T422, T512, T523, T712, T721, T722, T911, T913 into focused sub-tasks using .5 and .7 numbering convention | Ben Christian |
| 1.4 | 2025-09-18 | Added workflow adherence framework: Created /docs/templates/ directory with workflow templates (plan_reevaluation.md, pre_task_evaluation.md, post_task_validation.md, workflow_checklist.md); Added workflow validation sections to critical tasks (T113, T121-T123, T131-T132) | Claude Code |
| 1.5 | 2025-09-18 | Complete workflow validation implementation: Added **Workflow** sections to ALL 63 tasks in roadmap; Included Architecture Review requirements for database/deployment tasks; Enhanced roadmap with comprehensive workflow adherence guidelines and template references | Claude Code |
| 1.6 | 2025-09-19 | Added comprehensive testing tasks: T132.5 (Frontend Testing Framework Setup), T132.7 (Backend Authentication API Tests), T132.9 (Frontend Authentication Tests); Inserted between T132-T133 to ensure test coverage before dashboard implementation; Used simplified workflow for testing tasks | Claude Code |

---

*This roadmap is designed to evolve. Use the Plan Re-evaluation template before modifying any section to ensure changes are properly considered and documented.*