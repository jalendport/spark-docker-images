#!/bin/sh

cd /app

if [ ! -f "package-lock.json" ] || [ ! -d "node_modules" ]; then
    npm install
fi
