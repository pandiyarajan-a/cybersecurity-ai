#!/bin/bash

# Create Metasploit database config
mkdir -p ~/.msf4

cat > ~/.msf4/database.yml <<EOF
production:
  adapter: postgresql
  database: msf
  username: vuln_scan
  password: vuln_scan
  host: ${MSF_DB_HOST:-localhost}
  port: 5432
  pool: 75
  timeout: 5
EOF

# Generate workspace name from subnet (first argument)
WORKSPACE=$(echo "$1" | tr "./" "__")

# Run msfconsole to connect, create workspace, and import scan
msfconsole -q -x "db_status; workspace -a $WORKSPACE; db_import /home/node/.n8n/result.xml; exit"

