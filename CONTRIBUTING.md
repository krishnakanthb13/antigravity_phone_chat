# CONTRIBUTING - Antigravity Phone Connect

First off, thank you for considering contributing to Antigravity Phone Connect! It's people like you that make the AI development ecosystem so exciting.

## How to Contribute

### 1. Reporting Bugs
- **Check existing issues** to see if the bug has already been reported.
- **Provide context**: What OS are you using? Which port is Antigravity running on? HTTP or HTTPS?
- **Logs**: Include the output of `server.js` (the console logs) when the error occurred.

### 2. Suggesting Features
- Open a "Feature Request" on GitHub.
- Describe the use case (e.g., "I wish I could scroll the desktop from my phone").

### 3. Development Workflow
1.  **Fork** the repository.
2.  Create a **new branch** (`git checkout -b feature/amazing-feature`).
3.  **Implement** your changes.
    - If you are changing the UI, please test on a real mobile device screen.
    - If you are changing the server, ensure CDP discovery logic is still backward compatible.
    - If you are modifying SSL/HTTPS, test both with and without certificates.
4.  **Validate** your changes (see the checklist below).
5.  **Submit a PR** with a clear description of what changed and why.

## Local Setup

1.  Clone your fork: `git clone https://github.com/krishnakanthb13/antigravity_phone_chat.git`
2.  Install dependencies: `npm install`
3.  **(Optional)** Generate SSL certificates: `node generate_ssl.js`
4.  Start Antigravity with: `agy . --remote-debugging-port=9000`
5.  Run the monitor: `node server.js`
6.  Access from phone: Use the URL shown in terminal (http or https)

## Pre-submission Checklist

- [ ] Code follows existing style (clean, documented JS).
- [ ] No hardcoded personal IPs or credentials.
- [ ] SSL certificates are NOT committed (check `.gitignore`).
- [ ] Snapshot capture still works with the latest Antigravity version.
- [ ] UI is responsive on small (iPhone SE) and large (iPad) screens.
- [ ] Both HTTP and HTTPS modes work correctly.
- [ ] Shell scripts have LF line endings (not CRLF).
- [ ] All documentation updated if new features were added.

## File Structure Notes

| Directory/File | Purpose |
| :--- | :--- |
| `server.js` | Main server - add new API endpoints here |
| `public/` | Mobile UI files (index.html, css/style.css, js/app.js) |
| `generate_ssl.js` | SSL cert generator - uses pure Node.js crypto |
| `certs/` | Generated SSL files - gitignored, never commit |
| `.env.example` | Template for environment variables |
| `SECURITY.md` | Security documentation - update for security changes |
| `*.sh` files | Must have LF line endings for Linux/macOS |

## Testing HTTPS

```bash
# Generate certificates
node generate_ssl.js

# Restart server - should show "🔒 HTTPS enabled"
node server.js

# Test health endpoint
curl -k https://localhost:3000/health
```

## Author

**Krishna Kanth B** (@krishnakanthb13)
