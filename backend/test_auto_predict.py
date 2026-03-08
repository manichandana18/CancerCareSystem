import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_auto_predict.py <image_path> [url]")
        print("Example: python test_auto_predict.py sample_xray.jpg http://127.0.0.1:8000")
        raise SystemExit(2)

    image_path = sys.argv[1]
    base_url = sys.argv[2] if len(sys.argv) >= 3 else "http://127.0.0.1:8000"

    try:
        import requests
    except Exception:
        print("Missing dependency: requests")
        print("Install it in your backend venv: pip install requests")
        raise SystemExit(3)

    with open(image_path, "rb") as f:
        files = {"file": (image_path, f, "application/octet-stream")}
        resp = requests.post(f"{base_url}/predict/auto", files=files, timeout=120)

    print("Status:", resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)


if __name__ == "__main__":
    main()
