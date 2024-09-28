from flask import Flask
from routes import klotski_bp

def create_app():
    app = Flask(__name__)

    # Register the klotski Blueprint
    app.register_blueprint(klotski_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
