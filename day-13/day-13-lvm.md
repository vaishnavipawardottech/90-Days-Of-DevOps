# Day 13 – Linux Volume Management (LVM)

## Objective

The goal of this task was to learn Linux Logical Volume Management (LVM) and practice creating, formatting, mounting, and extending logical volumes.

## LVM Structure

```text
Physical Disk
     ↓
Physical Volume (PV)
     ↓
Volume Group (VG)
     ↓
Logical Volume (LV)
     ↓
Filesystem
     ↓
Mount Point
```

## Storage Check

The existing storage configuration was checked using:

```bash
lsblk
pvs
vgs
lvs
df -h
```

A separate AWS EBS volume was used for the LVM practice.

## Physical Volume

The new EBS volume was initialized as an LVM Physical Volume:

```bash
pvcreate /dev/nvme1n1 /dev/nvme2n1 /dev/nvme3n1
```

The result was verified using:

```bash
pvs
```

## Volume Group

A Volume Group named `vaishnavi_vg` was created:

```bash
vgcreate vaishnavi_vg /dev/nvme1n1 /dev/nvme2n1
```

The Volume Group was verified using:

```bash
vgs
```

## Logical Volume

A 10 GB Logical Volume named `vaishnavi_lv` was created:

```bash
lvcreate -L 10G -n vaishnavi_lv vaishnavi_vg
```

The Logical Volume was verified using:

```bash
lvs
```

## Format and Mount

The Logical Volume was formatted with the ext4 filesystem:

```bash
mkfs.ext4 /dev/vaishnavi_vg/vaishnavi_lv
```

A mount point was created:

```bash
mkdir /mnt/vaishnavi_lv_mount
```

The Logical Volume was mounted:

```bash
mount /dev/vaishnavi_vg/vaishnavi_lv /mnt/vaishnavi_lv_mount
```

The mounted filesystem was verified using:

```bash
df -h /mnt/vaishnavi_lv_mount
```

## Extend the Logical Volume

The Logical Volume was initially created with 10 GB of storage.

It was extended by 5 GB using:

```bash
lvextend -L +5G /dev/vaishnavi_vg/vaishnavi_lv
```

The ext4 filesystem was then resized:

```bash
resize2fs /dev/vaishnavi_vg/vaishnavi_lv
```

The final size was verified using:

```bash
df -h /mnt/vaishnavi_lv_mount
```

The Logical Volume was approximately 700 MB after the extension.


## What I Learned

1. LVM provides a flexible way to manage storage using Physical Volumes, Volume Groups, and Logical Volumes.
2. A Logical Volume can be extended without recreating the entire storage structure.
3. After extending an LV, the filesystem must also be resized so the additional space becomes available to the mounted filesystem.

## Screenshots (on LinkedIn)

The following screenshots were captured during the practice:

* Storage and LVM status using `lsblk`, `pvs`, `vgs`, `lvs`, and `df -h`
* Physical Volume creation using `pvcreate`
* Volume Group creation using `vgcreate`
* Logical Volume creation using `lvcreate`
* Formatting and mounting the Logical Volume
* Extending the Logical Volume and filesystem

---

Day 13 successfully completed: **Linux Volume Management (LVM)**.
