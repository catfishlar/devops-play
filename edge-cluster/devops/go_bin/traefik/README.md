## Traefik Download

Look for the release you want.  https://github.com/containous/traefik/releases

automate download. 
    
    # ARCH is darwin(mac) or linux
    export ARCH=darwin
    export VER=1.6.6
    wget "https://github.com/containous/traefik/releases/download/v${VER}/traefik_${ARCH}-amd64"
    mv traefik_${ARCH}-amd64 traefik && chmod +x traefik