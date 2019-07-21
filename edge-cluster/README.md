## Edge Cluster

Outside of the Kubernetes cluster is the Edge Cluster.

The primary thing here is the Dynamic Reverse Proxy `traefik` but also `consul` 
for managing this.  The idea of using consul instead of just the Kubernetes etcd
is because there are servers outside of the kubernetes cluster that we want to 
manage as well and having our consul outside of 
kubernetes lets us do both. 

Other things that belong at this layer are system services 
like prometheus and databases. 

We COULD put it inside the kubernetes cluster, but 
this lets me decide. 

This will work with 3 other go based system services  (which will not require me to
have root). 

 * [consul](consul.md) for service discovery
 * [traefik](traefik.md) for reverse proxy with consul as the provider
 * [promotheus](promotheus) metrics
 
The Deployment, configuration and starting of the services and the FlaskHub is manaaged in the [devops](devops/README.md) 
section of this repo. 

 