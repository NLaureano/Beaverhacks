# Beaverhacks Backend

Flask backend for the hackathon project. It provides username/password account creation and login backed by MySQL.

## Run locally

1. Create a `.env` file from `.env.example` and point it at your MySQL instance.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the server with `python run.py`.

## API

- `GET /health` returns a simple health check.
- `POST /api/auth/register` creates a user with `username`, `password`, and optional `email`.
- `POST /api/auth/login` returns a JWT access token for a valid username/password pair.
- `GET /api/auth/me` returns the authenticated user.