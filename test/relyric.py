import re

lyric='[01:23.45]flefdgdf'
m = re.match(r'\[(.+):(.+)\.(.+)\](.+)',lyric)
print(m.group(1))
print(m.group(2))
print(m.group(3))
print(m.group(4))
