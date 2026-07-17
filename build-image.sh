#!/bin/bash
#
# build-image.sh
#
# Builds the accounts Docker image and captures the image details
# (Name, Tag, Image ID, Created, Size) into a file named "kube-images".
#
# Works with either Docker or Podman (Skills Network labs commonly use Podman).
#
# Usage:
#   ./build-image.sh            # builds accounts:1
#   ./build-image.sh myrepo:tag # builds a custom tag
#
set -e

IMAGE="${1:-accounts:1}"

# Pick whichever container engine is available
if command -v docker >/dev/null 2>&1; then
    ENGINE="docker"
elif command -v podman >/dev/null 2>&1; then
    ENGINE="podman"
else
    echo "ERROR: neither 'docker' nor 'podman' is installed." >&2
    exit 1
fi

echo "Using container engine: ${ENGINE}"
echo "Building image: ${IMAGE}"
"${ENGINE}" build -t "${IMAGE}" .

echo "Writing image details to ./kube-images"
"${ENGINE}" images "${IMAGE}" | tee kube-images

echo ""
echo "Done. The file 'kube-images' now contains the image details for Task 30."
