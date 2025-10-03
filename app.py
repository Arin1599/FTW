import os
import socket
import base64
import io
from datetime import datetime
import pyperclip  # Add this import
from werkzeug.utils import secure_filename  # Add this import
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash, jsonify
import logging
from PIL import ImageGrab  # For clipboard image support
from PIL import Image, ImageTk
import threading
try:
    import tkinter as tk
except Exception:
    tk = None
import qrcode
import qrcode.image.svg

# --- Configuration ---
UPLOAD_FOLDER = 'uploads' # Folder to save uploaded files
DATA_FOLDER = 'data'      # Folder containing files for download
CLIPBOARD_FOLDER = os.path.join(UPLOAD_FOLDER, 'clipboard') # Subfolder for clipboard items
STATIC_FOLDER = 'static'  # Folder for static files

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATA_FOLDER'] = DATA_FOLDER
app.config['CLIPBOARD_FOLDER'] = CLIPBOARD_FOLDER
# Set a maximum upload size (e.g., 1GB). Adjust as needed.
# Be aware that the development server might struggle with very large files.
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024 # 1 GB
app.secret_key = os.urandom(24) # Generate a random secret key for session security (flash messages)

# --- Helper Functions ---

def get_ip_address():
    """Gets the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception as e:
        logging.warning(f"Could not determine local IP automatically: {e}. Falling back to 127.0.0.1.")
        IP = '127.0.0.1' # Fallback to localhost
    finally:
        s.close()
    return IP

def ensure_dirs():
    """Creates necessary directories if they don't exist."""
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        logging.info(f"Ensured upload directory exists: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
        os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)
        logging.info(f"Ensured data directory exists: {os.path.abspath(app.config['DATA_FOLDER'])}")
        os.makedirs(app.config['CLIPBOARD_FOLDER'], exist_ok=True)
        logging.info(f"Ensured clipboard directory exists: {os.path.abspath(app.config['CLIPBOARD_FOLDER'])}")
    except OSError as e:
        logging.error(f"Error creating directories: {e}")
        # Depending on the error, you might want to exit or handle differently
        raise # Re-raise the exception if directory creation fails critically

# --- Routes ---

@app.route('/')
def index():
    """Renders the main page, listing downloadable files."""
    ensure_dirs() # Ensure directories exist on first load or restart
    files_in_data = []
    try:
        # List files in the DATA_FOLDER, handling potential errors
        # Filter out directories, list only files
        data_path = app.config['DATA_FOLDER']
        files_in_data = sorted([f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))])
        logging.info(f"Listed {len(files_in_data)} files from data folder: {data_path}")
    except FileNotFoundError:
        flash(f"Data directory '{app.config['DATA_FOLDER']}' not found. Please create it.", "error")
        logging.error(f"Data directory not found: {os.path.abspath(data_path)}")
    except Exception as e:
        flash(f"An error occurred listing files: {e}", "error")
        logging.error(f"Error listing files in {data_path}: {e}")

    # Generate a QR code pointing to the server's advertised URL so users can scan to open the frontend
    try:
        host_ip = get_ip_address()
        port = 5000
        advertised_url = f'http://{host_ip}:{port}/'
        qr_data_uri = generate_qr_data_uri(advertised_url)
    except Exception as e:
        logging.error(f"Failed to generate QR code: {e}")
        qr_data_uri = None

    # Pass the DATA_FOLDER path and qr image data to the template for display purposes
    return render_template('index.html', files=files_in_data, data_folder_name=app.config['DATA_FOLDER'], qr_data_uri=qr_data_uri)


def generate_qr_data_uri(data, box_size=8, border=4):
    """Generate a PNG QR code and return a data URI (base64) suitable for embedding in an <img> tag.

    Keeps dependencies minimal by using Pillow (already a requirement) via qrcode.
    """
    try:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box_size, border=border)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        data_b64 = base64.b64encode(img_bytes).decode('ascii')
        return f'data:image/png;base64,{data_b64}'
    except Exception:
        raise

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file uploads."""
    ensure_dirs()
    if 'files[]' not in request.files:
        flash('No file part in the request', 'error')
        logging.warning("Upload attempt failed: 'files[]' part missing in request.")
        return redirect(url_for('index'))

    files = request.files.getlist('files[]') # Get list of files

    if not files or files[0].filename == '':
        flash('No file selected for upload', 'warning')
        logging.info("Upload attempt failed: No files selected.")
        return redirect(url_for('index'))

    uploaded_count = 0
    failed_files = []
    for file in files:
        if file and file.filename: # Check if file exists and has a name
            original_filename = file.filename
            filename = secure_filename(original_filename) # Sanitize filename
            if not filename: # Handle cases where secure_filename returns empty (e.g., filename is just "..")
                filename = f"unsafe_filename_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                logging.warning(f"Original filename '{original_filename}' sanitized to empty. Renaming to '{filename}'.")

            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(upload_path)
                uploaded_count += 1
                logging.info(f"Successfully saved uploaded file: {upload_path}")
            except Exception as e:
                 failed_files.append(original_filename)
                 logging.error(f"Error saving uploaded file '{original_filename}' to '{upload_path}': {e}")

    if uploaded_count > 0:
        flash(f'Successfully uploaded {uploaded_count} file(s).', 'success')
    if failed_files:
        flash(f'Failed to upload {len(failed_files)} file(s): {", ".join(failed_files)}', 'error')
    elif uploaded_count == 0:
         flash('No files were successfully uploaded.', 'warning')


    return redirect(url_for('index'))


@app.route('/upload_clipboard', methods=['POST'])
def upload_clipboard():
    """Handles clipboard content uploads (text or image)."""
    ensure_dirs()
    content_type = request.form.get('type')
    data = request.form.get('data')

    if not data:
        flash('No clipboard data received', 'warning')
        logging.warning("Clipboard upload attempt failed: No data received.")
        return redirect(url_for('index'))

    filepath = None
    try:
        if content_type == 'text':
            # Use fixed filename for text content
            filename = "clipboard_text.txt"
            filepath = os.path.join(app.config['CLIPBOARD_FOLDER'], filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data)
            flash(f'Clipboard text saved successfully', 'success')
            logging.info(f"Updated clipboard text file at: {filepath}")

        elif content_type == 'image':
            # Keep timestamp-based naming for images
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"clipboard_{timestamp}"
            try:
                header, encoded = data.split(',', 1)
                mime_type = header.split(';')[0].split(':')[1]
                if not mime_type.startswith('image/'):
                    raise ValueError("Invalid MIME type for image")

                file_ext = mime_type.split('/')[1]
                if file_ext not in ['png', 'jpeg', 'jpg', 'gif', 'bmp', 'webp']:
                    logging.warning(f"Unsupported image extension '{file_ext}' received. Defaulting to 'png'.")
                    file_ext = 'png'

                filename = f"{filename}.{file_ext}"
                filepath = os.path.join(app.config['CLIPBOARD_FOLDER'], filename)
                image_data = base64.b64decode(encoded)
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                flash(f'Clipboard image saved as {filename}', 'success')
                logging.info(f"Saved clipboard image to: {filepath}")

            except (ValueError, IndexError, TypeError) as e:
                flash(f'Invalid image data format received: {e}', 'error')
                logging.error(f"Invalid image data format: {e}. Data prefix: {data[:100]}...")
                return redirect(url_for('index'))
            except base64.binascii.Error as e:
                flash(f'Failed to decode base64 image data: {e}', 'error')
                logging.error(f"Base64 decoding error: {e}")
                return redirect(url_for('index'))

        else:
            flash(f'Unknown clipboard content type received: {content_type}', 'error')
            logging.warning(f"Received unknown clipboard content type: {content_type}")
            return redirect(url_for('index'))

    except Exception as e:
        flash(f"Error saving clipboard content: {e}", "error")
        logging.error(f"Error processing clipboard content (type: {content_type}): {e}")
        if filepath:
            logging.error(f"Attempted to save to: {filepath}")

    return redirect(url_for('index'))


@app.route('/download/<path:filename>')
def download_file(filename):
    """Serves files from the DATA_FOLDER for download."""
    ensure_dirs() # Ensure dir exists, though mainly needed for uploads/clipboard
    data_dir = os.path.abspath(app.config['DATA_FOLDER'])
    file_path = os.path.abspath(os.path.join(data_dir, filename))

    # Security Check: Ensure the requested path is within the DATA_FOLDER
    if not file_path.startswith(data_dir + os.sep) and file_path != data_dir:
         flash("Access denied: Attempted to download file outside designated directory.", "error")
         logging.warning(f"Access denied for download: '{filename}'. Resolved path '{file_path}' is outside '{data_dir}'.")
         return redirect(url_for('index')) # Or return 403 Forbidden

    if not os.path.isfile(file_path):
        flash(f"File '{filename}' not found in data folder.", "error")
        logging.warning(f"Download request for non-existent file: '{filename}' at path '{file_path}'.")
        return redirect(url_for('index')) # Or return 404 Not Found

    try:
        logging.info(f"Serving file for download: {file_path}")
        return send_from_directory(data_dir, filename, as_attachment=True)
    except Exception as e:
        flash(f"Error downloading file '{filename}': {e}", "error")
        logging.error(f"Error sending file '{filename}' from '{data_dir}': {e}")
        return redirect(url_for('index')) # Or return 500 Internal Server Error


@app.route('/get_server_clipboard')
def get_server_clipboard():
    """Returns the current clipboard content from the server (text or image)"""
    try:
        # Try to get image from clipboard first
        image = ImageGrab.grabclipboard()
        
        if image is not None:
            # Image found in clipboard
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            logging.info("Retrieved image from server clipboard")
            return jsonify({
                'success': True,
                'data': f'data:image/png;base64,{img_str}',
                'type': 'image'
            })
        else:
            # No image, try text
            clipboard_text = pyperclip.paste()
            logging.info("Retrieved text from server clipboard")
            return jsonify({
                'success': True,
                'data': clipboard_text,
                'type': 'text'
            })
            
    except Exception as e:
        logging.error(f"Error reading server clipboard: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# --- Main Execution ---
if __name__ == '__main__':
    try:
        ensure_dirs() # Ensure directories exist before starting the server
    except Exception as e:
        logging.critical(f"Failed to create necessary directories on startup: {e}. Exiting.")
        exit(1) # Exit if essential directories cannot be created

    host_ip = get_ip_address()
    port = 5000 # You can change the port number if needed (e.g., 8080)

    print("*" * 60)
    print(" LocalShare Server Starting ".center(60, "*"))
    print("*" * 60)
    print(f"INFO: Server will listen on all network interfaces (0.0.0.0).")
    print(f"INFO: Access the application from other devices on the same network:")
    print(f"      >>> http://{host_ip}:{port} <<<")
    print("-" * 60)
    print(f"INFO: Uploads will be saved to folder:")
    print(f"      '{os.path.abspath(UPLOAD_FOLDER)}'")
    print(f"INFO: Clipboard content will be saved to folder:")
    print(f"      '{os.path.abspath(CLIPBOARD_FOLDER)}'")
    print(f"INFO: Place files for download in folder:")
    print(f"      '{os.path.abspath(DATA_FOLDER)}'")
    print("-" * 60)
    print("INFO: Press CTRL+C to stop the server.")
    print("*" * 60)

    # Run the app making it accessible on the network '0.0.0.0'
    # We'll start Flask in a background thread and show a small desktop QR popup using tkinter
    server_url = f'http://{host_ip}:{port}/'

    def run_server():
        # Disable the reloader to avoid double-starting
        try:
            app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
        except Exception as e:
            logging.critical(f"Flask server failed: {e}")

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Try to show a small Tkinter window with the QR code so the user can scan immediately
    # This runs in a separate thread so closing it won't stop the server
    def show_qr_window():
        if tk is not None:
            try:
                # Create QR PIL image
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=6, border=2)
                qr.add_data(server_url)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color='black', back_color='white')

                # Convert to ImageTk
                root = tk.Tk()
                root.title('LocalShare - Scan to Open')
                # Keep window on top
                try:
                    root.attributes('-topmost', True)
                except Exception:
                    pass

                # Resize window to fit QR and some text
                img_w, img_h = qr_img.size
                max_size = 360
                scale = min(1.0, max_size / max(img_w, img_h))
                if scale != 1.0:
                    new_size = (int(img_w * scale), int(img_h * scale))
                    qr_img = qr_img.resize(new_size, Image.NEAREST)

                photo = ImageTk.PhotoImage(qr_img)

                # Image label
                img_label = tk.Label(root, image=photo)
                img_label.pack(padx=10, pady=(10, 0))

                # URL label with monospace font
                url_label = tk.Label(root, text=server_url, fg='#111', font=('Consolas', 10))
                url_label.pack(padx=10, pady=(6, 6))

                # Info label
                info_label = tk.Label(root, text='Closing this window will NOT stop the server', 
                                     fg='#666', font=('Arial', 8))
                info_label.pack(padx=10, pady=(0, 6))

                # Close button
                def close_window():
                    root.destroy()

                btn = tk.Button(root, text='Close', command=close_window)
                btn.pack(pady=(0, 10))

                # Auto-close after 30 seconds
                root.after(30000, lambda: (root.winfo_exists() and root.destroy()))

                # Start the Tk mainloop (this will block only this thread)
                root.mainloop()
            except Exception as e:
                logging.error(f"Failed to show desktop QR popup: {e}")
        else:
            logging.info('Tkinter not available; skipping desktop QR popup.')

    # Run QR window in a separate daemon thread
    qr_thread = threading.Thread(target=show_qr_window, daemon=True)
    qr_thread.start()

    print('\nServer is running. Press CTRL+C to stop.')
    try:
        # Keep the main thread alive
        while True:
            server_thread.join(timeout=1.0)
            if not server_thread.is_alive():
                break
    except KeyboardInterrupt:
        print('\nKeyboard interrupt received, exiting.')