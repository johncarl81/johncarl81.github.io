#!/usr/bin/env bash
# Regenerates the responsive WebP hero images from the original source photo.
# Overwrites images/hero/*.webp; the source JPEG is never modified.
# Requires ImageMagick built with WebP support.
set -euo pipefail

SOURCE_IMAGE="images/john_fagradalsfjall.jpg"
OUTPUT_DIR="images/hero"
WIDTHS=(640 1024 1600 2400)
QUALITY=80

cd "$(dirname "${0}")/.."
mkdir -p "${OUTPUT_DIR}"

base_name="$(basename "${SOURCE_IMAGE}" .jpg)"
for width in "${WIDTHS[@]}"; do
  output="${OUTPUT_DIR}/${base_name}-${width}.webp"
  convert "${SOURCE_IMAGE}" -auto-orient -resize "${width}x" -strip -quality "${QUALITY}" "${output}"
  echo "${output} $(du -h "${output}" | cut -f1)"
done
