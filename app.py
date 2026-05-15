import os
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret')

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.pilgrim_routes import pilgrim_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.qr_routes import qr_bp
    from routes.package_routes import package_bp
    from routes.payment_routes import payment_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pilgrim_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(package_bp)
    app.register_blueprint(payment_bp)

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the error here in a real app
        return {"status": "error", "message": str(e)}, 500

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Temporary UI routes (rendered via Blueprints later or kept here for simplicity)
    @app.route('/dashboard')
    def dashboard_ui():
        return render_template('dashboard.html', active_page='dashboard')

    @app.route('/pilgrims')
    def pilgrims_ui():
        return render_template('pilgrims.html', active_page='pilgrims')

    @app.route('/packages')
    def packages_ui():
        return render_template('packages.html', active_page='packages')

    @app.route('/payments')
    def payments_ui():
        return render_template('payments.html', active_page='payments')

    @app.route('/qr_details/<id>')
    def qr_details(id):
        from database.db import db
        pilgrim = db.pilgrims.find_one({"pilgrim_id": id})
        return render_template('qr_details.html', pilgrim=pilgrim, active_page='pilgrims')

    @app.route('/generate_report')
    def generate_report():
        # Professional demo for report generation
        return """
        <div style='font-family:sans-serif; padding: 50px; text-align:center;'>
            <h1 style='color:#0d6efd;'>Hajj Management System</h1>
            <h3>Project Status Report Generated</h3>
            <p>Report Date: 2026-05-15</p>
            <table border='1' style='margin: 0 auto; width: 60%; border-collapse: collapse;'>
                <tr style='background:#f8f9fa;'><th>Module</th><th>Status</th></tr>
                <tr><td>Pilgrim Records</td><td>Synchronized</td></tr>
                <tr><td>Financial Tracking</td><td>Active</td></tr>
                <tr><td>QR System</td><td>Operational</td></tr>
            </table>
            <br>
            <button onclick='window.print()' style='padding:10px 20px; background:#198754; color:white; border:none; border-radius:5px; cursor:pointer;'>Download PDF / Print</button>
            <p><a href='/dashboard'>Go Back to Dashboard</a></p>
        </div>
        """

    @app.route('/settings')
    def settings_ui():
        return """
        <div style='font-family:sans-serif; padding: 50px; text-align:center;'>
            <h1 style='color:#0d6efd;'>System Settings</h1>
            <p>Admin configuration and security parameters.</p>
            <div style='background:#f8f9fa; padding: 20px; border-radius:15px; display:inline-block; border:1px solid #ddd;'>
                <p><strong>System Version:</strong> v1.2.0 (Smart Build)</p>
                <p><strong>Database:</strong> MongoDB Local</p>
                <p><strong>Status:</strong> Ready for Viva</p>
                <hr>
                <p>New credentials can be managed in <code>.env</code></p>
            </div>
            <p><a href='/dashboard'>Go Back to Dashboard</a></p>
        </div>
        """

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
