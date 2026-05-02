from flask import Flask, jsonify
from dotenv import load_dotenv

from config import Config
from .extensions import cors, db, jwt
from .models import User
from .routes.auth import auth_bp


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.get("/health")
    def health_check() -> tuple[dict, int]:
        return {"status": "ok"}, 200

    @app.errorhandler(400)
    def bad_request(error):
        description = getattr(error, "description", "Bad request")
        return jsonify({"error": description}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    with app.app_context():
        db.create_all()

    return app
