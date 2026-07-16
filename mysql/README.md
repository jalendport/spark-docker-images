# jalendport/spark-mysql

MySQL images for developing and deploying Spark-based projects.

Built from [jalendport/spark-docker-images](https://github.com/jalendport/spark-docker-images).

## Tags

| Tag      | Version                                                                |
| -------- | ---------------------------------------------------------------------- |
| `5.7`    | MySQL 5.7, on [`biarms/mysql`](https://hub.docker.com/r/biarms/mysql) for arm64 support |
| `8.4`    | MySQL 8.4, on the official image                                        |
| `latest` | `8.4`                                                                  |

Pin a version in real projects — `latest` moves when a new version lands.

MySQL 5.7 reached end of life in October 2023 and receives no upstream security fixes. It is published for legacy projects only; use `8.4` for anything new.

## Usage

Configured through the same environment variables as the official image.

```yaml
services:
  mysql:
    image: jalendport/spark-mysql:8.4
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: spark
    volumes:
      - mysql:/var/lib/mysql

volumes:
  mysql:
```

## Configuration

The `5.7` image sets a `sql_mode` at `/etc/mysql/conf.d/yy-spark.cnf` that drops `ONLY_FULL_GROUP_BY`, a long-standing accommodation for older Craft installs. `8.4` runs stock, so it keeps `ONLY_FULL_GROUP_BY` on, and a query that passes on `5.7` can still fail there. Craft has not needed the workaround since Craft 3 stopped grouping element queries, so prefer fixing the query over loosening `8.4`.

Add your own config by mounting into the same directory:

```yaml
volumes:
  - ./my.cnf:/etc/mysql/conf.d/zz-project.cnf
```

## Support

Found a bug or have a question? [Open an issue](https://github.com/jalendport/spark-docker-images/issues).
