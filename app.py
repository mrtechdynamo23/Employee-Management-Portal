"""
EmployeeHub — Employment Task Management & Performance Tracking System
Entry point for the Flask application.
"""
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Seed data on first run if database is empty
        from app.models.user import User
        if User.query.count() == 0:
            print("[EmployeeHub] First run detected. Seeding demo data...")
            from app.utils.seed_data import seed_all
            seed_all()
            print("[EmployeeHub] Demo data seeded successfully!")
            print("[EmployeeHub] Login: admin@employeehub.com / admin123")

    print("\n=== EmployeeHub is running ===")
    print("URL: http://localhost:5000")
    print("Demo: admin@employeehub.com / admin123\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
