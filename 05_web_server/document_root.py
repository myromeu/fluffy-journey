import os


BINARY_FILES_EXTENSIONS = ['gif', 'jpeg', 'jpg', 'png', 'swf']


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
        encoded_path = path.replace("%20"," ")
        return os.path.join(self.document_root, encoded_path)

    def get_file_content(self, file_path):
        full_path = self._encoded_path(file_path)
        try:
            ext = full_path.rsplit(sep='.', maxsplit=1)[-1]
        except IndexError:
            ext = ''
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
            raise NotImplementedError('need list dir contents here')
        with open(full_path) as f:
            return f.read()
