#!/bin/sh

TMP="/tmp/`basename $0`.$$"			# Temp file
trap 'rm -f $TMP' 0 1 9 11 15			# Clean up on exit

rm -f $TMP					# Did somebody else leave this?
touch $TMP					# Now it's ours

FACTORIORC="$HOME/.factoriorc"			# Local settings here
FACTORIO=""					# Default executable

if [ -f $FACTORIORC ]; then			# Find user .rcfile and load
  source $HOME/.factoriorc			# settings from there
fi

function usage {
  cat << __EOF
USAGE: `basename $0` [ -h | -m <NUM> | -t <NUM> | -r <NUM> | -o <OUTFILE> ] save1 save2 .. saveN

 -h         	Displays this help
 -m <NUM>		Number of minutes of game time to run each benchmark
 -t <NUM>		Number of ticks to run each benchmark
 -r <NUM>		Number of times to run benchmark
 -o <OUTFILE>	Output to <OUTFILE> instead of stdout

This script used to simplify running factorio(1) benchmarks, it lets you specify
the list of save files to run, how many minutes (or ticks) to run each file, and
how often to re-run the benchmark, if anything.

The output is printed to STDOUT or saved to the output file specified.
__EOF
  exit 1
}

B_MINS=0
B_TICKS=`echo "$B_MINS * 3600" | bc`
B_RUNS=1
OUTPUT=""

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

if [ $B_TICKS -lt 1 ] && [ $B_MINS -gt 0 ]; then
  B_TICKS=`echo "$B_MINS * 3600" | bc`
fi

for FILE in $*; do
  if [ -f $FILE ]; then
      ( 
        /bin/echo -n "$FILE," 
        $FACTORIO --benchmark $FILE --benchmark-ticks $B_TICKS --benchmark-runs $B_RUNS 2>&1 | awk "/Performed.*updates/ {print \$5}" | xargs echo  | sed -e 's/ /,/g'
      ) | sed -e 's/\n//g' >> $TMP
  else
    echo "File '$FILE' not found!"
  fi
done

# Display results from above
if [ "x" == "x$OUTPUT" ]; then
  cat $TMP
else
  cp $TMP $OUTPUT.csv
fi
