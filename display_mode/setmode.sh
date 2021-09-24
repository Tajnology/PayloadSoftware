#!/bin/bash

# Ask user for the new display mode
echo "Set Display Mode"
echo "0: IP"
echo "1: Target Detection Feed"
echo "2: Temperature Feed"
read -p 'Selection: ' sel

# Handle selection
case $sel in
0)
echo "Changing display to IP"
echo "IP" > display_mode.txt ;;
1)
echo "Changing display to Target Detection"
echo "TARGET" > display_mode.txt ;;
2)
echo "Changing display to Temperature"
echo "TEMP" > display_mode.txt ;;
*)
echo "Option invalid" ;;
esac