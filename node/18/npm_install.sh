#!/bin/sh

set -e

echo "Checking for package.json and the absence of package-lock.json or node_modules..."
if [ -f "package.json" ] && ( [ ! -f "package-lock.json" ] || [ ! -d "node_modules" ] ); then
	echo "Running npm install..."
	npm install
else
	echo "No npm installation needed."
fi

exec "$@"
