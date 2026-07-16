# jalendport/spark-nginx

nginx images for developing and deploying Spark-based projects, built on the official Alpine images and preconfigured to serve a PHP-FPM application.

Built from [jalendport/spark-docker-images](https://github.com/jalendport/spark-docker-images).

## Tags

Published for `linux/amd64` and `linux/arm64`.

| Tag      | Version    |
| -------- | ---------- |
| `1.26`   | nginx 1.26 |
| `latest` | `1.26`     |

Pin a version in real projects — `latest` moves when a new version lands.

## Usage

The bundled server block serves `/app/web` and passes `.php` requests to a host named `php` on port 9000, matching [`jalendport/spark-php`](https://hub.docker.com/r/jalendport/spark-php)'s `-fpm` variants.

```yaml
services:
  nginx:
    image: jalendport/spark-nginx:1.26
    ports:
      - "80:80"
    volumes:
      - .:/app
    depends_on:
      - php

  php:
    image: jalendport/spark-php:8.4-fpm
    volumes:
      - .:/app
```

## Configuration

The server block lives at `/etc/nginx/conf.d/default.conf`. It sets a `/index.php?$query_string` fallback for front-controller routing, enables `gzip_static` and SSI, removes the upload size limit, and disables caching on PHP responses so local development always reflects the working tree.

Replace it by mounting your own:

```yaml
volumes:
  - ./default.conf:/etc/nginx/conf.d/default.conf
```

## Support

Found a bug or have a question? [Open an issue](https://github.com/jalendport/spark-docker-images/issues).
