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
    D --> E[Phase 5: Display]
    
    A1[Load Dataset] --> A2[Data Cleaning]
    A2 --> A3[Feature Engineering]
    A3 --> A4[Store in Database]
    
    B1[Web UI - HTML/CSS/JS] --> B2[Input Validation]
    B2 --> B3[Parameter Extraction]
    
    C1[Query Processing] --> C2[Filter by Locality]
    C2 --> C3[Filter by Price]
    C3 --> C4[Prepare Dataset]
    
    D1[Feature Vectorization] --> D2[Similarity Computation]
    D2 --> D3[Ranking Algorithm]
    D3 --> D4[Top-N Selection]
    
    E1[API Responses] --> E2[Zomato Glassmorphism UI]
    E2 --> E3[AI Reasoning Reasoning]
    
    F1[FastAPI Server] --> F2[Groq LLM Integration]
    F2 --> F3[Lucide Icons]
    
    A --> A1
    B --> B1
    C --> C1
    D --> D1
    E --> E1
    F --> F1
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
| **Language** | Python 3.8+ |
| **Backend** | FastAPI / Uvicorn |
| **Frontend** | Vanilla JS / CSS (Glassmorphism) |
| **AI/LLM** | Groq (Llama-3) |
| **Data Processing** | pandas, numpy |
| **Database** | SQLite |
| **Aesthetics** | Lucide Icons, Google Fonts |

---

## How to Run

### Web Application
```bash
python main.py
```
Then visit `http://localhost:8000` in your browser.
