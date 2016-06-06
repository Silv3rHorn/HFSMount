import argparse
import subprocess

__author__ = 'yk'
__version__ = '.20160502'

dmg_dir = "/Volumes/dmg/"


def unmount_img(number):
    disk = "/dev/disk" + str(number)
    cmd_unmount1 = "diskutil eject " + disk
    unmount1 = subprocess.Popen(cmd_unmount1.split(), stdout=subprocess.PIPE)
    print(unmount1.communicate()[0].decode('ascii'))
    cmd_unmount2 = "umount " + dmg_dir
    unmount2 = subprocess.Popen(cmd_unmount2.split(), stdout=subprocess.PIPE)
    print(unmount2.communicate()[0].decode('ascii'))

    return


parser = argparse.ArgumentParser(description="Un-mounts E01 image of a Mac")
parser.add_argument('-d', '--disk', dest='disk_no', type=int, nargs='?', help="specify disk number to un-mount")
args = parser.parse_args()

# un-mounting image...
if args.disk_no is None:
    cmd_getDisk = "diskutil list"
    getDisk = subprocess.Popen(cmd_getDisk.split(), stdout=subprocess.PIPE)
    print(getDisk.communicate()[0].decode('ascii'))
    disk_no = input("Enter disk number: ")
    unmount_img(disk_no)
else:
    unmount_img(args.disk_no)

