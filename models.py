from flask_sqlalchemy import SQLAlchemy
import hashlib
import secrets

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=True)
    tickets_done = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def generate_token(self):
        self.token = secrets.token_hex(32)
        return self.token

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "token": self.token,
            "tickets_done": self.tickets_done,
        }
