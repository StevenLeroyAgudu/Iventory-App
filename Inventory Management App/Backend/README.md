# Cloud-Based Inventory Monitoring System — Backend

Django REST Framework backend for the Cloud Inventory Monitoring System, deployed on AWS EC2 with RDS MySQL and SNS alerts.

---

## Project Structure

```
inventory_system/
├── manage.py
├── requirements.txt
├── .env.example              ← Copy to .env and fill in your values
├── deploy.sh                 ← EC2 deployment script
├── inventory.log             ← Created at runtime
│
├── inventory_system/         ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── products/                 ← Main app
    ├── models.py             ← Product model + StockStatus
    ├── serializers.py        ← DRF serializers + validation
    ├── views.py              ← All API endpoints
    ├── urls.py               ← URL routing
    └── services/
        ├── stock_service.py  ← Status computation logic
        └── alert_service.py  ← AWS SNS integration
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| POST | `/api/products/` | Add a new product |
| GET | `/api/products/{id}/` | Get a single product |
| PUT | `/api/products/{id}/` | Update a product |
| DELETE | `/api/products/{id}/` | Delete a product |
| GET | `/api/products/low-stock/` | Products below min threshold |
| GET | `/api/products/high-stock/` | Products above max threshold |
| GET | `/api/dashboard/` | Summary statistics |

### Example: Create Product (POST /api/products/)
```json
{
  "product_name": "Laptop",
  "quantity": 5,
  "min_threshold": 10,
  "max_threshold": 100
}
```

### Example: Dashboard Response (GET /api/dashboard/)
```json
{
  "total_products": 50,
  "low_stock": 5,
  "overstock": 3,
  "normal_stock": 42
}
```

---

## Stock Status Logic

| Condition | Status | SNS Alert |
|-----------|--------|-----------|
| quantity < min_threshold | LOW | ✅ Sent |
| quantity > max_threshold | HIGH | ✅ Sent |
| Otherwise | NORMAL | ❌ None |

Status is **automatically computed** on every create/update — never set manually.

---

## Local Development Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-group/inventory-system.git
cd inventory_system

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your DB credentials and AWS keys

# 5. Run migrations
python manage.py migrate

# 6. Start dev server
python manage.py runserver
```

---

## AWS Setup Guide

### 1. RDS (MySQL Database)

1. Go to AWS Console → RDS → Create Database
2. Choose **MySQL**, Free Tier
3. Set DB name: `inventory_db`, username: `admin`
4. Set a strong password → save it in `.env`
5. In Security Group: allow port **3306 from your EC2's Security Group only**
6. Copy the **RDS Endpoint** → paste into `.env` as `DB_HOST`

### 2. SNS (Alerts)

1. Go to AWS Console → SNS → Create Topic
2. Type: **Standard**, Name: `inventory-alerts`
3. Copy the **Topic ARN** → paste into `.env` as `SNS_TOPIC_ARN`
4. Click **Create Subscription** → Protocol: Email → Enter your email
5. Confirm the subscription from your email inbox

### 3. EC2 (Backend Hosting)

1. Launch EC2 instance: **Ubuntu 22.04**, t2.micro (Free Tier)
2. Security Group: allow ports **22 (SSH)**, **80 (HTTP)**, **8000 (Gunicorn)**
3. Create/download a key pair (.pem file)
4. SSH into instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```
5. Upload project or clone from GitHub
6. Run the deploy script:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

### 4. IAM Role for EC2

1. Go to IAM → Roles → Create Role → EC2
2. Attach policies:
   - `AmazonSNSFullAccess`
   - `CloudWatchLogsFullAccess`
3. Attach this role to your EC2 instance
4. Once IAM role is attached, you can remove `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` from `.env` (more secure)

### 5. S3 (Frontend Hosting)

1. Create S3 bucket → uncheck "Block all public access"
2. Enable **Static Website Hosting** → index document: `index.html`
3. Upload your frontend HTML/CSS/JS files
4. Add your S3 website URL to `CORS_ALLOWED_ORIGINS` in `settings.py`

---

## Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key (generate a new one for production) |
| `DEBUG` | `True` for dev, `False` for production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |
| `DB_NAME` | MySQL database name (`inventory_db`) |
| `DB_USER` | RDS username |
| `DB_PASSWORD` | RDS password |
| `DB_HOST` | RDS endpoint URL |
| `DB_PORT` | MySQL port (default: `3306`) |
| `AWS_ACCESS_KEY_ID` | AWS credentials (not needed if using IAM role) |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials (not needed if using IAM role) |
| `AWS_REGION` | AWS region (e.g., `us-east-1`) |
| `SNS_TOPIC_ARN` | Full ARN of your SNS topic |

---

## Implementation Checklist

- [x] Product Model
- [x] CRUD API
- [x] Low Stock Endpoint
- [x] High Stock Endpoint
- [x] Dashboard Endpoint
- [x] Stock Status Logic (auto-computed)
- [x] SNS Alert Integration
- [x] MySQL (RDS) Connection
- [x] Environment Variables
- [x] Logging
- [ ] EC2 Deployment ← Do this on your AWS account
- [ ] RDS Setup ← Do this on your AWS account
- [ ] SNS Topic + Subscription ← Do this on your AWS account
