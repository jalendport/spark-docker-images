# jalendport/spark-node

Node images for developing and deploying Spark-based projects, built on the official Alpine images.

Built from [jalendport/spark-docker-images](https://github.com/jalendport/spark-docker-images).

## Tags

Published for `linux/amd64` and `linux/arm64`.

| Tag      | Version |
| -------- | ------- |
| `16`     | Node 16 |
| `18`     | Node 18 |
| `20`     | Node 20 |
| `22`     | Node 22 |
| `24`     | Node 24 |
| `latest` | `24`    |

Pin a version in real projects — `latest` moves when a new runtime lands.

## Usage

The working directory is `/app`. Mount your project there.

```yaml
services:
  node:
    image: jalendport/spark-node:24
    volumes:
      - .:/app
```

On start, the image runs `npm install` when `package.json` exists but `package-lock.json` or `node_modules/` does not, then execs the container's command. An existing install costs nothing.

The default command is `npm run dev`. Pass your own to do something else:

```sh
docker compose run --rm node npm run build
```

## Support

Found a bug or have a question? [Open an issue](https://github.com/jalendport/spark-docker-images/issues).
