FROM alpine:3.4

RUN adduser -S doc

RUN set -xe \
    && echo "http://nl.alpinelinux.org/alpine/edge/community" | tee -a /etc/apk/repositories \
    && apk --no-cache add \
        bash \
        enchant \
        aspell-en \
        git \
        make \
        python \
        py-pip \
        inotify-tools \
        su-exec \
        shadow

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /doc

VOLUME ["/doc"]

CMD ["/bin/bash"]

COPY entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
