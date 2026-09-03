from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions, bounded to the application via factory patterns
db = SQLAlchemy()
migrate = Migrate()
