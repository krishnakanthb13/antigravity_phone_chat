#!/bin/bash

# Antigravity - Right-Click Context Menu Manager (Linux - Nautilus/GNOME)

show_menu() {
    clear
    echo "==================================================="
    echo "  Antigravity - Right-Click Context Menu Manager"
    echo "==================================================="
    echo ""
    echo "This tool manages 'Open with Antigravity (Debug)' in your"
    echo "Nautilus/GNOME file manager Right-Click menu."
    echo ""
    echo "WHAT IT DOES:"
    echo "  - Adds/Removes a script in ~/.local/share/nautilus/scripts/"
    echo "  - Adds a new option when you right-click a folder"
    echo "  - Clicking it will run: agy . --remote-debugging-port=9000"
    echo ""
    echo "REQUIREMENTS:"
    echo "  - Nautilus file manager (GNOME)"
    echo "  - Antigravity CLI must be installed and in your PATH"
    echo ""
    echo "NOTE: This only works on Linux with Nautilus."
    echo "      For macOS, see README.md for Automator Quick Action setup."
    echo ""
    echo "==================================================="
    echo ""
    echo "Choose an option:"
    echo "  [1] Install - Add Right-Click menu"
    echo "  [2] Remove  - Remove Right-Click menu"
    echo "  [3] Restart - Restart Nautilus (to apply changes)"
    echo "  [4] Backup  - Copy existing script before changes"
    echo "  [5] Exit"
    echo ""
}

NAUTILUS_PATH="$HOME/.local/share/nautilus/scripts"
SCRIPT_FILE="$NAUTILUS_PATH/Open with Antigravity (Debug)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/registry"

while true; do
    show_menu
    read -p "Enter choice (1-5): " choice

    case $choice in
        1)
            echo ""
            echo "[INSTALL] Creating Nautilus script..."
            if [ ! -d "$NAUTILUS_PATH" ]; then
                mkdir -p "$NAUTILUS_PATH"
            fi
            echo "#!/bin/bash" > "$SCRIPT_FILE"
            echo "# Antigravity context menu script" >> "$SCRIPT_FILE"
            echo "cd \"\$NAUTILUS_SCRIPT_CURRENT_URI\" 2>/dev/null || cd \"\$(pwd)\"" >> "$SCRIPT_FILE"
            echo "agy . --remote-debugging-port=9000" >> "$SCRIPT_FILE"
            chmod +x "$SCRIPT_FILE"
            echo ""
            echo "[SUCCESS] Context menu installed!"
            read -p "Press Enter to return to menu..."
            ;;
        2)
            echo ""
            echo "[REMOVE] Deleting Nautilus script..."
            if [ -f "$SCRIPT_FILE" ]; then
                rm "$SCRIPT_FILE"
                echo ""
                echo "[SUCCESS] Context menu removed!"
            else
                echo ""
                echo "[INFO] No Antigravity context menu script found."
            fi
            read -p "Press Enter to return to menu..."
            ;;
        3)
            echo ""
            echo "[RESTART] Restarting Nautilus..."
            nautilus -q
            echo "[SUCCESS] Nautilus signaled to quit. It will restart on next open."
            read -p "Press Enter to return to menu..."
            ;;
        4)
            echo ""
            echo "[BACKUP] Backing up existing script..."
            if [ -f "$SCRIPT_FILE" ]; then
                mkdir -p "$BACKUP_DIR"
                BACKUP_FILE="$BACKUP_DIR/antigravity_backup_$(date +%Y%m%d_%H%M%S).sh"
                cp "$SCRIPT_FILE" "$BACKUP_FILE"
                echo ""
                echo "[SUCCESS] Backup saved to: $BACKUP_FILE"
            else
                echo ""
                echo "[INFO] No existing Antigravity context menu script found to backup."
            fi
            read -p "Press Enter to return to menu..."
            ;;
        5)
            echo "[EXIT] Exiting..."
            exit 0
            ;;
        *)
            echo "[ERROR] Invalid choice."
            sleep 1
            ;;
    esac
done
