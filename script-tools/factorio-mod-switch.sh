#!/bin/bash

FACTORIO_RUN=0
FACTORIORC="$HOME/.factoriorc"                  # Local settings here
FACTORIO=""
DEFAULT_MODS=""
FACTORIO_DATA="$HOME/Library/Application Support/factorio"
FACTORIO_MODS="$FACTORIO_DATA/mods"

if [ -f $FACTORIORC ]; then			# Find user .rcfile and load 
  source $HOME/.factoriorc			# settings from there
fi

function usage {
  cat << __EOF
USAGE: `basename $0` [ -r | -h ] moddir_suffix

 -r         Launches factorio (if found)
 -h         Displays this help

This script is used to re-symlink factorio mod folders on Mac OS X,
since the Mac version of factorio(1) doesn't have a good way to run
multiple installs.
__EOF
  exit 1
}

while getopts "hr" OPTION; do
  case $OPTION in
    h)
      usage
      ;;
    r)
      FACTORIO_RUN=1
      ;;
  esac
done
shift "$(($OPTIND -1))"

if [ "x" != "x$1" ]; then
  NEW_MODS="$1"
else
  echo "No mod directory passed, using '$DEFAULT_MODS'"
  NEW_MODS="$DEFAULT_MODS" 
fi

if [ "x" == "x$NEW_MODS" ]; then
  usage
fi 

if [ "$FACTORIO_MODS-$NEW_MODS" -ef "$FACTORIO_MODS" ] ; then
  echo "Mod directory '$NEW_MODS' already linked."
else
  if [ -d "$FACTORIO_MODS-$NEW_MODS" ]; then
    rm -f "$FACTORIO_MODS"

    ln -s "$FACTORIO_MODS-$NEW_MODS" "$FACTORIO_MODS"

    ls -Fl "$FACTORIO_DATA" | grep 'mods'

    echo "Mod directory '$NEW_MODS' linked."
  else
    echo "No mod directory '$NEW_MODS' found."
    echo "Terminating"
    exit 1
  fi
fi

if [ $FACTORIO_RUN -gt 0 ]; then
  echo "Launching $FACTORIO"
  $FACTORIO
fi
