import sys
import subprocess
import time
import random
import string
import os
import socket
import argparse
import logging

# -----------------------------------------------------------------------------
# Dependency Management
# -----------------------------------------------------------------------------
def check_dependencies():
    """Checks and installs required Python packages."""
    needed = ["pyngrok", "python-dotenv", "qrcode", "pinggy"]
    installed = []
    
    # Check what is missing
    for pkg in needed:
        try:
            if pkg == "pyngrok": from pyngrok import ngrok
            elif pkg == "python-dotenv": from dotenv import load_dotenv
            elif pkg == "qrcode": import qrcode
            elif pkg == "pinggy": import pinggy
            installed.append(pkg)
        except ImportError:
            pass

    missing = [pkg for pkg in needed if pkg not in installed]
    
    if missing:
        print(f"📦 Installing missing dependencies: {', '.join(missing)}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✅ Dependencies installed.\n")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)

def check_node_environment():
    """Checks for Node.js and installs npm dependencies if needed."""
    # 1. Check if Node is installed
    try:
        subprocess.check_call(["node", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Error: Node.js is not installed. Please install it from https://nodejs.org/")
        sys.exit(1)

    # 2. Check for node_modules
    if not os.path.exists("node_modules"):
        print("📦 'node_modules' missing. Installing Node.js dependencies...")
        try:
            # shell=True often needed on Windows for npm. On *nix, 'npm' usually works directly if in PATH.
            is_windows = sys.platform == "win32"
            subprocess.check_call(["npm", "install"], shell=is_windows)
            print("✅ Node dependencies installed.\n")
        except Exception as e:
            print(f"❌ Failed to run 'npm install': {e}")
            sys.exit(1)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def get_local_ip():
    """Robustly determines the local LAN IP address."""
    s = None
    try:
        # Connect to a public DNS server (doesn't actually send data)
        # This forces the OS to determine the correct outgoing interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_passcode():
    """Generates a 6-digit passcode."""
    return ''.join(random.choices(string.digits, k=6))

def print_qr(url):
    """Generates and prints a QR code to the terminal."""
    import qrcode
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    # Using 'ANSI' implies standard block characters which work in most terminals
    # invert=True is often needed for dark terminals (white blocks on black bg)
    qr.print_ascii(invert=True)

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
def main():
    import signal
    def handle_sigterm(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, handle_sigterm)

    parser = argparse.ArgumentParser(description="Antigravity Phone Connect Launcher")
    parser.add_argument('--mode', choices=['local', 'web'], default='web', help="Mode to run in: 'local' (WiFi) or 'web' (Internet)")
    parser.add_argument('--provider', choices=['ngrok', 'cloudflare', 'pinggy', 'localtunnel'], help="Tunnel provider (defaults to .env TUNNEL_PROVIDER or 'ngrok')")
    args = parser.parse_args()

    # 1. Setup Environment
    check_dependencies()
    check_node_environment()
    
    # Suppress pyngrok noise (especially during shutdown)
    logging.getLogger("pyngrok").setLevel(logging.ERROR)
    
    from pyngrok import ngrok

    from dotenv import load_dotenv
    
    # Load .env if it exists
    load_dotenv()


    # Determine Provider
    provider = args.provider or os.environ.get('TUNNEL_PROVIDER', 'ngrok').lower()
    
    # Setup App Password
    passcode = os.environ.get('APP_PASSWORD')
    if not passcode:
        passcode = generate_passcode()
        os.environ['APP_PASSWORD'] = passcode # Set for child process
        print(f"⚠️  No APP_PASSWORD in .env. Using temporary: {passcode}")

    # 2. Start Node.js Server (Common to both modes)
    print(f"🚀 Starting Antigravity Server ({args.mode.upper()} mode)...")
    
    # Clean up old logs
    with open("server_log.txt", "w") as f:
        f.write(f"--- Server Started at {time.ctime()} ---\n")

    node_cmd = ["node", "server.js"]
    node_process = None
    
    try:
        # Redirect stdout/stderr to file
        log_file = open("server_log.txt", "a")
        if sys.platform == "win32":
            # On Windows, using shell=True can help with path resolution but makes killing harder.
            # We'll use shell=False and rely on PATH.
            node_process = subprocess.Popen(node_cmd, stdout=log_file, stderr=log_file, env=os.environ.copy())
        else:
            node_process = subprocess.Popen(node_cmd, stdout=log_file, stderr=log_file, env=os.environ.copy())
            
        time.sleep(2) # Give it a moment to crash if it's going to
        if node_process.poll() is not None:
            print("❌ Server failed to start immediately. Check server_log.txt.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Failed to launch node: {e}")
        sys.exit(1)

    # 3. Mode Specific Logic
    final_url = ""
    
    try:
        if args.mode == 'local':
            ip = get_local_ip()
            port = os.environ.get('PORT', '3000')
            
            # Detect HTTPS
            protocol = "http"
            if os.path.exists('certs/server.key') and os.path.exists('certs/server.cert'):
                protocol = "https"
            
            final_url = f"{protocol}://{ip}:{port}"
            
            print("\n" + "="*50)
            print(f"📡 LOCAL WIFI ACCESS")
            print("="*50)
            print(f"🔗 URL: {final_url}")
            print(f"🔑 Passcode: Not required for local WiFi (Auto-detected)")
            
            print("\n📱 Scan this QR Code to connect:")
            print_qr(final_url)

            print("-" * 50)
            print("📝 Steps to Connect:")
            print("1. Ensure your phone is on the SAME Wi-Fi network as this computer.")
            print("2. Open your phone's Camera app or a QR scanner.")
            print("3. Scan the code above OR manually type the URL into your browser.")
            print("4. You should be connected automatically!")
            
        elif args.mode == 'web':
            port = os.environ.get('PORT', '3000')
            
            # Detect HTTPS
            protocol = "http"
            if os.path.exists('certs/server.key') and os.path.exists('certs/server.cert'):
                protocol = "https"
                
            addr = f"{protocol}://localhost:{port}"
            public_url = ""

            if provider == 'pinggy':
                print("PLEASE WAIT... Establishing Pinggy Tunnel...")
                try:
                    import pinggy
                    pinggy_token = os.environ.get('PINGGY_TOKEN', '')  # Optional: for persistent subdomain
                    pinggy_tunnel = pinggy.start_tunnel(
                        forwardto=f"localhost:{port}",
                        token=pinggy_token,
                        localservertls=(protocol == "https")
                    )
                    # Prefer HTTPS URL from the returned list
                    tunnel_urls = pinggy_tunnel.urls if hasattr(pinggy_tunnel, 'urls') else []
                    public_url = next((u for u in tunnel_urls if u.startswith('https://')), None)
                    if not public_url and tunnel_urls:
                        public_url = tunnel_urls[0]  # fallback to first URL
                    if not public_url:
                        print("❌ Failed to obtain a Pinggy URL.")
                        sys.exit(1)
                except ImportError:
                    print("❌ Error: 'pinggy' package not found. Run: pip install pinggy")
                    sys.exit(1)
                except Exception as e:
                    print(f"❌ Failed to start Pinggy Tunnel: {e}")
                    sys.exit(1)

            elif provider == 'cloudflare':
                cf_name = os.environ.get('CLOUDFLARE_TUNNEL_NAME') or os.environ.get('CLOUDFLARE_TUNNEL_ID')
                cf_custom_url = os.environ.get('CLOUDFLARE_TUNNEL_URL')

                if cf_name:
                    print(f"PLEASE WAIT... Starting Persistent Cloudflare Tunnel: {cf_name}...")
                    # For a named tunnel, the user usually has it configured to point to localhost:PORT
                    # We run it using the name/ID.
                    cf_cmd = ["cloudflared", "tunnel", "run", cf_name]
                    public_url = cf_custom_url
                    
                    if not public_url:
                        print("⚠️  Warning: CLOUDFLARE_TUNNEL_URL not set. QR Code might be incorrect.")
                        public_url = "https://your-cloudflare-hostname.com"
                    
                    try:
                        cf_process = subprocess.Popen(cf_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        # Give it a moment to stabilize
                        time.sleep(2)
                    except FileNotFoundError:
                        print("❌ Error: 'cloudflared' binary not found.")
                        sys.exit(1)
                else:
                    print("PLEASE WAIT... Establishing Ephemeral Cloudflare Tunnel...")
                    # Start cloudflared in a separate process
                    # We use --url to create an ephemeral TryCloudflare tunnel
                    cf_cmd = ["cloudflared", "tunnel", "--url", addr]
                    
                    if protocol == "https":
                        cf_cmd.append("--no-tls-verify")
                    
                    # We need to capture stderr because cloudflared prints the URL there
                    try:
                        cf_process = subprocess.Popen(
                            cf_cmd, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT, 
                            text=True, 
                            bufsize=1, 
                            universal_newlines=True
                        )
                        
                        # Watch for the URL in the output
                        start_time = time.time()
                        timeout = 30 # seconds
                        
                        while time.time() - start_time < timeout:
                            line = cf_process.stdout.readline()
                            if not line:
                                break
                            
                            # Cloudflare outputs things like: 
                            # |  https://some-subdomain.trycloudflare.com                           |
                            if ".trycloudflare.com" in line:
                                import re
                                match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                                if match:
                                    public_url = match.group(0)
                                    break
                        
                        if not public_url:
                            print("❌ Failed to find Cloudflare Tunnel URL. Is 'cloudflared' installed?")
                            cf_process.terminate()
                            sys.exit(1)
                            
                    except FileNotFoundError:
                        print("❌ Error: 'cloudflared' binary not found. Please install it from: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/install-run/")
                        sys.exit(1)
                    except Exception as e:
                        print(f"❌ Failed to start Cloudflare Tunnel: {e}")
                        sys.exit(1)
            elif provider == 'localtunnel':
                lt_subdomain = os.environ.get('LOCALTUNNEL_SUBDOMAIN')
                print(f"PLEASE WAIT... Establishing Localtunnel Tunnel (Subdomain: {lt_subdomain or 'random'})...")
                
                lt_cmd = ["npx", "localtunnel", "--port", port]
                if lt_subdomain:
                    lt_cmd.extend(["--subdomain", lt_subdomain])
                
                try:
                    lt_process = subprocess.Popen(
                        lt_cmd, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        text=True, 
                        bufsize=1, 
                        universal_newlines=True
                    )
                    
                    # Watch for the URL in the output
                    start_time = time.time()
                    timeout = 30 # seconds
                    
                    while time.time() - start_time < timeout:
                        line = lt_process.stdout.readline()
                        if not line:
                            break
                        
                        # Localtunnel outputs: "your url is: https://subdomain.loca.lt"
                        if "your url is:" in line or ".loca.lt" in line:
                            import re
                            match = re.search(r'https://[a-zA-Z0-9-]+\.loca\.lt', line)
                            if match:
                                public_url = match.group(0)
                                break
                            if "your url is:" in line:
                                public_url = line.split("your url is:")[-1].strip()
                                break
                    
                    if not public_url:
                        print("❌ Failed to find Localtunnel URL. Make sure npx is installed.")
                        lt_process.terminate()
                        sys.exit(1)

                    # Check if requested subdomain was rejected
                    if lt_subdomain and lt_subdomain not in public_url:
                        print("\n" + "!"*60)
                        print(f"⚠️  WARNING: Requested subdomain '{lt_subdomain}' was rejected by the server.")
                        print("   (This usually happens due to server-side cooldown from a recent restart.)")
                        print("   To get your constant URL back, please stop this script,")
                        print("   wait 60 seconds for the server to release the name, and start it again.")
                        print("!"*60 + "\n")
                        
                except Exception as e:
                    print(f"❌ Failed to start Localtunnel Tunnel: {e}")
                    sys.exit(1)
            else:
                # Default to Ngrok
                # Check Ngrok Token
                token = os.environ.get('NGROK_AUTHTOKEN')
                if token:
                    ngrok.set_auth_token(token)
                else:
                    print("⚠️  Warning: NGROK_AUTHTOKEN not found in .env. Tunnel might expire.")

                print("PLEASE WAIT... Establishing Ngrok Tunnel...")
                tunnel = ngrok.connect(addr, host_header="rewrite")
                public_url = tunnel.public_url
            
            # Magic URL with password
            final_url = f"{public_url}?key={passcode}"
            
            print("\n" + "="*50)
            print(f"   🌍 GLOBAL WEB ACCESS ({provider.upper()})")
            print("="*50)
            print(f"🔗 Base URL: {public_url}")
            print(f"🔑 Passcode: {passcode}")
            
            print("\n📱 Scan this Magic QR Code (Auto-Logins):")
            print_qr(final_url)

            print("-" * 50)
            print("📝 Steps to Connect:")
            print("1. Switch your phone to Mobile Data or Turn off Wi-Fi.")
            print("2. Open your phone's Camera app or a QR scanner.")
            print("3. Scan the code above to auto-login.")
            print(f"4. Or visit {public_url}")
            print(f"5. Enter passcode: {passcode}")
            print("6. You should be connected automatically!")

        print("="*50)
        print("✅ Server is running in background. Logs -> server_log.txt")
        print("⌨️  Press Ctrl+C to stop.")
        
        # Keep alive loop
        last_log_pos = 0
        cdp_warning_shown = False
        
        while True:
            time.sleep(1)
            
            # Check process status
            if node_process.poll() is not None:
                print("\n❌ Server process died unexpectedly!")
                sys.exit(1)
                
            # Monitor logs for errors
            try:
                if os.path.exists("server_log.txt"):
                    with open("server_log.txt", "r", encoding='utf-8', errors='ignore') as f:
                        f.seek(last_log_pos)
                        new_lines = f.read().splitlines()
                        last_log_pos = f.tell()
                        
                        for line in new_lines:
                            if "CDP not found" in line and not cdp_warning_shown:
                                print("\n" + "!"*50)
                                print("❌ ERROR: Antigravity Editor Not Detected!")
                                print("!"*50)
                                print("   The server cannot see your editor.")
                                print("   1. Close Antigravity.")
                                print("   2. Re-open it with the debug flag:")
                                print("      antigravity . --remote-debugging-port=9000")
                                print("   3. Or use the 'Open with Antigravity (Debug)' context menu.")
                                print("!"*50 + "\n")
                                cdp_warning_shown = True
            except Exception:
                pass

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            if 'node_process' in locals() and node_process:
                node_process.terminate()
                try:
                    node_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    node_process.kill()
            
            if args.mode == 'web':
                if provider == 'pinggy' and 'pinggy_tunnel' in locals():
                    try:
                        pinggy_tunnel.stop()
                    except Exception:
                        pass
                elif provider == 'cloudflare' and 'cf_process' in locals():
                    cf_process.terminate()
                elif provider == 'localtunnel' and 'lt_process' in locals():
                    lt_process.terminate()
                elif 'ngrok' in locals():
                    ngrok.kill()
        except Exception:
            pass
        
        if 'log_file' in locals() and log_file:
            log_file.close()

if __name__ == "__main__":
    main()
