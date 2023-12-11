from pathlib import Path
from sys import argv
import re

image = ['JPEG', 'PNG', 'JPG', 'SVG']
video = ['AVI', 'MP4', 'MOV', 'MKV']
documents = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
music = ['MP3', 'OGG', 'WAV', 'AMR']
archives = ['ZIP', 'GZ', 'TAR']

my_dict = {}

for img in image:
    my_dict.setdefault(img, 'image')
for vid in video:
    my_dict.setdefault(vid, 'video')
for doc in documents:
    my_dict.setdefault(doc, 'documents')
for mus in music:
    my_dict.setdefault(mus, 'music')
for arc in archives:
    my_dict.setdefault(arc, 'archives')


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

def normalize(name):
    name = name.translate(TRANS)
    name = re.sub('\W', '_', name)

    return name

def move(root_path, path):
    name = path.stem
    file_type = path.suffix

    name_by_file_type = my_dict.get(file_type, 'others')
    new_name = normalize(name)
    path_dir = root_path / name_by_file_type
    path_file = path_dir / new_name

    if not path_dir.exists():
        path_dir.mkdir()

    path.replace(path_file)



def parse_folder(root_path, path):
    print('parse_folder', path)
    for i in path.iterdir():
        if i.is_file():
            move(root_path, i)
        if i.is_dir():
            parse_folder(root_path, i)

def main():
    path = Path(argv[1])
    parse_folder(path, path)
    ...

if __name__ == '__main__':
    main()
