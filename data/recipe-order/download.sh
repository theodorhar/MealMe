id="$1"
total="$2"
file="$3"
export http_proxy=$(cat ~/proxies | head -n "$1" | tail -n 1)
echo "#${id} using ${http_proxy}"
awk "NR % ${total} == ${id}" "$file" | wget --input-file=- --wait=5 -nd --html-extension -P pages -nv
