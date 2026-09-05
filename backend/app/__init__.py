from flask import Flask
from flask_cors import CORS
from app.config.config import Config
from app.extensions import db, migrate
from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.onboarding import onboarding_bp
from app.routes.exchange import exchange_bp

def create_app(config_class=Config):
    """Flask application factory function."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS for cross-origin frontend requests
    # Set supports_credentials=True to allow cookies across origins in dev
    CORS(app, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to register tables with SQLAlchemy metadata
    from app import models

    # Ensure all tables exist and skills are populated in database on startup
    with app.app_context():
        try:
            db.create_all()
            from app.models.skill import Skill
            from app.utils.skills_data import CATEGORIZED_SKILLS
            
            # Sync skills catalog if missing
            synced = False
            for s_info in CATEGORIZED_SKILLS:
                name = s_info["name"].strip()
                category = s_info["category"].strip()
                existing = Skill.query.filter(db.func.lower(Skill.name) == name.lower()).first()
                if not existing:
                    db.session.add(Skill(name=name, category=category))
                    synced = True
                elif existing.category != category:
                    existing.category = category
                    synced = True
            if synced:
                db.session.commit()
        except Exception as e:
            app.logger.error(f"Error initializing/syncing database on startup: {e}")

    # Register blueprints (routes)
    app.register_blueprint(health_bp, url_prefix='')
    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(onboarding_bp, url_prefix='')
    app.register_blueprint(exchange_bp, url_prefix='')

    return app
