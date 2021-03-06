# Copyright (c) 2015-2016, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os

env__mount_points = (
    "/mnt/tegra30-beaver-part1",
)

env__usb_dev_ports = (
    {
        "fixture_id": "micro_b",
        "tgt_usb_ctlr": "0",
        "host_ums_dev_node": "/dev/disk/by-path/pci-0000:00:1d.7-usb-0:4.7.2:1.0-scsi-0:0:0:0",
        "host_usb_dev_node": "/dev/usbdev-tegra30-beaver",
        "host_usb_port_path": "2-4.7.2",
    },
)

env__block_devs = (
    # SD card; present since I plugged one in
    {
        "fixture_id": "sd",
        "type": "mmc",
        "id": "1",
        "writable_fs_partition": 1,
        "writable_fs_subdir": "tmp/",
    },
    # eMMC; always present
    {
        "fixture_id": "emmc",
        "type": "mmc",
        "id": "0",
    },
)

env__dfu_configs = (
    # SD card, partition 1, ext4 filesystem
    {
        "fixture_id": "sd_fs",
        "alt_info": "/dfu_test.bin ext4 1 1;/dfu_dummy.bin ext4 1 1",
        "cmd_params": "mmc 1",
        "test_sizes": (
            64 - 1,
            64,
            64 + 1,
            4096 - 1,
        ),
    },
    # SD card, partition 3, partition
    {
        "fixture_id": "sd_part",
        "alt_info": "/dfu_test.bin part 1 3;/dfu_dummy.bin ext4 1 1",
        "cmd_params": "mmc 1",
        "test_sizes": (
            128 - 1,
            128,
            128 + 1,
            4096,
        ),
    },
    # SD card, partition 3, raw device (location overlays partition 3)
    {
        "fixture_id": "sd_raw",
        "alt_info": "/dfu_test.bin raw 4196352 18432;/dfu_dummy.bin ext4 1 1",
        "cmd_params": "mmc 1",
        "test_sizes": (
            960 - 1,
            960,
            960 + 1,
            4096 + 1,
        ),
    },
    # RAM
    {
        "fixture_id": "ram",
        "alt_info": "alt0 ram 80000000 01000000;alt1 ram 81000000 01000000",
        "cmd_params": "ram na",
        "test_sizes": (
            1024 * 1024 - 1,
            1024 * 1024,
            8 * 1024 * 1024,
        ),
    },
)

env__net_uses_usb = True

env__net_static_env_vars = [
    ("ipaddr", "192.168.100.101"),
    ("netmask", "255.255.255.0"),
    ("serverip", "192.168.100.1"),
    ("tftpserverip", "192.168.100.1"),
]

# The U-Boot branch used for these builds is old enough that PCIe auto-probes
# and we end up with both a PCIe and a USB Ethernet device. By default, U-Boot
# happens to pick the one we don't want to use, so we must tell it which to
# use. We don't define this variable statically, since the Ethernet device
# naming is different in the branches (mainline) that don't have this problem,
# so this value is not valid there:-( In the future, if we pull more recent
# versions of U-Boot into NVIDIA's git server, we will need to differentiate
# between the various branches here, by checking for more specific strings.
if 'gitmaster_3rdparty_uboot' in os.environ.get('JOB_NAME', ''):
    env__net_static_env_vars.append(('ethact', 'asx0'))

env__net_tftp_readable_file = {
    "fn": "ubtest-readable.bin",
    "size": 5058624,
    "crc32": "c2244b26",
}
