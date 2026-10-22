FROM php:8.2.35-cli-alpine

RUN apk add --no-cache --virtual .build-deps \
		# Build dependencies
		$PHPIZE_DEPS \
		freetype-dev \
		icu-dev \
		imagemagick-dev \
		libjpeg-turbo-dev \
		libpng-dev \
		libtool \
		libxml2-dev \
		libzip-dev \
		libwebp-dev \
		libavif-dev \
		libheif-dev \
	&& apk add --no-cache \
		# Runtime dependencies
		freetype \
		git \
		gnu-libiconv \
		icu \
		imagemagick \
		libgomp \
		libjpeg-turbo \
		libpng \
		libxml2 \
		libzip \
		mariadb-connector-c \
		mysql-client \
		zip \
		libwebp \
		libavif \
		libheif \
	# Fetch the imagick source; PECL is not used
	&& curl -fsSL -o /tmp/imagick.tar.gz https://github.com/Imagick/imagick/archive/refs/tags/3.8.1.tar.gz \
	&& mkdir -p /tmp/imagick \
	&& tar -xzf /tmp/imagick.tar.gz -C /tmp/imagick --strip-components=1 \
	&& rm /tmp/imagick.tar.gz \
	# Configure extensions
	&& docker-php-ext-configure \
		gd --with-freetype --with-jpeg --with-webp --with-avif \
	# Install extensions
	&& docker-php-ext-install -j$(nproc) \
		bcmath \
		gd \
		intl \
		pdo_mysql \
		soap \
		zip \
		/tmp/imagick \
	&& rm -r /tmp/imagick \
	# Remove dependencies
	&& apk del .build-deps

COPY --from=composer:2 /usr/bin/composer /usr/local/bin/composer

WORKDIR /app

COPY --chmod=+x ./composer_install.sh /app-tmp/composer_install.sh

# Runs "composer install" if composer.json exists but composer.lock or vendor do not exist
ENTRYPOINT ["/app-tmp/composer_install.sh"]

CMD ["php"]
