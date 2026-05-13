# AWS CI/CD Setup - File Placement & Quick Reference

## 📁 Complete File Structure After Setup

```
cicd/
├── app.py                          # ✅ Flask factory pattern entry point
├── wsgi.py                         # ✅ WSGI server entry point (NEW)
├── requirements.txt                # ✅ Python dependencies (UPDATED)
├── buildspec.yml                   # ✅ AWS CodeBuild config (UPDATED)
├── Dockerfile                      # ✅ Container image config (NEW)
├── .gitignore                      # ✅ Git exclusions (NEW)
├── .env.example                    # ✅ Environment template (NEW)
├── .dockerignore                   # ✅ Docker build exclusions (NEW)
├── .ebextensions/
│   └── python.config               # ✅ Elastic Beanstalk config (NEW)
├── setup.sh                        # ✅ Setup script - Linux/macOS (NEW)
├── setup.bat                       # ✅ Setup script - Windows (NEW)
├── AWS_SETUP_GUIDE.md              # ✅ Complete setup guide (NEW)
├── README.md                       # Existing documentation
├── config/
│   └── __init__.py                # Config module
├── models/
│   ├── __init__.py
│   └── models.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── main.py
│   └── admin.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/
├── templates/
│   └── *.html files
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_app.py
└── instance/                       # Flask instance folder (not committed)
```

---

## 🚀 Quick Start Commands

### Local Development (Windows)
```batch
# Run setup script (one-time setup)
setup.bat

# Manual setup if needed:
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
python app.py
```

### Local Development (macOS/Linux)
```bash
# Run setup script (one-time setup)
bash setup.sh

# Manual setup if needed:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_app.py -v

# Run with coverage
python -m pytest tests/ --cov
```

### Production (Local Testing)
```bash
# Install Gunicorn if not already installed
pip install gunicorn

# Run with Gunicorn (production server)
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# Access at http://localhost:5000
```

---

## 🐳 Docker Deployment (Local Testing)

### Build Docker Image
```bash
docker build -t campus-lost-found:latest .
```

### Run Docker Container
```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  campus-lost-found:latest
```

---

## 📤 AWS Deployment Pipeline

### 1. Configure AWS CLI (One-Time)
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
# Enter default output format (json)
```

### 2. Create CodeCommit Repository
```bash
aws codecommit create-repository \
  --repository-name campus-lost-found \
  --description "Flask Lost & Found Application"
```

### 3. Clone and Push Code
```bash
# Clone the repo
git clone <codecommit-url> campus-lost-found
cd campus-lost-found

# Add your code
git add .
git commit -m "Initial Flask application setup"
git push origin main
```

### 4. Create CodeBuild Project (AWS Console)
1. Go to AWS CodeBuild → Create Build Project
2. Name: `campus-lost-found-build`
3. Source: AWS CodeCommit
4. Repository: `campus-lost-found`
5. Environment: Managed image
   - Operating system: Amazon Linux 2
   - Runtime: Python
   - Image: aws/codebuild/standard:7.0
   - Compute type: Small
6. Buildspec: Use `buildspec.yml` in repository ✅
7. Service role: Create new (or use existing)
8. Create build project

### 5. Create CodePipeline (AWS Console)
1. Go to AWS CodePipeline → Create Pipeline
2. Pipeline name: `campus-lost-found-pipeline`
3. Service role: Create new
4. **Source Stage:**
   - Source provider: AWS CodeCommit
   - Repository: campus-lost-found
   - Branch: main
5. **Build Stage:**
   - Build provider: AWS CodeBuild
   - Project name: campus-lost-found-build
6. **Deploy Stage (Optional):**
   - Deployment provider: Choose one:
     - AWS Elastic Beanstalk
     - AWS EC2
     - AWS ECS
7. Review and create pipeline

### 6. Deploy to Elastic Beanstalk (Recommended)
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB environment
eb init -p python-3.11 campus-lost-found --region us-east-1

# Create environment
eb create campus-lost-found-prod

# Deploy
eb deploy

# Monitor
eb logs
```

---

## 🔑 Environment Variables Checklist

### Local Development (.env)
```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///campus_lost_found.db
```

### AWS Production (.env or CloudFormation/Secrets Manager)
```env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=<use-strong-random-key-from-AWS-Secrets-Manager>
DATABASE_URL=<RDS-PostgreSQL-connection-string>
AWS_REGION=us-east-1
```

**Generate strong SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🔐 AWS Permissions Required

### CodeBuild Service Role Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudWatchLogsAccess",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Sid": "CodeCommitAccess",
      "Effect": "Allow",
      "Action": [
        "codecommit:GitPull"
      ],
      "Resource": "arn:aws:codecommit:*:*:campus-lost-found"
    },
    {
      "Sid": "S3Artifacts",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::*/*"
    }
  ]
}
```

---

## 📋 Pre-Deployment Verification

- [ ] Local tests pass: `python -m pytest tests/ -v`
- [ ] App runs locally: `python app.py` → http://localhost:5000
- [ ] Gunicorn runs: `gunicorn -w 4 wsgi:app`
- [ ] Docker image builds: `docker build -t app:latest .`
- [ ] .env.example has all required variables
- [ ] No hardcoded secrets in code
- [ ] Database migrations ready
- [ ] Static files configured correctly
- [ ] requirements.txt has all dependencies
- [ ] buildspec.yml syntax valid (can validate in CodeBuild console)

---

## 📊 CI/CD Pipeline Status Monitoring

### View CodeBuild Logs
```bash
aws codebuild batch-get-builds \
  --ids <build-id> \
  --query 'builds[0].logs'
```

### View Pipeline Status
```bash
aws codepipeline get-pipeline-state \
  --name campus-lost-found-pipeline
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| CodeBuild fails at install | Check `requirements.txt` has all dependencies |
| Tests fail in CodeBuild | Run locally first: `python -m pytest tests/ -v` |
| Database errors | Set `DATABASE_URL` env var, ensure migrations run |
| Static files not served | Check `static/` path in Elastic Beanstalk config |
| 502 Bad Gateway on deployment | Check WSGI path is `wsgi:app` |
| buildspec.yml syntax error | Validate YAML: [yamllint.com](https://www.yamllint.com/) |

---

## 📞 Next Steps

1. ✅ Review all generated files
2. ✅ Run `setup.bat` or `setup.sh`
3. ✅ Test locally: `python app.py`
4. ✅ Push to CodeCommit
5. ✅ Create CodeBuild project in AWS
6. ✅ Create CodePipeline in AWS
7. ✅ Monitor pipeline execution

---

**Last Updated:** $(date)
**Python Version:** 3.11
**Flask Version:** 2.3.3
