#!/bin/zsh
# Fetch the David Potolski Medium corpus into raw/.
# Run from anywhere:  zsh corpus/david/fetch.sh
set -u

DIR="${0:A:h}/raw"
mkdir -p "$DIR"

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36'

fetch() {
  local out="$1" url="$2"
  curl -sL --compressed -A "$UA" "$url" -o "$DIR/$out"
  printf '%-28s %8s bytes\n' "$out" "$(wc -c < "$DIR/$out" | tr -d ' ')"
}

fetch feed.xml \
  'https://davidpotolskilafeta.medium.com/feed'

fetch a1-procrastination.html \
  'https://davidpotolskilafeta.medium.com/how-to-stop-procrastinating-and-reach-your-goals-faster-e673feb1508e'

fetch a2-savemoney.html \
  'https://davidpotolskilafeta.medium.com/2-tips-that-can-save-your-company-lots-of-money-a3fb78eb824c'

fetch a3-game.html \
  'https://davidpotolskilafeta.medium.com/lessons-learned-while-developing-my-first-game-982d227e5c30'

fetch a4-selling.html \
  'https://medium.datadriveninvestor.com/the-secret-of-selling-anything-f71b7341c933'

echo
echo "done -> $DIR"
