class ParserError(Exception):
    pass


class EmptyRecievedError(ParserError):
    pass


class BadMethod(ParserError):
    pass


class BadPath(ParserError):
    pass


class Forbidden(BadPath):
    pass


class BadVersion(ParserError):
    pass


class RequestParser:
    def __init__(self, received: str):
        self._source = received
        lines = received.split('\n')
        head_line = lines[0].split()
        if not self._source or not head_line:
            raise EmptyRecievedError('empty recieved')
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

        if '../' in self.path:
            raise Forbidden(f'document root escaping forbidden: {self.path}')

        self.query_string = ''
        try:
            end_of_path = self.path.rsplit(sep='/', maxsplit=1)[-1]
        except IndexError:
            pass
        else:
            if '?' in end_of_path:
                splited = self.path.rsplit(sep='?')
                self.path = splited[0]
                self.query_string = splited[1:]

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
    _chunk_size = 1024
    chunks = []
    bytes_recd = 0
    while True:
        chunk = sock.recv(_chunk_size)
        chunks.append(chunk)
        bytes_recd += len(chunk)
        if chunk == b'' or chunk.endswith(b'\r\n\r\n'):
            break
    return b''.join(chunks), bytes_recd
