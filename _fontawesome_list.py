from os import listdir
from os.path import join
from re import compile

icon = compile(r'id="([a-z\-]+)"')

path = join("public", "sprites")

FILES = list(map(lambda x: join(path, x), listdir(path)))

for f in FILES:
    with open(f, 'r') as file:
        print(f)
        print('enum("' + '", "'.join(icon.findall(file.read())) + '")')
        print()
