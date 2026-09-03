"""
Phase 12 Complete End-to-End Automated Test Suite for SkillSwap Campus
Uses Python standard library (urllib, http.cookiejar, json) to test the live API server.
"""
import sys
import os
import time
import json
import urllib.request
import urllib.parse
import http.cookiejar

BASE_URL = "http://127.0.0.1:5000"

results = {}

def log_test(name, passed, detail=""):
    results[name] = {"passed": passed, "detail": detail}
    status_str = "PASS" if passed else "FAIL"
    print(f"[{status_str}] {name}: {detail}")

class ApiClient:
    def __init__(self):
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))

    def request(self, method, path, data=None):
        url = f"{BASE_URL}{path}"
        req_data = None
        headers = {}
        if data is not None:
            req_data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        try:
            with self.opener.open(req) as resp:
                status = resp.status
                body = resp.read().decode('utf-8')
                try:
                    res_json = json.loads(body)
                except Exception:
                    res_json = body
                return status, res_json
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8')
            try:
                res_json = json.loads(body)
            except Exception:
                res_json = body
            return e.code, res_json
        except Exception as e:
            return 0, str(e)

    def get(self, path):
        return self.request('GET', path)

    def post(self, path, data=None):
        return self.request('POST', path, data)

def run_tests():
    print("==================================================")
    print("STARTING PHASE 12 END-TO-END VERIFICATION")
    print("==================================================")

    client_anon = ApiClient()

    # 1. Backend Health Test
    status, body = client_anon.get("/api/health")
    if status == 200 and isinstance(body, dict) and body.get("database") == "connected":
        log_test("1. Backend Health & DB Connection", True, "Local Flask API and PostgreSQL connected successfully.")
    else:
        log_test("1. Backend Health & DB Connection", False, f"Unexpected response: {status} {body}")

    # Test Public Render Endpoint
    try:
        req = urllib.request.Request("https://skillswap-campus-api.onrender.com/api/health")
        with urllib.request.urlopen(req, timeout=10) as resp:
            public_msg = f"Reachable (Status {resp.status})"
    except Exception as e:
        public_msg = f"Unreachable: {str(e)}"
    print(f"[*] Public Host Info: https://skillswap-campus-api.onrender.com/api/health -> {public_msg}")

    # 2. Authentication Test
    alice = ApiClient()
    bob = ApiClient()
    ts = int(time.time())
    alice_email = f"alice_{ts}@campus.edu"
    bob_email = f"bob_{ts}@campus.edu"

    # Register Alice
    s_a, b_a = alice.post("/api/auth/register", {
        "name": "Alice Smith",
        "email": alice_email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "major": "Computer Science",
        "grad_year": 2026,
        "bio": "Python enthusiast."
    })
    alice_registered = (s_a == 201)

    # Register Bob
    s_b, b_b = bob.post("/api/auth/register", {
        "name": "Bob Jones",
        "email": bob_email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "major": "Mathematics",
        "grad_year": 2027,
        "bio": "Calculus tutor."
    })
    bob_registered = (s_b == 201)

    # Duplicate registration test
    s_dup, _ = client_anon.post("/api/auth/register", {
        "name": "Alice Dup",
        "email": alice_email,
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    dup_blocked = (s_dup == 409)

    # Invalid login test
    s_bad, _ = client_anon.post("/api/auth/login", {
        "email": alice_email,
        "password": "WrongPassword!"
    })
    bad_login_blocked = (s_bad == 401)

    # Login Alice
    s_al, _ = alice.post("/api/auth/login", {
        "email": alice_email,
        "password": "Password123!"
    })
    alice_logged_in = (s_al == 200)

    # Profile & Session persistence check
    s_ap, b_ap = alice.get("/api/auth/me")
    alice_prof_ok = (s_ap == 200 and isinstance(b_ap, dict) and b_ap.get("email") == alice_email)
    alice_id = b_ap.get("id") if alice_prof_ok else None

    # Login Bob
    s_bl, _ = bob.post("/api/auth/login", {
        "email": bob_email,
        "password": "Password123!"
    })
    s_bp, b_bp = bob.get("/api/auth/me")
    bob_prof_ok = (s_bp == 200 and isinstance(b_bp, dict) and b_bp.get("email") == bob_email)
    bob_id = b_bp.get("id") if bob_prof_ok else None

    auth_passed = (alice_registered and bob_registered and dup_blocked and 
                   bad_login_blocked and alice_logged_in and alice_prof_ok and bob_prof_ok)
    log_test("2. Authentication (Register, Login, Duplicate, Session)", auth_passed,
             f"Alice ID: {alice_id}, Bob ID: {bob_id}")

    # 3. Skills Test
    s_sk, b_sk = client_anon.get("/api/skills")
    all_skills = b_sk if isinstance(b_sk, list) else b_sk.get("skills", [])
    python_skill = next((s for s in all_skills if "Python" in s.get("name", "")), None)
    math_skill = next((s for s in all_skills if "Calculus" in s.get("name", "")), None)

    # Alice teaches Python, wants Calculus
    s_au, b_au = alice.post("/api/onboarding/skills", {
        "teach": [{"skill_id": python_skill["id"], "proficiency": "advanced"}],
        "learn": [{"skill_id": math_skill["id"], "proficiency": "beginner"}]
    })

    # Bob teaches Calculus, wants Python
    s_bu, b_bu = bob.post("/api/onboarding/skills", {
        "teach": [{"skill_id": math_skill["id"], "proficiency": "advanced"}],
        "learn": [{"skill_id": python_skill["id"], "proficiency": "intermediate"}]
    })

    skills_passed = (len(all_skills) >= 12 and python_skill is not None and math_skill is not None and s_au == 200 and s_bu == 200)
    log_test("3. Skills Catalog & User Profile Skills", skills_passed,
             f"{len(all_skills)} catalog skills available. Portfolios updated successfully.")

    # 4. Matching Test
    s_m, b_m = alice.get("/api/matches")
    matches_alice = b_m if isinstance(b_m, list) else b_m.get("matches", [])
    bob_match = next((m for m in matches_alice if m.get("user", {}).get("id") == bob_id), None)
    is_reciprocal = bob_match and (bob_match.get("reciprocal") is True or bob_match.get("match_type") == "reciprocal")
    
    log_test("4. Matching System (Reciprocal & Compatibility)", bool(bob_match and is_reciprocal),
             f"Reciprocal match found with match_score {bob_match.get('match_score') if bob_match else 'None'}")

    # 5. Swap Request Test
    s_sr, b_sr = alice.post("/api/swap-requests", {
        "receiver_id": bob_id,
        "teach_skill_id": python_skill["id"],
        "learn_skill_id": math_skill["id"],
        "message": "Hi Bob, let's swap Python for Calculus!"
    })
    swap_id = b_sr.get("id") if isinstance(b_sr, dict) else None

    # Bob views incoming
    _, b_bi = bob.get("/api/swap-requests")
    bob_incoming = b_bi.get("incoming", []) if isinstance(b_bi, dict) else []
    bob_has_req = any(r.get("id") == swap_id for r in bob_incoming)

    # Alice views outgoing
    _, b_ao = alice.get("/api/swap-requests")
    alice_outgoing = b_ao.get("outgoing", []) if isinstance(b_ao, dict) else []
    alice_has_req = any(r.get("id") == swap_id for r in alice_outgoing)

    # Bob accepts
    s_acc, b_acc = bob.post(f"/api/swap-requests/{swap_id}/respond", {"action": "accept"})
    req_accepted = (s_acc == 200 and isinstance(b_acc, dict) and b_acc.get("status") == "accepted")

    log_test("5. Swap Requests (Send, View, Accept, Status)", bool(swap_id and bob_has_req and alice_has_req and req_accepted),
             f"SwapRequest #{swap_id} created and accepted.")

    # 6. Session Creation & Credit Hold Test
    s_sch, b_sch = alice.post("/api/sessions", {
        "request_id": swap_id,
        "teacher_id": alice_id,
        "learner_id": bob_id,
        "skill_id": python_skill["id"],
        "scheduled_at": "2026-09-04 14:00:00",
        "duration_hours": 1.0,
        "venue": "Campus Library Room 3B"
    })
    session_id = b_sch.get("id") if isinstance(b_sch, dict) else None

    # View sessions
    _, b_ses = alice.get("/api/sessions")
    alice_sessions = b_ses if isinstance(b_ses, list) else []
    session_found = any(s.get("id") == session_id for s in alice_sessions)

    # Open session details
    _, b_dt = alice.get(f"/api/sessions/{session_id}")
    sched_valid = (b_dt.get("status") == "scheduled" if isinstance(b_dt, dict) else False)

    # Complete session
    s_cmp, b_cmp = alice.post(f"/api/sessions/{session_id}/respond", {"action": "complete"})
    comp_ok = (s_cmp == 200 and isinstance(b_cmp, dict) and b_cmp.get("status") == "completed")

    # Double-spend protection test
    s_dc, _ = alice.post(f"/api/sessions/{session_id}/respond", {"action": "complete"})
    double_spend_protected = (s_dc == 409)

    log_test("6. Session Scheduling & State Machine", bool(session_id and session_found and sched_valid and comp_ok and double_spend_protected),
             f"Session #{session_id} scheduled, completed, and double-action protected.")

    # 7. Credit Ledger & Non-negative Balances Test
    _, b_ap_after = alice.get("/api/auth/me")
    _, b_bp_after = bob.get("/api/auth/me")
    
    alice_bal = float(b_ap_after.get("credit_balance", 0))
    bob_bal = float(b_bp_after.get("credit_balance", 0))
    # Alice started with 2.0, earned 1.0 -> 3.0
    # Bob started with 2.0, spent 1.0 -> 1.0
    credit_math_ok = (alice_bal == 3.0 and bob_bal == 1.0)

    log_test("7. Credit Balance & Ledger Auditing", credit_math_ok,
             f"Alice Balance: {alice_bal} (was 2.0, +1.0 earned), Bob Balance: {bob_bal} (was 2.0, -1.0 spent)")

    # 8. Double-Blind Review Test
    s_ra, b_ra = alice.post("/api/reviews", {
        "session_id": session_id,
        "rating": 5,
        "comment": "Bob was an eager and sharp learner!"
    })
    alice_blind = (s_ra == 201 and b_ra.get("is_visible") is False)

    # Check public reviews for Bob before he reviews (should be 0)
    _, b_rb_bef = client_anon.get(f"/api/reviews/user/{bob_id}")
    bob_blind_ok = (len(b_rb_bef.get("reviews", [])) == 0)

    # Bob reviews Alice
    s_rb, b_rb = bob.post("/api/reviews", {
        "session_id": session_id,
        "rating": 5,
        "comment": "Alice explained algorithms exceptionally well!"
    })
    bob_unlock = (s_rb == 201 and b_rb.get("is_visible") is True)

    # Check public reviews after mutual submission (both should now have 1 review)
    _, b_rb_aft = client_anon.get(f"/api/reviews/user/{bob_id}")
    _, b_ra_aft = client_anon.get(f"/api/reviews/user/{alice_id}")
    mutual_visible = (len(b_rb_aft.get("reviews", [])) == 1 and len(b_ra_aft.get("reviews", [])) == 1)

    review_passed = (alice_blind and bob_blind_ok and bob_unlock and mutual_visible)
    log_test("8. Double-Blind Review Workflow", review_passed,
             f"Blind lock verified. Both reviews unlocked on mutual submission.")

    # 9. Notification Test
    _, b_nb = bob.get("/api/notifications")
    _, b_na = alice.get("/api/notifications")
    notifs_bob = b_nb.get("notifications", []) if isinstance(b_nb, dict) else []
    notifs_alice = b_na.get("notifications", []) if isinstance(b_na, dict) else []
    has_notifs = (len(notifs_bob) > 0 and len(notifs_alice) > 0)

    read_ok = False
    if has_notifs:
        notif_id = notifs_bob[0]["id"]
        s_nr, _ = bob.post(f"/api/notifications/{notif_id}/read")
        read_ok = (s_nr == 200)

    log_test("9. User Notifications & Read Status", bool(has_notifs and read_ok),
             f"Notifications generated and marked read. Alice: {len(notifs_alice)}, Bob: {len(notifs_bob)}")

    print("==================================================")
    all_passed = all(r["passed"] for r in results.values())
    print(f"OVERALL BACKEND SUITE RESULT: {'ALL PASS' if all_passed else 'SOME FAILED'}")
    print("==================================================")
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
