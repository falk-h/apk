#!/bin/sh
PYTHON="python3" # Need Python 3
API="https://www.systembolaget.se/api/assortment/products/xml" # URL to get the API
OUT="/var/www/hoppner/apk_raw.html" # Output file for the table

tmp="$(mktemp)"

curl "$API" -o "$tmp"
"$PYTHON" /home/fh/apk/apk.py "$tmp" > "$OUT"
rm "$tmp"
