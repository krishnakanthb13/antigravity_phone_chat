# 📦 Release Notes

---

## v0.1.0 - Initial Release 🎉
**Release Date:** January 17, 2026

We are thrilled to announce the **first official release** of **Antigravity Phone Connect**! This tool transforms your mobile device into a real-time wireless viewport for your Antigravity AI coding sessions, allowing you to step away from your desk while maintaining full visibility and control.

---

### ✨ Features

#### 🔄 Real-Time Mirroring
- **1-Second Polling**: Near-instant sync keeps your phone's display updated with your desktop session.
- **WebSocket Notifications**: Efficient push updates notify your phone only when content changes.
- **Smart Content Hashing**: Minimizes bandwidth by detecting actual UI changes.

#### 🎮 Remote Control
- **Send Messages**: Compose and send prompts to your AI directly from your phone.
- **Stop Generations**: Halt long-running AI generations with a single tap.
- **Mode Switching**: Toggle between **Fast** and **Planning** modes remotely.
- **Model Selection**: Switch between AI models (Gemini, Claude, GPT) on the fly.

#### 🧠 Thought Expansion
- **Remote Click Relay**: Tap on "Thinking..." or "Thought" blocks on your phone to expand them on your desktop IDE.
- **Full Reasoning Access**: Peek into the AI's internal reasoning process from anywhere in your home.

#### 🔁 Bi-Directional Sync
- **State Synchronization**: Changes made on your desktop (model, mode) are automatically reflected on your phone.
- **Force Refresh**: Manually trigger a full sync with the Refresh button when needed.

#### 🎨 Premium Mobile UI
- **Dark-Themed Design**: Sleek, modern slate-dark interface optimized for mobile viewing.
- **Touch-Optimized**: Large tap targets and responsive layouts for comfortable mobile interaction.
- **Aggressive CSS Inheritance**: VS Code theme-agnostic rendering ensures consistent mobile appearance.

#### 📁 Context Menu Integration
- **Windows**: Right-click any folder and select "Open with Antigravity (Debug)" for instant debugging sessions.
- **Linux (Nautilus/GNOME)**: Native Nautilus script integration for seamless right-click access.
- **macOS**: Step-by-step Quick Action guide for Automator-based integration.

#### 🛠️ Context Menu Management Scripts
- **Install/Remove**: Easy toggle for context menu entries.
- **Backup**: Automatic backup before making registry/script changes.
- **Restart**: One-click Explorer (Windows) or Nautilus (Linux) restart to apply changes.

---

### 🖥️ Platform Support

| Platform | Launcher Script | Context Menu Script |
|:---------|:----------------|:--------------------|
| **Windows** | `start_ag_phone_connect.bat` | `install_context_menu.bat` |
| **macOS** | `start_ag_phone_connect.sh` | Manual Automator setup |
| **Linux** | `start_ag_phone_connect.sh` | `install_context_menu.sh` |

---

### 📡 API Endpoints

All endpoints are REST-based and return JSON responses.

---

#### `GET /health`
**Purpose:** Check server status and CDP connection health.

**Response:**
```json
{
  "status": "ok",
  "cdpConnected": true,
  "uptime": 123.456,
  "timestamp": "2026-01-17T01:10:00.000Z"
}
```

**Usage:**
```bash
curl http://192.168.1.x:3000/health
```

---

#### `GET /snapshot`
**Purpose:** Get the latest captured HTML/CSS snapshot of the Antigravity chat.

**Response:**
```json
{
  "html": "<div id=\"cascade\">...</div>",
  "css": "/* Captured stylesheets */",
  "backgroundColor": "rgb(30, 41, 59)",
  "color": "rgb(248, 250, 252)",
  "fontFamily": "Inter, system-ui, sans-serif",
  "stats": {
    "nodes": 245,
    "htmlSize": 52480,
    "cssSize": 128000
  }
}
```

**Usage:**
```bash
curl http://192.168.1.x:3000/snapshot
```

---

#### `GET /app-state`
**Purpose:** Get the current Mode (Fast/Planning) and AI Model selection from the desktop.

**Response:**
```json
{
  "mode": "Fast",
  "model": "Gemini 3 Pro (High)"
}
```

**Usage:**
```bash
curl http://192.168.1.x:3000/app-state
```

**Notes:** Used by the mobile UI to sync state every 5 seconds and on manual refresh.

---

#### `POST /send`
**Purpose:** Send a message/prompt to the Antigravity chat.

**Request Body:**
```json
{
  "message": "Please create a function to sort an array."
}
```

**Response (Success):**
```json
{
  "success": true,
  "method": "click_submit"
}
```

**Response (Error):**
```json
{
  "success": false,
  "reason": "busy"
}
```

**Usage:**
```bash
curl -X POST http://192.168.1.x:3000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Continue"}'
```

---

#### `POST /stop`
**Purpose:** Stop the current AI generation in progress.

**Response (Success):**
```json
{
  "success": true
}
```

**Response (No Active Generation):**
```json
{
  "error": "No active generation found to stop"
}
```

**Usage:**
```bash
curl -X POST http://192.168.1.x:3000/stop
```

---

#### `POST /set-mode`
**Purpose:** Switch between Fast and Planning modes.

**Request Body:**
```json
{
  "mode": "Planning"
}
```

**Valid Values:** `"Fast"` or `"Planning"`

**Response (Success):**
```json
{
  "success": true
}
```

**Response (Already Set):**
```json
{
  "success": true,
  "alreadySet": true
}
```

**Usage:**
```bash
curl -X POST http://192.168.1.x:3000/set-mode \
  -H "Content-Type: application/json" \
  -d '{"mode": "Planning"}'
```

---

#### `POST /set-model`
**Purpose:** Change the AI model.

**Request Body:**
```json
{
  "model": "Claude Sonnet 4.5"
}
```

**Available Models (Example):**
- `"Gemini 3 Pro (High)"`
- `"Gemini 3 Pro (Low)"`
- `"Gemini 3 Flash"`
- `"Claude Sonnet 4.5"`
- `"Claude Sonnet 4.5 (Thinking)"`
- `"Claude Opus 4.5 (Thinking)"`
- `"GPT-OSS 120B (Medium)"`

**Response (Success):**
```json
{
  "success": true
}
```

**Usage:**
```bash
curl -X POST http://192.168.1.x:3000/set-model \
  -H "Content-Type: application/json" \
  -d '{"model": "Claude Sonnet 4.5"}'
```

---

#### `POST /remote-click`
**Purpose:** Trigger a click event on the desktop to expand/collapse "Thinking" or "Thought" blocks.

**Request Body:**
```json
{
  "selector": "div",
  "index": 0,
  "textContent": "Thought for 3s"
}
```

**Response (Success):**
```json
{
  "success": true
}
```

**Usage:**
```bash
curl -X POST http://192.168.1.x:3000/remote-click \
  -H "Content-Type: application/json" \
  -d '{"selector": "summary", "index": 0, "textContent": "Thinking"}'
```

**Notes:** Automatically triggered when tapping on Thought/Thinking blocks in the mobile UI.

---

#### `GET /debug-ui`
**Purpose:** Get a serialized UI tree for debugging element selection.

**Response:** JSON representation of the inspected UI tree.

**Usage:**
```bash
curl http://192.168.1.x:3000/debug-ui
```

**Notes:** Outputs to server console as well. Useful for troubleshooting selector issues.

---

### 📊 Endpoint Summary Table

| Endpoint | Method | Used By | Auto-Called |
|:---------|:-------|:--------|:------------|
| `/health` | GET | Health checks, monitoring | No |
| `/snapshot` | GET | Mobile UI rendering | Yes (on WebSocket notification) |
| `/app-state` | GET | Mode/Model sync | Yes (every 5 seconds) |
| `/send` | POST | Message input, Quick Actions | User-initiated |
| `/stop` | POST | Stop button | User-initiated |
| `/set-mode` | POST | Mode selector modal | User-initiated |
| `/set-model` | POST | Model selector modal | User-initiated |
| `/remote-click` | POST | Thought expansion | Tap on Thought blocks |
| `/debug-ui` | GET | Developer debugging | Manual only |

---

### 📋 Requirements

- **Node.js**: v16.0.0 or higher
- **Network**: Phone and PC must be on the same Wi-Fi network
- **Antigravity**: Running with `--remote-debugging-port=9000`

---

### 📦 Dependencies

| Package | Version | Purpose |
|:--------|:--------|:--------|
| `express` | ^4.18.2 | HTTP server for UI and API |
| `ws` | ^8.18.0 | WebSocket for real-time updates |

---

### 🔒 Security

- **Local Network Only**: By design, the app is constrained to your LAN. Your project snapshots and AI tokens are never exposed to the public internet.
- **No Authentication Required**: Simplified setup for trusted home/office networks.
- **CDP Sandboxing**: DOM snapshots are cloned before capture to prevent interference with your desktop session.

---

### 🐛 Known Limitations

- **CDP Port Range**: Auto-discovery scans ports 9000-9003. Ensure Antigravity uses one of these ports.
- **macOS Context Menu**: Requires manual Automator Quick Action setup (no script automation available).
- **Theme Variance**: While CSS inheritance handles most themes, some extreme custom VS Code themes may render differently on mobile.

---

### 🙏 Acknowledgments

This project is a refined fork/extension based on the original [Antigravity Shit-Chat](https://github.com/gherghett/Antigravity-Shit-Chat) by **@gherghett**. Thank you for the foundation that made this possible!

---

### 📄 License

Licensed under the [GNU GPL v3](LICENSE).  
Copyright (C) 2026 **Krishna Kanth B** ([@krishnakanthb13](https://github.com/krishnakanthb13))

---

### 🚀 Getting Started

1. Clone this repository
2. Run `start_ag_phone_connect.bat` (Windows) or `./start_ag_phone_connect.sh` (macOS/Linux)
3. Open the displayed URL on your phone's browser
4. Launch Antigravity with `antigravity . --remote-debugging-port=9000`

**Happy coding from the couch!** 🛋️

---

*For detailed documentation, see [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) and [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md).*
