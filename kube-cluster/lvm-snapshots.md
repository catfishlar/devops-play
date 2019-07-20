## LVM Snapshots

Source docs: 
 * [Understanding LVM Snapshots (create, merge, remove, extend)](https://www.golinuxhub.com/2017/09/understanding-lvm-snapshots-create.html)


### Getting around Lvm

source docs: 
 * [How to list all hard disks in linux from command line (handy commands)](http://www.lostsaloon.com/technology/how-to-list-disks-in-linux/)
 * [Linux Basics - LVM Tutorial](https://www.ostechnix.com/linux-basics-lvm-logical-volume-manager-tutorial/)
 

#### Handy Commands

 * `sudo lvs` - ls for lvm drives. 
 * `df -Th /` - `-h` is human readable `-T` is show type
 * `lsblk` - shows a nice tree view of devices and partitions and lvm 
 * `sudo lshw -class disk` shows detailed physical information about the drive and its logical name. 
 * `lsscsi` list scsi. 
 * `cat /proc/partitions`
 
#### How to go from mount location to LVM File system

First get a listing of filesystems

    [centos@control01 centos]$ df -Th
    Filesystem               Type      Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root  xfs        50G 1008M   49G   2% /
    devtmpfs                 devtmpfs  7.7G     0  7.7G   0% /dev
    tmpfs                    tmpfs     7.8G     0  7.8G   0% /dev/shm
    tmpfs                    tmpfs     7.8G  9.1M  7.7G   1% /run
    tmpfs                    tmpfs     7.8G     0  7.8G   0% /sys/fs/cgroup
    /dev/sda3                xfs      1014M  147M  868M  15% /boot
    /dev/mapper/centos-home  xfs       357G   33M  357G   1% /home
    /dev/mapper/centos-spare xfs        50G   33M   50G   1% /spare
    tmpfs                    tmpfs     1.6G     0  1.6G   0% /run/user/1000

The `/dev/mapper` ones like `/dev/mapper/centos-root` is actualy visible as 
`/dev/centos/root`

    [centos@control01 dev]$ ls -lah /dev/centos
    total 0
    drwxr-xr-x.  2 root root  120 Jun  9 08:23 .
    drwxr-xr-x. 20 root root 3.3K Jun  9 20:58 ..
    lrwxrwxrwx.  1 root root    7 Jun  9 08:23 home -> ../dm-2
    lrwxrwxrwx.  1 root root    7 Jun  9 08:23 root -> ../dm-0
    lrwxrwxrwx.  1 root root    7 Jun  9 08:23 spare -> ../dm-3
    lrwxrwxrwx.  1 root root    7 Jun  9 08:23 swap -> ../dm-1
    
These are not directories they are devices.  You can also see these with 

    [centos@control01 dev]$ cat /proc/partitions
    major minor  #blocks  name
    
       8        0  488386584 sda
       8        1     204800 sda1
       8        2       1024 sda2
       8        3    1048576 sda3
       8        4  487131136 sda4
     253        0   52428800 dm-0
     253        1    8192000 dm-1
     253        2  374079488 dm-2
     253        3   52424704 dm-3  
     
That file is shown in a better way

    [centos@control01 dev]$ lsblk
    NAME             MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    sda                8:0    0 465.8G  0 disk 
    ├─sda1             8:1    0   200M  0 part 
    ├─sda2             8:2    0     1M  0 part 
    ├─sda3             8:3    0     1G  0 part /boot
    └─sda4             8:4    0 464.6G  0 part 
      ├─centos-root  253:0    0    50G  0 lvm  /
      ├─centos-swap  253:1    0   7.8G  0 lvm  [SWAP]
      ├─centos-home  253:2    0 356.8G  0 lvm  /home
      └─centos-spare 253:3    0    50G  0 lvm  /spare          

In this case above, there is one hard drive. a 500G device that is sda.  Sda has 4 partitions. 
These are created with `fdisk` and is the physical partitioning of the disk. 

The partition 'sda4' is additionally turned into a lvm physical volume and that is the source of the 
`centos` volume group.  And then this is broken into logical volumes.  

The lvm display commands

pvdisplay

    [centos@resource02 ~]$ sudo pvdisplay
      --- Physical volume ---
      PV Name               /dev/sda4
      VG Name               centos
      PV Size               <657.82 GiB / not usable 3.00 MiB
      Allocatable           yes 
      PE Size               4.00 MiB
      Total PE              168401
      Free PE               1
      Allocated PE          168400
      PV UUID               yBvzOK-3FCu-d7MV-lFio-o7xZ-wgqO-jl6X4H
      
vgdisplay

    [centos@resource02 ~]$ sudo vgdisplay
      --- Volume group ---
      VG Name               centos
      System ID             
      Format                lvm2
      Metadata Areas        1
      Metadata Sequence No  4
      VG Access             read/write
      VG Status             resizable
      MAX LV                0
      Cur LV                3
      Open LV               3
      Max PV                0
      Cur PV                1
      Act PV                1
      VG Size               <657.82 GiB
      PE Size               4.00 MiB
      Total PE              168401
      Alloc PE / Size       168400 / 657.81 GiB
      Free  PE / Size       1 / 4.00 MiB
      VG UUID               kitv8j-zLPg-a4Zd-cDIJ-aZFr-yj4D-McCzaW      
   
lvdisplay

    [centos@resource02 ~]$ sudo lvdisplay
      --- Logical volume ---
      LV Path                /dev/centos/root
      LV Name                root
      VG Name                centos
      LV UUID                6Zkb7j-0lBq-fe2j-3Zlj-hzqy-AfVF-5wGR2Z
      LV Write Access        read/write
      LV Creation host, time localhost.localdomain, 2019-06-09 00:22:03 -0700
      LV Status              available
      # open                 1
      LV Size                50.00 GiB
      Current LE             12800
      Segments               1
      Allocation             inherit
      Read ahead sectors     auto
      - currently set to     256
      Block device           253:0
       
      --- Logical volume ---
      LV Path                /dev/centos/home
      LV Name                home
        .
        .
        .  

### Specifically Snapshots

source doc: 
 
 * [Understanding LVM snapshots (create, merge, remove, extend) ](https://www.golinuxhub.com/2017/09/understanding-lvm-snapshots-create.html)
 
 LVM Snapshots only contain the difference from the first snap shot  So the first snapshot starts
 capturing any changes.  If you do another snapshots, that is just another checkpoint in the 
 change log of the target file system.   As such, it only containts the changes to files in 
 a volume.  
 
 ##### Shrinking Home to make room for the snap shot
 
 We are going to take 20Gs out of /home to make room for  snapshot volume. 
 
 source doc: 
  
  * [How to shrink /home and add more space on CentOS7](https://serverfault.com/questions/771921/how-to-shrink-home-and-add-more-space-on-centos7)


    $ sudo tar -czvf /root/home.tgz -C /home .
    $ cd /tmp
    $ sudo umount /dev/mapper/centos-home
    $ sudo lvremove /dev/mapper/centos-home
    Do you really want to remove active logical volume centos/home? [y/n]: y
      Logical volume "home" successfully removed
    $ sudo lvcreate -L 550GB -n home centos
    WARNING: xfs signature detected on /dev/centos/home at offset 0. Wipe it? [y/n]: y
      Wiping xfs signature on /dev/centos/home.
      Logical volume "home" created.    
    $ sudo mkfs.xfs /dev/centos/home
    meta-data=/dev/centos/home       isize=512    agcount=4, agsize=36044800 blks
             =                       sectsz=4096  attr=2, projid32bit=1
             =                       crc=1        finobt=0, sparse=0
    data     =                       bsize=4096   blocks=144179200, imaxpct=25
             =                       sunit=0      swidth=0 blks
    naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
    log      =internal log           bsize=4096   blocks=70400, version=2
             =                       sectsz=4096  sunit=1 blks, lazy-count=1
    realtime =none                   extsz=4096   blocks=0, rtextents=0
    $ sudo mount /dev/mapper/centos-home /home
    $ df -hT
    Filesystem              Type      Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root xfs        50G 1008M   49G   2% /
    devtmpfs                devtmpfs  7.7G     0  7.7G   0% /dev
    tmpfs                   tmpfs     7.7G     0  7.7G   0% /dev/shm
    tmpfs                   tmpfs     7.7G  9.0M  7.7G   1% /run
    tmpfs                   tmpfs     7.7G     0  7.7G   0% /sys/fs/cgroup
    /dev/sda3               xfs      1014M  147M  868M  15% /boot
    tmpfs                   tmpfs     1.6G     0  1.6G   0% /run/user/1000
    /dev/mapper/centos-home xfs       550G   33M  550G   1% /home 
    
    sudp tar -xzvf /root/home.tgz -C /home
    
After I did this.. I would get a password request when I ssh'ed in from my laptop.  Files
were not lost.. but finally I just looked for passwordless ssh not working troubleshooting. 

  *  https://unix.stackexchange.com/questions/311408/passwordless-ssh-is-not-working-in-centos-7    
  
Jesus, magical SELinux problem. 

     restorecon -Rv ~/.ssh 
     
But.. doing that didn't work for later. So Finally I just got rid of the SELINUX as is everyone's plan.  While I 
discovered the problem at this point, I am putting the instructions in the main [README.md](README.md)


####  Create the snapshot

I am only using 20G of the 50 I freed up.. cause yeah.  I am not going to need it, it just contains differences.   
     
    sudo lvcreate -L 20G -s -n snap_home /dev/centos/home
    
    