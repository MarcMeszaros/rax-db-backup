# Rackspace Database Backup
Automatically create a backup of hosted databases based on schedule.

## Unit Files

Trigger the service. (`rax-db-backup.service`)
```
[Unit]
Description=Rackspace LB Backup
Requires=docker.service
After=docker.service

[Service]
User=core
TimeoutStartSec=0
Type=simple
ExecStartPre=-/usr/bin/docker kill rax-db-backup
ExecStartPre=-/usr/bin/docker rm rax-db-backup
ExecStartPre=-/usr/bin/docker pull marcmeszaros/rax-db-backup

ExecStart=-/usr/bin/docker run --name rax-db-backup \
    -e RAX_ACCOUNT=<rackspace account> \
    -e RAX_API=<api key> \
    -e BACKUP_NAME=<backup name> \
    marcmeszaros/rax-db-backup

ExecStop=-/usr/bin/docker kill rax-db-backup
```

The timer on a repeating schedule. (`rax-db-backup.timer`)
```
[Unit]
Description=Rackspace DB Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[X-Fleet]
MachineOf=rax-db-backup.service
```
