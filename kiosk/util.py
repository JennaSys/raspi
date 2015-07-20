#!/usr/bin/python
import sys
import psutil

def usbdrive_available():

    partitions = psutil.disk_partitions()

    # Look for removable media
    if 'win' in sys.platform:
        return any('rw,removable' in partition.opts for partition in partitions)
    elif 'linux' in sys.platform:
        return any('/dev/sda' in partition.device for partition in partitions)


def get_usb_drive():

    partitions = psutil.disk_partitions()

    # Get partitions that are both read/write and removable
    if 'win' in sys.platform:
        mounts = [partition.mountpoint for partition in partitions if 'rw,removable' in partition.opts]
    elif 'linux' in sys.platform:
        mounts = [partition.mountpoint for partition in partitions if '/dev/sda' in partition.device]
   

    if len(mounts) > 0:
        return mounts[0]



