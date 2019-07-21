## Prometheus

The main UI is located on port 9090 of the prometheus server. 

If you have consul-exporter set up correctly you could enter this 

    min(consul_catalog_service_node_healthy) by (service_name)
    
in the little window and get the healthy services from consul. 


### Consul Exporter

this talks to consul and feeds prometheus with data from Consul.  

https://github.com/prometheus/consul_exporter



 