from flask import Blueprint, jsonify, render_template_string
from app.extensions import db

health_bp = Blueprint('health', __name__)

PRIVACY_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkillSwap Campus - Privacy Policy</title>
    <style>
        :root {
            --bg: #0f172a;
            --surface: #1e293b;
            --surface-card: #334155;
            --primary: #6366f1;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #14b8a6;
            --border: #475569;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            padding: 24px 16px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px 24px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        .header {
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 24px;
        }
        h1 {
            color: var(--text-main);
            font-size: 28px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .badge {
            display: inline-block;
            background: var(--primary);
            color: #fff;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 12px;
            margin-top: 8px;
        }
        .meta {
            color: var(--text-muted);
            font-size: 14px;
            margin-top: 6px;
        }
        h2 {
            color: var(--accent);
            font-size: 20px;
            margin-top: 28px;
            margin-bottom: 12px;
            border-left: 4px solid var(--primary);
            padding-left: 10px;
        }
        h3 {
            color: var(--text-main);
            font-size: 16px;
            margin-top: 16px;
            margin-bottom: 6px;
        }
        p, li {
            color: #cbd5e1;
            font-size: 15px;
            margin-bottom: 10px;
        }
        ul {
            padding-left: 20px;
            margin-bottom: 16px;
        }
        .card {
            background: var(--surface-card);
            padding: 16px;
            border-radius: 10px;
            margin: 16px 0;
            border: 1px solid var(--border);
        }
        .footer {
            border-top: 1px solid var(--border);
            margin-top: 36px;
            padding-top: 20px;
            text-align: center;
            color: var(--text-muted);
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 SkillSwap Campus</h1>
            <span class="badge">Official Privacy Policy</span>
            <div class="meta">
                <strong>Effective Date:</strong> September 3, 2026 | <strong>Last Updated:</strong> September 3, 2026
            </div>
        </div>

        <p><strong>SkillSwap Campus</strong> ("we", "our", or "the App") is a peer-to-peer student skill exchange and time-bank learning application designed for college and university campuses. This Privacy Policy explains how we collect, use, store, process, and protect your information when you use our Android mobile application and associated web APIs.</p>

        <h2>1. Information We Collect</h2>
        <p>We collect and store information necessary to provide peer tutoring, matchmaking, and credit accounting:</p>
        
        <h3>A. Account & Profile Information</h3>
        <ul>
            <li><strong>Full Name:</strong> Provided during registration to identify you to matched peers.</li>
            <li><strong>Institutional Email Address:</strong> Collected for authentication and institutional student verification (<code>.edu</code> domain verification).</li>
            <li><strong>Password (Hashed):</strong> Cryptographically hashed using secure one-way hashing (<code>pbkdf2:sha256</code>). Plaintext passwords are never stored or logged.</li>
            <li><strong>Academic Profile:</strong> Major/course of study, expected graduation year, college/university name, and optional bio.</li>
        </ul>

        <h3>B. Skills & Portfolio Information</h3>
        <ul>
            <li><strong>Teaching Skills:</strong> Subjects, technologies, or topics you offer to teach, with proficiency levels (<code>Beginner</code>, <code>Intermediate</code>, <code>Advanced</code>).</li>
            <li><strong>Learning Goals:</strong> Subjects or topics you wish to learn from other students.</li>
        </ul>

        <h3>C. Swap Requests & Communications</h3>
        <ul>
            <li><strong>Exchange Invitations:</strong> Records of swap requests sent and received between students.</li>
            <li><strong>User Notes:</strong> Text messages and custom notes included in exchange proposals.</li>
        </ul>

        <h3>D. Scheduled Learning Sessions</h3>
        <ul>
            <li><strong>Session Records:</strong> Participants, skill topic, scheduled date/time, duration (e.g. 1.0 hr), meeting venue (e.g., campus library), and completion status.</li>
        </ul>

        <h3>E. Time-Bank Credit Ledger</h3>
        <ul>
            <li><strong>Credit Balance & History:</strong> Record of earned, spent, and escrow-held non-monetary time credits (1 hour teaching = 1 credit earned).</li>
        </ul>

        <h3>F. Post-Session Reviews & Ratings</h3>
        <ul>
            <li><strong>Double-Blind Ratings:</strong> 1 to 5 star ratings and feedback comments, unlocked simultaneously only after both participants submit reviews.</li>
        </ul>

        <h2>2. Information We DO NOT Collect</h2>
        <div class="card">
            <ul>
                <li><strong>No Financial / Payment Data:</strong> No credit card numbers, bank accounts, or monetary payment processing. The app operates exclusively on a non-monetary time-bank credit model.</li>
                <li><strong>No Precise GPS Location:</strong> We do not track or store device GPS coordinates.</li>
                <li><strong>No Advertising Trackers:</strong> We do not collect advertising IDs (AAID), MAC addresses, or analytics tracking cookies.</li>
                <li><strong>No Device Files or Contacts:</strong> We do not access contacts, SMS, phone calls, camera, or external storage.</li>
            </ul>
        </div>

        <h2>3. How We Use Your Information</h2>
        <ul>
            <li><strong>Authentication:</strong> To verify university student status and maintain secure sessions.</li>
            <li><strong>Peer Matchmaking:</strong> To calculate reciprocal skill compatibility between students.</li>
            <li><strong>Session & Credit Management:</strong> To schedule study appointments and manage time-bank credit accounting.</li>
            <li><strong>Community Trust:</strong> To display academic profiles and double-blind ratings.</li>
        </ul>

        <h2>4. Data Sharing & Disclosure</h2>
        <p><strong>We do NOT sell, rent, monetize, or share your personal data with any third parties or advertisers.</strong> User profile information (name, major, skills, reviews) is visible solely to authenticated peers within the campus network.</p>

        <h2>5. Security & In-Transit Encryption</h2>
        <ul>
            <li><strong>HTTPS / TLS 1.3:</strong> All network communication between the Android application and backend APIs is encrypted in transit.</li>
            <li><strong>Password Protection:</strong> Passwords are protected using salted cryptographic one-way hashing.</li>
        </ul>

        <h2>6. Account Deletion & Data Retention</h2>
        <p>Users can request account deletion at any time by contacting our support team or initiating deletion through their profile. Upon request, user records, skill portfolios, and session history are permanently purged from the database.</p>

        <h2>7. Contact Us</h2>
        <p>If you have any questions, concerns, or requests regarding this Privacy Policy, please contact us at:</p>
        <div class="card">
            <p><strong>SkillSwap Campus Support</strong></p>
            <p>Email: <a href="mailto:support@skillswapcampus.app" style="color: var(--accent);">support@skillswapcampus.app</a></p>
            <p>Platform: SkillSwap Campus Network</p>
        </div>

        <div class="footer">
            &copy; 2026 SkillSwap Campus. All rights reserved.
        </div>
    </div>
</body>
</html>
"""

@health_bp.route('/health', methods=['GET'])
@health_bp.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint checking application status and database connectivity."""
    database_status = "connected"
    try:
        # Perform simple check query to test DB driver/connection state
        db.session.execute(db.text("SELECT 1"))
    except Exception as e:
        # Could log details here if logging utilities were initialized
        database_status = "disconnected"
    
    status_code = 200 if database_status == "connected" else 503
    return jsonify({
        "status": "ok",
        "database": database_status
    }), status_code

@health_bp.route('/privacy', methods=['GET'])
@health_bp.route('/api/privacy', methods=['GET'])
def privacy_policy():
    """Publicly accessible HTML privacy policy endpoint."""
    return render_template_string(PRIVACY_HTML), 200, {'Content-Type': 'text/html; charset=utf-8'}

