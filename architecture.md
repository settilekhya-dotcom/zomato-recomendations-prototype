# Zomato AI Restaurant Recommendation Service - Architecture
> **Helping you find the best places to eat in bangalore city**

## Overview

This document outlines the architecture for an AI-powered restaurant recommendation service using the Zomato dataset. The system accepts user inputs (locality and price range) and provides personalized restaurant recommendations through a modern glassmorphism web interface and an AI reasoning layer.

## Dataset

**Source**: [Zomato Restaurant Recommendation Dataset](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)

**Loading Method**:
```python
from datasets import load_dataset
ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
```

---

## System Architecture

```mermaid
graph TD
    A[Phase 1: Data Input] --> B[Phase 2: User Input]
    B --> C[Phase 3: Integration]
    C --> D[Phase 4: Recommendation]
    D --> E[Phase 5: Display & Feedback]
    E --> F[Phase 6: API Layer]
    
    A1[Load Dataset] --> A2[Data Cleaning]
    A2 --> A3[Store in SQLite]
    
    B1[Input Validation] --> B2[Pydantic Models]
    
    C1[Query Processing] --> C2[Recommendation Engine]
    
    D1[Groq LLM Integration] --> D2[AI Reasoning]
    
    E1[Streamlit UI] --> E3[User Feedback]
    E2[FastAPI/HTML UI] --> E3
    
    F1[FastAPI Server] --> F2[REST Endpoints]
```

---

## Phase-wise Development Plan

### **PHASE 1: Input the Zomato Data**
**Objective**: Load, process, and prepare the Zomato dataset for the recommendation system.

### **PHASE 2: User Input**
**Objective**: Create an interface to capture user preferences (locality and price range).

### **PHASE 3: Integration**
**Objective**: Connect user input with the dataset to filter and prepare relevant restaurants.

### **PHASE 4: Recommendation (AI Reasoning)**
**Objective**: Implement AI-powered recommendation algorithm to suggest best restaurants and provide reasoning via Groq LLM.

### **PHASE 5: Display & Frontend**
**Objective**: Present recommendations in a premium glassmorphism web format and collect feedback.

### **PHASE 6: API Layer**
**Objective**: Expose the logic via FastAPI to serve the modern frontend.

---

## Project Structure

```
zomato-2/
├── data/
│   └── database/               # SQLite database file
├── frontend/                   # Modern Web UI (HTML, CSS, JS)
│   ├── index.html              # Main UI structure
│   ├── style.css               # Glassmorphism styling
│   └── app.js                  # Frontend logic & API calls
├── phase1/                     # Data processing
├── phase2/                     # Input validation & models
├── phase3/                     # Filtering engine
├── phase4/                     # AI Recommender & Groq integration
├── phase6/                     # FastAPI Server logic
├── main.py                     # Project entry point (Uvicorn)
├── requirements.txt            # Python dependencies
└── architecture.md             # System documentation
```

---

## Key Technologies Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.9+ |
| **UIs** | Streamlit, Vanilla JS/HTML5 |
| **Backend** | FastAPI / Uvicorn |
| **AI/LLM** | Groq (Llama-3.3-70b) |
| **Data Processing** | pandas, datasets |
| **Database** | SQLite |
| **Styling** | Glassmorphism CSS, Lucide Icons |

---

### Streamlit Dashboard (Recommended)
```bash
streamlit run streamlit_app.py
```

### FastAPI Web Application
```bash
python main.py
```
Then visit `http://localhost:8000` in your browser.
