#!/usr/bin/env python3
'''\
  Parses Factorio's desync report level_with_tags_tick_XXXXXXX.dat files into something more human readable, while trying to preserve the base data as much as possible.

  Does convert binary data into it's readable integer equivalent, for better or worse.
'''

## Import modules
import sys, os
from argparse import ArgumentParser

## Write a single raw byte to file (will be made superfluous soon)
def byte_to_file(file, byte):
  '''byte_to_file(file, byte) -- writes <byte> to <file>'''
  if file:
    file.write(byte)

## Read NUM bytes from file, catch exceptions
def from_file(file, num = 1):
  '''from_file(file, num) -- reads <num> bytes from <file>'''
  if file and num:
    try:
      buf = file.read(num)
    except IOError as e:
      sys.stderr.write ("Error[{0}]: {1}\n".format(e.errno, e.strerror))
    except ValueError as e:
      sys.stderr.write ("Error[{0}]: {1}\n".format(e.errno, e.strerror))
    except EOFError as e:
      sys.stderr.write ("Error[{0}]: {1}\n".format(e.errno, e.strerror))
    except:
      sys.stderr.write ("Error[{0}]: {1}\n".format(e.errno, e.strerror))

    return buf


## Make a string of bytes human-readable
def sanitize_string(s, convert_newline=1):
  '''sanitize_string(string, convert_newlines) -- makes <string> human-readable, possibly converting newlines to str(10)'''
  d = ord(s)
  if d < 32 and d != 10:
    return str(d)
  elif d == 10:
    if convert_newline:
      return str(d)
    else:
      return "\n"
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
def slurp_tag(file, indent = 0, DEBUG = False):
  if file:
    file.seek(file.tell()-1)
    tag = "<"
    leaving = False

    b = from_file(file, 1)
    
    while ord(b) != 62:
      b = from_file(file,1)

      if ord(b) == 47:
        leaving = True
        indent -= 1

      tag += sanitize_string(b)

      if DEBUG:
        if leaving:
          sys.stderr.write("OUT " + str(indent) + ": " + tag + "\n")
        else:
          sys.stderr.write("IN " + str(indent) + ": " + tag + "\n")
      
    return (tag, leaving, indent)


## Most of  the work happens here
def main():
  parser = ArgumentParser(description=__doc__)
  parser.add_argument('-v', '--version', action='version', version='%(prog)s 2.0')
  parser.add_argument('-d', '--debug', action='store_true', default=False, dest='DEBUG', help='Enable debug mode')
  parser.add_argument('in_file')
  parser.add_argument('out_file')
  args = parser.parse_args()

  if(not args.in_file or not args.out_file):
    parser.error("incorrect number of arguments")
    sys.exit(1)

  try:
    outF = open(args.out_file, 'w')
  except IOError as e:
    sys.stderr.write ("Output file error: {0}\n".format(e.strerror))
    sys.exit(1)
  else:
    try:
      inF = open(args.in_file, 'rb')
    except IOError as e:
      sys.stderr.write ("Input file error: {0}\n".format(e.strerror))
      sys.exit(1)
    else:
      with outF:
        with inF:
          inF.seek(0, os.SEEK_END)
          fsize = inF.tell()
          inF.seek(0)
            
          indent = 0

          while True:
            byte = from_file(inF,1)

            if byte == b'':
              if inF.tell() != fsize:
                sys.stderr.write('Unexpected EOF found, exiting\n')
              else:
                sys.stderr.write("Finished, exiting\n")
              break
            
            d = ord(byte)
            if d == 60:
              indent += 1
              
              (buf, leaving, indent) = slurp_tag(inF, indent, args.DEBUG)

              if leaving:
                indent -= 1
                string_to_file(outF, buf, 0, leaving)
              else:
                string_to_file(outF, buf, indent, leaving)
            else:  
              byte_to_file(outF, sanitize_string(byte))

if __name__ == "__main__":
  main()

