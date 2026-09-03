import os
from app import create_app

# Instantiate Flask application using factory pattern
app = create_app()

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")
    port = int(os.getenv("PORT", os.getenv("APP_PORT", 5000)))
    debug = os.getenv("DEBUG", "False" if os.getenv("PORT") else "True").lower() in ("true", "1", "yes")
    
    app.run(host=host, port=port, debug=debug)

