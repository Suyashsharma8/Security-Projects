To prevent log files from filling up your disk you can setup log rotation rule to manage logs in /var/log/

1. Create logrotate configuration file:
```bash
sudo nano /etc/logrotate.d/misp
```

2. Add the example configuration:
```ini
/var/log/*.log {
    daily                 # Rotate logs daily
    rotate 2              # Keep the last 2 rotated logs, delete older ones
    compress              # Compress logs to save space
    missingok             # Ignore errors if log files are missing
    notifempty            # Don't rotate if the log file is empty
    create 640 root adm   # Set correct permissions after rotation
}
```

3. Test logrotate configuration:
```bash
sudo logrotate -d /etc/logrotate.d/misp
```

4. This debugs the rotation process without making actual changes. If everything looks fine, run to force immediate log rotation:

```bash
sudo logrotate -f /etc/logrotate.d/misp
```

Logrotate is already managed by a cron job in /etc/cron.daily/logrotate. You don’t need to do anything extra—Linux will automatically rotate logs daily.
