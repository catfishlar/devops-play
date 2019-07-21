#      ARCH (linux,darwin)
export ARCH=linux
export PROD=prometheus
export VER=2.11.0


wget https://github.com/prometheus/${PROD}/releases/download/v${VER}/${PROD}-${VER}.${ARCH}-amd64.tar.gz
tar xvzf prometheus-${VER}.${ARCH}-amd64.tar.gz



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
