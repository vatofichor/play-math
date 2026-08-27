#!/usr/bin/env bash
# play-math Environment Setup and Installer for macOS / Linux

echo "========================================================"
echo " Checking Environment Dependencies for play-math..."
echo "========================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Check if PHP is installed
if ! command -v php >/dev/null 2>&1; then
    echo "[ERROR] PHP is not installed on this system!"
    echo "Linux/macOS users must have PHP 5.3 or greater installed."
    exit 1
fi

# 2. Check if PHP version is >= 5.3
if ! php -r "exit(version_compare(PHP_VERSION, '5.3.0', '>=') ? 0 : 1);" >/dev/null 2>&1; then
    echo "[ERROR] System PHP version is lower than 5.3!"
    exit 1
fi

echo "[OK] System PHP version requirement (>= 5.3) is met."

# 3. Deploy ONLY POSIX launcher scripts and uninstaller from assets/lib/installer/
echo "[INSTALLING] Deploying POSIX launcher scripts and uninstaller..."
[ -f "${SCRIPT_DIR}/assets/lib/installer/run-server.sh" ] && cp -f "${SCRIPT_DIR}/assets/lib/installer/run-server.sh" "${SCRIPT_DIR}/run-server.sh" && chmod +x "${SCRIPT_DIR}/run-server.sh"
[ -f "${SCRIPT_DIR}/assets/lib/installer/run_server.sh" ] && cp -f "${SCRIPT_DIR}/assets/lib/installer/run_server.sh" "${SCRIPT_DIR}/run_server.sh" && chmod +x "${SCRIPT_DIR}/run_server.sh"
[ -f "${SCRIPT_DIR}/assets/lib/installer/uninstall.sh" ] && cp -f "${SCRIPT_DIR}/assets/lib/installer/uninstall.sh" "${SCRIPT_DIR}/uninstall.sh" && chmod +x "${SCRIPT_DIR}/uninstall.sh"

echo "[OK] POSIX server launchers (run-server.sh) and uninstaller deployed to project root."
echo ""
echo "========================================================"
echo " Environment setup complete! Run ./run-server.sh to start."
echo "========================================================"
