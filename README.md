# Zomato AI Restaurant Recommender - Bangalore City

An AI-powered restaurant recommendation system that uses the Zomato dataset and Groq LLM to provide personalized suggestions with premium glassmorphism styling.

## 🚀 Features

- **Premium Web UI**: Stunning glassmorphism design with dynamic background blobs and Lucide icons (available in both FastAPI/HTML and Streamlit).
- **AI-Powered Reasoning**: Uses Large Language Models (LLMs) via the Groq API to explain *why* a restaurant matches your preferences.
- **Multiple Interfaces**: Choose between a high-performance FastAPI/Vanilla JS frontend or a streamlined Streamlit dashboard.
- **Smart Filtering**: Filter by locality (30 areas in Bangalore), price range, cuisines, and minimum ratings.
- **Real-time Stats**: Displays the scale of the dataset (Localities and Cuisines covered).

## 🛠️ Tech Stack

- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (ES6+), **Streamlit**
- **Backend**: FastAPI, Uvicorn
- **AI/LLM**: Groq (Llama 3.3)
- **Database**: SQLite (SQLAlchemy ORM)
- **Styling**: Google Fonts (Outfit), Lucide Icons

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd zomato-2
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

### Option 1: Streamlit Dashboard (Recommended)
```bash
python -m streamlit run streamlit_dashboard/app.py
```

### Option 2: FastAPI + Vanilla JS Web App
Launch the application:
```bash
python main.py
```
Then visit **[http://localhost:8000](http://localhost:8000)** in your browser.

## 📐 Architecture

Detailed technical architecture can be found in [architecture.md](architecture.md).

## 📂 Project Structure

- `streamlit_dashboard/app.py`: The Streamlit dashboard entry point.
- `frontend/`: Web UI files for the FastAPI version (HTML, CSS, JS).
- `phase6/`: FastAPI server implementation.
- `phase1-5/`: Core logic modules (Data processing, Validation, Engine, Recommender, Feedback).
- `data/`: Database storage.
- `main.py`: Entry point for the FastAPI application.

## 📄 License
MIT License
