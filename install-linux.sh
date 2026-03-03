#!/bin/bash
# TrendRadar Linux Installation Script
# ===================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}TrendRadar Linux Installer${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="$PROJECT_DIR/../.venv"

# Check Python
echo -e "${YELLOW}[1/4] Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}Python $PYTHON_VERSION found${NC}"

# Create virtual environment if not exists
echo -e "${YELLOW}[2/4] Setting up virtual environment...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo -e "${GREEN}Virtual environment already exists${NC}"
fi

# Install dependencies
echo -e "${YELLOW}[3/4] Installing dependencies...${NC}"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q
pip install -r "$PROJECT_DIR/requirements.txt" -q
echo -e "${GREEN}Dependencies installed${NC}"

# Make scripts executable
echo -e "${YELLOW}[4/4] Setting up scripts...${NC}"
chmod +x "$PROJECT_DIR/run-monitor.sh"
echo -e "${GREEN}Scripts made executable${NC}"

# Update paths in service file
SERVICE_FILE="$PROJECT_DIR/trendradar-monitor.service"
if [ -f "$SERVICE_FILE" ]; then
    echo ""
    echo -e "${YELLOW}[Optional] systemd Service${NC}"
    echo "To install as a system service, run:"
    echo -e "${CYAN}  sudo sed -i 's|/path/to/TrendRadar|$PROJECT_DIR|g' $SERVICE_FILE${NC}"
    echo -e "${CYAN}  sudo cp $SERVICE_FILE /etc/systemd/system/${NC}"
    echo -e "${CYAN}  sudo systemctl daemon-reload${NC}"
    echo -e "${CYAN}  sudo systemctl enable trendradar-monitor${NC}"
    echo -e "${CYAN}  sudo systemctl start trendradar-monitor${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Installation complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "To start monitoring:"
echo -e "${CYAN}  cd $PROJECT_DIR${NC}"
echo -e "${CYAN}  ./run-monitor.sh${NC}"
echo ""
echo "Or run in background:"
echo -e "${CYAN}  nohup ./run-monitor.sh > monitor.log 2>&1 &${NC}"
echo ""
