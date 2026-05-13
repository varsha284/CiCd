# AWS CI/CD Setup Guide for Flask Application

## 📋 Project Overview
This is a production-ready Flask application configured for AWS CI/CD pipeline integration using CodeCommit, CodeBuild, and CodePipeline.

---

## 📁 Generated Files and Their Purpose

### 1. **requirements.txt**
**Location:** `c:\Users\DELL\Downloads\cicd\requirements.txt`

**Purpose:** Lists all Python dependencies with pinned versions for reproducible builds.

**Key Dependencies:**
- Flask 2.3.3 - Web framework
- Flask-SQLAlchemy 3.0.5 - ORM for database
- Flask-Login 0.6.3 - User session management
- Gunicorn 21.2.0 - Production WSGI server
- pytest 7.4.0 - Testing framework
- python-dotenv 1.0.0 - Environment variable management

**When to Update:** Add new dependencies and run `pip freeze > requirements.txt` locally.

---

### 2. **buildspec.yml**
**Location:** `c:\Users\DELL\Downloads\cicd\buildspec.yml`

**Purpose:** AWS CodeBuild specification file that defines CI/CD pipeline stages.

**Phases:**
- **Install:** Python 3.11 runtime + pip dependencies
- **Pre_Build:** Runs pytest for unit testing
- **Build:** Compiles Python code and verifies syntax
- **Post_Build:** Finalizes build and indicates readiness for deployment

**Features:**
- ✅ Python 3.11 runtime
- ✅ Automatic pip cache optimization
- ✅ Unit test execution with pytest
- ✅ Syntax verification before deployment
- ✅ Production environment configuration
- ✅ Excludes sensitive files from artifacts

---

### 3. **.gitignore**
**Location:** `c:\Users\DELL\Downloads\cicd\.gitignore`

**Purpose:** Prevents committing sensitive, temporary, or unnecessary files to version control.

**Key Exclusions:**
- `__pycache__/` - Python bytecode cache
- `.pytest_cache/` - Test artifacts
- `*.db` - Database files (keep local only)
- `static/uploads/*` - User-uploaded files
- `.env` - Environment secrets
- `venv/` - Virtual environment
- `.vscode/`, `.idea/` - IDE configurations

**Why:** These files are machine-generated, contain secrets, or are large and shouldn't be in repository.

---

### 4. **.env.example**
**Location:** `c:\Users\DELL\Downloads\cicd\.env.example`

**Purpose:** Template showing required environment variables.

**Usage:** Copy to `.env` and fill in actual values (not committed to git).

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.11+ installed
- Git installed
- pip package manager

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env with your settings
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

### Step 4: Create Database (First Time)
```bash
# Flask creates SQLite database automatically on first run
# Or manually initialize with:
python -c "from app import create_app; app = create_app(); app.app_context().push()"
```

### Step 5: Run Flask Application Locally
```bash
# Development mode (debug enabled)
python app.py

# The application will start at http://localhost:5000
```

### Step 6: Run Tests Locally
```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_app.py -v

# Run with coverage report
python -m pytest tests/ --cov
```

---

## 🔌 AWS CI/CD Pipeline Setup

### Architecture Flow
```
AWS CodeCommit (Repository)
        ↓
AWS CodePipeline (Orchestrator)
        ↓
AWS CodeBuild (Build & Test)
        ↓
Deployment Target (EC2, ECS, Elastic Beanstalk)
```

### Step-by-Step AWS Configuration

#### 1. Create AWS CodeCommit Repository
```bash
# Using AWS CLI
aws codecommit create-repository \
  --repository-name campus-lost-found \
  --description "Flask Lost & Found Application"

# Get the clone URL
aws codecommit get-repository --repository-name campus-lost-found
```

#### 2. Push Code to CodeCommit
```bash
# Add AWS CodeCommit as remote
git remote add aws <codecommit-clone-url>

# Push to CodeCommit
git push -u aws main
```

#### 3. Create CodeBuild Project
```bash
# Using AWS CLI
aws codebuild create-project \
  --name campus-lost-found-build \
  --source type=CODECOMMIT,location=<codecommit-url> \
  --artifacts type=NO_ARTIFACTS \
  --environment type=LINUX_CONTAINER,image=aws/codebuild/standard:7.0,computeType=BUILD_GENERAL1_SMALL \
  --service-role arn:aws:iam::<ACCOUNT_ID>:role/CodeBuildServiceRole
```

#### 4. Create CodePipeline
AWS Console Steps:
1. Go to AWS CodePipeline → Create Pipeline
2. Set source to CodeCommit (campus-lost-found repo)
3. Add build stage with CodeBuild
4. Configure deployment target (EC2, ECS, or Elastic Beanstalk)
5. Review and create pipeline

#### 5. Set IAM Permissions
Ensure CodeBuild role has permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "codecommit:GitPull"
      ],
      "Resource": "arn:aws:codecommit:*:*:campus-lost-found"
    }
  ]
}
```

---

## 🌐 Deployment Options

### Option 1: AWS Elastic Beanstalk (Recommended for Flask)
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB environment
eb init -p python-3.11 campus-lost-found

# Create environment and deploy
eb create campus-lost-found-env
eb deploy

# View logs
eb logs
```

**buildspec.yml modification for Beanstalk:**
```yaml
artifacts:
  files:
    - '**/*'
  discard-paths: no
```

### Option 2: AWS EC2
1. Launch EC2 instance (Amazon Linux 2 or Ubuntu)
2. Install Python 3.11, pip, and gunicorn
3. Clone from CodeCommit
4. Run: `gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app`

### Option 3: AWS ECS (Docker)
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

---

## 🔍 Verification Checklist

Before uploading to AWS, verify:

- [ ] `app.py` exists and uses Flask factory pattern ✅
- [ ] `requirements.txt` lists all dependencies ✅
- [ ] `buildspec.yml` configured for Python 3.11 ✅
- [ ] `.gitignore` prevents committing sensitive files ✅
- [ ] `.env.example` shows required environment variables ✅
- [ ] All tests pass: `python -m pytest tests/ -v` ✅
- [ ] Application runs locally: `python app.py` ✅
- [ ] No hardcoded secrets in code ✅
- [ ] Database file not tracked in git ✅

---

## 📝 Flask Entry Point Detection

Your project has a **Flask factory pattern** in:
- **File:** `app.py`
- **Function:** `create_app()`
- **Entry Point:** `if __name__ == '__main__': app = create_app(); app.run(debug=True)`

This is the **recommended pattern** for large Flask applications.

For AWS Elastic Beanstalk, create `wsgi.py`:
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

---

## 🚨 Production Configuration Changes

When deploying to production:

### 1. Update .env
```env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=<use-strong-random-key>
DATABASE_URL=<production-database-url>
```

### 2. Generate Strong Secret Key
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Use Production Database
- PostgreSQL (AWS RDS): `postgresql://user:pass@rds-endpoint:5432/dbname`
- MySQL: `mysql+pymysql://user:pass@host/dbname`
- Don't use SQLite in production

### 4. Enable HTTPS
Update `app.py`:
```python
@app.after_request
def set_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

---

## 🔧 Common Commands

| Command | Purpose |
|---------|---------|
| `python app.py` | Run app locally (dev mode) |
| `python -m pytest tests/ -v` | Run all tests |
| `pip install -r requirements.txt` | Install dependencies |
| `pip freeze > requirements.txt` | Update requirements |
| `git push -u aws main` | Push to CodeCommit |
| `eb deploy` | Deploy to Elastic Beanstalk |
| `gunicorn -w 4 app:create_app()` | Production server |

---

## 📞 Troubleshooting

### buildspec.yml fails at install phase
- ✅ Verify `requirements.txt` has all dependencies
- ✅ Check for private packages that need authentication

### Tests fail in CodeBuild
- ✅ Ensure `.env.example` has all required variables
- ✅ Run tests locally first: `python -m pytest tests/ -v`

### Database errors in production
- ✅ Set `DATABASE_URL` environment variable
- ✅ Run migrations before deployment
- ✅ Ensure database user has proper permissions

---

## 📚 Additional Resources

- [AWS CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/)
- [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## ✅ Summary

Your Flask application is now configured with:
- ✅ Production-ready dependencies
- ✅ AWS CodeBuild specification (Python 3.11)
- ✅ Proper `.gitignore` for Flask/Python
- ✅ Environment configuration template
- ✅ Ready for CodeCommit → CodeBuild → CodePipeline workflow

**Next Steps:**
1. Run `pip install -r requirements.txt` locally
2. Run `python -m pytest tests/ -v` to verify tests pass
3. Run `python app.py` to test locally
4. Commit and push to AWS CodeCommit
5. Set up CodeBuild project in AWS Console
6. Create CodePipeline for CI/CD automation
