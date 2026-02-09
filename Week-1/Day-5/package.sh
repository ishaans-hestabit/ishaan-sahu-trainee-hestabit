#!/bin/bash

TARGET_FOLDERS="src logs docs"

echo "Starting Packaging"

find $TARGET_FOLDERS -type f -exec sha1sum {} + > checksum1.sha1

TS=$(date +%Y%m%d_%H%M)

zip -r "bundle-$TS.zip" $TARGET_FOLDERS checksum1.sha1

echo "Build Complete: bundle-$TS.zip"