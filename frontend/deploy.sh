#!/bin/bash

docker build --platform linux/amd64 --tag sqr-frontend .
docker image tag sqr-frontend fk12344321/sqr-frontend:latest
docker push fk12344321/sqr-frontend:latest

ssh -i ~/.ssh/ssd root@10.90.137.146 <<EOF
docker pull fk12344321/sqr-frontend:latest
docker stop frontend
docker rm frontend
docker run --name frontend -d --rm -p 9000:9000 fk12344321/sqr-frontend:latest
EOF