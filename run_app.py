import os
import sys
import subprocess

def main():
    print("🚀 Initializing GyaanSetu | Desktop Edition...")
    
    # 1. Get the absolute path of the GyaanSetu folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Force the PYTHONPATH to include our base directory
    # This prevents the "ModuleNotFoundError: No module named 'config'" error
    os.environ["PYTHONPATH"] = base_dir
    
    # 3. Locate the Streamlit UI file
    app_path = os.path.join(base_dir, "ui", "app.py")
    
    if not os.path.exists(app_path):
        print(f"❌ Error: Could not find the UI file at {app_path}")
        sys.exit(1)

    print("✅ Paths configured correctly.")
    print("🧠 Starting local LLM engine interface...")
    
    # 4. Launch Streamlit programmatically
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    except KeyboardInterrupt:
        print("\n🛑 Shutting down GyaanSetu...")
        sys.exit(0)

if __name__ == "__main__":
    main()
