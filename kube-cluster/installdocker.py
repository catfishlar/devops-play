from fabric import Connection
hosts = ['r1','r2','r3','c1','c2','c3']
commands = [
             'sudo lvcreate -L 30GB -n docker centos',
             'sudo mkfs.xfs /dev/centos/docker',
             'sudo yum install -y yum-utils device-mapper-persistent-data lvm2',
             'sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo',
             'sudo yum install -y docker-ce docker-ce-cli containerd.io',
             'sudo systemctl start docker',
             'sudo systemctl stop docker',
             'sudo mount /dev/mapper/centos-docker /var/lib/docker',
             'sudo sed -i  "\$a/dev/mapper/centos-docker /var/lib/docker                  xfs     defaults        0 0" /etc/fstab',
             'sudo systemctl start docker',
             'sudo systemctl enable docker'


        ]

def run(c,com,sum) :
    r = c.run(com)
    if not r.ok :
        sum.write(f"command |{com}| run on {r.connection.host} resulted in {r.stdout}")
        raise RuntimeError(f"command |{com}| run on {r.connection.host} resulted in {r.stdout}")

    sum.write(f"Success : {r.connection.host} : command |{com}| \n")
    return r

with open("summary.out",'w') as sum:
    for host in hosts:
        c = Connection(host=host, user='centos')
        for com in commands:
            run(c,com,sum)