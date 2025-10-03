# LocalShare Documentation

Welcome to the LocalShare documentation folder!

## 🚀 New Here?

### [START_HERE.md](./START_HERE.md) - Your Starting Point ⭐
Choose your path based on your role and needs. Perfect entry point for everyone!

## 🗺️ Navigation

### [INDEX.md](./INDEX.md) - Complete Navigation Guide
Comprehensive index with topic-based navigation, search by keyword, and learning paths.

## 📚 Available Documents

### [SUMMARY.md](./SUMMARY.md) - Start Here! ⭐
Quick overview of all changes and improvements. Perfect for getting up to speed fast.

### [CHANGES.md](./CHANGES.md) - Complete Changelog
Detailed documentation of all improvements, fixes, and features added to LocalShare.

**Contents:**
- QR Window Closing Issue Fix
- Modern Frontend Redesign
- Server Clipboard Image Copy Enhancement
- Technical implementation details
- Testing recommendations
- Version history

### [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical Deep Dive
System architecture, data flows, and technical diagrams.

**Contents:**
- System architecture diagrams
- Threading model comparison
- Image copy flow
- Component interactions
- File structure
- Technology stack

### [VISUAL_GUIDE.md](./VISUAL_GUIDE.md) - Visual Reference
Before/after comparisons, UI states, and visual examples.

**Contents:**
- Before/after UI comparison
- QR widget states
- Server clipboard feature visuals
- Responsive design layouts
- Button states and animations
- Color scheme and icons

## 🚀 Quick Links

### Main Features
1. **File Upload/Download** - Share files across your local network
2. **Clipboard Sharing** - Copy/paste text and images between devices
3. **Server Clipboard Access** - Access the server machine's clipboard
4. **QR Code Widget** - Easy mobile access via QR code

### Recent Improvements
- ✅ Fixed QR window closing bug
- ✅ Redesigned UI with floating QR widget
- ✅ Enhanced image copy with multiple fallback methods
- ✅ Added download button for images
- ✅ Improved responsive design for all devices

## 📖 How to Use

### Starting the Server
```bash
python app.py
```

### Accessing the Interface
1. **Desktop**: Open browser to `http://[your-ip]:5000`
2. **Mobile**: Scan the QR code or enter the URL
3. **QR Widget**: Click the blue button in bottom-right corner

### Features Guide

#### Upload Files
- Drag and drop files or click to browse
- Multiple file selection supported
- Files saved to `uploads/` folder

#### Share Clipboard
- Click in the paste area
- Paste text or images (Ctrl+V / Cmd+V)
- Click "Send Pasted Content"

#### Server Clipboard
- Click "Fetch" to get server clipboard
- For images: Use "Copy" or download button
- Works with text and images

#### Download Files
- Files in `data/` folder are listed
- Click any file to download

## 🔧 Technical Stack

- **Backend**: Flask (Python)
- **Image Processing**: Pillow
- **Clipboard**: pyperclip, PIL ImageGrab
- **QR Codes**: qrcode library
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Icons**: Font Awesome 6

## 📱 Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| File Upload | ✅ | ✅ | ✅ | ✅ |
| Text Clipboard | ✅ | ✅ | ✅ | ✅ |
| Image Copy | ✅ | ✅ | ✅ | ✅ |
| QR Widget | ✅ | ✅ | ✅ | ✅ |
| Responsive | ✅ | ✅ | ✅ | ✅ |

## 🐛 Troubleshooting

### QR Window Won't Close
- **Fixed!** You can now close the QR popup without stopping the server

### Image Copy Not Working
- Try the download button instead
- Right-click and select "Copy Image"
- Check browser console for errors

### Server Not Accessible
- Check firewall settings
- Verify you're on the same network
- Try accessing via `localhost:5000` on server machine

## 📝 Contributing

If you'd like to contribute or report issues:
1. Document the issue clearly
2. Include browser/OS information
3. Provide steps to reproduce
4. Check existing documentation first

## 📄 License

LocalShare is a local network file sharing tool.
Use responsibly and only on trusted networks.

---

*For detailed technical changes, see [CHANGES.md](./CHANGES.md)*
