# -*- coding: utf-8 -*-
import envitro
import pyrax

# pyrax connection
pyrax.set_setting('identity_type', 'rackspace')
pyrax.set_setting('region', envitro.str('RAX_REGION', 'DFW'))
pyrax.set_credentials(envitro.str('RAX_ACCOUNT'), envitro.str('RAX_API'))
cdb = pyrax.cloud_databases

BACKUP_NAME = envitro.str('BACKUP_NAME', 'rax-db-backup')
MAX_BACKUPS = envitro.int('MAX_BACKUPS', 30)

instances = cdb.list()
for instance in instances:
    # create the backup
    instance.create_backup(BACKUP_NAME)

    # get the backups and delete the extra ones if there are too many
    backups = instance.list_backups()
    backups_filtered = filter(lambda backup: backup.name == BACKUP_NAME, backups)
    if len(backups_filtered) > MAX_BACKUPS:
        for backup in backups_filtered[MAX_BACKUPS:]:
            backup.delete()
