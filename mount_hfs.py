import argparse
import os
import subprocess

__author__ = 'yk'
__version__ = '.20160502'

dmg_dir = "/Volumes/dmg/"


def mount_img(img_path, mnt_dir, segments):
    img_path = img_path.replace("~/", os.path.expanduser("~") + "/")  # replace '~' with user's home directory
    img_filename = os.path.basename(img_path)  # get file name

    if mnt_dir[-1] != '/':
        mnt_dir += '/'

    if not os.path.exists(dmg_dir):
        os.makedirs(dmg_dir)
    if not os.path.exists(mnt_dir):
        os.makedirs(mnt_dir)

    # mount e01 as dmg
    cmd_xmount = "xmount --in ewf --out dmg"
    if img_path[-2:] == '??':
        for segment in segments:
            cmd_xmount += " " + segment
    else:
        cmd_xmount += " " + img_path
    cmd_xmount += " " + dmg_dir
    xmount = subprocess.Popen(cmd_xmount.split(), stdout=subprocess.PIPE)
    print(xmount.communicate()[0].decode('ascii'))

    # mount dmg
    dmg_filename = img_filename.replace(".E01", ".dmg").replace(".E??", ".dmg").replace(".e01", ".dmg")\
        .replace(".e??", ".dmg")
    cmd_attach = "hdiutil attach -nomount " + dmg_dir + dmg_filename
    attach = subprocess.Popen(cmd_attach.split(), stdout=subprocess.PIPE)
    output_hdiutil = attach.communicate()[0].decode('ascii')

    hfs_disk = output_hdiutil.split(' ')[0]
    disks = output_hdiutil.split('\n')
    if len(disks) > 2:
        for disk in disks:
            if 'Apple_HFS' in disk:
                hfs_disk = disk.split(' ')[0]

    cmd_mount = "mount_hfs -j -o rdonly,noexec,noowners " + hfs_disk + " " + mnt_dir
    mount = subprocess.Popen(cmd_mount.split(), stdout=subprocess.PIPE)
    print(mount.communicate()[0].decode('ascii'))

    return hfs_disk


parser = argparse.ArgumentParser(description='Mounts E01 image of a Mac')
parser.add_argument("img_path", metavar="img", type=str, nargs='*', help="specify path to E01 image, use .e?? if there"
                                                                         "are multiple segments")
parser.add_argument('-m', '--mountpt', dest='mnt_pt', type=str, nargs='*', help="specify mount point")
args = parser.parse_args()

img = args.img_path[0]
if len(args.img_path) > 1 and args.img_path[1][-2:] == '02':
    img = args.img_path[0][:-2] + '??'

# mounting image...
if args.mnt_pt is None:
    print(mount_img(img, "/Volumes/mount/", args.img_path))
else:
    print(mount_img(img, args.mnt_pt[0], args.img_path))
