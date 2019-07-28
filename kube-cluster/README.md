# Set up a Kubernetes Cluster

## Get the Baremetal ready for Ansible

### Make a Thumb Drive

Start with getting a thumb drive. http://www.myiphoneadventure.com/os-x/create-a-bootable-centos-usb-drive-with-a-mac-os-x

I downloaded the DVD iso from https://wiki.centos.org/Download.  7 Was at 1611. 

    hdiutil convert -format UDRW -o CentOS-7-x86_64-DVD.img CentOS-7-x86_64-DVD.iso

did `diskutil list` and figured out that disk3 is the USB stick (which I putin a USB slot)

    diskutil unmountDisk /dev/disk3
    time sudo dd if=CentOS-7-x86_64-DVD.img.dmg of=/dev/disk3 bs=1m
    
### The Reboot and Install

On reboot, there is a menu that shows up rather quickly where it tells me that f10 
goes to boot menu. 
 
 * UEFI : USB : PNY USB 3.0 FD 1100 : PART 0 : OS Bootloader

Was the right choice. There was another entry with USB, that is the Boot Drive.   

THen you are offered a chance to install centos7, do that.

##### Install type

 * minimal install.   

##### Network

Set Date & Time to PST.  

So I went into the network and enabled the Ethernet and then configured it. 

Hit Configure at the bottom right. Then pick IPv4 Settings and add:

So on the cluster.. looking at the front. 

| control  |  resource  |                   
|----------------|---------------|
| 172.16.222.21  | 172.16.222.24 |
| 172.16.222.22  | 172.16.222.25 |
| 172.16.222.23  | 172.16.222.26 |


 * manual
 * Set Address(172.16.222.24), netmask (255.255.255.0) and gateway (172.16.222.1)
 * DNS Servers set to 8.8.8.8, 8.8.4.4
 * search domain to kafush.in
 * I checked "require IPv4 addressing for this connection to complete" becuase unchecking it means the connection work
even if only IP6 goes through.  I think I want it to scream louder if it cant get IPv4, I
hope that is what I am getting.  https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Installation_Guide/sn-Netconfig-s390.html

##### Drive Partitioning

There is some weirdness with various storage products that want raw partitions, so 
the standard partitioning schemas are not a good idea for this cluster. 

I went ahead and deleted existing partions and then did an automatic partions. 
It put the bulk in home .  I reduced that to 600G leaving 1200G unformated. 

 * /home 600G
 * /boot 1024M
 * /boot/efi 200M
 * / 50G
 * swap 8G

 
That leaves 1200 Gs to play with later on the 2 TB drive on 3 of my machines.  For 
the 3 that have the 500G ssds, I took 50 GiB out of the /home and added a mount point called /spare.

Once you start the install it gives you a place to add the root password and create the first user. 

I created `Centos` and made it adminstrator.  passwords are the same on all nodes. 

### Reboot and set name

    hostnamectl set-hostname resource03.kafush.in
    
### set up Tmux

This is the last thing we do before switching to Ansible.  

On your mac, you need `tmux` to do the next thing.  you get that with 

    brew install tmux
    
Then you need [this script locally (tmux-cssh)](tmux-cssh)

And you could simplify your life by adding the new hosts in your ` /etc/hosts`

    ##
    # Host Database
    #
    # localhost is used to configure the loopback interface
    # when the system is booting.  Do not change this entry.
    ##
    127.0.0.1       localhost Larrys-MacBook-Pro-3.local
    255.255.255.255 broadcasthost
    ::1             localhost
    172.16.222.21 c1 control01 control01.kafush.in
    172.16.222.22 c2 control02 control02.kafush.in
    172.16.222.23 c3 control03 control03.kafush.in
    172.16.222.24 r1 resource01 resource01.kafush.in
    172.16.222.25 r2 resource02 resource02.kafush.in
    172.16.222.26 r3 resource03 resource03.kafush.in
        
Then you can log into all of them with. 

    ./tmux-cssh centos@c1 centos@c2 centos@c3 centos@r1 centos@r2 centos@r3


at this point, anything you do to one of these will happen to all 6.           

### Set up authorized keys

First you log into all 6

    ./tmux-cssh centos@c1 centos@c2 centos@c3 centos@r1 centos@r2 centos@r3
    
 log in with your centos password, you should have made it all the same on all 6  
 
 There should not be a .ssh directory in your home.  Make it..create the   `authorized-keys` file in `.ssh`
 
    ls -al
    mkdir .ssh
    chmod 700 .ssh 
    cd .ssh
    vi authorized_keys

At thiis point you should be editing 6 authorized_keys files in `vi`, go into insert mode `i`.



On your mac copy the contents if `~/.ssh/id_ras` into the clipboard.     Then paste into your tmux sessions. 

New escape out of insert mode (`<esc>`) and write the file out and quit ()`:wq`). 

    chmod 644 authorized_keys
    

Then type `exit` at the command line
and all your shells should close. 

To Test just up arrow to get the tumx call. 


#### set up /etc/hosts

So in the 6 paned `tmux-cssh` window

    sudo vi /etc/hosts
    
Go to insert mode and then insert the host file that identifies all the machines.  

        ##
        # Host Database
        #
        # localhost is used to configure the loopback interface
        # when the system is booting.  Do not change this entry.
        ##
        127.0.0.1       localhost Larrys-MacBook-Pro-3.local
        255.255.255.255 broadcasthost
        ::1             localhost
        172.16.222.21 c1 control01 control01.kafush.in
        172.16.222.22 c2 control02 control02.kafush.in
        172.16.222.23 c3 control03 control03.kafush.in
        172.16.222.24 r1 resource01 resource01.kafush.in
        172.16.222.25 r2 resource02 resource02.kafush.in
        172.16.222.26 r3 resource03 resource03.kafush.in
        
### Kill Selinux

    ./tmux-cssh centos@c1 centos@c2 centos@c3 centos@r1 centos@r2 centos@r3
    sudo vi /etc/selinux/config

Edit the `SELINUX=` line to say `SELINUX=disabled`
    

### Set Sudo with no Password
edit `/etc/sudoers` on all cluster machines.  Find this part. 

    ## Allows people in group wheel to run all commands
    %wheel  ALL=(ALL)       ALL
    
    ## Same thing without a password
    
    # %wheel        ALL=(ALL)       NOPASSWD: ALL     

Change which line is uncommented.  to 

    ## Allows people in group wheel to run all commands
    # %wheel  ALL=(ALL)       ALL
    
    ## Same thing without a password
    
    %wheel        ALL=(ALL)       NOPASSWD: ALL  


Your systems are ready for efficient system update with Ansible.   

This would be a good time to take a [lvm snapshot](lvm-snapshots.md)     

### Set up LVM Snapshots

I freed up 50 GB from the /home partition and then put 20 toward LVM snapshots and 30 was left 
over for the docker install, see next. 

if things get ugly.. I can reset to all the stuff above. Which should help. 

see the doc [lvm-snapshots.md](lvm-snapshots.md)

So the following things.. were done AFTER I set up the snapshot.  


### Turn off Password Login

On the entry machine, c1 I am going to turn off logging in with a password.  

To do that.. 

    sudo vi /etc/ssh/sshd_config

and change this line. 

    PasswordAuthentication no
    
It was `PasswordAuthentication yes`
    
Then:

    sudo systemctl reload sshd.service

If you do a status then it will show you things like.. 

    [centos@control01 ssh]$ sudo systemctl status sshd.service
    ● sshd.service - OpenSSH server daemon
       Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
       Active: active (running) since Sun 2019-06-09 08:23:30 PDT; 1 months 3 days ago
         Docs: man:sshd(8)
               man:sshd_config(5)
      Process: 7018 ExecReload=/bin/kill -HUP $MAINPID (code=exited, status=0/SUCCESS)
     Main PID: 5084 (sshd)
       CGroup: /system.slice/sshd.service
               └─5084 /usr/sbin/sshd -D
    
    Jul 12 20:02:10 control01.kafush.in systemd[1]: Reloading OpenSSH server daemon.
    Jul 12 20:02:10 control01.kafush.in sshd[5084]: Received SIGHUP; restarting.
    Jul 12 20:02:10 control01.kafush.in systemd[1]: Reloaded OpenSSH server daemon.
    Jul 12 20:02:10 control01.kafush.in sshd[5084]: Server listening on 0.0.0.0 port 22.
    Jul 12 20:02:10 control01.kafush.in sshd[5084]: Server listening on :: port 22.
    Jul 12 20:04:55 control01.kafush.in systemd[1]: Reloading OpenSSH server daemon.
    Jul 12 20:04:55 control01.kafush.in sshd[5084]: Received SIGHUP; restarting.
    Jul 12 20:04:55 control01.kafush.in systemd[1]: Reloaded OpenSSH server daemon.
    Jul 12 20:04:55 control01.kafush.in sshd[5084]: Server listening on 0.0.0.0 port 22.
    Jul 12 20:04:55 control01.kafush.in sshd[5084]: Server listening on :: port 22.
 
        
    
 Full details [here](https://www.liberiangeek.net/2014/07/enable-ssh-key-logon-disable-password-password-less-logon-centos/)



### Setting up Docker the right way..

This install of Docker is going to have a partition for the backing store. Not sure if this 
is just a RHEL oddness, but it does seem to be freaquently brought up. 

I put this in its own doc as well [docker-install.md](docker-install.md)


## System Management with Ansible



