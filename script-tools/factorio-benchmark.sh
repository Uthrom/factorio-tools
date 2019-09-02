#!/bin/sh

FACTORIORC="$HOME/.factoriorc"			# Local settings here
FACTORIO=""

if [ -f $FACTORIORC ]; then			# Find user .rcfile and load
  source $HOME/.factoriorc			# settings from there
fi

function usage {
  cat << __EOF
USAGE: `basename $0` [ -h | -m <NUM> | -t <NUM> | -r <NUM> | ] -o <OUTFILE> save1 save2 .. saveN

 -h         	Displays this help
 -m <NUM>		Number of minutes of game time to run each benchmark
 -t <NUM>		Number of ticks to run each benchmark
 -r <NUM>		Number of times to run benchmark
 -o <OUTFILE>	Output to <OUTFILE> instead of stdout

This script used to simplify running factorio(1) benchmarks, it lets you specify
the list of save files to run, how many minutes (or ticks) to run each file, and
how often to re-run the benchmark, if anything.

The output is saved to the output file specified.
__EOF
  exit 1
}

B_MINS=0
B_TICKS=`echo "$B_MINS * 3600" | bc`
B_RUNS=0
OUTPUT="benchmark-out"

while getopts "hm:t:r:o:" OPTION; do
  case $OPTION in
    h)
      usage
      ;;
    m)
      B_MINS=$OPTARG
      ;;
    t)
      B_TICKS=$OPTARG
      ;;
    r)
      B_RUNS=$OPTARG
      ;;
    o)
      OUTPUT=$OPTARG
      ;;
  esac
done
shift "$(($OPTIND -1))"

if [ $# -lt 1 ]; then
  echo "Not enough arguments"
  usage
fi

if [ "x" == "x$OUTPUT" ]; then
  OUTPUT="`echo $1 | sed -e 's/\.zip//'`"
fi

if [ $B_TICKS -lt 1 ] && [ $B_MINS -gt 0 ]; then
  B_TICKS=`echo "$B_MINS * 3600" | bc`
fi

for FILE in $*; do
  if [ -f $FILE ]; then
    (
      /bin/echo -n "$FILE,"
      $FACTORIO --benchmark $FILE --benchmark-ticks $B_TICKS --benchmark-runs $B_RUNS 2>&1 | awk "/Performed.*updates/ {print \$5}" | xargs echo  | sed -e 's/ /,/g'
    ) | sed -e 's/\n//g' >> $OUTPUT.csv
  else
    echo "File '$FILE' not found!"
  fi
done
