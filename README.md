<h1 align="center">Spark Docker Images</h1>

<p align="center"><em>Docker images for developing and deploying Spark-based projects.</em></p>

## Features

- **One set of images everywhere** — the same PHP and Node builds back local development, [CI](https://github.com/jalendport/spark-github-actions), and deploys, so a green pipeline means something.
- **Batteries included for Craft and Laravel** — `gd`, `imagick`, `intl`, `pdo_mysql`, `soap`, `zip`, and `bcmath` are compiled in, and Composer ships in the image.
- **Installs dependencies on first run** — the PHP and Node images run `composer install` / `npm install` on start when the lockfile or vendor directory is missing, so a fresh clone comes up with `docker compose up`.
- **Alpine based** — small images and fast pulls.
- **amd64 and arm64** — every tag is a multi-arch manifest, so Apple Silicon runs natively.
- **Only what changed is rebuilt** — a push builds the affected versions, not the whole matrix.

## Images

All images are published to Docker Hub under [`jalendport`](https://hub.docker.com/u/jalendport).

| Image                                                            | Tags                                                                                                                   | Purpose                           |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| [`spark-php`](https://hub.docker.com/r/jalendport/spark-php)     | `7.4-cli` `7.4-fpm` `8.0-cli` `8.0-fpm` `8.1-cli` `8.1-fpm` `8.2-cli` `8.2-fpm` `8.3-cli` `8.3-fpm` `8.4-cli` `8.4-fpm` | Application runtime               |
| [`spark-node`](https://hub.docker.com/r/jalendport/spark-node)   | `16` `18` `20` `22` `24`                                                                                                | Front-end builds                  |
| [`spark-nginx`](https://hub.docker.com/r/jalendport/spark-nginx) | `1.26`                                                                                                                 | Web server, preconfigured for FPM |
| [`spark-mysql`](https://hub.docker.com/r/jalendport/spark-mysql) | `5.7` `8.4`                                                                                                            | Database                          |
| [`spark-redis`](https://hub.docker.com/r/jalendport/spark-redis) | `7.2`                                                                                                                  | Cache and queues                  |

### Alias tags

Every image carries `latest`, pointing at the newest version. `spark-php` carries a few more, because it publishes two variants per version:

| Alias                                    | Points at               |
| ---------------------------------------- | ----------------------- |
| `latest`, `latest-cli`                   | `8.4-cli`               |
| `latest-fpm`                             | `8.4-fpm`               |
| `7.4`, `8.0`, `8.1`, `8.2`, `8.3`, `8.4` | the matching `-cli` tag |

Pin a version in real projects — `latest` moves when a new runtime lands.

## Usage

A typical `compose.yaml` for a Craft or Laravel project:

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
    depends_on:
      - mysql
      - redis

  node:
    image: jalendport/spark-node:24
    volumes:
      - .:/app

  mysql:
    image: jalendport/spark-mysql:8.4
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: spark
    volumes:
      - mysql:/var/lib/mysql

  redis:
    image: jalendport/spark-redis:7.2

volumes:
  mysql:
```

Mount the project at `/app` — it is the working directory in the PHP and Node images, and `spark-nginx` serves `/app/web` and passes PHP to a host named `php` on port 9000.

### First-run installs

`spark-php` and `spark-node` check for dependencies on start:

- **`spark-php`** runs `composer install` when `composer.json` exists but `composer.lock` or `vendor/` does not.
- **`spark-node`** runs `npm install` when `package.json` exists but `package-lock.json` or `node_modules/` does not.

Both then exec the container's command, so an existing install costs nothing. Pass a command as usual to skip past the default:

```sh
docker compose run --rm php php craft up
docker compose run --rm node npm run build
```

### PHP configuration

Both variants compile in `bcmath`, `gd` (with FreeType, JPEG, WebP, and — on 8.1 and newer — AVIF), `imagick`, `intl`, `pdo_mysql`, `soap`, and `zip`, and ship `composer`, `git`, `mysql-client`, and `zip`. The `-fpm` variants also apply:

| Setting               | Value  |
| --------------------- | ------ |
| `memory_limit`        | `512M` |
| `max_execution_time`  | `5000` |
| `upload_max_filesize` | `512M` |
| `post_max_size`       | `512M` |
| `max_input_vars`      | `5000` |

Override by mounting your own file — anything in `/usr/local/etc/php/conf.d/` sorting after `yy-spark.ini` wins:

```yaml
volumes:
  - ./php.ini:/usr/local/etc/php/conf.d/zz-project.ini
```

`spark-redis` starts with `--requirepass`, defaulting to `root`. Set `REDIS_PASSWORD` to change it.

## Repository layout

Each image is a directory of versions, and each version is a directory holding a `Dockerfile` and its config:

```
php/8.4-fpm/Dockerfile     # → jalendport/spark-php:8.4-fpm
node/24/Dockerfile         # → jalendport/spark-node:24
```

The directory name is the tag. A per-image workflow in `.github/workflows/` declares the versions and their alias tags, then calls `generic.yml`, which builds and pushes them. Adding a version means adding a directory and naming it in that image's workflow — a version the workflow does not name is never built, so `validate-workflows.py` checks the two against each other.

## Building locally

```sh
docker build -t spark-php:8.4-fpm php/8.4-fpm
```

Before pushing a change to the workflows:

```sh
python3 .github/scripts/validate-workflows.py
```

The workflows themselves can be run with [act](https://github.com/nektos/act). `event.json` sets `act: true`, which the workflows read to skip the login, push, and Docker Hub steps:

```sh
act push --eventpath event.json
```

## Support

Found a bug or have a question? [Open an issue](https://github.com/jalendport/spark-docker-images/issues).

---

<p align="center">Made by <a href="https://jalendport.com">Jalen Davenport</a></p>
