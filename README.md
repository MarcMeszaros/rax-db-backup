# Rackspace Database Backup
Automatically create a backup of hosted databases based on schedule.

## Environment Variables
You can configure the backups using environment variables.

| Name                          | Description
|-------------------------------|------------------------------------------------------------------
| RAX_ACCOUNT                   | Rackspace account name
| RAX_API                       | Rackspace api key
| RAX_REGION                    | The Rackspace region (default: DFW)
| BACKUP_NAME                   | The name to use for backups (default: rax-db-backup)
| MAX_BACKUPS                   | The maximum number of backups for the backup name (default: 30)

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
