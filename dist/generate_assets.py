"""
Generates high-resolution, pixel-perfect Google Play Store visual assets for SkillSwap Campus:
1. App Icon (512x512 PNG)
2. Feature Graphic (1024x500 PNG)
3. 6 Phone Screenshots (1080x1920 PNG each) showing the exact existing app UI.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "play_store_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Color Palette (Matching Jetpack Compose & Web theme)
COLOR_BG_DARK = (15, 23, 42)         # Slate 900
COLOR_SURFACE = (30, 41, 59)         # Slate 800
COLOR_SURFACE_LIGHT = (51, 65, 85)   # Slate 700
COLOR_CARD = (30, 41, 59)
COLOR_PRIMARY = (99, 102, 241)       # Indigo 500
COLOR_PRIMARY_DARK = (79, 70, 229)   # Indigo 600
COLOR_ACCENT_TEAL = (20, 184, 166)   # Teal 500
COLOR_ACCENT_CYAN = (6, 182, 212)    # Cyan 500
COLOR_ACCENT_GREEN = (16, 185, 129)  # Emerald 500
COLOR_ACCENT_AMBER = (245, 158, 11)  # Amber 500
COLOR_TEXT_WHITE = (248, 250, 252)   # Slate 50
COLOR_TEXT_MUTED = (148, 163, 184)   # Slate 400
COLOR_BORDER = (71, 85, 105)         # Slate 600

def get_font(size, bold=False):
    # Try system fonts on Windows
    font_names = ["segoeuib.ttf" if bold else "segoeui.ttf", "arialbd.ttf" if bold else "arial.ttf", "calibrib.ttf" if bold else "calibri.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

# ==========================================
# 1. App Icon (512x512)
# ==========================================
def create_app_icon():
    # If AI generated icon exists, resize and crop to exact 512x512
    ai_icon_path = r"C:\Users\BRINDHA\.gemini\antigravity\brain\a10a9228-c12e-4747-b351-02b0d36eb5bb\skillswap_app_icon_1788430300148.jpg"
    out_path = os.path.join(ASSETS_DIR, "app_icon_512x512.png")
    
    if os.path.exists(ai_icon_path):
        img = Image.open(ai_icon_path)
        img = img.resize((512, 512), Image.Resampling.LANCZOS)
        img.save(out_path, "PNG")
        print(f"[OK] App Icon saved: {out_path} (512x512)")
    else:
        img = Image.new("RGBA", (512, 512), COLOR_BG_DARK)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([20, 20, 492, 492], radius=96, fill=COLOR_PRIMARY_DARK)
        # Cap & arrows emblem
        font_large = get_font(90, bold=True)
        draw.text((256, 256), "🎓 ⇄", fill=COLOR_TEXT_WHITE, font=font_large, anchor="mm")
        img.save(out_path, "PNG")
        print(f"[OK] Fallback App Icon saved: {out_path} (512x512)")

# ==========================================
# 2. Feature Graphic (1024x500)
# ==========================================
def create_feature_graphic():
    img = Image.new("RGBA", (1024, 500), COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Background gradient overlay
    for y in range(500):
        alpha = int(255 * (1 - (y / 600)))
        r = int(15 + (99 - 15) * (y / 500) * 0.4)
        g = int(23 + (102 - 23) * (y / 500) * 0.3)
        b = int(42 + (241 - 42) * (y / 500) * 0.5)
        draw.line([(0, y), (1024, y)], fill=(r, g, b, 255))
        
    # Decorative glow circles
    draw.ellipse([800, -100, 1100, 200], fill=(99, 102, 241, 40))
    draw.ellipse([-50, 300, 250, 600], fill=(20, 184, 166, 35))

    # Left Side: Typography & Brand
    font_badge = get_font(20, bold=True)
    font_title = get_font(52, bold=True)
    font_subtitle = get_font(22, bold=False)
    font_desc = get_font(18, bold=False)
    
    # Campus Badge
    draw.rounded_rectangle([60, 60, 280, 100], radius=20, fill=COLOR_SURFACE_LIGHT)
    draw.text((170, 80), "CAMPUS NETWORK", fill=COLOR_ACCENT_CYAN, font=font_badge, anchor="mm")
    
    # Title
    draw.text((60, 125), "SkillSwap Campus", fill=COLOR_TEXT_WHITE, font=font_title)
    
    # Subtitle
    draw.text((60, 195), "Peer-to-Peer Student Learning & Time-Bank", fill=COLOR_ACCENT_TEAL, font=font_subtitle)
    
    # Bullet highlights
    bullets = [
        "✓ Verified Institutional (.edu) Student Network",
        "✓ 100% Reciprocal Peer Matchmaking",
        "✓ 1 Hour Teaching = 1 Credit Earned",
        "✓ Post-Session Double-Blind Reviews"
    ]
    for i, b in enumerate(bullets):
        draw.text((60, 260 + i * 36), b, fill=COLOR_TEXT_MUTED, font=font_desc)

    # Right Side: Interactive Card Visual Mockup
    card_x, card_y = 620, 70
    draw.rounded_rectangle([card_x, card_y, card_x + 340, card_y + 360], radius=24, fill=COLOR_CARD, outline=COLOR_BORDER, width=2)
    
    # Card Header
    draw.ellipse([card_x + 30, card_y + 30, card_x + 80, card_y + 80], fill=COLOR_PRIMARY)
    draw.text((card_x + 55, card_y + 55), "AS", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True), anchor="mm")
    
    draw.text((card_x + 95, card_y + 38), "Alice Smith", fill=COLOR_TEXT_WHITE, font=get_font(22, bold=True))
    draw.text((card_x + 95, card_y + 65), "Computer Science '26", fill=COLOR_TEXT_MUTED, font=get_font(16))
    
    # Compatibility score pill
    draw.rounded_rectangle([card_x + 230, card_y + 32, card_x + 320, card_y + 66], radius=12, fill=COLOR_ACCENT_GREEN)
    draw.text((card_x + 275, card_y + 49), "100% Match", fill=(0, 0, 0), font=get_font(14, bold=True), anchor="mm")
    
    # Divider
    draw.line([(card_x + 20, card_y + 105), (card_x + 320, card_y + 105)], fill=COLOR_BORDER, width=1)
    
    # Teach skill pill
    draw.text((card_x + 30, card_y + 125), "TEACHES", fill=COLOR_ACCENT_CYAN, font=get_font(14, bold=True))
    draw.rounded_rectangle([card_x + 30, card_y + 148, card_x + 240, card_y + 185], radius=10, fill=COLOR_SURFACE_LIGHT)
    draw.text((card_x + 42, card_y + 166), "Python Programming", fill=COLOR_TEXT_WHITE, font=get_font(16), anchor="lm")
    
    # Learn skill pill
    draw.text((card_x + 30, card_y + 205), "WANTS TO LEARN", fill=COLOR_ACCENT_AMBER, font=get_font(14, bold=True))
    draw.rounded_rectangle([card_x + 30, card_y + 228, card_x + 180, card_y + 265], radius=10, fill=COLOR_SURFACE_LIGHT)
    draw.text((card_x + 42, card_y + 246), "Calculus II", fill=COLOR_TEXT_WHITE, font=get_font(16), anchor="lm")
    
    # Time-bank badge at bottom of card
    draw.rounded_rectangle([card_x + 30, card_y + 290, card_x + 310, card_y + 335], radius=12, fill=COLOR_PRIMARY_DARK)
    draw.text((card_x + 170, card_y + 312), "🤝 Propose 1:1 Skill Swap", fill=COLOR_TEXT_WHITE, font=get_font(16, bold=True), anchor="mm")

    out_path = os.path.join(ASSETS_DIR, "feature_graphic_1024x500.png")
    img.save(out_path, "PNG")
    print(f"[OK] Feature Graphic saved: {out_path} (1024x500)")

# ==========================================
# 3. 6 Phone Screenshots (1080x1920 each)
# ==========================================
def create_phone_screenshot(title_banner, subtitle_banner, filename, render_content_fn):
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Top Marketing Header Banner
    font_header_title = get_font(46, bold=True)
    font_header_sub = get_font(26, bold=False)
    
    # Subtle top header container
    draw.rectangle([0, 0, W, 220], fill=(15, 23, 42))
    draw.line([(0, 220), (W, 220)], fill=COLOR_BORDER, width=2)
    
    draw.text((W // 2, 75), title_banner, fill=COLOR_ACCENT_CYAN, font=font_header_title, anchor="mm")
    draw.text((W // 2, 140), subtitle_banner, fill=COLOR_TEXT_MUTED, font=font_header_sub, anchor="mm")
    
    # Phone Body Container (Canvas for screen)
    phone_x, phone_y = 60, 250
    phone_w, phone_h = W - 120, H - 290
    
    # Phone frame outer border
    draw.rounded_rectangle([phone_x, phone_y, phone_x + phone_w, phone_y + phone_h], radius=36, fill=(18, 24, 38), outline=COLOR_PRIMARY_DARK, width=3)
    
    # Top Android Status Bar inside phone
    draw.text((phone_x + 40, phone_y + 25), "9:41", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True))
    draw.text((phone_x + phone_w - 90, phone_y + 25), "5G  🔋", fill=COLOR_TEXT_WHITE, font=get_font(20))
    
    # App Bar
    appbar_y = phone_y + 60
    draw.rectangle([phone_x + 3, appbar_y, phone_x + phone_w - 3, appbar_y + 70], fill=COLOR_CARD)
    draw.text((phone_x + 30, appbar_y + 35), "SkillSwap Campus", fill=COLOR_TEXT_WHITE, font=get_font(26, bold=True), anchor="lm")
    draw.line([(phone_x, appbar_y + 70), (phone_x + phone_w, appbar_y + 70)], fill=COLOR_BORDER, width=1)
    
    # Render Specific Screen UI inside phone
    content_y = appbar_y + 85
    render_content_fn(draw, phone_x + 30, content_y, phone_w - 60)
    
    # Bottom Navigation Bar
    nav_y = phone_y + phone_h - 90
    draw.rectangle([phone_x + 3, nav_y, phone_x + phone_w - 3, phone_y + phone_h - 3], fill=COLOR_CARD)
    draw.line([(phone_x, nav_y), (phone_x + phone_w, nav_y)], fill=COLOR_BORDER, width=1)
    
    nav_items = ["🏠 Home", "🔍 Explore", "⇄ Requests", "📅 Sessions", "👤 Profile"]
    nav_step = phone_w // len(nav_items)
    for idx, item in enumerate(nav_items):
        item_x = phone_x + idx * nav_step + nav_step // 2
        col = COLOR_ACCENT_CYAN if idx == 0 and "dashboard" in filename else (COLOR_PRIMARY if idx == 1 and "matches" in filename else COLOR_TEXT_MUTED)
        draw.text((item_x, nav_y + 45), item, fill=col, font=get_font(20, bold=True), anchor="mm")

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, "PNG")
    print(f"[OK] Phone Screenshot saved: {out_path} (1080x1920)")

# ------------------------------------------
# Screen 1: Login / Register
# ------------------------------------------
def render_screen_login(draw, x, y, w):
    draw.ellipse([x + w//2 - 60, y + 20, x + w//2 + 60, y + 140], fill=COLOR_PRIMARY_DARK)
    draw.text((x + w//2, y + 80), "🎓", fill=COLOR_TEXT_WHITE, font=get_font(50), anchor="mm")
    
    draw.text((x + w//2, y + 180), "Welcome to SkillSwap", fill=COLOR_TEXT_WHITE, font=get_font(34, bold=True), anchor="mm")
    draw.text((x + w//2, y + 225), "Sign in with your university .edu email", fill=COLOR_TEXT_MUTED, font=get_font(22), anchor="mm")
    
    # Email Field
    draw.text((x, y + 280), "Institutional Email Address", fill=COLOR_TEXT_MUTED, font=get_font(18, bold=True))
    draw.rounded_rectangle([x, y + 310, x + w, y + 380], radius=14, fill=COLOR_SURFACE, outline=COLOR_BORDER, width=1)
    draw.text((x + 25, y + 345), "alex.morgan@university.edu", fill=COLOR_TEXT_WHITE, font=get_font(22), anchor="lm")
    
    # Password Field
    draw.text((x, y + 410), "Password", fill=COLOR_TEXT_MUTED, font=get_font(18, bold=True))
    draw.rounded_rectangle([x, y + 440, x + w, y + 510], radius=14, fill=COLOR_SURFACE, outline=COLOR_BORDER, width=1)
    draw.text((x + 25, y + 475), "••••••••••••", fill=COLOR_TEXT_WHITE, font=get_font(26), anchor="lm")
    
    # Login Button
    draw.rounded_rectangle([x, y + 550, x + w, y + 625], radius=16, fill=COLOR_PRIMARY)
    draw.text((x + w//2, y + 587), "Sign In to Campus Network", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True), anchor="mm")
    
    # Divider
    draw.text((x + w//2, y + 675), "— OR REGISTER NEW ACCOUNT —", fill=COLOR_TEXT_MUTED, font=get_font(18), anchor="mm")
    
    # Register Card Info
    draw.rounded_rectangle([x, y + 720, x + w, y + 860], radius=18, fill=COLOR_SURFACE_LIGHT)
    draw.text((x + 30, y + 760), "🎁 New Student Welcome Bonus", fill=COLOR_ACCENT_TEAL, font=get_font(22, bold=True))
    draw.text((x + 30, y + 805), "Receive 2.0 free time-bank credits instantly upon registration.", fill=COLOR_TEXT_WHITE, font=get_font(18))
    draw.text((x + 30, y + 835), "Valid exclusively for verified college students.", fill=COLOR_TEXT_MUTED, font=get_font(16))

# ------------------------------------------
# Screen 2: Dashboard
# ------------------------------------------
def render_screen_dashboard(draw, x, y, w):
    draw.text((x, y + 10), "Hello, Alex! 👋", fill=COLOR_TEXT_WHITE, font=get_font(34, bold=True))
    draw.text((x, y + 55), "Computer Science '26 • University Campus", fill=COLOR_TEXT_MUTED, font=get_font(20))
    
    # Credit Balance Banner Card
    draw.rounded_rectangle([x, y + 95, x + w, y + 265], radius=20, fill=COLOR_PRIMARY_DARK)
    draw.text((x + 35, y + 140), "TIME-BANK CREDIT BALANCE", fill=COLOR_ACCENT_CYAN, font=get_font(18, bold=True))
    draw.text((x + 35, y + 205), "3.00", fill=COLOR_TEXT_WHITE, font=get_font(52, bold=True))
    draw.text((x + 165, y + 215), "Credits Available", fill=COLOR_TEXT_WHITE, font=get_font(22))
    draw.text((x + w - 40, y + 205), "+1.0 Earned", fill=COLOR_ACCENT_GREEN, font=get_font(20, bold=True), anchor="rm")
    
    # Quick Action Buttons
    draw.text((x, y + 295), "Quick Actions", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True))
    btn_w = (w - 30) // 2
    
    # Action 1
    draw.rounded_rectangle([x, y + 335, x + btn_w, y + 435], radius=16, fill=COLOR_SURFACE, outline=COLOR_BORDER)
    draw.text((x + 25, y + 370), "🔍 Find Matches", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True))
    draw.text((x + 25, y + 400), "12 active peers", fill=COLOR_ACCENT_TEAL, font=get_font(16))
    
    # Action 2
    draw.rounded_rectangle([x + btn_w + 30, y + 335, x + w, y + 435], radius=16, fill=COLOR_SURFACE, outline=COLOR_BORDER)
    draw.text((x + btn_w + 55, y + 370), "📅 View Sessions", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True))
    draw.text((x + btn_w + 55, y + 400), "1 upcoming session", fill=COLOR_ACCENT_AMBER, font=get_font(16))
    
    # Activity Section
    draw.text((x, y + 470), "Recent Activity & Alerts", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True))
    
    # Activity Item 1
    draw.rounded_rectangle([x, y + 510, x + w, y + 615], radius=16, fill=COLOR_CARD, outline=COLOR_BORDER)
    draw.text((x + 30, y + 545), "⭐ Review Unlocked: Python Tutoring", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True))
    draw.text((x + 30, y + 580), "Mutual reviews unlocked for Session #2 with Bob Jones", fill=COLOR_TEXT_MUTED, font=get_font(17))
    
    # Activity Item 2
    draw.rounded_rectangle([x, y + 635, x + w, y + 740], radius=16, fill=COLOR_CARD, outline=COLOR_BORDER)
    draw.text((x + 30, y + 670), "⇄ Swap Request Accepted", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True))
    draw.text((x + 30, y + 705), "Elena Rostova accepted your French for React exchange", fill=COLOR_ACCENT_GREEN, font=get_font(17))

# ------------------------------------------
# Screen 3: Skills Catalog
# ------------------------------------------
def render_screen_skills(draw, x, y, w):
    draw.text((x, y + 10), "Skills Portfolio", fill=COLOR_TEXT_WHITE, font=get_font(34, bold=True))
    draw.text((x, y + 55), "Manage what you teach and what you want to learn", fill=COLOR_TEXT_MUTED, font=get_font(20))
    
    # Teaching Skills Section
    draw.text((x, y + 105), "💡 SKILLS YOU CAN TEACH", fill=COLOR_ACCENT_CYAN, font=get_font(20, bold=True))
    
    teach_skills = [
        ("Python Programming", "Technology", "Advanced"),
        ("Data Structures & Algorithms", "Computer Science", "Advanced"),
        ("Web Development (React)", "Web & Mobile", "Intermediate")
    ]
    
    for idx, (s_name, s_cat, s_prof) in enumerate(teach_skills):
        item_y = y + 145 + idx * 105
        draw.rounded_rectangle([x, item_y, x + w, item_y + 90], radius=16, fill=COLOR_CARD, outline=COLOR_BORDER)
        draw.text((x + 25, item_y + 30), s_name, fill=COLOR_TEXT_WHITE, font=get_font(22, bold=True))
        draw.text((x + 25, item_y + 60), s_cat, fill=COLOR_TEXT_MUTED, font=get_font(16))
        
        # Proficiency Badge
        draw.rounded_rectangle([x + w - 150, item_y + 25, x + w - 25, item_y + 65], radius=12, fill=COLOR_PRIMARY_DARK)
        draw.text((x + w - 87, item_y + 45), s_prof, fill=COLOR_TEXT_WHITE, font=get_font(16, bold=True), anchor="mm")

    # Learning Goals Section
    learn_y = y + 490
    draw.text((x, learn_y), "🎯 SKILLS YOU WANT TO LEARN", fill=COLOR_ACCENT_AMBER, font=get_font(20, bold=True))
    
    learn_skills = [
        ("Calculus II", "Mathematics", "Beginner"),
        ("Conversational Spanish", "Languages", "Beginner"),
        ("Graphic Design & UI/UX", "Design", "Intermediate")
    ]
    
    for idx, (s_name, s_cat, s_prof) in enumerate(learn_skills):
        item_y = learn_y + 40 + idx * 105
        draw.rounded_rectangle([x, item_y, x + w, item_y + 90], radius=16, fill=COLOR_CARD, outline=COLOR_BORDER)
        draw.text((x + 25, item_y + 30), s_name, fill=COLOR_TEXT_WHITE, font=get_font(22, bold=True))
        draw.text((x + 25, item_y + 60), s_cat, fill=COLOR_TEXT_MUTED, font=get_font(16))
        
        # Proficiency Badge
        draw.rounded_rectangle([x + w - 150, item_y + 25, x + w - 25, item_y + 65], radius=12, fill=COLOR_SURFACE_LIGHT)
        draw.text((x + w - 87, item_y + 45), s_prof, fill=COLOR_ACCENT_TEAL, font=get_font(16, bold=True), anchor="mm")

# ------------------------------------------
# Screen 4: Reciprocal Matches
# ------------------------------------------
def render_screen_matches(draw, x, y, w):
    draw.text((x, y + 10), "Peer Matches", fill=COLOR_TEXT_WHITE, font=get_font(34, bold=True))
    draw.text((x, y + 55), "Students with compatible teach/learn skills", fill=COLOR_TEXT_MUTED, font=get_font(20))
    
    # Match Card 1 (Reciprocal 100%)
    card1_y = y + 100
    draw.rounded_rectangle([x, card1_y, x + w, card1_y + 310], radius=22, fill=COLOR_CARD, outline=COLOR_PRIMARY, width=2)
    
    draw.ellipse([x + 30, card1_y + 30, x + 90, card1_y + 90], fill=COLOR_PRIMARY_DARK)
    draw.text((x + 60, card1_y + 60), "BJ", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True), anchor="mm")
    
    draw.text((x + 110, card1_y + 38), "Bob Jones", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True))
    draw.text((x + 110, card1_y + 70), "Mathematics '27 • Calculus Peer Tutor", fill=COLOR_TEXT_MUTED, font=get_font(17))
    
    draw.rounded_rectangle([x + w - 160, card1_y + 35, x + w - 30, card1_y + 75], radius=12, fill=COLOR_ACCENT_GREEN)
    draw.text((x + w - 95, card1_y + 55), "100% Match", fill=(0, 0, 0), font=get_font(16, bold=True), anchor="mm")
    
    draw.line([(x + 25, card1_y + 110), (x + w - 25, card1_y + 110)], fill=COLOR_BORDER)
    
    draw.text((x + 30, card1_y + 130), "Can Teach You:", fill=COLOR_ACCENT_CYAN, font=get_font(16, bold=True))
    draw.text((x + 160, card1_y + 130), "Calculus II (Advanced)", fill=COLOR_TEXT_WHITE, font=get_font(16))
    
    draw.text((x + 30, card1_y + 165), "Wants To Learn:", fill=COLOR_ACCENT_AMBER, font=get_font(16, bold=True))
    draw.text((x + 160, card1_y + 165), "Python Programming (Beginner)", fill=COLOR_TEXT_WHITE, font=get_font(16))
    
    # Propose Swap Button
    draw.rounded_rectangle([x + 25, card1_y + 215, x + w - 25, card1_y + 280], radius=14, fill=COLOR_PRIMARY)
    draw.text((x + w//2, card1_y + 247), "⇄ Propose Skill Swap", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True), anchor="mm")

    # Match Card 2
    card2_y = card1_y + 340
    draw.rounded_rectangle([x, card2_y, x + w, card2_y + 310], radius=22, fill=COLOR_CARD, outline=COLOR_BORDER)
    
    draw.ellipse([x + 30, card2_y + 30, x + 90, card2_y + 90], fill=(20, 184, 166))
    draw.text((x + 60, card2_y + 60), "ER", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True), anchor="mm")
    
    draw.text((x + 110, card2_y + 38), "Elena Rostova", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True))
    draw.text((x + 110, card2_y + 70), "Modern Languages '25 • French Native", fill=COLOR_TEXT_MUTED, font=get_font(17))
    
    draw.rounded_rectangle([x + w - 160, card2_y + 35, x + w - 30, card2_y + 75], radius=12, fill=COLOR_PRIMARY_DARK)
    draw.text((x + w - 95, card2_y + 55), "Reciprocal", fill=COLOR_TEXT_WHITE, font=get_font(16, bold=True), anchor="mm")
    
    draw.line([(x + 25, card2_y + 110), (x + w - 25, card2_y + 110)], fill=COLOR_BORDER)
    draw.text((x + 30, card2_y + 130), "Can Teach You:", fill=COLOR_ACCENT_CYAN, font=get_font(16, bold=True))
    draw.text((x + 160, card2_y + 130), "Conversational French (Advanced)", fill=COLOR_TEXT_WHITE, font=get_font(16))
    
    draw.text((x + 30, card2_y + 165), "Wants To Learn:", fill=COLOR_ACCENT_AMBER, font=get_font(16, bold=True))
    draw.text((x + 160, card2_y + 165), "Web Development (React)", fill=COLOR_TEXT_WHITE, font=get_font(16))
    
    draw.rounded_rectangle([x + 25, card2_y + 215, x + w - 25, card2_y + 280], radius=14, fill=COLOR_PRIMARY)
    draw.text((x + w//2, card2_y + 247), "⇄ Propose Skill Swap", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True), anchor="mm")

# ------------------------------------------
# Screen 5: Swap Requests
# ------------------------------------------
def render_screen_requests(draw, x, y, w):
    draw.text((x, y + 10), "Swap Requests", fill=COLOR_TEXT_WHITE, font=get_font(34, bold=True))
    draw.text((x, y + 55), "Manage peer exchange invitations", fill=COLOR_TEXT_MUTED, font=get_font(20))
    
    # Tabs: Incoming (Active) vs Outgoing
    tab_w = w // 2
    draw.rounded_rectangle([x, y + 100, x + tab_w - 10, y + 155], radius=14, fill=COLOR_PRIMARY)
    draw.text((x + tab_w//2 - 5, y + 127), "Incoming (1)", fill=COLOR_TEXT_WHITE, font=get_font(20, bold=True), anchor="mm")
    
    draw.rounded_rectangle([x + tab_w + 10, y + 100, x + w, y + 155], radius=14, fill=COLOR_SURFACE)
    draw.text((x + tab_w + tab_w//2 + 5, y + 127), "Outgoing (2)", fill=COLOR_TEXT_MUTED, font=get_font(20, bold=True), anchor="mm")
    
    # Request Card
    req_y = y + 185
    draw.rounded_rectangle([x, req_y, x + w, req_y + 360], radius=20, fill=COLOR_CARD, outline=COLOR_BORDER)
    
    draw.text((x + 30, req_y + 35), "Invitation from Bob Jones", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True))
    draw.text((x + 30, req_y + 68), "Proposed swap: Python Programming ⇄ Calculus II", fill=COLOR_ACCENT_CYAN, font=get_font(18))
    
    # Custom note box
    draw.rounded_rectangle([x + 25, req_y + 110, x + w - 25, req_y + 220], radius=14, fill=COLOR_SURFACE_LIGHT)
    draw.text((x + 45, req_y + 135), '"Hi Alex! I saw you are teaching Python. I can help', fill=COLOR_TEXT_WHITE, font=get_font(18))
    draw.text((x + 45, req_y + 165), 'you with Calculus problem sets for your upcoming midterm."', fill=COLOR_TEXT_WHITE, font=get_font(18))
    
    # Status
    draw.text((x + 30, req_y + 250), "Status: Pending Response", fill=COLOR_ACCENT_AMBER, font=get_font(18, bold=True))
    
    # Action buttons
    btn_w = (w - 70) // 2
    # Accept Button
    draw.rounded_rectangle([x + 25, req_y + 285, x + 25 + btn_w, req_y + 335], radius=12, fill=COLOR_ACCENT_GREEN)
    draw.text((x + 25 + btn_w//2, req_y + 310), "✓ Accept", fill=(0, 0, 0), font=get_font(18, bold=True), anchor="mm")
    
    # Decline Button
    draw.rounded_rectangle([x + 45 + btn_w, req_y + 285, x + w - 25, req_y + 335], radius=12, fill=COLOR_SURFACE_LIGHT)
    draw.text((x + 45 + btn_w + btn_w//2, req_y + 310), "✕ Decline", fill=COLOR_TEXT_WHITE, font=get_font(18, bold=True), anchor="mm")

# ------------------------------------------
# Screen 6: Sessions & Profile
# ------------------------------------------
def render_screen_sessions(draw, x, y, w):
    draw.text((x, y + 10), "Scheduled Sessions", fill=COLOR_TEXT_WHITE, font=get_font(34, bold=True))
    draw.text((x, y + 55), "1-on-1 tutoring appointments & credit ledger", fill=COLOR_TEXT_MUTED, font=get_font(20))
    
    # Session Card 1
    s_y = y + 100
    draw.rounded_rectangle([x, s_y, x + w, s_y + 280], radius=20, fill=COLOR_CARD, outline=COLOR_PRIMARY, width=2)
    
    draw.text((x + 30, s_y + 35), "Python Tutoring with Bob Jones", fill=COLOR_TEXT_WHITE, font=get_font(24, bold=True))
    draw.text((x + 30, s_y + 68), "Role: You are Teaching • 1.0 Credit Earned upon completion", fill=COLOR_ACCENT_CYAN, font=get_font(17))
    
    # Venue & Time pills
    draw.rounded_rectangle([x + 30, s_y + 110, x + w - 30, s_y + 160], radius=12, fill=COLOR_SURFACE_LIGHT)
    draw.text((x + 45, s_y + 135), "📍 Venue: Campus Library Room 3B (or Virtual Meet)", fill=COLOR_TEXT_WHITE, font=get_font(17), anchor="lm")
    
    draw.rounded_rectangle([x + 30, s_y + 175, x + w - 30, s_y + 225], radius=12, fill=COLOR_SURFACE_LIGHT)
    draw.text((x + 45, s_y + 200), "⏰ Tomorrow, 2:00 PM - 3:00 PM (1.0 Hour)", fill=COLOR_ACCENT_AMBER, font=get_font(17), anchor="lm")
    
    # Status
    draw.text((x + 30, s_y + 250), "Status: Scheduled (Credits on Escrow Hold)", fill=COLOR_ACCENT_GREEN, font=get_font(16, bold=True))

    # Double-Blind Reviews Section
    rev_y = s_y + 310
    draw.text((x, rev_y), "⭐ VERIFIED PEER REVIEWS", fill=COLOR_ACCENT_AMBER, font=get_font(20, bold=True))
    
    draw.rounded_rectangle([x, rev_y + 35, x + w, rev_y + 215], radius=18, fill=COLOR_CARD, outline=COLOR_BORDER)
    draw.text((x + 30, rev_y + 65), "★★★★★  5.0 / 5.0", fill=COLOR_ACCENT_AMBER, font=get_font(22, bold=True))
    draw.text((x + 230, rev_y + 68), "• Bob Jones (Math '27)", fill=COLOR_TEXT_MUTED, font=get_font(18))
    
    draw.text((x + 30, rev_y + 110), '"Alex was an amazing tutor! He broke down complex recursion', fill=COLOR_TEXT_WHITE, font=get_font(18))
    draw.text((x + 30, rev_y + 140), 'and tree traversal concepts very clearly with live coding examples."', fill=COLOR_TEXT_WHITE, font=get_font(18))
    draw.text((x + 30, rev_y + 180), "🔒 Double-blind mutual review unlocked", fill=COLOR_ACCENT_TEAL, font=get_font(15, bold=True))

# ==========================================
# Run All Generators
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print("GENERATING PLAY STORE ASSETS")
    print("==========================================")
    
    create_app_icon()
    create_feature_graphic()
    
    create_phone_screenshot(
        "CAMPUS-VERIFIED STUDENT LOGIN",
        "Fast & secure authentication with .edu institutional email",
        "screenshot_1_login_register.png",
        render_screen_login
    )
    
    create_phone_screenshot(
        "TIME-BANK CREDIT DASHBOARD",
        "Track active credits, quick actions, and peer swap alerts",
        "screenshot_2_dashboard.png",
        render_screen_dashboard
    )
    
    create_phone_screenshot(
        "CUSTOM SKILLS PORTFOLIO",
        "Select what you teach and what you want to learn",
        "screenshot_3_skills.png",
        render_screen_skills
    )
    
    create_phone_screenshot(
        "SMART RECIPROCAL MATCHING",
        "Discover 100% compatible peer tutoring exchange partners",
        "screenshot_4_matches.png",
        render_screen_matches
    )
    
    create_phone_screenshot(
        "SWAP PROPOSALS & NEGOTIATIONS",
        "Send and accept 1-on-1 skill exchange proposals in seconds",
        "screenshot_5_requests.png",
        render_screen_requests
    )
    
    create_phone_screenshot(
        "1-ON-1 SESSIONS & MUTUAL REVIEWS",
        "Schedule study meetups, manage escrow, and unlock ratings",
        "screenshot_6_sessions_profile.png",
        render_screen_sessions
    )
    
    print("==========================================")
    print("ALL ASSETS GENERATED SUCCESSFULLY!")
    print("==========================================")
