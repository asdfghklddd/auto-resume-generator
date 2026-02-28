import os
import sys
import subprocess
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
        print("⚠️  Frontend is not built. Attempting to build it now...")
        frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
        try:
            print("Installing npm dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, shell=True, check=True)
            print("Building Vite project...")
            subprocess.run(["npm", "run", "build"], cwd=frontend_dir, shell=True, check=True)
            print("✅ Frontend build completely successfully!")
        except Exception as e:
            print(f"❌ Failed to build frontend: {e}")
            print("Please ensure Node.js is installed, or build the frontend manually.")
            sys.exit(1)
    
    print("✅ Starting Uvicorn API Server & Frontend Server on http://127.0.0.1:8000")
    print("="*60)
    
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
