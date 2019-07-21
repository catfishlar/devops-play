## Prometheus metrics

Downloads are here. 

https://prometheus.io/download/

I started making a download program but curling these urls doesn't work.  

if I click on the same link.. it does download so I am missing some peice of 
information on how to get this data down.. but you can go to the site. 

I did download a bunch of things so here is some examples of tools that might 
be nice to have. 

    # linux or darwin
    export ARCH=linux

    https://github.com/prometheus/${PROD}/releases/download/v${VER}/${PROD}-${VER}.${ARCH}-amd64.tar.gz
    prometheus-${VER}.${ARCH}-amd64.tar
    
    export PROD=prometheus
    export VER=2.10.0.0
    
    
    export PROD=alertmanager
    export VER=0.17.0
    
    export PROD=consul_exporter
    export VER=0.4.0
    
    export PROD=node_exporter
    export VER=0.18.1
    
    export PROD=pushgateway
    export VER=0.8.0
    
    export PROD=statsd_exporter
    export VER=0.11.2