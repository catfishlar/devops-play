## Flaskhub devops

This is a tiny installation, and so we are not going to use even Ansible.  

Instead everything will be based on Python Fabric.  Brain dead simple 
push install and configure.  

To run Fabric and Flask you need a  

### Conda Environment

You need a conda environment with at least Anaconda 3 with Python 3.6. 

    conda env create -f environment.yml
    
With this [environment.yml](environment.yml)


### Go Programs

#### Downloads

The go programs are binaries, there is a series of docs and scripts to grab these
binaries in `go_bin`  you can read more in the [go_bin README](go_bin/README.md)

After cloning the repo, you have to populate the `go_bin` directory.

### Service Deploy Config Start

#### Consul 

We got a traefik-consul.json from https://github.com/mantl/mantl/blob/master/roles/traefik/files/traefik-consul.json
The simplified version we actual use is in `etc/consul.d/traefik.json`

Also an entry for the flaskHub in `etc/consul.d/flaskhub.json`

//#todo get checks in.  Add a health end point to flaskhub app and use it for the 
check. 

#### Prometheus  

##### Consul exporter

This is available on the promotheus download page but also the [github](https://github.com/prometheus/consul_exporter)

Need to run that and add this to `prometheus.yml`:

      - job_name: 'consul'
        static_configs:
        - targets: ['localhost:9107']

#### Traefik

Need a default config file.  https://raw.githubusercontent.com/containous/traefik/v1.7/traefik.sample.toml

In order to be nonroot we need to have a default port > 1024.  I changed ":80" to ":2222"

    [entryPoints]
      [entryPoints.web]
      address = ":2222"

I created the log directory and had logs and access go to that.  Again the goal we have is to 
not have anything go into restricted directories since we don't have sudo. 

Need to make Consul the back end provider https://docs.traefik.io/configuration/backends/consul/

And the you need to set up Consul to have the right KV values needed by 
Traefik. https://docs.traefik.io/user-guide/kv-config/#key-value-storage-structure

Finally a good tutorial on setting it up with Consul as your provider.  
https://rogerwelin.github.io/traefik/reverse/proxy/micro/services/2018/09/17/traefik-tutorial.html

#### PostgreSQL

[Postgres without Root](https://www.endpoint.com/blog/2013/06/12/installing-postgresql-without-root)

##### Mac Postgres.app

Downloaded the app https://postgresapp.com/

Added the command line tools to the shell.  https://postgresapp.com/documentation/install.html

    sudo mkdir -p /etc/paths.d && echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp