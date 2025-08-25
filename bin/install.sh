#!/bin/bash
# Installation script for Tyrone Redfish binary

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BINARY_NAME="tyrone_redfish"
INSTALL_DIR="/usr/local/bin"

echo -e "${BLUE}Tyrone Redfish Binary Installer${NC}"
echo "================================"

# Check if running as root for system-wide installation
if [ "$EUID" -eq 0 ]; then
    echo -e "${GREEN}Running as root - will install system-wide${NC}"
    SYSTEM_INSTALL=true
else
    echo -e "${YELLOW}Not running as root - will suggest user installation${NC}"
    SYSTEM_INSTALL=false
fi

# Check if binary exists
if [ ! -f "$BINARY_NAME" ]; then
    echo -e "${RED}Error: $BINARY_NAME binary not found in current directory${NC}"
    echo "Please run this script from the bin/ directory containing the binary"
    exit 1
fi

# Test the binary
echo -e "${YELLOW}Testing binary...${NC}"
if ./$BINARY_NAME --version >/dev/null 2>&1; then
    echo -e "${GREEN}Binary test passed${NC}"
else
    echo -e "${RED}Binary test failed${NC}"
    exit 1
fi

if [ "$SYSTEM_INSTALL" = true ]; then
    # System-wide installation
    echo -e "${YELLOW}Installing $BINARY_NAME to $INSTALL_DIR...${NC}"
    
    # Create backup if file already exists
    if [ -f "$INSTALL_DIR/$BINARY_NAME" ]; then
        echo -e "${YELLOW}Backing up existing binary...${NC}"
        cp "$INSTALL_DIR/$BINARY_NAME" "$INSTALL_DIR/$BINARY_NAME.backup.$(date +%Y%m%d-%H%M%S)"
    fi
    
    # Copy binary
    cp "$BINARY_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$BINARY_NAME"
    
    echo -e "${GREEN}Installation completed!${NC}"
    echo -e "${BLUE}You can now use: $BINARY_NAME <command> [options]${NC}"
    
    # Test system installation
    if command -v $BINARY_NAME >/dev/null 2>&1; then
        echo -e "${GREEN}System installation verified${NC}"
        echo ""
        echo -e "${BLUE}Examples:${NC}"
        echo "  $BINARY_NAME help"
        echo "  $BINARY_NAME power --help"
        echo "  $BINARY_NAME power -H 192.168.1.100 -u admin -p password --get-state"
    else
        echo -e "${YELLOW}Warning: Binary not found in PATH. You may need to restart your shell${NC}"
    fi
    
else
    # User installation suggestions
    echo -e "${YELLOW}For user installation, you can:${NC}"
    echo ""
    echo -e "${BLUE}Option 1: Add to your local bin directory${NC}"
    echo "  mkdir -p ~/.local/bin"
    echo "  cp $BINARY_NAME ~/.local/bin/"
    echo "  chmod +x ~/.local/bin/$BINARY_NAME"
    echo "  echo 'export PATH=\$PATH:\$HOME/.local/bin' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""
    echo -e "${BLUE}Option 2: Use from current directory${NC}"
    echo "  ./$BINARY_NAME help"
    echo ""
    echo -e "${BLUE}Option 3: Create an alias${NC}"
    echo "  echo 'alias $BINARY_NAME=$(pwd)/$BINARY_NAME' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""
    echo -e "${BLUE}Option 4: Run with sudo for system-wide installation${NC}"
    echo "  sudo ./install.sh"
fi

echo ""
echo -e "${GREEN}Installation guide completed!${NC}"
