from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, User
import os
import sys
import tempfile
import shutil
import importlib.util
import traceback

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
@app.route("/ticket", methods=["POST"])
def ticket():
    data = request.get_json()

    token = data.get("token")
    ticket_id = data.get("ticket_id")

    print(f"/ticket for {token} for ticket {ticket_id}")
    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    if not ticket_id:
        return jsonify({"error": "Missing ticket_id"}), 400

    user = User.query.filter_by(token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 401
    
    # Run the codebase against the tests for the current ticket and return the results
    with tempfile.TemporaryDirectory() as tmpdir:
        ticket_dir = os.path.join(tmpdir, f"Ticket-{ticket_id}")
        codebase_dir = os.path.join(ticket_dir, "Codebase")
        tests_dir = os.path.join(ticket_dir, "tests")
        os.makedirs(codebase_dir, exist_ok=True)

        # Write submitted code files
        for rel_path, content in codebase.items():
            dest_path = os.path.join(codebase_dir, rel_path)
            dest_parent = os.path.dirname(dest_path)
            if dest_parent:
                os.makedirs(dest_parent, exist_ok=True)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)

        # Copy official tests from repository into the temporary ticket tests directory
        repo_tests_path = os.path.join(f"Tickets/Ticket-{ticket_id}", "tests")
        if not os.path.exists(repo_tests_path):
            return jsonify({"error": "No tests found for ticket"}), 404

        shutil.copytree(repo_tests_path, tests_dir)

        # Run pytest as a subprocess for isolation
        cmd = [sys.executable, "-m", "pytest", "-q", "--disable-warnings", "--maxfail=1"]
        try:
            proc = __import__("subprocess").run(cmd, cwd=ticket_dir, capture_output=True, text=True, timeout=30)
        except Exception as exc:
            return jsonify({"error": "Failed to run tests", "details": str(exc)}), 500

        stdout = proc.stdout
        stderr = proc.stderr
        exit_code = proc.returncode

        # Parse pytest summary from stdout (e.g., "== 4 passed, 1 failed in 0.12s ==")
        import re
        summary = {"total": None, "passed": 0, "failed": 0, "skipped": 0}
        m = re.search(r"(\d+) passed", stdout)
        if m:
            summary["passed"] = int(m.group(1))
        m = re.search(r"(\d+) failed", stdout)
        if m:
            summary["failed"] = int(m.group(1))
        m = re.search(r"(\d+) skipped", stdout)
        if m:
            summary["skipped"] = int(m.group(1))
        # total = passed + failed + skipped (if numbers present)
        counts = [summary["passed"], summary["failed"], summary["skipped"]]
        if any(c > 0 for c in counts):
            summary["total"] = sum(counts)
        else:
            # fallback: if pytest prints nothing matching, set total to 0
            summary["total"] = 0

        # Update user's tickets_done only if all tests passed and at least one test ran
        if summary["failed"] == 0 and summary["total"] > 0:
            user.tickets_done += 1
            db.session.commit()

        status = "Code passed all tests for this ticket!" if summary["failed"] == 0 and summary["total"] > 0 else "Code failed some tests for this ticket!"
        return jsonify({
            "Testing Output": status,
            "Details": {
                "exit_code": exit_code,
                "stdout": stdout,
                "stderr": stderr,
                "summary": summary
            },
            "tickets_done": user.tickets_done
        }), 200

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
@app.route("/codebase", methods=["POST"])
def codebase():
    data = request.get_json()
    token = data.get("token")

    print(f"/codebase for {token}")
    print(f"{request.get_json()}")

    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    user = User.query.filter_by(token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 401
    
    #optional ticket_id for debugging
    ticket_id = data.get("ticket_id")
    current_ticket = user.tickets_done if ticket_id is None else ticket_id

    #get the codebase for the current ticket under Tickets/ticket-{current_ticket}
    codebase_path = os.path.join(f"Tickets/Ticket-{current_ticket}", "Codebase")
    if not os.path.exists(codebase_path):
        return jsonify({"error": "No codebase for current ticket"}), 404
    
    #Jsonify the codebase
    codebase = {}
    for root, dirs, files in os.walk(codebase_path):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                codebase[os.path.relpath(os.path.join(root, file), codebase_path)] = f.read()
                
    return jsonify({"codebase": codebase}), 200

"""
input:
{
    token: "UUID token",
    ticket_id: "0",
    codebase: {
        "file1.py": "print('Hello, world!')",
        "subdir/file2.py": "def add(a, b): return a + b"
    }
}

SUCCESSFUL output:
{
    "Testing Output": "Code passed all tests for this ticket!"
}

FAILURE output:
{
    "Testing Output": "Code failed some tests for this ticket!"
    "Details": { 
                Total tests: 10,
                Passed: 8,
                Failed: 2 
                "Traceback or error message from the test runner"
    }
}
"""
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    token = data.get("token")
    ticket_id = data.get("ticket_id")
    codebase = data.get("codebase")

    print(f"/submit for {token} for ticket {ticket_id}")

    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    if not ticket_id:
        return jsonify({"error": "Missing ticket_id"}), 400

    if not codebase:
        return jsonify({"error": "Missing codebase"}), 400

    user = User.query.filter_by(token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 401
    
    #Run the codebase against the tests for the current ticket and return the results
    


    # For now, just increment the user's tickets_done and return success
    user.tickets_done += 1
    db.session.commit()

    return jsonify({"message": "Code submitted successfully", "tickets_done": user.tickets_done}), 200



@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
