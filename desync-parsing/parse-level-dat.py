#!/usr/bin/env python3
'''\
%prog [options] <infile> <outfile>

  Parses Factorio's desync report level_with_tags_tick_XXXXXXX.dat files into something more human readable, while trying to preserve the base data as much as possible.

  Does convert binary data into it's readable integer equivalent, for better or worse.
'''

## Import modules
import sys
from optparse import OptionParser


## Global variables
opts = []


## Write a single raw byte to file (will be made superfluous soon)
def byte_to_file(file, byte):
  '''byte_to_file(file, byte) -- writes <byte> to <file>'''
  if file and byte:
    file.write(byte)


## Make a string of bytes human-readable
def sanitize_string(s, newline=0):
  d = ord(s)
  if d < 32 and d != 10:
    return str(d)
  elif d == 10:
    if newline:
      return "\n"
    else:
      return str(d)
  elif d == 45:
    return chr(d)
  elif d == 64:
    return chr(d)
  elif d > 126:
    return str(d)
  else:
    return chr(d)


## Write a string to file, possibly indenting appropriately
def string_to_file(file, s, indent = 0, leaving = 0):
  if file and s:
    if not leaving:
      file.write("\n")
      
    if indent:        
      x = 0
      while x < indent:
        file.write(" ")
        x += 1
        if x > 10:
          break

    file.write(s)
    if leaving:
      file.write("\n")

## Suck in an entire <...> XML-ish tag, and return whether it's opening or closing
def slurp_tag(file, indent = 0):
  if file:
    file.seek(file.tell()-1)
    tag = "<"
    leaving = False

    b = file.read(1)
    
    while ord(b) != 62:
      b = file.read(1)

      if ord(b) == 47:
        leaving = True
        indent -= 1

      tag += sanitize_string(b, 1)

      if opts.DEBUG:
        if leaving:
          sys.stderr.write("OUT " + str(indent) + ": " + tag + "\n")
        else:
          sys.stderr.write("IN " + str(indent) + ": " + tag + "\n")
      
    return (tag, leaving, indent)


## Most of  the work happens here
def main():
  parser = OptionParser(usage=__doc__, version='%prog v0.2')
  parser.add_option('-d', '--debug', action='store_true', default=False, dest='DEBUG', help='Enable debug mode')

  (opts, args) = parser.parse_args()

  if(len(args) < 2):
    parser.error("incorrect number of arguments")
    sys.exit(1)

  with open(args[1], 'w') as outF:
    with open(args[0], 'rb') as inF:
      indent = 0

      while True:
        byte = inF.read(1)

        if byte == b'':
          sys.stderr.write('Quitting')
          break
        
        d = ord(byte)
        if d == 60:
          indent += 1
          
          (buf, leaving, indent) = slurp_tag(inF, indent)

          if leaving:
            indent -= 1
            string_to_file(outF, buf, 0, leaving)
          else:
            string_to_file(outF, buf, indent, leaving)
        else:  
          byte_to_file(outF, sanitize_string(byte))

if __name__ == "__main__":
  main()

