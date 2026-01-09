# ⚡ QUICK START: Phase 3 Implementation Guide

**Last Updated**: January 10, 2026 | **Status**: Ready to Execute 🚀

---

## 🔴 WHAT TO DO RIGHT NOW (Next 5 minutes)

### 1. Read Full Plan (5 minutes)
```
File: PHASE2_EXECUTION_REPORT_AND_NEXT_STEPS.md
OR: CURRENT_STATUS_DASHBOARD.html (visual overview)
```

### 2. Check Current Test Results (2 minutes)
```bash
cd backend
python -m pytest tests/ -v --tb=short
```

### 3. Verify User Model (1 minute)
```bash
python -c "from app.models import User; 
print('Columns:', [c.name for c in User.__table__.columns])
print('Methods:', [m for m in dir(User) if not m.startswith('_')])"
```

---

## 🔴 CRITICAL TASKS (Do in this order)

### TASK 1: Fix User Model (1-2 hours)

**Check if User model has these attributes:**
```python
email = db.Column(db.String(255), unique=True, nullable=False, index=True)
username = db.Column(db.String(100), unique=True, nullable=False)  
password_hash = db.Column(db.String(255), nullable=False)
role = db.Column(db.String(20), default='candidate')
```

**Check if User model has these methods:**
```python
def to_dict(self):
    return {
        'id': self.id,
        'email': self.email,
        'username': self.username,
        'role': self.role
    }
```

**File**: `backend/app/models.py`

**If missing**, add them and commit:
```bash
git add backend/app/models.py
git commit -m "fix: Add missing User model attributes and methods"
```

---

### TASK 2: Implement Password Hashing (1 hour)

**Step 1**: Install werkzeug
```bash
cd backend
pip install werkzeug
pip freeze > requirements.txt
```

**Step 2**: Update User model (in `backend/app/models.py`)
```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # ... existing fields ...
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password hash."""
        return check_password_hash(self.password_hash, password)
```

**Step 3**: Update auth endpoints in `backend/app/api/routes.py`

In `register` endpoint:
```python
new_user = User(
    email=data['email'],
    username=data['username'],
    role='candidate'
)
new_user.set_password(data['password'])  # Use new method
db.session.add(new_user)
db.session.commit()
```

In `login` endpoint:
```python
user = db.session.query(User).filter_by(email=data['email']).first()
if not user or not user.check_password(data['password']):  # Use new method
    return jsonify({'error': 'Invalid credentials'}), 401
```

**Commit**:
```bash
git add backend/
git commit -m "feat: Implement password hashing with werkzeug"
```

---

### TASK 3: Fix Auth Endpoints (1-2 hours)

**Step 1**: Add detailed logging to endpoints
```python
import traceback

@api_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        logger.debug(f"Register request: {data}")
        
        # ... validation and user creation ...
        
        logger.info(f"User created: {new_user.id}")
        return jsonify({...}), 201
    except Exception as e:
        logger.error(f"Register error: {str(e)}", exc_info=True)
        print(traceback.format_exc())  # Debug output
        return jsonify({'error': str(e)}), 500
```

**Step 2**: Run tests with debug output
```bash
cd backend
python -m pytest tests/test_auth.py::test_register -v -s
```

**Step 3**: Fix any errors found
- Common issues: db.session not committed, missing imports, attribute errors
- Add required User model attributes if they don't exist
- Ensure database session is properly initialized

**Step 4**: Verify endpoints work
```bash
# Should return 201
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"testuser","password":"pass123"}'

# Should return 200 after registration
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123"}'
```

**Commit**:
```bash
git add backend/
git commit -m "fix: Debug and fix auth endpoints 500 errors"
```

---

## 🟡 IMPORTANT NEXT STEPS (After critical tasks)

### TASK 4: Add Input Validation (1-2 hours)

```bash
cd backend
pip install marshmallow
```

Create `backend/app/api/validators.py`:
```python
from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    password = fields.Str(required=True, validate=validate.Length(min=8))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
```

Use in routes:
```python
from app.api.validators import RegisterSchema

@api_bp.route('/auth/register', methods=['POST'])
def register():
    schema = RegisterSchema()
    try:
        data = schema.load(request.get_json())
        # ... rest of implementation ...
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
```

---

### TASK 5: Setup Database Migrations (1-2 hours)

```bash
cd backend
alembic init alembic
```

Edit `alembic/env.py`:
```python
from app import create_app
from app.database import db

app = create_app('development')
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])
target_metadata = db.metadata
```

Create migration:
```bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

## 🟢 RUN FINAL TESTS

```bash
cd backend

# Full test suite
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ -v --cov=app

# Expected output:
# PASSED: 6+ tests
# FAILED: 0-2 tests
# ERRORS: 0 errors
# Pass rate: 80%+
```

---

## 🔍 DEBUGGING TIPS

### Issue: AttributeError on User model
```bash
# Check what's actually in the model
python -c "from app.models import User; print(User.__table__.columns.keys())"

# If missing columns, add them to backend/app/models.py
```

### Issue: 500 errors from endpoints
```bash
# Run with full stack trace
python -m pytest tests/test_auth.py -v -s --tb=long

# Check logs for details
grep -r "error\|Error\|ERROR" backend/*.log
```

### Issue: db.session not working
```python
# Make sure to import and initialize properly
from app.database import db
from app import create_app

app = create_app('testing')
with app.app_context():
    db.session.add(user)
    db.session.commit()
```

---

## 📂 FILES TO MODIFY

| File | Task | Status |
|------|------|--------|
| `backend/app/models.py` | Fix User attributes | 🔴 CRITICAL |
| `backend/app/api/routes.py` | Fix auth endpoints | 🔴 CRITICAL |
| `backend/app/api/validators.py` | Add validation | 🟡 CREATE |
| `backend/app/api/matching_engine.py` | Matching logic | 🟢 CREATE |
| `backend/tests/conftest.py` | Fix fixtures | 🔴 CRITICAL |
| `alembic/env.py` | Migrations | 🟡 CONFIGURE |
| `requirements.txt` | Add dependencies | 🔴 UPDATE |

---

## ✅ COMMIT MESSAGES TEMPLATE

```bash
# After fixing User model
git commit -m "fix: Add missing User model attributes and to_dict method"

# After password hashing
git commit -m "feat: Implement password hashing with werkzeug"

# After fixing auth endpoints  
git commit -m "fix: Debug and fix auth endpoints 500 errors"

# After adding validation
git commit -m "feat: Add input validation schemas with Marshmallow"

# After migrations
git commit -m "feat: Setup Alembic database migrations"

# Final
git commit -m "feat: Complete Phase 3 core implementation"
```

---

## 🔗 RESOURCES

- **Full Plan**: [PHASE2_EXECUTION_REPORT_AND_NEXT_STEPS.md](./PHASE2_EXECUTION_REPORT_AND_NEXT_STEPS.md)
- **Visual Dashboard**: [CURRENT_STATUS_DASHBOARD.html](./CURRENT_STATUS_DASHBOARD.html)
- **Repository**: https://github.com/maksimmishakov/mismatch-recruiter
- **Actions**: https://github.com/maksimmishakov/mismatch-recruiter/actions

---

## 📢 SUMMARY

**Time Estimate**: 5-8 hours for all critical tasks

**Expected Outcome**:
- ✅ Auth endpoints fully functional (201/200 responses)
- ✅ Password hashing implemented
- ✅ Input validation working
- ✅ Database migrations ready
- ✅ 80%+ test pass rate

**Next Milestone**: Jan 14, 14:00 MSK - Lamoda Demo

---

**🚀 LET'S GO! START WITH TASK 1 NOW!**
