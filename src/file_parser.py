import sys
from pathlib import Path

JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []

AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []

DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []

MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []

ARCHIVES = []

OTHER = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    # повертаємо розширення (без крапки) від name в верхньому регістрі
    return Path(name).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():  # ітеруємось по папкам
        # обробка папок і наповнення списку папок
        if item.is_dir():
            if item.name not in ('images', 'documents', 'audio', 'video', 'archives', 'OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        # обробка файлів і наповнення списків файлів
        # отримуємо розширення файлу використовуючи функцію get_extension
        extension = get_extension(item.name)
        full_name = folder / item.name  # повний шлях до файлу
        if not extension:
            OTHER.append(full_name)
        else:
            try:
                REGISTER_EXTENSION[extension].append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                OTHER.append(full_name)


if __name__ == '__main__':
    folder_process = sys.argv[1]
    scan(Path(folder_process))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images png: {PNG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')
    print(f'Video avi: {AVI_VIDEO}')
    print(f'Video mp4: {MP4_VIDEO}')
    print(f'Video mov: {MOV_VIDEO}')
    print(f'Video mkv: {MKV_VIDEO}')
    print(f'Documnets doc: {DOC_DOCUMENTS}')
    print(f'Documnets docx: {DOCX_DOCUMENTS}')
    print(f'Documnets txt: {TXT_DOCUMENTS}')
    print(f'Documnets pdf: {PDF_DOCUMENTS}')
    print(f'Documnets xlsx: {XLSX_DOCUMENTS}')
    print(f'Documnets pptx: {PPTX_DOCUMENTS}')
    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Audio ogg: {OGG_AUDIO}')
    print(f'Audio wav: {WAV_AUDIO}')
    print(f'Audio amr: {AMR_AUDIO}')
    print(f'Archives: {ARCHIVES}')

    print(f'Extensions: {EXTENSIONS}')
    print(f'Unknown: {UNKNOWN}')
