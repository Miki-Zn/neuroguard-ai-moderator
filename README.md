# NeuroGuard: AI-Powered Content Moderation API

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Django Version](https://img.shields.io/badge/django-5.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📖 Overview
NeuroGuard is a high-performance, asynchronous SaaS backend designed for automated content moderation. Built with scalability in mind, it leverages **OpenAI** to analyze user-generated content (text and images) in real-time, protecting platforms from spam, hate speech, and harassment. 

This project demonstrates production-ready backend architecture, including background task processing, real-time webhooks, and advanced SQL aggregations.

## ✨ Key Features
- **AI-Driven Analysis:** Automated detection of policy violations using OpenAI's GPT models.
- **Asynchronous Processing:** Non-blocking architecture using **Celery** and **Redis** for handling high-volume moderation queues.
- **Webhook Dispatch System:** Real-time callbacks to client applications upon completion of asynchronous AI analysis.
- **Robust Authentication & Throttling:** JWT-based user authentication with tier-based API Rate Limiting (Free vs. Pro).
- **Advanced Analytics:** Complex database-level aggregations (Django ORM) providing 7-day trend analysis and moderation metrics.
- **CI/CD & Testing:** Automated testing pipeline using GitHub Actions, PyTest, and Flake8.
- **Interactive Documentation:** Fully documented REST endpoints via OpenAPI 3 (Swagger UI & ReDoc).

## 🛠 Tech Stack
- **Core:** Python 3.11, Django 5.0, Django REST Framework
- **Task Queue:** Celery, Redis
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose
- **Testing:** PyTest, PyTest-Django
- **Third-Party APIs:** OpenAI API

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.
- An active OpenAI API Key.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Miki-Zn/neuroguard-ai-moderator.git](https://github.com/Miki-Zn/neuroguard-ai-moderator.git)
   cd neuroguard-ai-moderator
   ```

2. **Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```ini
   DEBUG=True
   SECRET_KEY=your-super-secret-key
   DATABASE_URL=postgres://postgres:postgres@db:5432/neuroguard_db
   REDIS_URL=redis://redis:6379/0
   OPENAI_API_KEY=sk-your-real-openai-api-key
   ```

3. **Build and Run with Docker:**
   ```bash
   docker-compose up --build -d
   ```

4. **Run Migrations:**
   ```bash
   docker-compose run --rm web python manage.py migrate
   ```

5. **Create a Superuser (Optional but recommended):**
   ```bash
   docker-compose run --rm web python manage.py createsuperuser
   ```

## 📚 API Documentation
Once the server is running, you can interact with the API via the auto-generated OpenAPI documentation:
- **Swagger UI:** `http://localhost:8000/api/docs/swagger/`
- **ReDoc:** `http://localhost:8000/api/docs/redoc/`

## 🧪 Running Tests
This project uses `pytest` for unit testing. To run the test suite inside the Docker container:
```bash
docker-compose run --rm web pytest
```