from app import create_app
import urllib.request
import ssl

app = create_app()
client = app.test_client()

print("--- 1. Testing Local Endpoints ---")
resp_priv = client.get('/privacy')
print(f"Local /privacy status: {resp_priv.status_code}")
assert resp_priv.status_code == 200, f"Expected 200, got {resp_priv.status_code}"
assert b"SkillSwap Campus - Privacy Policy" in resp_priv.data, "Title missing in HTML"
print("Local /privacy: PASS (HTML returned successfully)")

resp_health = client.get('/health')
print(f"Local /health status: {resp_health.status_code}")
assert resp_health.status_code == 200, f"Expected 200, got {resp_health.status_code}"
print("Local /health: PASS")

print("\n--- 2. Testing Production Render Endpoints ---")
ctx = ssl.create_default_context()
try:
    req = urllib.request.Request('https://skillswap-campus-api.onrender.com/health', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        print(f"Production /health status: {r.status} (OK)")
except Exception as e:
    print(f"Production /health: {e}")

try:
    req2 = urllib.request.Request('https://skillswap-campus-api.onrender.com/privacy', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req2, timeout=10, context=ctx) as r2:
        print(f"Production /privacy status: {r2.status} (Deployed)")
except urllib.error.HTTPError as e:
    print(f"Production /privacy returned HTTP {e.code} (Status: REQUIRES DEPLOYMENT TO RENDER)")
except Exception as e:
    print(f"Production /privacy check: {e} (Status: REQUIRES DEPLOYMENT TO RENDER)")
