build_docker() {
    cat <<EOT >Dockerfile
    FROM python:latest
    EXPOSE 8000
    CMD cd /share
    CMD python -m http.server 8000
EOT

    docker build -t python_http_server .

    rm Dockerfile
}

make_available_everywhere() {
    target="share.sh"
    sudo ln -s `realpath "$target"` /usr/local/bin/"$target"
    echo alias share=\"$target\" >> ~/.zshrc
}

build_docker
make_available_everywhere
