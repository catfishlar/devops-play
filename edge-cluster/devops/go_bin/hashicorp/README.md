### Hashicorp downloads

[Kelsey Hightower uses consul nomad and vault to deploy an app](https://www.youtube.com/watch?v=gf43TcWjBrE&list=PL81sUbsFNc5b-Gd59Lpz7BW0eHJBt0GvE&index=1)

#### Consul Service discovery and health check

[download page](https://www.consul.io/downloads.html)

There is also a tools directory that is worth looking into. 

    export ARCH=linux
    export VER=1.5.2
    wget https://releases.hashicorp.com/consul/${VER}/consul_${VER}_${ARCH}_amd64.zip
    unzip consul_${VER}_${ARCH}_amd64.zip

[tools page](https://www.consul.io/downloads_tools.html)

Some things to think about:

 * git2consul - mirrors the contents of a git Repository into a Consul KV
 * cfg4j-pusher - Command line app that pushes values from configuration fikes to consul KVs
 * confd - Manage local application configuration files using templates and data from etcd or Consul
 * consul-announcer - Command line wrapper for registering services in Consul
 
 