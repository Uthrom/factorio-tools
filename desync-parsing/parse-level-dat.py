#!/usr/local/bin/python3

import sys

# Setup Functions
def byte_to_file(file, byte):
  if file and byte:
    file.write(byte)

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

##    if leaving:
##      sys.stderr.write("OUT " + str(indent) + ": " + tag + "\n")
##    else:
##      sys.stderr.write("IN " + str(indent) + ": " + tag + "\n")
      
    return (tag, leaving, indent)


def main():
  if(len(sys.argv) < 2):
    sys.stderr.write("USAGE: "+ sys.argv[0] + " <inputfile> <outputfile>\n\n")
    sys.exit(1)

  # main code
  with open(sys.argv[2], 'w') as outF:
    with open(sys.argv[1], 'rb') as inF:

      indent = 0
      debugI = 0

      while True:
        byte = inF.read(1)

        if byte == b'':
          sys.stderr.write('Quitting')
          break
        
        # debugI += 1
        # sys.stderr.write(str(i) + ": " + str(d) + "\n")
        
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

