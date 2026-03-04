"""
Enigma LIMS — Desktop Launcher
Double-click this (or EnigmaLIMS.exe) to start the lab system offline.
Opens your browser automatically at http://127.0.0.1:8080
"""

import sys
import os
import time
import threading
import webbrowser

PORT = 8080


def resource_path(relative):
    """Works both in development and when bundled by PyInstaller."""
    try:
        base = sys._MEIPASS  # PyInstaller extracts files here at runtime
    except AttributeError:
        base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, relative)


def start_server():
    backend_dir = resource_path('backend')
    frontend_dir = resource_path('docs')

    # Tell FastAPI where to find the frontend for static file serving
    os.environ['LIMS_FRONTEND_DIR'] = frontend_dir

    # Add backend to Python path and switch to it
    sys.path.insert(0, backend_dir)
    os.chdir(backend_dir)

    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=PORT,
        log_level="warning",
        access_log=False,
    )


def open_browser():
    time.sleep(2.5)
    webbrowser.open(f'http://127.0.0.1:{PORT}/index.html')


if __name__ == '__main__':
    print("=" * 60)
    print("  Enigma LIMS — Desktop")
    print(f"  Starting on http://127.0.0.1:{PORT}")
    print("  Your browser will open automatically.")
    print("  Keep this window open while using the system.")
    print("  Close this window to stop the server.")
    print("=" * 60)

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    start_server()
