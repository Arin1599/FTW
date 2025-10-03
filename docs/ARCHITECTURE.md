# LocalShare Architecture & Changes

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     LocalShare Server                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Main Thread  │  │ Flask Server │  │  QR Window   │     │
│  │   (Loop)     │  │   (Thread)   │  │   (Thread)   │     │
│  │              │  │              │  │              │     │
│  │  Manages     │  │  Handles     │  │  Shows QR    │     │
│  │  Lifecycle   │  │  HTTP        │  │  Popup       │     │
│  │              │  │  Requests    │  │  (Optional)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
└────────────────────────────┼────────────────────────────────┘
                             │
                             │ HTTP (Port 5000)
                             │
                    ┌────────┴────────┐
                    │                 │
            ┌───────▼──────┐  ┌──────▼───────┐
            │   Desktop    │  │    Mobile    │
            │   Browser    │  │    Browser   │
            └──────────────┘  └──────────────┘
```

## Frontend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface (HTML)                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Header: LocalShare Title & Description               │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Upload     │  │    Share     │  │   Server     │     │
│  │   Files      │  │  Clipboard   │  │  Clipboard   │     │
│  │              │  │              │  │              │     │
│  │  Drag/Drop   │  │  Paste Area  │  │  Fetch/Copy  │     │
│  │  Multiple    │  │  Text/Image  │  │  Download    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐                                           │
│  │  Download    │          ┌──────────────────┐            │
│  │   Files      │          │   QR Widget      │            │
│  │              │          │  (Bottom-Right)  │            │
│  │  File List   │          │                  │            │
│  └──────────────┘          │  [QR] Button     │            │
│                            │   ↓ Click        │            │
│                            │  QR Panel        │            │
│                            └──────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## Image Copy Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  Image Copy Process                          │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ User Clicks    │
                    │ "Copy" Button  │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Method 1:     │
                    │  Clipboard API │
                    └────────┬───────┘
                             │
                    ┌────────▼────────┐
                    │   Success?      │
                    └────┬───────┬────┘
                         │       │
                    YES  │       │  NO
                         │       │
                         │       ▼
                         │  ┌────────────────┐
                         │  │  Method 2:     │
                         │  │  Canvas Copy   │
                         │  └────────┬───────┘
                         │           │
                         │  ┌────────▼────────┐
                         │  │   Success?      │
                         │  └────┬───────┬────┘
                         │       │       │
                         │  YES  │       │  NO
                         │       │       │
                         │       │       ▼
                         │       │  ┌────────────────┐
                         │       │  │  Method 3:     │
                         │       │  │ ContentEditable│
                         │       │  └────────┬───────┘
                         │       │           │
                         │       │  ┌────────▼────────┐
                         │       │  │   Success?      │
                         │       │  └────┬───────┬────┘
                         │       │       │       │
                         │       │  YES  │       │  NO
                         │       │       │       │
                         │       │       │       ▼
                         │       │       │  ┌────────────────┐
                         │       │       │  │  Show User     │
                         │       │       │  │  Instructions  │
                         │       │       │  └────────────────┘
                         │       │       │
                         └───────┴───────┴───────┐
                                                 │
                                                 ▼
                                        ┌────────────────┐
                                        │ Show Success   │
                                        │ Message        │
                                        └────────────────┘
```

## Threading Model Comparison

### Before (v1.0)
```
Main Thread
    │
    ├─► Start Flask Server (daemon=False)
    │
    └─► Show QR Window (BLOCKS HERE)
            │
            └─► User closes window
                    │
                    └─► ENTIRE APP EXITS ❌
```

### After (v2.0)
```
Main Thread
    │
    ├─► Start Flask Server (daemon=True)
    │       │
    │       └─► Runs independently ✅
    │
    ├─► Start QR Window (daemon=True)
    │       │
    │       └─► Runs independently ✅
    │
    └─► Keep-alive loop
            │
            └─► Server continues even if QR closes ✅
```

## Data Flow

### File Upload
```
Client Browser
    │
    ├─► Select/Drop Files
    │
    ▼
POST /upload
    │
    ├─► Validate Files
    │
    ├─► Secure Filename
    │
    └─► Save to uploads/
            │
            └─► Return Success
```

### Clipboard Share
```
Client Browser
    │
    ├─► Paste Content (Ctrl+V)
    │
    ├─► Detect Type (text/image)
    │
    ▼
POST /upload_clipboard
    │
    ├─► Process Data
    │
    └─► Save to uploads/clipboard/
            │
            └─► Return Success
```

### Server Clipboard Fetch
```
Client Browser
    │
    └─► Click "Fetch"
            │
            ▼
    GET /get_server_clipboard
            │
            ├─► Try ImageGrab (image)
            │       │
            │       └─► Found? Return base64
            │
            └─► Try pyperclip (text)
                    │
                    └─► Return text
                            │
                            ▼
                    Client Receives Data
                            │
                            ├─► Display in UI
                            │
                            └─► Enable Copy/Download
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                      Flask Backend                           │
│                                                              │
│  Routes:                                                     │
│  • GET  /                    → index.html                   │
│  • POST /upload              → Save files                   │
│  • POST /upload_clipboard    → Save clipboard               │
│  • GET  /download/<file>     → Send file                    │
│  • GET  /get_server_clipboard → Get clipboard               │
│                                                              │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       │ JSON/HTML/Files
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                   Frontend JavaScript                        │
│                                                              │
│  Functions:                                                  │
│  • setupFileUpload()         → Drag/drop handling           │
│  • setupClipboard()          → Paste handling               │
│  • setupServerClipboard()    → Fetch/copy/download          │
│  • setupQRWidget()           → Toggle QR panel              │
│  • flashMessage()            → User feedback                │
│                                                              │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       │ DOM Updates
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                      HTML/CSS UI                             │
│                                                              │
│  Components:                                                 │
│  • Feature Cards             → Main content areas           │
│  • QR Widget                 → Floating corner button       │
│  • Flash Messages            → Notifications                │
│  • Buttons & Forms           → User interactions            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
LocalShare/
│
├── app.py                      # Flask server & threading
│
├── requirements.txt            # Python dependencies
│
├── templates/
│   └── index.html             # Main UI (HTML + JavaScript)
│
├── static/
│   └── css/
│       └── styles.css         # All styles + QR widget
│
├── uploads/                   # User uploaded files
│   └── clipboard/             # Clipboard content
│
├── data/                      # Files for download
│
└── docs/                      # Documentation
    ├── README.md              # Documentation index
    ├── CHANGES.md             # Complete changelog
    ├── SUMMARY.md             # Quick overview
    └── ARCHITECTURE.md        # This file
```

## Key Technologies

### Backend
- **Flask**: Web framework
- **Pillow (PIL)**: Image processing
- **pyperclip**: Text clipboard access
- **ImageGrab**: Image clipboard access
- **qrcode**: QR code generation
- **threading**: Concurrent execution

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling & animations
- **JavaScript (Vanilla)**: Interactivity
- **Font Awesome**: Icons
- **Clipboard API**: Modern clipboard access
- **Canvas API**: Image manipulation

## Security Considerations

### Current Implementation
- ✅ Secure filename sanitization
- ✅ File type validation
- ✅ Path traversal prevention
- ✅ Local network only (0.0.0.0)
- ✅ No authentication (local network trust)

### Recommendations for Production
- 🔒 Add authentication
- 🔒 HTTPS/TLS encryption
- 🔒 Rate limiting
- 🔒 File size limits (already implemented)
- 🔒 Virus scanning
- 🔒 Access logging

## Performance Characteristics

### File Upload
- **Max Size**: 1 GB (configurable)
- **Concurrent**: Multiple files supported
- **Speed**: Limited by network bandwidth

### Clipboard Operations
- **Text**: Instant
- **Images**: < 1 second for typical sizes
- **Copy Methods**: Automatic fallback ensures success

### QR Code
- **Generation**: < 100ms
- **Display**: Instant (cached)
- **Widget Toggle**: Smooth 300ms animation

---

*For implementation details, see [CHANGES.md](./CHANGES.md)*
