# Quickstart: Viewing the Frontend

## Local Development (Static)
Before the Flask backend is fully functional, you can view the layouts by opening the HTML files in a browser:
1. Navigate to the `templates/` directory.
2. Open `dashboard.html` or `login.html` in Chrome/Edge.
3. Use Chrome DevTools (F12) to toggle the device toolbar and test mobile responsiveness.

## Backend Integration
1. Ensure Python 3.12+ and Flask are installed.
2. Run the main Flask application: `python app.py`.
3. Navigate to `http://127.0.0.1:5000/dashboard`.

## Testing UI Components
- **Sidebar**: Click the toggle button to verify collapse behavior.
- **Charts**: Verify that the doughnut chart renders correctly on the dashboard.
- **Search**: Type in the pilgrim table search bar to see real-time filtering (using mock data if backend is offline).
- **Forms**: Attempt to submit empty registration forms to trigger Bootstrap validation styles.
