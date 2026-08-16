import os
import sys
import uvicorn

def main():
    print("="*60)
    print("🚀 Auto Resume Generator")
    print("="*60)
    
    # Simple check if dependencies are installed
    try:
        import fastapi
    except ImportError:
        print("❌ FastAPI is not installed. Run: pip install -r requirements.txt")
        sys.exit(1)
        
    frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")
    
    if not os.path.exists(frontend_dist):
        print("Frontend build not found. Run 'npm ci' and 'npm run build' in frontend/ first.")
        sys.exit(1)
    
    print("✅ Starting Uvicorn API Server & Frontend Server on http://127.0.0.1:8000")
    print("="*60)
    
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
