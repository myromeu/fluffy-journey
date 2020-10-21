import os


class NotFound(Exception):
    pass


class FileNotFound(NotFound):
    pass


class DirectoryNotFound(NotFound):
    pass


class DocumentRootHelper:
    def __init__(self, document_root: str):
        self.document_root = document_root

    def get_file_content(self, file_path):
        full_path = os.path.join(self.document_root, file_path)
        if not os.path.isfile(full_path):
            raise FileNotFound(f'file {file_path} not found')
        with open(full_path) as f:
            return f.read()

    def get_dir_index_file_content(self, dir_path):
        full_dir_path = os.path.join(self.document_root, dir_path)
        if not os.path.isdir(full_dir_path):
            raise DirectoryNotFound(f'dir {full_dir_path} not found')

        full_path = os.path.join(full_dir_path, 'index.html')
        if not os.path.isfile(full_path):
            raise NotImplementedError('need list dir contents here')
        with open(full_path) as f:
            return f.read()
