from flask import Blueprint, send_from_directory, abort
import os

qr_bp = Blueprint('qr', __name__)

@qr_bp.route('/api/qr/<filename>')
def serve_qr(filename):
    qr_dir = os.path.abspath(os.path.join('static', 'images', 'qr'))
    if not os.path.exists(os.path.join(qr_dir, filename)):
        abort(404)
    return send_from_directory(qr_dir, filename)
