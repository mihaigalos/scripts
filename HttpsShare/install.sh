#! /bin/bash

create_server_certificate() {
    if [ ! -f server_certificate.pem ]; then
        echo "We'll generate a certificate now.\n"
        openssl req -new -x509 -keyout server_certificate.pem -out server_certificate.pem -days 365 -nodes
    fi
}

build_docker() {
    cat <<EOT >Dockerfile
    FROM python:latest
    EXPOSE 8000
    COPY https_server.py /https_server.py
    COPY server_certificate.pem /server_certificate.pem
    CMD cd /share
EOT

    docker build -t python_https_server .
}

make_available_everywhere() {
    target="share.sh"
    if [ ! -f /usr/local/bin/"$target" ]; then
        sudo ln -s `realpath "$target"` /usr/local/bin/"$target"
        echo alias share=\"$target\" >> ~/.zshrc
	source ~/.zshrc
    fi
}

teardown() {
    rm Dockerfile
    rm server_certificate.pem
}

create_server_certificate
build_docker
make_available_everywhere
teardown

