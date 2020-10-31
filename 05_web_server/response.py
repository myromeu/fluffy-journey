from document_root import (
    FileNotFound, DirectoryNotFound, EXTENSION_TO_CTYPE
)

from status import STATUS_TO_CODE

class Response:
    def __init__(self, *,  status=405, body=None):
        self.status = status or 405
        self.body = body or ''

    def content_length(self):
        return len(body) if self.body else 0


def create_response(status, headers=None, body=None):
    start = f'HTTP/1.1 {status} {STATUS_TO_CODE[status]}'
    if headers is None:
        headers = {}
    headers.update({'Server': 'little_0.01'})
    if body is None:
        body = ''
    headers['Content-Length'] = len(body)
    response = start + '\r\n' + '\r\n'.join([f'{k}: {str(v)}' for k, v in headers.items()]) + '\r\n\r\n' + str(body) + '\r\n\r\n'
    return response


def empty_handler(*, method=None, request_parser=None, doc_root_helper=None, **kwargs):
    body_content = 'Unsupported method'
    if method:
        body_content = f'Unsupported method `{method}``'
    return Response(body=body_content), {}


def get_handler(*, method=None, request_parser=None, doc_root_helper=None, **kwargs):
    assert request_parser
    assert doc_root_helper
    status = 200
    body_content = None
    headers = {}
    if request_parser.is_file():
        try:
            body_content = doc_root_helper.get_file_content(request_parser.get_path())
            headers['Content-Type'] = EXTENSION_TO_CTYPE[doc_root_helper.extension(request_parser.get_path())]
        except FileNotFound:
            status = 404
            body_content = f'file {request_parser.path} not found'
    elif request_parser.is_dir():
        try:
            body_content = doc_root_helper.get_dir_index_file_content(request_parser.get_path())
        except DirectoryNotFound:
            status = 404
            body_content = f'index.html does not exist in {request_parser.path} directory'
        except FileNotFound as e:
            status = 404
            body_content = str(e)
        except Exception as e:
            print(f'Error is shouted: {e}')
    return Response(status=status, body=body_content), headers


def post_handler(*, method=None, request_parser=None, doc_root_helper=None, **kwargs):
    return Response(body='POST method not implemented'), {}


def head_handler(*, method=None, request_parser=None, doc_root_helper=None, **kwargs):
    return Response(body='HEAD method not implemented'), {}
