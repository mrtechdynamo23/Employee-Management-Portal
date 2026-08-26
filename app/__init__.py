"""
EmployeeHub Application Factory
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access the dashboard.'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # User loader for Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.employees import employees_bp
    from app.routes.tasks import tasks_bp
    from app.routes.performance import performance_bp
    from app.routes.attendance import attendance_bp
    from app.routes.analytics import analytics_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(performance_bp, url_prefix='/performance')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # Context processor for templates
    @app.context_processor
    def inject_globals():
        from flask_login import current_user
        return dict(current_user=current_user)

    # Initialize database and seed demo data on first start (non-testing)
    if not app.config.get('TESTING'):
        with app.app_context():
            import os
            os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
            db.create_all()
            from app.models.user import User
            if User.query.count() == 0:
                try:
                    from app.utils.seed_data import seed_all
                    seed_all()
                except Exception as ex:
                    print(f"[EmployeeHub] Notice: Initial seed skipped or already present: {ex}")

    return app
