#!/bin/bash

FILES_TO_PACKAGE="src/ logs/ docs/"

echo "Starting Packaging"

sha1sum $FILES_TO_PACKAGE > checksums.sha1

TS=$(date +%Y%m%d_%H%M)

zip -r "bundle-$TS.zip" $FILES_TO_PACKAGE checksums.sha1

echo "Build Complete: bundle-$TS.zip"