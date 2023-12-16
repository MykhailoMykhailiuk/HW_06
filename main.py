import re
import shutil
import sys
from pathlib import Path


Image = list()
Video = list()
Documents = list()
Music = list()
Archives = list()
Others = list()
Extentions = set()
Unknown_extentions = set()

image = ['JPEG', 'PNG', 'JPG', 'SVG']
video = ['AVI', 'MP4', 'MOV', 'MKV']
documents = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
music = ['MP3', 'OGG', 'WAV', 'AMR']
archives = ['ZIP', 'GZ', 'TAR'] 

folder_list = ['image', 'video', 'documents', 'music', 'archives', 'others']

my_dict = {}

for img in image:
    my_dict.setdefault(img, 'Image')
for vid in video:
    my_dict.setdefault(vid, 'Video')
for doc in documents:
    my_dict.setdefault(doc, 'Documents')
for mus in music:
    my_dict.setdefault(mus, 'Music')
for arc in archives:
    my_dict.setdefault(arc, 'Archives')


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

def normalize(name: str) -> str:
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)

    return f"{new_name}.{'.'.join(extension)}"

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def move_files(root_path, path):
    new_name = normalize(path.name)
    file_type = get_extensions(path)

    new_dir = root_path/my_dict.get(file_type, 'Others')
    new_dir.mkdir(exist_ok=True)
    path.replace(new_dir/new_name)

def move_archives(root_path, path):
    file_type = get_extensions(path)
    new_dir = root_path/my_dict.get(file_type, 'Others')
    new_dir.mkdir(exist_ok=True)


    new_name = normalize(path.name.replace(file_type, ''))
    archive_folder = new_dir/new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

def scan_folder(root_path, path):
    for item in path.iterdir():
        if item.is_dir():
            if item.name not in folder_list:
                scan_folder(root_path, item)

        if item.is_file():
            file_type = item.suffix
            file_type = file_type.replace('.', '').upper()
            if file_type not in archives:
                move_files(root_path, item)
            else:
                move_archives(root_path, item)
            
            extention = get_extensions(file_name=item.name)
            try:
                container = my_dict[extention]
                Extentions.add(extention)
            except KeyError:
                    Unknown_extentions.add(extention)
 
def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass 

def main():
     
    path = Path(sys.argv[1]) 
    scan_folder(path, path)
    remove_empty_folders(path)

    if len(Image) != 0:
        print(f'Image: {Image}')
    if len(Video) != 0:
        print(f'Video: {Video}')
    if len(Documents) != 0:
        print(f'Documents: {Documents}')
    if len(Music) != 0:
        print(f'Music: {Music}')
    if len(Archives) != 0:
        print(f'Archives: {Archives}')
    if len(Others) != 0:
        print(f'Others: {Others}')
    if len(Extentions) != 0:
        print(f'Registered extentions: {Extentions}')
    if len(Unknown_extentions) != 0:
        print(f'Unknown extentions: {Unknown_extentions}')

if __name__ == '__main__':
  
    main()
