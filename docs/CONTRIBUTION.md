# Contributing to TipZed

**Welcome to the TipZed monetization platform!** This guide explains how to contribute code, fix bugs, and propose features during our 2-week MVP sprint.

**Project Lead:** Peter Zyambo  
**Backend Lead:** Peter Zyambo  
**Frontend Lead:** George Mugale  
**Frontend Support:** Barnabas Mwaipaya

---

## 🚀 Quick Start for Contributors

1. **Fork & Clone**
   ```bash
   git clone https://github.com/zyambo/creator-monetization.git
   cd creator-monetization
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/creator-profiles-ui
   ```

3. **Make Changes** (see guidelines below)

4. **Commit with Clear Messages**
   ```bash
   git commit -m "feat(frontend): add creator profile editor component"
   ```

5. **Push & Create Pull Request**
   ```bash
   git push origin feature/creator-profiles-ui
   ```

6. **Wait for Review** (Peter approves APIs, George leads frontend/backend coordination)

---

## 📋 Branching Strategy

### Branch Naming Convention

```
<type>/<feature-name>

Where type is:
- feature/    → New feature
- fix/        → Bug fix
- refactor/   → Code restructuring
- docs/       → Documentation only
- test/       → Testing updates
- chore/      → Dependency updates
```

### Examples

```bash
# Feature branches
git checkout -b feature/creator-profiles-ui
git checkout -b feature/payment-webhook-integration
git checkout -b feature/admin-payout-approval

# Bug fix branches
git checkout -b fix/jwt-token-refresh-issue
git checkout -b fix/wallet-balance-calculation

# Documentation
git checkout -b docs/api-authentication-guide

# Refactoring
git checkout -b refactor/payment-service-structure
```

### Branch Lifecycle
1. Create feature branch from `main`
2. Make commits (with message convention below)
3. Push to origin
4. Create pull request on GitHub
5. After approval & tests pass → merge to `main`
6. Delete branch

---

## 💬 Commit Message Convention

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat** - New feature
- **fix** - Bug fix
- **refactor** - Code restructuring (no feature/bug change)
- **docs** - Documentation changes
- **test** - Test additions/updates
- **chore** - Dependency/tooling updates
- **perf** - Performance optimization

### Scope
- `frontend` - React app changes
- `backend` - Django API changes
- `auth` - Authentication feature
- `payment` - Payment processing
- `payout` - Payout management
- `wallet` - Wallet/ledger
- `admin` - Admin dashboard
- `devops` - Deployment/infrastructure
- `config` - Configuration

### Subject
- ✅ Imperative mood ("add" not "added" or "adds")
- ✅ First letter lowercase
- ✅ No period at end
- ✅ Under 50 characters
- ❌ Avoid: "Update", "Fix", "Implement"

### Examples

**Good Commits:**
```bash
git commit -m "feat(frontend): add creator profile editor component"
git commit -m "fix(backend): correct wallet balance calculation query"
git commit -m "refactor(payment): simplify payment service structure"
git commit -m "docs(readme): add backend setup instructions"
git commit -m "test(auth): add JWT token refresh tests"
```

**Bad Commits:**
```bash
git commit -m "update stuff"
git commit -m "Fixes JWT issue"
git commit -m "REFACTOR: Payment.js"
```

### Commit Body (Optional)
For complex changes, add context:

```bash
git commit -m "fix(wallet): correct transaction ledger balance calculation

The balance calculation was not accounting for reversed transactions.
This caused creator balances to appear higher than actual.

Now queries filter out reversed transactions from sum.
Fixes issue #42.
"
```

### Commit Footer (Optional)
Reference issues:
```
Fixes #42
Closes #43
Related to #44
```

---

## 🔀 Pull Requests

### PR Title Format

```
<type>(<scope>): <description>

Same format as commit messages:
```

### Examples
```
feat(frontend): add payment form validation
fix(backend): handle mobile money webhook failures
refactor(auth): simplify JWT verification logic
```

### PR Description Template

```markdown
## Description
What does this PR do? (1-2 sentences)

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring
- [ ] Documentation

## Related Issues
Fixes #42

## Changes Made
- Change 1
- Change 2
- Change 3

## How to Test
1. Step 1 to reproduce/test
2. Step 2
3. Step 3

## Screenshots (if UI change)
[Attach screenshots for frontend changes]

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] All tests passing locally
```

### PR Example

```markdown
## Description
Add creator profile editor allowing creators to update their bio, category, and bank account.

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Refactoring

## Related Issues
Fixes #15

## Changes Made
- Add CreatorProfileEditor component
- Add updateProfile API endpoint
- Add form validation for bank account
- Add success/error notifications
- Update creator profile page to use new editor

## How to Test
1. Login as creator
2. Click "Edit Profile"
3. Update bio (test validation: max 500 chars)
4. Update category
5. Update bank account (validate format)
6. Click Save
7. Verify profile updated in database

## Screenshots
[image: profile editor UI]
[image: validation error messages]

## Checklist
- [x] Code follows style guidelines
- [x] Tests added (95% coverage)
- [x] Documentation updated in README
- [x] No breaking changes
- [x] All tests passing locally
- [x] Ran backend tests: `pytest apps/creators/tests.py`
- [x] Ran frontend tests: `npm test`
```

---

## ✅ Code Review Process

### Before Submitting PR
1. ✅ Code follows style guidelines (see below)
2. ✅ All tests pass locally
3. ✅ No console warnings/errors
4. ✅ Documentation updated
5. ✅ Commit messages follow convention

### Review by Project Leads

**Peter (Backend Lead):**
- Reviews backend code
- Approves API contract changes
- Ensures security best practices
- Validates database schema changes

**George (Frontend/Backend Support):**
- Reviews frontend code
- Ensures mobile responsiveness
- Validates component structure
- Coordinates backend-frontend integration

**Barnabas (Frontend Support):**
- Reviews styling/responsive design
- Tests cross-browser compatibility
- Validates accessibility

### Integration Windows (Days 3-10)
During daily integration syncs (15 min standups):
- Backend + frontend verify API contracts
- Test endpoints with real data
- Log any integration issues
- Peter approves before merge

### Approval Flow
```
Developer submits PR
    ↓
Code review (24 hour SLA)
    ↓
Tests passing (automated)
    ↓
Peter approves (API owner)
    ↓
Merge to main
    ↓
Deploy to staging
```

---

## 🏗️ Code Style Guidelines

### Backend (Django/Python)

**Python Style:**
- Follow PEP 8
- Line length: 88 characters (Black formatter)
- Use type hints where possible
- Docstrings for functions/classes

```python
# ✅ Good
def calculate_wallet_balance(user_id: int) -> Decimal:
    """Calculate total wallet balance from transaction ledger.
    
    Args:
        user_id: The user ID
        
    Returns:
        Decimal: Total balance
        
    Raises:
        User.DoesNotExist: If user not found
    """
    transactions = TransactionLedger.objects.filter(
        user_id=user_id,
        status='completed'
    )
    return sum(t.amount for t in transactions)

# ❌ Bad
def calc_balance(uid):
    t = TransactionLedger.objects.filter(user_id=uid, status='completed')
    return sum([tr.amount for tr in t])
```

**Django Models:**
```python
# ✅ Good
class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.user.username
```

**API Serializers:**
```python
# ✅ Good
class CreatorSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Creator
        fields = ['id', 'user_email', 'bio', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_bio(self, value):
        if len(value) > 500:
            raise serializers.ValidationError(
                "Bio must be 500 characters or less"
            )
        return value
```

### Frontend (React/JavaScript)

**Component Style:**
- Functional components only (hooks)
- PropTypes validation
- One component per file
- Descriptive naming

```javascript
// ✅ Good: CreatorProfileEditor.jsx
import PropTypes from 'prop-types';
import { useState } from 'react';

export default function CreatorProfileEditor({ creator, onSave }) {
  const [formData, setFormData] = useState({
    bio: creator?.bio || '',
    category: creator?.category || '',
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await onSave(formData);
    } catch (err) {
      setErrors(err.response?.data || {});
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto">
      <input
        type="text"
        name="bio"
        value={formData.bio}
        onChange={handleChange}
        maxLength="500"
        className="w-full px-3 py-2 border rounded"
      />
      {errors.bio && <p className="text-red-500">{errors.bio}</p>}
      <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">
        Save
      </button>
    </form>
  );
}

CreatorProfileEditor.propTypes = {
  creator: PropTypes.shape({
    bio: PropTypes.string,
    category: PropTypes.string,
  }),
  onSave: PropTypes.func.isRequired,
};
```

**Styling (Tailwind):**
```jsx
// ✅ Good: Use Tailwind utility classes
<div className="flex flex-col gap-4 max-w-md">
  <input className="px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
  <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition" />
</div>

// ❌ Bad: Custom CSS for simple utilities
<style>
  .input { padding: 8px 12px; border: 1px solid #ccc; }
</style>
```

---

## 🧪 Testing Requirements

### Backend Tests

**Minimum Coverage:** 80%

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific app
pytest apps/auth/tests.py
```

**Test Example:**
```python
import pytest
from django.contrib.auth import get_user_model
from apps.creators.models import Creator

User = get_user_model()

@pytest.mark.django_db
class TestCreatorProfile:
    
    def test_create_creator_profile(self):
        user = User.objects.create_user(
            email='creator@example.com',
            password='pass123'
        )
        creator = Creator.objects.create(
            user=user,
            bio='My bio',
            category='music'
        )
        
        assert creator.bio == 'My bio'
        assert creator.category == 'music'
    
    def test_creator_str_representation(self):
        user = User.objects.create_user(email='test@example.com')
        creator = Creator.objects.create(user=user)
        
        assert str(creator) == user.username
```

### Frontend Tests

**Minimum Coverage:** 75%

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific file
npm test -- CreatorProfileEditor.test.jsx
```

**Test Example:**
```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CreatorProfileEditor from './CreatorProfileEditor';

describe('CreatorProfileEditor', () => {
  const mockCreator = {
    id: 1,
    bio: 'Original bio',
    category: 'music',
  };
  
  it('renders form with creator data', () => {
    const mockOnSave = jest.fn();
    render(
      <CreatorProfileEditor creator={mockCreator} onSave={mockOnSave} />
    );
    
    expect(screen.getByDisplayValue('Original bio')).toBeInTheDocument();
  });
  
  it('calls onSave with updated data', async () => {
    const mockOnSave = jest.fn().mockResolvedValue({});
    render(
      <CreatorProfileEditor creator={mockCreator} onSave={mockOnSave} />
    );
    
    fireEvent.change(screen.getByDisplayValue('Original bio'), {
      target: { value: 'Updated bio' },
    });
    fireEvent.click(screen.getByRole('button', { name: /save/i }));
    
    await waitFor(() => {
      expect(mockOnSave).toHaveBeenCalledWith({
        bio: 'Updated bio',
        category: 'music',
      });
    });
  });
});
```

---

## 📦 Dependency Updates

### Adding Dependencies

**Backend:**
```bash
# Add to requirements.txt, then:
pip install -r requirements.txt
```

**Frontend:**
```bash
# Add to package.json, then:
npm install
```

### Before Committing
1. Test with new dependency
2. Update lock files
3. Document breaking changes
4. Verify size impact

---

## 🚨 Common Issues & Solutions

### Issue: Merge Conflicts
```bash
# Update branch with main
git fetch origin
git rebase origin/main

# Resolve conflicts in editor, then:
git add .
git rebase --continue
```

### Issue: Forgot to Create Feature Branch
```bash
# Create branch from current commits
git branch feature/forgot-branch
git reset --hard origin/main
git checkout feature/forgot-branch
```

### Issue: Need to Undo Commits
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Issue: Tests Failing in CI but Passing Locally
```bash
# Ensure environment matches CI
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest

# Check for environment-specific issues
echo $DJANGO_SETTINGS_MODULE
echo $PYTHONPATH
```

---

## 📞 Getting Help

**Have questions?**
- Check [README.md](README.md) for project overview
- See [backend/README.md](backend/README.md) for API docs
- See [frontend/README.md](frontend/README.md) for UI setup
- Review [EXAMPLE_WEEK1_ISSUES.md](docs/EXAMPLE_WEEK1_ISSUES.md) for real examples

**During integration windows (Days 3-10):**
- Daily 15-min standup at [time TBD]
- Ask in Slack or GitHub issues
- George coordinates backend-frontend alignment
- Peter approves API changes

---

## 🎯 Definition of Done

A PR is ready to merge when:

- ✅ Code follows style guidelines
- ✅ All tests pass (80%+ coverage for backend, 75%+ for frontend)
- ✅ No console warnings/errors
- ✅ Documentation updated
- ✅ Commit messages follow convention
- ✅ Peter approved (for APIs/backend)
- ✅ George approved (for frontend/integration)
- ✅ Accessibility verified (frontend changes)
- ✅ Mobile responsiveness verified (frontend changes)
- ✅ No breaking changes (or properly versioned)

---

## 🚀 Deployment After Merge

Once PR is merged to `main`:

1. **Staging Deployment** (automatic CI/CD)
   ```bash
   git push origin main
   # Triggers: run tests, build, deploy to staging
   ```

2. **Verify in Staging**
   - Test endpoints
   - Check logs for errors
   - Verify integration with frontend

3. **Production Deployment** (manual approval)
   - Peter reviews staging results
   - Approves production push
   - Monitors logs for errors

---

**Last Updated:** January 27, 2026  
**Sprint:** 2-Week MVP  
**Questions?** Reach out to Peter, George, or Barnabas
