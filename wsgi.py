"""
WSGI entry point for EmployeeHub.
Used by Gunicorn or other WSGI servers in production.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
