#!/usr/bin/env bash
# Execute every translated notebook with the system Python / Jupyter (no venv, no docker).
# Executed copies are written to $OUT (default: ./_executed) so the shipped notebooks keep
# the book's original outputs.  Exit code 1 if any notebook fails.
#
#   cd zh-TW && bash tools/run_all.sh            # all notebooks
#   bash tools/run_all.sh 01-g-h-filter.ipynb    # just one
set -u
cd "$(dirname "$0")/.."
OUT=${OUT:-$(pwd)/_executed}
TIMEOUT=${TIMEOUT:-1800}
mkdir -p "$OUT"
if [ $# -gt 0 ]; then NBS=("$@"); else
  NBS=( *.ipynb Supporting_Notebooks/*.ipynb animations/*.ipynb )
fi
fail=0
for nb in "${NBS[@]}"; do
  d=$(dirname "$nb"); b=$(basename "$nb")
  mkdir -p "$OUT/$d"
  start=$(date +%s)
  if ( cd "$d" && jupyter nbconvert --to notebook --execute \
        --ExecutePreprocessor.timeout="$TIMEOUT" \
        --output-dir="$OUT/$d" --output "$b" "$b" >"$OUT/$d/${b%.ipynb}.log" 2>&1 ); then
    echo "OK    $nb ($(( $(date +%s) - start ))s)"
  else
    echo "FAIL  $nb  (see $OUT/$d/${b%.ipynb}.log)"; fail=1
  fi
done
exit $fail
