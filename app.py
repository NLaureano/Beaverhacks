from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, User
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)


@app.before_request
def create_tables():
    db.create_all()


"""
{
  "username": "john_doe",
  "password": "secure_password_123"
}
"""
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400

    username = data.get("username")
    password = data.get("password")

    print(f"Attempting /register {username}")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 409

    user = User(username=username)
    user.set_password(password)
    user.generate_token()

    db.session.add(user)
    db.session.commit()

    print(f"Creating {username}")

    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201

"""
{
  "username": "john_doe",
  "password": "secure_password_123"
}
"""
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400

    username = data.get("username")
    password = data.get("password")

    print(f"Attempting /login {username}")

    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        print(f"/login failed for {username}")
        return jsonify({"error": "Invalid username or password"}), 401

    token = user.generate_token()
    db.session.commit()

    print(f"/login SUCCESS for {username}")

    return jsonify({"message": "Login successful", "token": token, "user": user.to_dict()}), 200


"""
{
    "token": "UUID token",
    "ticket_id": "0"
}
"""
@app.route("/ticket", methods=["GET"])
def ticket():
    token = request.args.get("token")
    ticket_id = request.args.get("ticket_id")

    print(f"/ticket for {token} for ticket {ticket_id}")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    if not ticket_id:
        return jsonify({"error": "Missing ticket_id"}), 400

    user = User.query.filter_by(token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 401

    return jsonify({"message": "Ticket endpoint", "user_id": user.id, "ticket_id": ticket_id}), 200

"""
input:
{
    "token": "UUID token",
    OPTIONAL "ticket_id": "0"
}

output:
{
    "codebase": {
        "file1.py": "print('Hello, world!')",
        "subdir/file2.py": "def add(a, b): return a + b"
    }
}
"""
@app.route("/codebase", methods=["GET"])
def codebase():
    token = request.args.get("token")

    print(f"/codebase for {token}")

    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    user = User.query.filter_by(token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 401
    
    #optional ticket_id for debugging
    ticket_id = request.args.get("ticket_id")
    current_ticket = user.tickets_done if ticket_id is None else ticket_id

    #get the codebase for the current ticket
    codebase_path = os.path.join("codebases", f"ticket_{current_ticket}")
    if not os.path.exists(codebase_path):
        return jsonify({"error": "No codebase for current ticket"}), 404
    
    #Jsonify the codebase
    codebase = {}
    for root, dirs, files in os.walk(codebase_path):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                codebase[os.path.relpath(os.path.join(root, file), codebase_path)] = f.read()
                
    return jsonify({"codebase": codebase}), 200



@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
