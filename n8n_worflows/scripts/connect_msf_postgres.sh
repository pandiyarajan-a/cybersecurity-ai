#!/bin/bash

# Generate workspace name from subnet (first argument)
WORKSPACE=$(echo "$1" | tr "./" "_")

# Run msfconsole to connect, create workspace, and import scan
msfconsole -q -x "db_status; workspace -a $WORKSPACE; db_import /home/node/.n8n/scans/$WORKSPACE/nmap_scan_result.xml; exit"