cat <<EOT >Dockerfile
FROM python:latest
EXPOSE 8000
CMD cd /share
CMD python -m http.server 8000
EOT

docker build -t python_http_server .

rm Dockerfile
