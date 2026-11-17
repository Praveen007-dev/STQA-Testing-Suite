import subprocess
import time
import urllib.request
import urllib.error

print("🚀 STEP 1: Starting FastAPI server with White-Box Coverage...")
# Start the server in the background
server = subprocess.Popen(
    ["coverage", "run", "--source=main", "--branch", "-m", "uvicorn", "main:app"]
)

# Wait 3 seconds to ensure the server is fully booted up
time.sleep(3)

print("\n🧪 STEP 2: Running Playwright API Tests...")
subprocess.run(["pytest", "test_api.py", "--html=report.html", "--self-contained-html"])

print("\n🛑 STEP 3: Shutting down server gracefully to save coverage data...")
try:
    # Ping the shutdown endpoint
    req = urllib.request.Request("http://127.0.0.1:8000/shutdown", method="POST")
    urllib.request.urlopen(req)
except Exception:
    # Safely catch any Windows network disconnection quirks during shutdown
    pass

# Wait for the server to finish shutting down and write the .coverage file
server.wait()

print("\n📊 STEP 4: Generating White-Box Reports...")
subprocess.run(["coverage", "html"])

# Print a quick summary directly in the terminal
subprocess.run(["coverage", "report", "-m"]) 

print("\n✅ PIPELINE COMPLETE!")
print("➡️  Execution & Assertions Report: report.html")
print("➡️  White-Box Coverage Report: htmlcov/index.html")