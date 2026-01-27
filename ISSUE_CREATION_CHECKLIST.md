# ✅ Issue Creation Checklist

Use this checklist when creating new issues to ensure completeness.

---

## 🎯 Before You Start

- [ ] Understand what problem this issue solves
- [ ] Identify the correct template type
- [ ] Check if similar issue already exists
- [ ] Review related issues & dependencies

---

## 📝 All Issues: Basic Requirements

- [ ] **Title is clear & specific**
  - Bad: `Update auth`
  - Good: `[BE] Authentication & JWT Models`

- [ ] **Description uses template sections**
  - Fill in all required sections
  - Delete optional sections not needed
  - Remove template comments

- [ ] **At least 3 labels applied**
  - Type: `backend` / `frontend` / `integration` / `qa` / `devops` / `bug`
  - Priority: `high-priority` (if blocking)
  - Sprint: `2-week-mvp` (required for MVP)

- [ ] **Assigned to owner**
  - Backend → George Mugale
  - Frontend Lead → George Mugale
  - Frontend Support → Barnabas Mwaipaya
  - Integration → Peter Zyambo
  - QA → Team members
  - DevOps → Team lead

- [ ] **Sprint day indicated**
  - Which day 1-10 should this be done?
  - Realistic based on dependencies?

- [ ] **Dependencies listed**
  - Link to blocking issues
  - Link to related issues
  - Clear on unblocking criteria

---

## 🔗 Backend Feature Issues (`[BE]`)

### Content Checklist
- [ ] Feature description: What does it do?
- [ ] Scope checklist: Models, endpoints, services?
- [ ] Database changes: New tables? Migrations?
- [ ] API endpoints: URLs, methods, auth?
- [ ] Request/response examples: JSON bodies?
- [ ] Error cases: 400, 401, 403, 500?
- [ ] Acceptance criteria: 5-8 specific criteria?
- [ ] Testing: Unit tests? Integration tests?
- [ ] Performance: Query optimization needed?
- [ ] Security: Auth check? Input validation?

### Questions to Answer
- What data model(s) are needed?
- Which endpoints does this create/update?
- What are the validation rules?
- Who can access this data (auth/authz)?
- What edge cases exist?
- How long should this take?

### Sign-Off
- [ ] Tests written?
- [ ] API contract defined?
- [ ] Frontend reviewed contract?

---

## 🎨 Frontend Feature Issues (`[FE][Lead]`)

### Content Checklist
- [ ] Feature description: What's the user benefit?
- [ ] User story: As a [role], I want [action], so that [benefit]
- [ ] Scope checklist: Components? State? API integration?
- [ ] API dependencies: Which endpoints needed?
- [ ] Request/response examples: What data from API?
- [ ] Acceptance criteria: 5-8 specific criteria?
- [ ] Testing: Manual steps? Browsers? Devices?
- [ ] Mobile responsive: 320px-2560px?
- [ ] Accessibility: WCAG standards?

### Questions to Answer
- What UI components are needed?
- Which API endpoints will be called?
- How should errors be displayed?
- What's the loading state?
- What if API is slow (timeout)?
- Works on mobile & desktop?
- No console errors?

### Sign-Off
- [ ] Tested with real backend (not mocks)?
- [ ] Mobile responsive verified?
- [ ] No console errors?

---

## 🎨 Frontend Support Issues (`[FE][Support]`)

### Content Checklist
- [ ] Task description: What's the UI issue?
- [ ] UI focus checkboxes: Styling? Responsive? Polish?
- [ ] Design reference: Link to design or screenshot
- [ ] Related feature: Link to parent feature issue
- [ ] Acceptance criteria: Specific measurable criteria
- [ ] Browser testing: Chrome, Firefox, Safari, Mobile?

### Questions to Answer
- What's visually broken or unpolished?
- What's the desired outcome?
- Is there a design mockup?
- Which browsers/devices need testing?
- What's the priority?

### Sign-Off
- [ ] Tested on mobile & desktop?
- [ ] Matches design reference?
- [ ] Reviewed by Frontend Lead?

---

## 🔗 Integration Issues (`[INT]`)

### Content Checklist
- [ ] Integration area: What flow (Auth, Payments, etc.)?
- [ ] API contract: Method, URL, request/response?
- [ ] Error responses: 400, 401, 403, 404, 500?
- [ ] End-to-end flow: Step-by-step user journey?
- [ ] Acceptance criteria: Alignment, data, errors, state?
- [ ] Test evidence: Screenshots, logs, evidence?
- [ ] Integration owner: Who approves?
- [ ] Sign-off checklist: Contract? Real endpoint? Approved?

### Questions to Answer
- What's being integrated (backend + frontend)?
- What's the complete user flow?
- What data needs to be exchanged?
- What can go wrong (errors)?
- Are there any timing/race condition issues?
- Is idempotency needed (duplicate handling)?
- How will this be tested end-to-end?

### Sign-Off
- [ ] API contract previously approved?
- [ ] Both systems fully implemented?
- [ ] End-to-end tested?
- [ ] Integration owner signed off?

---

## 📡 API Contract Issues (`[API-SPEC]`)

### Content Checklist
- [ ] Endpoint name: Clear, RESTful path?
- [ ] HTTP method: GET, POST, PUT, DELETE, PATCH?
- [ ] Authentication: Required? Type (JWT, API key)?
- [ ] Authorization: Who can access?
- [ ] Request body: Full JSON example?
- [ ] Query/path params: All params documented?
- [ ] Response body: Full JSON example (success)?
- [ ] Error responses: 400, 401, 403, 404, 500?
- [ ] Rate limiting: If applicable?
- [ ] Idempotency: If applicable (payments, etc.)?
- [ ] Example cURL request: Copy-paste ready?

### Questions to Answer
- What's this endpoint's purpose?
- What data must be sent?
- What data comes back?
- What validations are needed?
- What could go wrong (errors)?
- How fast should it respond?
- Is duplicate prevention needed?

### Sign-Off
- [ ] Backend developer reviewed?
- [ ] Frontend developer reviewed?
- [ ] Both agreed on contract?
- [ ] No breaking changes to existing contracts?

---

## 🧪 QA / Testing Issues (`[QA]`)

### Content Checklist
- [ ] Test area: What's being tested?
- [ ] QA checklist: Specific test cases?
- [ ] Browsers tested: Chrome, Firefox, Safari, Mobile?
- [ ] Devices tested: Desktop, tablet, mobile?
- [ ] Issues found: Any bugs? Links to bug issues?
- [ ] Go-live status: Ready? Needs fixes? Blocked?

### Questions to Answer
- What feature(s) are being tested?
- What are the happy path steps?
- What edge cases should be tested?
- What error cases need testing?
- Does it work on all browsers?
- Does it work on mobile?
- Performance acceptable?

### Sign-Off
- [ ] All tests passed?
- [ ] No critical bugs found?
- [ ] Mobile responsive verified?
- [ ] Ready for production?

---

## 🚀 DevOps / Deployment Issues (`[DevOps]`)

### Content Checklist
- [ ] Task summary: What's being deployed/configured?
- [ ] Scope checklist: Env? Database? CI/CD? Monitoring?
- [ ] Configuration: Environment variables needed?
- [ ] Database migrations: Any migrations to run?
- [ ] Deployment steps: Step-by-step instructions?
- [ ] Pre-deployment checklist: Ready to deploy?
- [ ] Post-deployment verification: Smoke tests?
- [ ] Rollback plan: How to rollback if needed?

### Questions to Answer
- What changes to infrastructure?
- What environment variables needed?
- Are database migrations needed?
- How do you verify deployment success?
- What could go wrong?
- How do you rollback?
- Who supports this in production?

### Sign-Off
- [ ] Pre-deployment checklist completed?
- [ ] Post-deployment verification passed?
- [ ] Monitoring alerts configured?
- [ ] Rollback plan documented?

---

## 🐛 Bug Report Issues (`[BUG]`)

### Content Checklist
- [ ] Bug summary: Clear 1-sentence description
- [ ] Environment: Platform, browser, OS, user role?
- [ ] Steps to reproduce: Clear numbered steps?
- [ ] Expected vs actual: What should happen vs what does?
- [ ] Screenshots/videos: Visual evidence?
- [ ] Severity: Critical? High? Medium? Low?
- [ ] Console errors: Any JavaScript errors?
- [ ] API errors: Any backend error responses?
- [ ] Workaround: Can users work around this?
- [ ] Impact: Who's affected?

### Questions to Answer
- What's broken?
- When did it start?
- How consistently can you reproduce it?
- Does it affect all users or specific ones?
- Is there a temporary workaround?
- How urgent is this?

### Sign-Off
- [ ] Reproducible by someone else?
- [ ] Assigned to appropriate developer?
- [ ] Blocked by any other issues?

---

## ⚙️ Configuration Issues (`[CONFIG]`)

### Content Checklist
- [ ] Task summary: What's being configured?
- [ ] Type checkboxes: Env vars? Secrets? Database?
- [ ] Is sensitive data? (Affects how it's stored)
- [ ] Details: What needs configuring where?
- [ ] Implementation steps: How to apply config?
- [ ] Verification: How to test it worked?
- [ ] Documentation: Setup instructions?

### Questions to Answer
- What configuration is needed?
- Is it different per environment (dev/staging/prod)?
- Is it sensitive (secrets)?
- How is it applied (env var, file, vault)?
- How do you know it's working?
- What breaks if it's wrong?

### Sign-Off
- [ ] Configuration applied?
- [ ] Verified in all environments?
- [ ] No hardcoded secrets?

---

## 🔗 Linking Issues

**When linking issues:**

1. **Dependencies:**
   ```
   Blocked by: #123
   Blocks: #456, #789
   Related: #111
   ```

2. **Parent/Child:**
   ```
   Part of: #100 (auth epic)
   Sub-task of: #200
   ```

3. **Integration:**
   ```
   Backend implementation: #BE-123
   Frontend implementation: #FE-456
   Integration test: #INT-789
   ```

---

## ✅ Pre-Submit Verification

Before submitting your issue, verify:

- [ ] Title is clear & specific
- [ ] Template sections filled completely
- [ ] No placeholder text left
- [ ] All acceptance criteria measurable (not vague)
- [ ] Dependencies linked
- [ ] Owner assigned
- [ ] Labels applied (type, priority, sprint)
- [ ] Sprint day indicated (1-10)
- [ ] Related issues linked
- [ ] No duplicate issues exist
- [ ] Follows MVP scope (doesn't ship non-essential features)

---

## 💡 Pro Tips

1. **Copy examples from [EXAMPLE_WEEK1_ISSUES.md](EXAMPLE_WEEK1_ISSUES.md)**
   - Real working examples of all issue types
   - Shows proper structure & detail level

2. **Link dependencies early**
   - Helps with sprint planning
   - Prevents missed blockers

3. **Be specific in acceptance criteria**
   - "Works on mobile" → "Tested on iPhone 6+, iPhone SE, Android 8+"
   - "API returns data" → "Returns {id, name, balance, created_at}"

4. **Include examples**
   - Code snippets for backend
   - Mock data for frontend
   - cURL examples for API specs

5. **Think about edge cases**
   - Empty data?
   - Invalid input?
   - Network timeout?
   - Race conditions?

6. **Don't over-scope**
   - Smaller issues are better
   - Can be done in 1-2 days
   - Keep MVP focus

---

## 📞 Questions?

Review:
- [ISSUE_TEMPLATE_GUIDE.md](ISSUE_TEMPLATE_GUIDE.md) — Full guide
- [ISSUE_TEMPLATES_QUICK_REF.md](ISSUE_TEMPLATES_QUICK_REF.md) — Quick reference
- [EXAMPLE_WEEK1_ISSUES.md](EXAMPLE_WEEK1_ISSUES.md) — Real examples

Still stuck? Ask the project lead (Peter Zyambo).
