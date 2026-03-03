#!/bin/bash
# TrendRadar Force Majeure Monitor - Linux Script
# ================================================

# Project directory (auto-detect from script location)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$PROJECT_DIR/../.venv/bin/python"
POLLING_INTERVAL=600  # 10 minutes in seconds
LOCK_FILE="$PROJECT_DIR/.monitor.lock"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Single instance check
if [ -f "$LOCK_FILE" ]; then
    LOCK_PID=$(cat "$LOCK_FILE" 2>/dev/null)
    if [ -n "$LOCK_PID" ] && kill -0 "$LOCK_PID" 2>/dev/null; then
        echo -e "${YELLOW}[INFO] Monitor is already running (PID: $LOCK_PID)${NC}"
        echo -e "${YELLOW}[INFO] Exiting to avoid duplicate instances...${NC}"
        exit 0
    else
        echo -e "${YELLOW}[WARN] Stale lock file found, cleaning up...${NC}"
        rm -f "$LOCK_FILE"
    fi
fi

# Create lock file
echo $$ > "$LOCK_FILE"

# Cleanup function
cleanup() {
    rm -f "$LOCK_FILE"
    echo -e "${RED}[STOP] Monitor stopped${NC}"
}
trap cleanup EXIT INT TERM

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}TrendRadar Force Majeure Monitor${NC}"
echo -e "${CYAN}Polling: 10 minutes${NC}"
echo -e "${CYAN}Push Window: 08:00-21:00${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${GREEN}[START] Monitor started (PID: $$)${NC}"

cd "$PROJECT_DIR"

while true; do
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Starting monitor...${NC}"

    # Run TrendRadar
    "$VENV_PYTHON" -m trendradar

    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Monitor complete, waiting 10 minutes...${NC}"
    echo ""

    # Wait 10 minutes
    sleep "$POLLING_INTERVAL"
done
