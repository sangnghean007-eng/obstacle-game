#!/usr/bin/env bash
# Download a CC-licensed reference photo from Wikimedia Commons for proportion study ONLY.
# Usage: fetch_ref.sh "<search words>"            -> lists matching file names
#        fetch_ref.sh --get "<File name.jpg>" <outdir> -> downloads (600-800 px wide)
# Rules: photos stay OUTSIDE the repo (scratchpad). Never ship, trace or commit them. Commons rate-limits: we sleep 6 s.
UA="Soccer365ResearchBot/1.0 (character proportion study; low volume)"
if [ "$1" = "--get" ]; then
  f="$2"; out="${3:-.}"; mkdir -p "$out"; n=$(echo "$f" | tr ' ,()' '____'); sleep 6
  curl -sSL -A "$UA" -o "$out/$n" "https://commons.wikimedia.org/wiki/Special:FilePath/$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$f")?width=800" && echo "$out/$n"
else
  sleep 6; curl -sS -A "$UA" --get "https://commons.wikimedia.org/w/api.php" --data-urlencode action=query --data-urlencode list=search \
    --data-urlencode srnamespace=6 --data-urlencode "srsearch=$1" --data-urlencode srlimit=12 --data-urlencode format=json \
    | python3 -c "import json,sys
try: print('\n'.join(x['title'][5:] for x in json.load(sys.stdin)['query']['search']))
except Exception: print('rate-limited: wait a minute and retry')"
fi
