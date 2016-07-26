FROM nginx:stable-alpine

# 82 is the standard uid/gid for "www-data" in Alpine
# http://git.alpinelinux.org/cgit/aports/tree/main/apache2/apache2.pre-install?h=v3.3.2
# http://git.alpinelinux.org/cgit/aports/tree/main/lighttpd/lighttpd.pre-install?h=v3.3.2
# http://git.alpinelinux.org/cgit/aports/tree/main/nginx-initscripts/nginx-initscripts.pre-install?h=v3.3.2
# (we use nginx in our case)
# TODO: use www-data?
RUN set -xe \
    && echo "http://nl.alpinelinux.org/alpine/edge/testing" | tee -a /etc/apk/repositories \
    && apk add --no-cache shadow \
    && usermod -u 82 nginx \
    && groupmod -g 82 nginx \
    && apk del --no-cache shadow \
    && head -n -1 /etc/apk/repositories | tee /etc/apk/repositories
