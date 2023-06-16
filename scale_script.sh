#!/bin/bash

read -p "Enter the desired scale value: " SCALE_VALUE

# Update NGINX configuration based on the scale value
if [[ $SCALE_VALUE -ge 1 ]]; then
  # Generate the upstream backend server list
  server_list=""
  for ((i = 1; i <= $SCALE_VALUE; i++)); do
    server_list+="server app-test-app-$i:5000;\n"
  done

  # Insert the server_list into the NGINX configuration file after the upstream backend block starts
  sed -i "/upstream backend {/a $server_list" nginx/nginx.conf
else
  echo "Invalid scale value. Exiting..."
  exit 1
fi

# Start the containers with the updated configuration
docker-compose up --scale app=$SCALE_VALUE
