# jalendport/spark-redis

Redis images for developing and deploying Spark-based projects, built on the official Alpine images and password-protected by default.

Built from [jalendport/spark-docker-images](https://github.com/jalendport/spark-docker-images).

## Tags

Published for `linux/amd64` and `linux/arm64`.

| Tag      | Version    |
| -------- | ---------- |
| `7.2`    | Redis 7.2  |
| `latest` | `7.2`      |

Pin a version in real projects — `latest` moves when a new version lands.

## Usage

```yaml
services:
  redis:
    image: jalendport/spark-redis:7.2
```

## Configuration

The server starts with `--requirepass`, reading `REDIS_PASSWORD`, which defaults to `root`. Clients must authenticate.

```yaml
services:
  redis:
    image: jalendport/spark-redis:7.2
    environment:
      REDIS_PASSWORD: something-else
```

The default is meant for local development. Set a real password anywhere the port is reachable.

## Support

Found a bug or have a question? [Open an issue](https://github.com/jalendport/spark-docker-images/issues).
