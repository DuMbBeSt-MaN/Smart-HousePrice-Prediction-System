import sys
import os
from pathlib import Path

# Unset SSL_CERT_FILE if it points to a non-existent file (common in conda envs)
ssl_cert = os.environ.get("SSL_CERT_FILE")
if ssl_cert and not Path(ssl_cert).exists():
    print(f"[run.py] Unsetting broken SSL_CERT_FILE: {ssl_cert}")
    del os.environ["SSL_CERT_FILE"]

# Load .env before anything else — absolute path so uvicorn reloader inherits it
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
