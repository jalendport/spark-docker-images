FROM php:7.4-fpm-alpine

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
	# Pecl extensions
	&& pecl install \
		imagick \
	# Configure extensions
	&& docker-php-ext-configure \
		gd --with-freetype --with-jpeg --with-webp \
	# Install extensions
	&& docker-php-ext-install -j$(nproc) \
		bcmath \
		gd \
		intl \
		pdo_mysql \
		soap \
		zip \
	# Enable extensions
	&& docker-php-ext-enable \
		imagick \
	# Remove dependencies
	&& apk del .build-deps

COPY ./php.ini /usr/local/etc/php/conf.d/yy-spark.ini
COPY ./phpfpm.conf /usr/local/etc/php-fpm.d/yy-spark.conf

COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

WORKDIR /app

COPY --chmod=+x ./composer_install.sh /app-tmp/composer_install.sh

# Runs "composer install" if composer.json exists but composer.lock or vendor do not exist
ENTRYPOINT ["/app-tmp/composer_install.sh"]

CMD ["php-fpm"]
