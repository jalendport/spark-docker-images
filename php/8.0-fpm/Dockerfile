FROM php:8.0-fpm-alpine

# https://github.com/docker-library/php/issues/105#issuecomment-249716758
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
	# Pecl extensions
	&& pecl install \
		imagick \
	# Configure extensions
	&& docker-php-ext-configure \
		gd --with-freetype --with-jpeg \
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

RUN mkdir -p /app /app-tmp

WORKDIR /app

COPY ./composer_install.sh /app-tmp/composer_install.sh
RUN chmod a+x /app-tmp/composer_install.sh

# Runs "composer install" if composer.json exists but composer.lock or vendor do not exist
ENTRYPOINT ["/app-tmp/composer_install.sh"]

CMD ["php-fpm"]
