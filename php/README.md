# jalendport/spark-php

PHP images for developing and deploying Spark-based projects, built on the official Alpine images. Preloaded with the extensions Craft CMS and Laravel expect, and with Composer.

Built from [jalendport/spark-docker-images](https://github.com/jalendport/spark-docker-images).

## Tags

Every version publishes a `-cli` and an `-fpm` variant, for `linux/amd64` and `linux/arm64`.

| Tag                                      | Variant                 |
| ---------------------------------------- | ----------------------- |
| `7.4-cli` `7.4-fpm`                      | PHP 7.4                 |
| `8.0-cli` `8.0-fpm`                      | PHP 8.0                 |
| `8.1-cli` `8.1-fpm`                      | PHP 8.1                 |
| `8.2-cli` `8.2-fpm`                      | PHP 8.2                 |
| `8.3-cli` `8.3-fpm`                      | PHP 8.3                 |
| `8.4-cli` `8.4-fpm`                      | PHP 8.4                 |
| `7.4`, `8.0`, `8.1`, `8.2`, `8.3`, `8.4` | the matching `-cli` tag |
| `latest`, `latest-cli`                   | `8.4-cli`               |
| `latest-fpm`                             | `8.4-fpm`               |

Pin a version in real projects — `latest` moves when a new runtime lands.

## What's included

Extensions: `bcmath`, `gd` (FreeType, JPEG, WebP, and AVIF on 8.1 and newer), `imagick`, `intl`, `pdo_mysql`, `soap`, `zip`.

Also on `PATH`: `composer`, `git`, `mysql-client`, `zip`.

## Usage

The working directory is `/app`. Mount your project there.

```yaml
services:
  php:
    image: jalendport/spark-php:8.4-fpm
    volumes:
      - .:/app
```

On start, the image runs `composer install` when `composer.json` exists but `composer.lock` or `vendor/` does not, then execs the container's command. An existing install costs nothing.

```sh
docker compose run --rm php php craft up
```

## Configuration

The `-fpm` variants ship a `php.ini` at `/usr/local/etc/php/conf.d/yy-spark.ini`:

| Setting               | Value  |
| --------------------- | ------ |
| `memory_limit`        | `512M` |
| `max_execution_time`  | `5000` |
| `upload_max_filesize` | `512M` |
| `post_max_size`       | `512M` |
| `max_input_vars`      | `5000` |

Override it by mounting a file that sorts after it:

```yaml
volumes:
  - ./php.ini:/usr/local/etc/php/conf.d/zz-project.ini
```

FPM process manager settings live at `/usr/local/etc/php-fpm.d/yy-spark.conf` and can be overridden the same way.

## Support

Found a bug or have a question? [Open an issue](https://github.com/jalendport/spark-docker-images/issues).
