# Smart Government Services Recommendation Engine

AI-powered backend engine that prioritizes government services using multi-factor scoring (urgency, seasonality, importance, behavior) – built with FastAPI and Python

> Built as an independent project by **Ghadeer Sameer**.

---

## Overview

It is a backend recommendation engine that analyzes government services and identifies which actions users should prioritize first.

This system was built to solve a real problem:

> Citizens forget service renewals, face fines, and struggle to track dozens of government services.

It fixes that by turning information into **actionable intelligence**.

---

## What It Does

✅ Calculates a priority score for each service  
✅ Explains why the service is important  
✅ Ranks services from urgent → low priority  
✅ Returns structured data to any frontend  
✅ Generates SMS-style alerts (mocked)

---

## Recommendation Logic

BioSync uses a **rule-based AI scoring system**.

### Final score formula:

Final Score =  
(Urgency × 40%) +  
(Seasonality × 25%) +  
(Category Importance × 20%) +  
(User Activity × 15%)

---

## How Scores Are Computed

### Urgency
Higher score for fewer days remaining.

### Seasonality
Services in peak seasons (e.g., travel) receive additional weight.

### Category Importance
Critical services (identity, travel) are ranked higher.

### User Activity
Active users receive increased priority weighting.

---

## Priority Levels

| Score Range | Priority |
|--------------|----------|
| 80–100 | 🔴 Critical |
| 65–79 | 🟡 High |
| 50–64 | 🟢 Medium |
| < 50 | ⚪ Low |

---

## Tech Stack

| Layer | Technology |
|--------|------------|
| Backend | FastAPI |
| AI Logic | Python |
| Validation | Pydantic |
| Database | Mock JSON |
| Deployment | Local / Docker-ready |
| API Docs | Swagger UI |

---

## API Endpoints

### POST `/api/recommendations`

Returns ranked services.

### Example Request:
```json
{
  "user": {
    "id": 1,
    "name": "Ghadeer Sameer",
    "activity_level": "high",
    "phone": "+966500000000"
  },
  "services": [
    {
      "service_id": 101,
      "name": "Passport Renewal",
      "days_left": 28,
      "seasonality": "in_season",
      "category_importance": 0.9
    }
  ],
  "top_n": 5
}
```

### Example Response:
```json
{
  "top_recommendation": {
    "service_name": "Passport Renewal",
    "final_score": 87,
    "priority": "Critical",
    "reasons": [
      "Expires soon",
      "High-demand season",
      "Frequently used category"
    ]
  }
}
```

### GET `/api/health`
Health check endpoint.

---

## Project Structure

```
biosync-backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── scoring.py
│   │   └── recommender.py
│   ├── api/
│   │   └── routes.py
│   ├── models/
│   │   └── schemas.py
│   └── data/
│       └── mock_users.json
├── test_scoring.py
├── test_recommender.py
├── requirements.txt
```

---

## Run Tests

```
python test_scoring.py
python test_recommender.py
```

---

## Run Backend Server

### Step 1: Create virtual environment
```
python -m venv venv
```

### Step 2: Activate

Windows:
```
venv\Scripts\activate
```

Mac/Linux:
```
source venv/bin/activate
```

### Step 3: Install dependencies
```
pip install -r requirements.txt
```

### Step 4: Start FastAPI server
```
uvicorn app.main:app --reload
```

### Step 5: Open API Docs
Open in browser:
```
http://localhost:8000/docs
```

---

## Future Plans

- PostgreSQL integration  
- Machine learning model  
- SMS integration  
- Authentication  
- Admin dashboard  

---

## 👩‍💻 Author

**Ghadeer Sameer**  
Backend & AI Engineer  

📧 Email: Ghadeer.55.s@outlook.com  
🐙 GitHub: https://github.com/rGhadeer52  
💼 LinkedIn: https://linkedin.com/in/GhadeerSamir  

---

## Note

This repository reflects **only my individual work**.  
There are no team contributions.

---

## 📄 License

MIT License