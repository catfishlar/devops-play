## Docker Install 

This install assumes there is an LVM unused space of 30 GBs.  This is for the overlay2 storage
driver.  The official docs https://docs.docker.com/install/linux/docker-ce/centos/ mention 

> The overlay2 storage driver is recommended.

But that section uses the default non production setup.  To get to the recommended you have 
to go to https://docs.docker.com/storage/storagedriver/overlayfs-driver/  but this lead me to 
reading the previous sections.. until I hopefully got it. 

There are some tutorials that simplify it, but it is pretty useful to read:

 * the [overview](https://docs.docker.com/storage/storagedriver/)
 * the [select a storage driver](https://docs.docker.com/storage/storagedriver/select-storage-driver/)
 * and then do the [overlay2 one](https://docs.docker.com/storage/storagedriver/overlayfs-driver/)

### Is there hard disk for the storage?

So long ago I created a Lvm physical volume.  Then I created a virtual group and put some 
logical volumes in there.  The some of the Logical volumes can not be bigger than the 
Physical volume. So later I wanted to create snapshots and I carved out 50gb and then only used
only 20 of it for the snapshot.  Why I am doing a snapshot of home.. is a mystery at this point.
pretty sure that should have been root.  But what the heck.  I wouldn't mind having to build this
all again. 

So how can I prove that I have 30GB left over?

    [centos@control02 ~]$ sudo pvs
      PV         VG     Fmt  Attr PSize   PFree 
      /dev/sda4  centos lvm2 a--  464.56g 30.00g
      
So thats going to be the space docker storage. The Volume Group is `centos` and I think 
we'll call it `docker`.

### building the Logical volume

    [centos@control02 ~]$ sudo lvcreate -L 30GB -n docker centos
      Logical volume "docker" created.
    [centos@control02 ~]$ sudo pvs
      PV         VG     Fmt  Attr PSize   PFree
      /dev/sda4  centos lvm2 a--  464.56g    0    
      
    [centos@control02 ~]$ sudo mkfs.xfs /dev/centos/docker
    meta-data=/dev/centos/docker     isize=512    agcount=4, agsize=1966080 blks
             =                       sectsz=512   attr=2, projid32bit=1
             =                       crc=1        finobt=0, sparse=0
    data     =                       bsize=4096   blocks=7864320, imaxpct=25
             =                       sunit=0      swidth=0 blks
    naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
    log      =internal log           bsize=4096   blocks=3840, version=2
             =                       sectsz=512   sunit=0 blks, lazy-count=1
    realtime =none                   extsz=4096   blocks=0, rtextents=0  

One thing to note that under naming ftype=1. This is required and is the default. 
    
    
### Mount it where the Docker Storage Goes

Docker storage goes in `/var/lib/docker`    

    [centos@control02 ~]$ sudo mount /dev/mapper/centos-docker /var/lib/docker
    mount: mount point /var/lib/docker does not exist

So that mount point gets created in teh docker install.  I think we want to install 
docker the normal way then finish the mount and setting the storage driver.


### Docker Base Install

Following along with https://docs.docker.com/install/linux/docker-ce/centos/

     [centos@control02 lib]$ sudo yum remove docker \
    >                   docker-client \
    >                   docker-client-latest \
    >                   docker-common \
    >                   docker-latest \
    >                   docker-latest-logrotate \
    >                   docker-logrotate \
    >                   docker-engine
    Loaded plugins: fastestmirror
    No Match for argument: docker
    No Match for argument: docker-client
    No Match for argument: docker-client-latest
    No Match for argument: docker-common
    No Match for argument: docker-latest
    No Match for argument: docker-latest-logrotate
    No Match for argument: docker-logrotate
    No Match for argument: docker-engine
    No Packages marked for removal   
    
Install some base things.     

    sudo yum install -y yum-utils \
      device-mapper-persistent-data \
      lvm2
      
Lot of output from that. 

next set the docker repo to stable. 

    [centos@control02 lib]$ sudo yum-config-manager \
    >     --add-repo \
    >     https://download.docker.com/linux/centos/docker-ce.repo
    Loaded plugins: fastestmirror
    adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
    grabbing file https://download.docker.com/linux/centos/docker-ce.repo to /etc/yum.repos.d/docker-ce.repo
    repo saved to /etc/yum.repos.d/docker-ce.repo
 
Install the most recent version of docker engine      

    sudo yum install -y docker-ce docker-ce-cli containerd.io
    
Losts of output and need to say eys to further installs

At this point it is installed.  Before we proceed we want to mount that directory and.. its not there
so hmm.  lets start docker and see if it creates it then. 

    [centos@control02 lib]$ sudo systemctl start docker
    [centos@control02 lib]$ sudo systemctl status docker
    ● docker.service - Docker Application Container Engine
       Loaded: loaded (/usr/lib/systemd/system/docker.service; disabled; vendor preset: disabled)
       Active: active (running) since Sat 2019-07-27 18:58:10 PDT; 12s ago
         Docs: https://docs.docker.com
     Main PID: 14110 (dockerd)
        Tasks: 13
       Memory: 44.0M
       CGroup: /system.slice/docker.service
               └─14110 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
    
    Jul 27 18:58:09 control02.kafush.in dockerd[14110]: time="2019-07-27T18:58:09.856551659-07:00" level=info msg="...grpc
    Jul 27 18:5....
    
    
and now the directory is there and full of things... 

    [centos@control02 lib]$ sudo ls -la /var/lib/docker
    total 4
    drwx--x--x. 14 root root  182 Jul 27 18:58 .
    drwxr-xr-x. 27 root root 4096 Jul 27 18:58 ..
    drwx------.  2 root root   24 Jul 27 18:58 builder
    drwx------.  4 root root   92 Jul 27 18:58 buildkit
    drwx------.  2 root root    6 Jul 27 18:58 containers
    drwx------.  3 root root   22 Jul 27 18:58 image
    drwxr-x---.  3 root root   19 Jul 27 18:58 network
    drwx------.  3 root root   40 Jul 27 18:58 overlay2
    drwx------.  4 root root   32 Jul 27 18:58 plugins
    drwx------.  2 root root    6 Jul 27 18:58 runtimes
    drwx------.  2 root root    6 Jul 27 18:58 swarm
    drwx------.  2 root root    6 Jul 27 18:58 tmp
    drwx------.  2 root root    6 Jul 27 18:58 trust
    drwx------.  2 root root   25 Jul 27 18:58 volumes
    
At this point.. what is the storage device?

To find that I had to go back to https://docs.docker.com/storage/storagedriver/overlayfs-driver/ and find 

    [centos@control02 lib]$ sudo docker info 
    Client:
     Debug Mode: false
    
    Server:
     Containers: 0
      Running: 0
      Paused: 0
      Stopped: 0
     Images: 0
     Server Version: 19.03.1
     Storage Driver: overlay2
      Backing Filesystem: xfs
      Supports d_type: true
      Native Overlay Diff: true
     Logging Driver: json-file
     Cgroup Driver: cgroupfs
     Plugins:
      Volume: local
      Network: bridge host ipvlan macvlan null overlay
      Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
     Swarm: inactive
     Runtimes: runc
     Default Runtime: runc
     Init Binary: docker-init
     containerd version: 894b81a4b802e4eb2a91d1ce216b8817763c29fb
     runc version: 425e105d5a03fabd737a126ad93d62a9eeede87f
     init version: fec3683
     Security Options:
      seccomp
       Profile: default
     Kernel Version: 3.10.0-957.el7.x86_64
     Operating System: CentOS Linux 7 (Core)
     OSType: linux
     Architecture: x86_64
     CPUs: 4
     Total Memory: 15.4GiB
     Name: control02.kafush.in
     ID: 7KOI:N26L:BGRY:MWHN:UQKD:IOUD:HKEJ:LIUR:KNN3:5OTU:UR2Q:E644
     Docker Root Dir: /var/lib/docker
     Debug Mode: false
     Registry: https://index.docker.io/v1/
     Labels:
     Experimental: false
     Insecure Registries:
      127.0.0.0/8
     Live Restore Enabled: false
     
So it already is overlay2 type.  Well how cool is that.  I guess that means it is now the 
default, and I don't have to do the part about setting the storage device part.

### Mount our Docker Partition to /etc/lib/docker

Stop the docker service

    sudo systemctl stop docker
    
    
Copy intermediate stuff    
    
    sudo cp -au /var/lib/docker /var/lib/docker.bk


Mount the data
      
    sudo mount /dev/mapper/centos-docker /var/lib/docker
    
Instead of copying the backed up stuff.. I just restarted the docker service and all the 
directories showed up.. so I killed the backups.

Add to `/etc/fstab` :

    #
    # /etc/fstab
    # Created by anaconda on Sun Jun  9 08:40:35 2019
    #
    # Accessible filesystems, by reference, are maintained under '/dev/disk'
    # See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
    #
    /dev/mapper/centos-root /                       xfs     defaults        0 0
    UUID=6892e062-d120-4285-9a1f-3fe530b2b3b3 /boot                   xfs     defaults        0 0
    /dev/mapper/centos-home /home                   xfs     defaults        0 0
    /dev/mapper/centos-spare /spare                  xfs     defaults        0 0
    /dev/mapper/centos-swap swap                    swap    defaults        0 0
    /dev/mapper/centos-docker /var/lib/docker                  xfs     defaults        0 0

### Restart and enable

    sudo systemctl start docker
    sudo systemctl enable docker

### Test it

    [centos@control02 etc]$  sudo docker run hello-world
    Unable to find image 'hello-world:latest' locally
    latest: Pulling from library/hello-world
    1b930d010525: Pull complete 
    Digest: sha256:6540fc08ee6e6b7b63468dc3317e3303aae178cb8a45ed3123180328bcc1d20f
    Status: Downloaded newer image for hello-world:latest
    
    Hello from Docker!
    This message shows that your installation appears to be working correctly.
    
    To generate this message, Docker took the following steps:
     1. The Docker client contacted the Docker daemon.
     2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
        (amd64)
     3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
     4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.
    
    To try something more ambitious, you can run an Ubuntu container with:
     $ docker run -it ubuntu bash
    
    Share images, automate workflows, and more with a free Docker ID:
     https://hub.docker.com/
    
    For more examples and ideas, visit:
     https://docs.docker.com/get-started/


## Lets do Python Fabric

This is a library for doing remote execution.  Devops lite 

First we have [environment.yml](environment.yml) for creating a conda environment. 

create the environment with:

    conda env create -f environment.yml
    conda activate fabric

All the commands in this section are in [installdocker.py](installdocker.py) run it with:

    python installdocker.py
    
## Check it all with tmux-cssh

    ./tmux-cssh centos@c1 centos@c2 centos@c3 centos@r1 centos@r2 centos@r3
    

   
    
    



      