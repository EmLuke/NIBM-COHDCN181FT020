import sys, os

if os.path.isfile(sys.argv[1]):
    f=sys.argv[1]

file = open(f, "rb")
rawContent = file.read()
strContent = str(rawContent)

line=0
read=0

for c in range(int(len(strContent)/16)):
    text = "{:08x}".format(line) + ": "
    text += " ".join("{:04x}".format(ord(x)) \
                     for x in strContent[read:read + 8])
    text += " " + strContent[read:read + 16]
    line += 16	
    read += 16



    print(text)
