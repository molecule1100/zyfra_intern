#!/bin/bash
# Продление сертификата Let's Encrypt
set -e
cd /root/vkr/zyfra_intern
docker compose run --rm --entrypoint certbot certbot renew --webroot -w /var/www/certbot --quiet
docker compose exec -T nginx nginx -s reload
