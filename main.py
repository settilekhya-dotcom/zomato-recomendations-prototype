import sys
from phase5.main import run_final_app
from phase6.api_server import app # Entrypoint for Vercel/Deployment

if __name__ == "__main__":
    try:
        run_final_app()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
