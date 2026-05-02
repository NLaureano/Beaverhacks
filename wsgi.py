from app import app

# Expose the Flask `app` for WSGI servers (gunicorn, waitress, etc.)
# Railway or other hosts can start the server with:
#   gunicorn wsgi:app --bind 0.0.0.0:$PORT
