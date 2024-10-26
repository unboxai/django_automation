#!/bin/bash

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to reload Apache configuration
reload_apache() {
    echo -e "${YELLOW}Testing Apache configuration...${NC}"
    if apache2ctl configtest; then
        echo -e "${YELLOW}Restarting Apache service...${NC}"
        systemctl restart apache2
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Apache restarted successfully!${NC}"
        else
            echo -e "${RED}Failed to restart Apache${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Apache configuration test failed${NC}"
        exit 1
    fi
}

# Function to display available log files
show_log_options() {
    echo -e "${YELLOW}Available Apache log files:${NC}"
    echo "1) Amy Error Log (/var/log/apache2/amy_error.log)"
    echo "2) Amy Access Log (/var/log/apache2/amy_access.log)"
    echo "3) Apache Error Log (/var/log/apache2/error.log)"
    echo "4) Apache Access Log (/var/log/apache2/access.log)"
    echo "5) All Amy logs (both error and access)"
    echo "6) Exit"
}

# Function to view logs
view_logs() {
    local choice
    while true; do
        show_log_options
        read -p "Which log would you like to view? (1-6): " choice
        
        case $choice in
            1)
                echo -e "${YELLOW}Viewing Amy Error Log:${NC}"
                tail -f /var/log/apache2/amy_error.log
                ;;
            2)
                echo -e "${YELLOW}Viewing Amy Access Log:${NC}"
                tail -f /var/log/apache2/amy_access.log
                ;;
            3)
                echo -e "${YELLOW}Viewing Apache Error Log:${NC}"
                tail -f /var/log/apache2/error.log
                ;;
            4)
                echo -e "${YELLOW}Viewing Apache Access Log:${NC}"
                tail -f /var/log/apache2/access.log
                ;;
            5)
                echo -e "${YELLOW}Viewing All Amy Logs:${NC}"
                tail -f /var/log/apache2/amy_error.log /var/log/apache2/amy_access.log
                ;;
            6)
                echo -e "${GREEN}Exiting log viewer${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option. Please select 1-6${NC}"
                ;;
        esac
    done
}

# Main script execution
echo -e "${GREEN}Amy Apache Management Script${NC}"
echo "1) Reload Apache configuration"
echo "2) View logs"
echo "3) Exit"

read -p "Please select an option (1-3): " main_choice

case $main_choice in
    1)
        reload_apache
        ;;
    2)
        view_logs
        ;;
    3)
        echo -e "${GREEN}Exiting script${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid option. Please select 1-3${NC}"
        exit 1
        ;;
esac
