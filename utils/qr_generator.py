import qrcode
import os

def generate_pilgrim_qr(pilgrim_id, data):
    """
    Generates a QR code for a pilgrim and saves it to static/images/qr/
    """
    qr_dir = os.path.join('static', 'images', 'qr')
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # QR content: Could be a URL to the pilgrim pass or just JSON data
    qr.add_data(f"Pilgrim ID: {pilgrim_id}\nName: {data.get('name')}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    file_name = f"{pilgrim_id}.png"
    file_path = os.path.join(qr_dir, file_name)
    img.save(file_path)
    
    return f"/static/images/qr/{file_name}"
