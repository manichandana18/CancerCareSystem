"""
Direct Browser Launch - Opens working page automatically
"""

import webbrowser
import time

def launch_working_page():
    """Launch the working page in browser"""
    
    print("🚀 LAUNCHING CANCERCARE AI WORKING PAGE")
    print("=" * 50)
    print("Opening your working cancer detection system...")
    print("=" * 50)
    
    # Try different URLs
    urls = [
        "http://127.0.0.1:8084",
        "http://localhost:8084", 
        "http://127.0.0.1:8080",
        "http://localhost:8080"
    ]
    
    for url in urls:
        try:
            print(f"🌐 Trying: {url}")
            webbrowser.open(url)
            time.sleep(2)
            print(f"✅ Opened: {url}")
            break
        except Exception as e:
            print(f"❌ Failed: {url} - {e}")
            continue
    
    print("\n" + "=" * 50)
    print("🎯 IF PAGE STILL DOESN'T LOAD:")
    print("1. Copy this URL: http://127.0.0.1:8084")
    print("2. Open browser manually")
    print("3. Paste URL and press Enter")
    print("4. Or try: http://localhost:8084")
    print("=" * 50)

if __name__ == "__main__":
    launch_working_page()
