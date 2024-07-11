#!/bin/sh

set -e

echo "Checking for composer.json and the absence of composer.lock or vendor..."
if [ -f "composer.json" ] && ( [ ! -f "composer.lock" ] || [ ! -d "vendor" ] ); then
	echo "Running composer install..."
	composer \
		--no-ansi \
		--no-dev \
		--no-interaction \
		--no-progress \
		--no-scripts \
		--optimize-autoloader \
		install
else
	echo "No composer installation needed."
fi

exec "$@"
