# LocalShare

LocalShare is a web-based file sharing and clipboard synchronization application designed for local network use. It allows users to easily share files and clipboard content between devices on the same network.

## Features

- **File Upload**: Drag & drop or select files to upload to the server
- **File Download**: Access and download files from a shared directory
- **Clipboard Sharing**:
  - Text sharing across devices
  - Image sharing support
  - Server clipboard synchronization
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Instant feedback on operations
- **Network Accessible**: Available to all devices on the local network

## Requirements

- Python 3.x
- Flask >= 2.0.0
- Werkzeug >= 2.0.0
- pyperclip >= 1.8.2

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Directory Structure

```
LocalShare/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── data/              # Directory for shared files
├── static/            # Static assets
│   └── css/
│       └── styles.css # Application styling
├── templates/         # HTML templates
│   └── index.html    # Main application interface
└── uploads/          # Upload directory
    └── clipboard/    # Clipboard content storage
```

## Usage

1. Start the server:
   ```bash
   python app.py
   ```

2. The application will display the local IP address and port (default: 5000)
   ```
   http://<your-local-ip>:5000
   ```

3. Access the web interface from any device on the same network using the provided URL

## Features in Detail

### File Sharing

- Upload files through drag & drop or file selection
- Files are securely saved with sanitized filenames
- Download files from the shared data directory
- Support for multiple file uploads
- Maximum upload size: 1GB (configurable)

### Clipboard Sharing

- **Text Sharing**: 
  - Paste text content directly into the interface
  - Synchronize with server clipboard
  - View and copy shared text content

- **Image Sharing**:
  - Paste images directly from clipboard
  - Supports common image formats (PNG, JPEG, GIF, BMP, WEBP)
  - Preview images before sharing

### Security Features

- Filename sanitization
- Path traversal protection
- Upload size limits
- MIME type validation for images
- Random secret key generation for sessions

## Configuration

The following settings can be modified in `app.py`:

- `UPLOAD_FOLDER`: Directory for uploaded files
- `DATA_FOLDER`: Directory for downloadable files
- `CLIPBOARD_FOLDER`: Directory for clipboard content
- `MAX_CONTENT_LENGTH`: Maximum upload size (default: 1GB)

## Development

- Debug mode is enabled by default (`debug=True`)
- Comprehensive logging system included
- Error handling for all operations
- Modular design for easy extension

## Production Deployment

For production deployment, it's recommended to:

1. Disable debug mode
2. Use a production-ready WSGI server (e.g., Waitress or Gunicorn)
3. Configure appropriate security settings
4. Set up proper file permissions

Example using Waitress:
```python
from waitress import serve
serve(app, host='0.0.0.0', port=5000)
```

