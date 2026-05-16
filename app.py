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
    from routes.offer_routes import offer_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pilgrim_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(package_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(offer_bp)

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
        from database.db import db
        from datetime import datetime, time

        # Get start and end of TODAY
        today_start = datetime.combine(datetime.now().date(), time.min)
        today_end = datetime.combine(datetime.now().date(), time.max)

        # Fetch pilgrims registered today
        pilgrims_today = list(db.pilgrims.find({
            "created_at": {"$gte": today_start, "$lte": today_end}
        }))

        # Generate rows for the table
        rows_html = ""
        if not pilgrims_today:
            rows_html = "<tr><td colspan='4' style='text-align:center; padding:20px;'>No records found for today.</td></tr>"
        else:
            for p in pilgrims_today:
                reg_time = p.get('created_at').strftime('%I:%M %p') if p.get('created_at') else 'N/A'
                rows_html += f"""
                <tr>
                    <td style='padding:12px;'>{reg_time}</td>
                    <td style='padding:12px;'>{p.get('name')}</td>
                    <td style='padding:12px;'>{p.get('package')}</td>
                    <td style='padding:12px;'><strong>{p.get('status', 'Pending')}</strong></td>
                </tr>
                """

        return f"""
        <html>
        <head>
            <title>Daily Report - ALKHAMS</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, sans-serif; padding: 40px; color: #333; }}
                .report-header {{ text-align: center; margin-bottom: 40px; border-bottom: 2px solid #0d6efd; padding-bottom: 20px; }}
                .agency-name {{ color: #0d6efd; font-size: 28px; font-weight: bold; margin-bottom: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background-color: #f8f9fa; color: #666; text-align: left; padding: 12px; border-bottom: 2px solid #dee2e6; }}
                td {{ border-bottom: 1px solid #eee; }}
                .no-print {{ margin-top: 30px; text-align: center; }}
                .btn-print {{ padding: 10px 25px; background: #198754; color: white; border: none; border-radius: 50px; cursor: pointer; font-weight: bold; }}
                @media print {{ .no-print {{ display: none; }} }}
            </style>
        </head>
        <body>
            <div class='report-header'>
                <div class='agency-name'>ALKHAMS AGENCY</div>
                <div style='text-transform: uppercase; letter-spacing: 2px; font-size: 14px;'>Daily Registration Report</div>
                <div style='margin-top: 10px; font-weight: bold;'>Date: {datetime.now().strftime('%d %B, %Y')}</div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Time of Entry</th>
                        <th>Pilgrim Name</th>
                        <th>Hajj Package</th>
                        <th>Payment Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>

            <div class='no-print'>
                <button onclick='window.print()' class='btn-print'>
                    <i class='fas fa-file-pdf'></i> Download as PDF / Print
                </button>
                <p><a href='/dashboard' style='color: #666; text-decoration: none;'>← Back to Dashboard</a></p>
            </div>
        </body>
        </html>
        """

    @app.route('/settings')
    def settings_ui():
        # Premium System Intelligence Hub for Viva
        return """
        <html>
        <head>
            <title>System Intelligence - ALKHAMS</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
            <style>
                body { background: #f8fafc; font-family: 'Segoe UI', Tahoma, sans-serif; padding: 50px; }
                .doc-card { background: white; border-radius: 2rem; border: none; box-shadow: 0 10px 30px rgba(0,0,0,0.05); padding: 3rem; max-width: 900px; margin: 0 auto; }
                .module-box { background: #f1f5f9; border-radius: 1.5rem; padding: 1.5rem; margin-bottom: 1.5rem; border-left: 5px solid #0d6efd; }
                .tech-badge { background: #0d6efd; color: white; padding: 5px 15px; border-radius: 50px; font-size: 0.8rem; margin-right: 5px; }
            </style>
        </head>
        <body>
            <div class="doc-card">
                <div class="text-center mb-5">
                    <h1 class="fw-bold text-primary">System Intelligence Hub</h1>
                    <p class="text-muted">A technical guide to the ALKHAMS Smart Hajj Management Architecture</p>
                    <hr style="width: 100px; margin: 20px auto; border-top: 3px solid #0d6efd;">
                </div>

                <div class="row g-4">
                    <!-- Overall Flow -->
                    <div class="col-12">
                        <h4 class="fw-bold mb-3"><i class="fas fa-project-diagram me-2"></i> How the System Works</h4>
                        <p>The project follows a <strong>Full-Stack Modular Architecture</strong>. When a user interacts with the UI, a JavaScript <code>fetch()</code> request is sent to the <strong>Flask Backend</strong>, which processes the logic and communicates with the <strong>Local MongoDB</strong> database to store or retrieve real-time data.</p>
                    </div>

                    <!-- Module Breakdown -->
                    <div class="col-md-6">
                        <div class="module-box">
                            <h5 class="fw-bold text-dark"><i class="fas fa-th-large me-2"></i> Dashboard</h5>
                            <p class="small text-muted">Uses <strong>MongoDB Aggregation</strong> to calculate live revenue and pilgrim counts. Integrated with <strong>Chart.js</strong> for visual financial insights.</p>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="module-box" style="border-left-color: #1cc88a;">
                            <h5 class="fw-bold text-dark"><i class="fas fa-users me-2"></i> Pilgrim Directory</h5>
                            <p class="small text-muted">A full <strong>CRUD system</strong>. Features real-time client-side filtering and automated <strong>QR Generation</strong> triggers upon registration.</p>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="module-box" style="border-left-color: #f6c23e;">
                            <h5 class="fw-bold text-dark"><i class="fas fa-wallet me-2"></i> Financial Ledger</h5>
                            <p class="small text-muted">Implemented a <strong>Database Sync Trigger</strong>. Any status change in the directory automatically updates the financial balance here.</p>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="module-box" style="border-left-color: #e74a3b;">
                            <h5 class="fw-bold text-dark"><i class="fas fa-qrcode me-2"></i> Smart Identification</h5>
                            <p class="small text-muted">Utilizes the <code>python-qrcode</code> library to create unique, printable digital passes for every registered pilgrim.</p>
                        </div>
                    </div>

                    <!-- Security & Environment -->
                    <div class="col-12 mt-4">
                        <h4 class="fw-bold mb-3"><i class="fas fa-shield-alt me-2"></i> Security & Core Stack</h4>
                        <div class="mb-3">
                            <span class="tech-badge">Python 3.12+</span>
                            <span class="tech-badge">Flask Framework</span>
                            <span class="tech-badge">MongoDB NoSQL</span>
                            <span class="tech-badge">Bootstrap 5 UI</span>
                        </div>
                        <p class="small">Administrative access is secured via <strong>Session Authentication</strong>. All sensitive configurations (Database URI, Secret Keys) are protected within a <code>.env</code> environment file.</p>
                    </div>
                </div>

                <div class="text-center mt-5">
                    <a href="/dashboard" class="btn btn-outline-primary rounded-pill px-4">← Return to Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
