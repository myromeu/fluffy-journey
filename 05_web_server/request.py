class ParserError(Exception):
    pass


class BadMethod(ParserError):
    pass


class BadPath(ParserError):
    pass


class BadVersion(ParserError):
    pass


class Parser:
    def __init__(self, received: bytes):
        self._source = received
        lines = received.split('\n')
        head_line = lines[0].split()
        self.method = head_line[0].strip()
        self.path = head_line[1].strip()
        self.version = head_line[2].strip()
        self.headers = lines[1:]
        if not self.method:
            raise BadMethod(f'bad method: {self.method}')
        if not self.path:
            raise BadPath(f'bad path: {self.path}')
        if not self.version:
            raise BadVersion(f'bad version: {self.version}')

    def _ends_with_slash(self):
        if not self.path.endswith('/'):
            return False
        else:
            return True

    def is_file(self):
        if not self.path.startswith('/'):
            raise ValueError('path must starts with `/`')
        return not self._ends_with_slash()

    def is_dir(self):
        if not self.path.startswith('/'):
            raise ValueError('path must starts with `/`')
        return self._ends_with_slash()

    def get_path(self):
        # todo избавиться
        return self.path[1:]


def receive_on_socket(sock):
    chunks = []
    bytes_recd = 0
    while True:
        chunk = sock.recv(2048)
        if chunk == b'':
            break
        chunks.append(chunk)
        bytes_recd += len(chunk)
    return b''.join(chunks), bytes_recd
