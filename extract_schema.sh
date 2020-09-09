#!/usr/bin/env bash

test -d schema || mkdir schema
find -name '*.sqlite'|while read fname; do
	TMPOUT=schema/${fname//\//_}.txt
	FINALOUT=schema/${fname##*/}.txt
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
