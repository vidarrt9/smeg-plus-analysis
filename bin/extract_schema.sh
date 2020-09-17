#!/usr/bin/env bash
pushd $(dirname $0) > /dev/null; BASEDIR=$(readlink -nf "$(pwd)"); popd > /dev/null

SCHDIR="$BASEDIR/../schema"
test -d "$SCHDIR" || mkdir "$SCHDIR"
(cd "$BASEDIR/.." && find -name '*.sqlite')|while read fname; do
	TMPOUT="$SCHDIR/${fname//\//_}.txt"
	FINALOUT="$SCHDIR/${fname##*/}.txt"
	sqlite3 $fname '.schema' > "$TMPOUT"
	if [[ -e "$FINALOUT" ]]; then
		# compare existing and new
		if diff "$FINALOUT" "$TMPOUT"; then
			rm "$TMPOUT"
			echo "Contents of $FINALOUT identical to schema from $fname"
		fi
	else
		mv "$TMPOUT" "$FINALOUT"
	fi
done
