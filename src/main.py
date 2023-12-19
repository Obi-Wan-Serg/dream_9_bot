from pathlib import Path
import shutil
import sys
import file_parser
from normalize import normalize

def handle_files(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True) # створення папки для файлів
    file_name.replace(target_folder / normalize(file_name.name)) # переміщення файлів в створену папку

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True) # створення папки для файлів
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, '')) # створення шляху до папки для розпакованих файлів
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute())) # розпаковка архіву по вказаному шляху
    except shutil.ReadError:
        folder_for_file.rmdir() # видалення папки якщо розпаковка архіву призвела до помилки ReadError
        return
    file_name.unlink() # видалення початкового файлу архіву

def main(folder: Path):
    file_parser.scan(folder)
    for file in file_parser.JPEG_IMAGES:
        handle_files(file, folder / 'images' / 'JPEG')
    for file in file_parser.PNG_IMAGES:
        handle_files(file, folder / 'images' / 'PNG')
    for file in file_parser.JPG_IMAGES:
        handle_files(file, folder / 'images' / 'JPG')
    for file in file_parser.SVG_IMAGES:
        handle_files(file, folder / 'images' / 'SVG')
    for file in file_parser.AVI_VIDEO:
        handle_files(file, folder / 'video' / 'AVI')
    for file in file_parser.MP4_VIDEO:
        handle_files(file, folder / 'video' / 'MP4')
    for file in file_parser.MOV_VIDEO:
        handle_files(file, folder / 'video' / 'MOV')
    for file in file_parser.MKV_VIDEO:
        handle_files(file, folder / 'video' / 'MKV')
    for file in file_parser.DOC_DOCUMENTS:
        handle_files(file, folder / 'documents' / 'DOC')
    for file in file_parser.DOCX_DOCUMENTS:
        handle_files(file, folder / 'documents' / 'DOCX')
    for file in file_parser.TXT_DOCUMENTS:
        handle_files(file, folder / 'documents' / 'TXT')
    for file in file_parser.PDF_DOCUMENTS:
        handle_files(file, folder / 'documents' / 'PDF')
    for file in file_parser.XLSX_DOCUMENTS:
        handle_files(file, folder / 'documents' / 'XLSX')
    for file in file_parser.PPTX_DOCUMENTS:
        handle_files(file, folder / 'documents' / 'PPTX')
    for file in file_parser.MP3_AUDIO:
        handle_files(file, folder / 'audio' / 'MP3')
    for file in file_parser.OGG_AUDIO:
        handle_files(file, folder / 'audio' / 'OGG')
    for file in file_parser.WAV_AUDIO:
        handle_files(file, folder / 'audio' / 'WAV')
    for file in file_parser.AMR_AUDIO:
        handle_files(file, folder / 'audio' / 'AMR')
    for file in file_parser.OTHER:
        handle_files(file, folder / 'OTHER')

    for file in file_parser.ARCHIVES:
        handle_archive(file, folder / 'archives' / 'ARCHIVES')

    for folder in file_parser.FOLDERS[::-1]:
        # видалення пустих папок після сортування
        try:
            folder.rmdir()
        except OSError:
            print(f'Error while deleting the folder {folder}')


if __name__ == '__main__':
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())