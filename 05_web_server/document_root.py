import os
import urllib.parse


BINARY_FILES_EXTENSIONS = ['.gif', '.jpeg', '.jpg', '.png', '.swf']

EXTENSION_TO_CTYPE = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.gif': 'image/gif',
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.swf': 'application/x-shockwave-flash',
    '.txt': 'text/plain',
    '': '',
}


class NotFound(Exception):
    pass


class FileNotFound(NotFound):
    pass


class DirectoryNotFound(NotFound):
    pass


class DocumentRootHelper:
    def __init__(self, document_root: str):
        self.document_root = document_root
    
    def _encoded_path(self, path):
        encoded_path = urllib.parse.unquote(path)
        return os.path.join(self.document_root, encoded_path)
    
    def extension(self, full_path):
        ext = ''
        try:
            _, ext = os.path.splitext(full_path)
        except IndexError:
            ...
        return ext

    def get_file_content(self, file_path):
        full_path = self._encoded_path(file_path)
        ext = self.extension(full_path)
        mode = 'rt'
        if ext in BINARY_FILES_EXTENSIONS:
            mode = 'rb'
        if not os.path.isfile(full_path):
            raise FileNotFound(f'file {file_path} not found')
        with open(full_path, mode=mode) as f:
            return f.read()

    def get_dir_index_file_content(self, dir_path):
        full_dir_path = self._encoded_path(dir_path)
        if not os.path.isdir(full_dir_path):
            raise DirectoryNotFound(f'dir {full_dir_path} not found')

        full_path = os.path.join(full_dir_path, 'index.html')
        if not os.path.isfile(full_path):
            raise FileNotFound(f'index file absent in directory {dir_path}')
        with open(full_path) as f:
            return f.read()
