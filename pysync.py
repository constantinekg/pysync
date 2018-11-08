 #!/usr/bin/env python3
 
import os
import datetime
import sys
 
controlsize=250 #minimum size of dir when synchronization can be started
sourcesync="/mnt/alby-office-f/" # what directory we need to sync
alloweddays=[0,4] # days when we can make synchronization (monday and friday)
sourceserver="10.0.0.3" # server what we need to check what the server is online
 
# set destinations of sync process by week day (specify here output directories for sync)
def get_weekday_backup_dest_description(dow):
        return {
                dow == 0: '/backup/monday-backup/', # destination sync of monday
                dow == 1: 'Tuesday',
                dow == 2: 'Wednesday',
                dow == 3: 'Thursday',
                dow == 4: '/backup2/friday-backup/', # destination sync of friday
                dow == 5: 'Saturday',
                dow == 6: 'Sunday',
    }[True]
 
def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size
 
# test of source server is alive
def test_source_server(source):
        res = os.system("ping -c 1 " + source + " 2>&1 >/dev/null")
        if res == 0:
                return True
        else:
                return False
 
# checking directories for read, write and existing
def dirchecker():
        if os.path.exists(sourcesync) == True and os.path.exists(get_weekday_backup_dest_description(datetime.datetime.today().weekday())) == True:
                pass
        else:
                print ('Error! Source or destination directory is not in system!')
                print ('Process ended at:')
                print (datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
                sys.exit(1)
        if os.access(sourcesync, os.R_OK) == True:
                pass
        else:
                print ('Source directory is not readable! Exiting..')
                print ('Process ended at:')
                print (datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
                sys.exit(1)
        if os.access(get_weekday_backup_dest_description(datetime.datetime.today().weekday()), os.W_OK) == True:
                pass
        else:
                print ('Destination directory is not writeable! Exiting...')
                print ('Process ended at:')
                print (datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
                sys.exit(1)
 
# Main body
if __name__ == '__main__':
        print ('Process started at:')
        print (datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
        dirchecker()
        sourcesize=getFolderSize(sourcesync)/(1e+9)
        if test_source_server(sourceserver) == True:
                print ('Source server is alive, checking size of source and destination...')
                if sourcesize >= controlsize:
                        print ('Source dir ('+str(sourcesize)+'gb) is bigger than minimum control size ('+str(controlsize)+'gb) so let\s trying to sync...')
                        os.system("rsync -vzrh --delete-before --exclude 'System Volume Information' "+sourcesync+" "+get_weekday_backup_dest_description(datetime.datetime.today().weekday())+" | sed '0,/^$/d'")
                        print ('Process ended at:')
                        print (datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
                        print ('Syncing complete!')
                else:
                        print ('Something wrong, because source dir ('+str(sourcesize)+'gb) is smaller than minimum control size ('+str(controlsize)+'gb), exiting...')
                        print ('Process ended at:')
                        print (datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
                        sys.exit(1)
        else:
                print ('Source server is offline, exiting...')
                print ('Process ended at:')
                print (datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
                sys.exit(1)
