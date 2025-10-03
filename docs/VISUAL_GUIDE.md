# LocalShare Visual Guide

## Before & After Comparison

### QR Code Placement

#### Before (v1.0)
```
┌─────────────────────────────────────────┐
│           LocalShare Header             │
├─────────────────────────────────────────┤
│                                         │
│     ┌─────────────────────────┐        │
│     │                         │        │
│     │    [QR CODE IMAGE]      │        │
│     │      (Large)            │        │
│     │                         │        │
│     │  http://192.168.1.5/    │        │
│     │   [Copy URL Button]     │        │
│     └─────────────────────────┘        │
│                                         │
│  Takes up significant space! ❌         │
│                                         │
├─────────────────────────────────────────┤
│  Upload Files Card                      │
├─────────────────────────────────────────┤
│  Share Clipboard Card                   │
└─────────────────────────────────────────┘
```

#### After (v2.0)
```
┌─────────────────────────────────────────┐
│           LocalShare Header             │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐  ┌─────────────┐     │
│  │   Upload    │  │   Share     │     │
│  │   Files     │  │  Clipboard  │     │
│  │             │  │             │     │
│  └─────────────┘  └─────────────┘     │
│                                         │
│  ┌─────────────┐  ┌─────────────┐     │
│  │   Server    │  │  Download   │     │
│  │  Clipboard  │  │   Files     │     │
│  │             │  │             │     │
│  └─────────────┘  └─────────────┘     │
│                                         │
│  More space for features! ✅            │
│                                    ┌───┐│
│                                    │[QR]││
│                                    └───┘│
└─────────────────────────────────────────┘
     QR Widget in corner (click to expand)
```

### QR Widget States

#### Collapsed (Default)
```
                              ┌─────┐
                              │     │
                              │ QR  │  ← Blue circular button
                              │     │     with gradient
                              └─────┘
```

#### Expanded (On Click)
```
                    ┌─────────────────────┐
                    │ Scan to Connect  [X]│
                    ├─────────────────────┤
                    │                     │
                    │   [QR CODE IMAGE]   │
                    │                     │
                    ├─────────────────────┤
                    │ http://192.168.1.5/ │
                    ├─────────────────────┤
                    │   [Copy URL] 📋     │
                    └─────────────────────┘
                              ┌─────┐
                              │     │
                              │ QR  │
                              │     │
                              └─────┘
```

## Server Clipboard Feature

### Text Content
```
┌─────────────────────────────────────────┐
│  Server Clipboard                       │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Hello, this is text from the      │ │
│  │ server clipboard!                 │ │
│  │                                   │ │
│  │ You can copy this to your         │ │
│  │ clipboard.                        │ │
│  └───────────────────────────────────┘ │
│                                         │
├─────────────────────────────────────────┤
│  [Fetch] 🔄    [Copy] 📋               │
└─────────────────────────────────────────┘
```

### Image Content
```
┌─────────────────────────────────────────┐
│  Server Clipboard                       │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐ │
│  │                                   │ │
│  │      [IMAGE PREVIEW]              │ │
│  │                                   │ │
│  └───────────────────────────────────┘ │
│                                         │
├─────────────────────────────────────────┤
│  [Fetch] 🔄  [Copy] 📋  [Download] 💾  │
└─────────────────────────────────────────┘
         ↑           ↑           ↑
         │           │           └─ NEW! Download option
         │           └─ Enhanced with fallbacks
         └─ Fetch from server
```

## Image Copy Process (Visual)

### User Perspective
```
1. Click "Fetch"
   ┌─────────────┐
   │   [Fetch]   │ ← Click
   └─────────────┘

2. Image Appears
   ┌─────────────┐
   │   [IMAGE]   │
   └─────────────┘

3. Click "Copy"
   ┌─────────────┐
   │   [Copy]    │ ← Click
   └─────────────┘

4. See Success Message
   ┌──────────────────────────────────┐
   │ ✅ Image copied successfully!    │
   └──────────────────────────────────┘

5. Paste Anywhere
   Ctrl+V / Cmd+V in any app!
```

### Behind the Scenes
```
User Clicks Copy
      │
      ▼
┌─────────────────┐
│ Try Method 1    │ ← Modern Clipboard API
│ (Clipboard API) │
└────────┬────────┘
         │
    Success? ──YES──> ✅ Done!
         │
         NO
         │
         ▼
┌─────────────────┐
│ Try Method 2    │ ← Canvas-based
│ (Canvas Copy)   │
└────────┬────────┘
         │
    Success? ──YES──> ✅ Done!
         │
         NO
         │
         ▼
┌─────────────────┐
│ Try Method 3    │ ← Legacy method
│(ContentEditable)│
└────────┬────────┘
         │
    Success? ──YES──> ✅ Done!
         │
         NO
         │
         ▼
┌─────────────────┐
│ Show Help       │ ← User guidance
│ Message         │
└─────────────────┘
```

## Responsive Design

### Desktop (> 1024px)
```
┌────────────────────────────────────────────────────┐
│                  LocalShare                        │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Upload   │  │  Share   │  │  Server  │       │
│  │ Files    │  │Clipboard │  │Clipboard │       │
│  │          │  │          │  │          │       │
│  │          │  │          │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│                                                    │
│  ┌──────────┐                                     │
│  │Download  │                              ┌────┐ │
│  │ Files    │                              │[QR]│ │
│  │          │                              └────┘ │
│  └──────────┘                                     │
└────────────────────────────────────────────────────┘
```

### Tablet (768px - 1024px)
```
┌──────────────────────────────────┐
│         LocalShare               │
├──────────────────────────────────┤
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │  Upload    │  │   Share    │ │
│  │  Files     │  │ Clipboard  │ │
│  └────────────┘  └────────────┘ │
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │  Server    │  │ Download   │ │
│  │ Clipboard  │  │  Files     │ │
│  └────────────┘  └────────────┘ │
│                                  │
│                          ┌────┐  │
│                          │[QR]│  │
│                          └────┘  │
└──────────────────────────────────┘
```

### Mobile (< 768px)
```
┌────────────────────┐
│    LocalShare      │
├────────────────────┤
│                    │
│  ┌──────────────┐ │
│  │   Upload     │ │
│  │   Files      │ │
│  └──────────────┘ │
│                    │
│  ┌──────────────┐ │
│  │    Share     │ │
│  │  Clipboard   │ │
│  └──────────────┘ │
│                    │
│  ┌──────────────┐ │
│  │   Server     │ │
│  │  Clipboard   │ │
│  └──────────────┘ │
│                    │
│  ┌──────────────┐ │
│  │  Download    │ │
│  │   Files      │ │
│  └──────────────┘ │
│                    │
│            ┌────┐  │
│            │[QR]│  │
│            └────┘  │
└────────────────────┘
```

## Button States

### Upload Files Button
```
Disabled (No files selected)
┌──────────────────────────┐
│ 📤 Upload Selected Files │ ← Gray, not clickable
└──────────────────────────┘

Enabled (Files selected)
┌──────────────────────────┐
│ 📤 Upload Selected Files │ ← Blue, clickable
└──────────────────────────┘

Hover
┌──────────────────────────┐
│ 📤 Upload Selected Files │ ← Darker blue
└──────────────────────────┘
```

### Server Clipboard Buttons
```
Initial State
┌────────┐  ┌──────┐  ┌──────────┐
│ Fetch  │  │ Copy │  │ Download │
└────────┘  └──────┘  └──────────┘
   Blue      Gray       Hidden
  Active    Disabled

After Fetching Text
┌────────┐  ┌──────┐  ┌──────────┐
│ Fetch  │  │ Copy │  │ Download │
└────────┘  └──────┘  └──────────┘
   Blue      Gray       Hidden
  Active    Active

After Fetching Image
┌────────┐  ┌──────┐  ┌──────────┐
│ Fetch  │  │ Copy │  │ Download │
└────────┘  └──────┘  └──────────┘
   Blue      Gray       Gray
  Active    Active     Active
```

## Flash Messages

### Success
```
┌────────────────────────────────────────┐
│ ✅ Image copied successfully!      [×] │
└────────────────────────────────────────┘
Green background, auto-dismiss after 5s
```

### Warning
```
┌────────────────────────────────────────┐
│ ⚠️  Right-click and select "Copy"  [×] │
└────────────────────────────────────────┘
Yellow background, helpful guidance
```

### Error
```
┌────────────────────────────────────────┐
│ ❌ Failed to fetch clipboard       [×] │
└────────────────────────────────────────┘
Red background, clear error message
```

### Info
```
┌────────────────────────────────────────┐
│ ℹ️  Server URL copied to clipboard [×] │
└────────────────────────────────────────┘
Blue background, informational
```

## Animation Examples

### QR Widget Toggle
```
Collapsed → Expanding
    ┌───┐         ┌─────────┐
    │QR │   →     │ Scan to │
    └───┘         │ Connect │
                  └─────────┘
                  
Opacity: 0 → 1
Transform: translateY(10px) → translateY(0)
Scale: 0.95 → 1
Duration: 300ms
Easing: cubic-bezier(0.4, 0, 0.2, 1)
```

### Button Hover
```
Normal → Hover
┌──────────┐     ┌──────────┐
│  Button  │  →  │  Button  │
└──────────┘     └──────────┘
                 (Darker shade)

Transform: scale(1) → scale(1.02)
Duration: 200ms
```

### Flash Message Appear/Disappear
```
Appear:
Opacity: 0 → 1
Transform: translateY(-10px) → translateY(0)
Duration: 300ms

Disappear:
Opacity: 1 → 0
Transform: translateY(0) → translateY(-10px)
Duration: 300ms
```

## Color Scheme

### Primary Colors
```
┌────────┐  ┌────────┐  ┌────────┐
│ Blue   │  │ Green  │  │ Purple │
│#3b82f6 │  │#10b981 │  │#8b5cf6 │
└────────┘  └────────┘  └────────┘
 Primary     Success     Accent
```

### Status Colors
```
┌────────┐  ┌────────┐  ┌────────┐
│ Yellow │  │  Red   │  │  Gray  │
│#f59e0b │  │#ef4444 │  │#6b7280 │
└────────┘  └────────┘  └────────┘
 Warning     Error      Secondary
```

### Background Colors
```
┌────────┐  ┌────────┐  ┌────────┐
│ White  │  │ Light  │  │ Border │
│#ffffff │  │#f3f4f6 │  │#e5e7eb │
└────────┘  └────────┘  └────────┘
  Cards      Page BG    Dividers
```

## Icon Usage

### Feature Icons
- 📤 Upload Files: `fa-upload`
- 📋 Share Clipboard: `fa-paste`
- 🖥️ Server Clipboard: `fa-server`
- 📥 Download Files: `fa-download`
- 🔄 Refresh/Fetch: `fa-sync`
- 📱 QR Code: `fa-qrcode`

### Action Icons
- ✅ Success: `fa-check-circle`
- ❌ Error: `fa-exclamation-circle`
- ⚠️ Warning: `fa-exclamation-triangle`
- ℹ️ Info: `fa-info-circle`
- 📋 Copy: `fa-copy`
- 💾 Download: `fa-download`
- ✖️ Close: `fa-times`

---

*For technical details, see [ARCHITECTURE.md](./ARCHITECTURE.md)*  
*For complete changelog, see [CHANGES.md](./CHANGES.md)*
