Script to auto feed cache and fetch

```bash
                                              
#!/bin/bash
 
# Command to check the status of workers
CMD="sudo -u www-data /var/www/MISP/app/Console/cake Admin getWorkers all"
 
# Execute the command and store its output
RESULT=$($CMD)

# Ensure RESULT is not empty and valid JSON
if [[ -z "$RESULT" ]]; then
    echo "Error: Empty worker status result"
    exit 1
fi

# Check if RESULT is valid JSON
echo "$RESULT" | jq empty
if [[ $? -ne 0 ]]; then
    echo "Error: Invalid JSON received"
    exit 1
fi
 
# Check for any worker with "ok": false using jq
DEAD_WORKERS=$(echo "$RESULT" | jq '[to_entries[] | select(.value.ok == false) | length')

# If jq fails, print the error
if [[ $? -ne 0 ]]; then
    echo "Error: jq failed to process JSON"
    echo "Raw output:"
    echo "$RESULT"
    exit 1
fi
 
if [[ $DEAD_WORKERS -gt 0 ]]; then
    # If there's at least one dead worker, execute the following commands and print the output:

    echo "Restarting all workers..."
    sudo -u www-data /var/www/MISP/app/Console/cake Admin restartWorkers
    sleep 5
 
    echo "Restarting cache worker..."
    sudo -u www-data /var/www/MISP/app/Console/cake Admin restartWorkers cache
    sleep 5
 
    echo "Restarting default worker..."
    sudo -u www-data /var/www/MISP/app/Console/cake Admin restartWorkers default
    sleep 5
 
    echo "Restarting email worker..."
    sudo -u www-data /var/www/MISP/app/Console/cake Admin restartWorkers email
    sleep 5
 
    echo "Restarting prio worker..."
    sudo -u www-data /var/www/MISP/app/Console/cake Admin restartWorkers prio
    sleep 5
 
    echo "Restarting update worker..."
    sudo -u www-data /var/www/MISP/app/Console/cake Admin restartWorkers update
    sleep 5
 
    echo "Restarting scheduler worker..."
    sudo -u www-data /var/www/MISP/app/Console/cake Admin restartWorkers scheduler
fi
 
echo "$(date +"%Y-%m-%d %H:%M:%S")"
echo  "--- Script completed --"
 

