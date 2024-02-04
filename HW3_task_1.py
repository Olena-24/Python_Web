import os
import shutil
import re
import sys
from pathlib import Path
from threading import Thread
from queue import Queue

# Константы для перевода кириллицы в латиницу
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {ord(cyrillic): latin for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION)}

def normalize(name: str) -> str:
    parts = name.split('.')
    base_name = parts[0]
    extension = ".".join(parts[1:])
    base_name = re.sub(r'\W', '_', base_name.translate(TRANS))
    if extension:
        return f"{base_name}.{extension}"
    return base_name

def get_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()

def process_file(item_path, extensions, destination):
    extension = get_extension(item_path).lstrip('.')
    found_category = None
    for category, ext_list in extensions.items():
        if extension in ext_list:
            found_category = category
            break
    if found_category:
        dest_folder = os.path.join(destination, found_category)
    else:
        dest_folder = os.path.join(destination, 'UNKNOWN')
    os.makedirs(dest_folder, exist_ok=True)
    new_file_name = normalize(os.path.basename(item_path))
    shutil.move(item_path, os.path.join(dest_folder, new_file_name))

def process_directory(queue, extensions, destination):
    while not queue.empty():
        current_path = queue.get()
        for file in os.listdir(current_path):
            item_path = os.path.join(current_path, file)
            if os.path.isdir(item_path):
                queue.put(item_path)
            else:
                process_file(item_path, extensions, destination)
        queue.task_done()

def remove_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except OSError:
                pass 

def main(folder_process):
    extensions = {
        'video': ['mp4', 'mov', 'avi', 'mkv'],
        'audio': ['mp3', 'ogg', 'wav', 'amr'],
        'image': ['jpg', 'png', 'jpeg', 'svg'],
        'archive': ['zip', 'rar', 'gz'],
        'text': ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'pptx'],
    }
    destination = folder_process 

    file_queue = Queue()
    file_queue.put(folder_process)

    threads = []
    for _ in range(5):  # Количество потоков
        t = Thread(target=process_directory, args=(file_queue, extensions, destination))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    remove_empty_folders(folder_process) 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Укажите имя папки!")
        sys.exit()

    folder_process = Path(sys.argv[1]).resolve()
    main(folder_process)
