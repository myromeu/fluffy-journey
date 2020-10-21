import os
import argparse
import socket

from document_root import DocumentRootHelper, FileNotFound, DirectoryNotFound
from request import receive_on_socket, Parser, BadVersion, BadPath, BadMethod

STATUS_TO_CODE = {
    200: 'OK',
    404: 'Not Found',
}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='workers', type=int, help='count of workers')
    parser.add_argument('-r', dest='document_root', type=str, help='path to DOCUMENT_ROOT')
    parser.add_argument('-H', dest='host', type=str, help='host', default='localhost')
    parser.add_argument('-p', dest='port', type=int, help='port', default=8080)
    args = parser.parse_args()
    print(args.__dict__)
    return args


def create_response(status, headers=None, body=None):
    start = f'HTTP/1.1 {status} {STATUS_TO_CODE[status]}'
    if headers is None:
        headers = {}
    headers.update({'Server': 'little_0.01'})
    if body is None:
        body = ''
    response = start + '\r\n' + '\r\n'.join([f'{k}: {v}' for k, v in headers.items()]) + '\r\n\r\n' + body + '\r\n\r\n'
    return response


def handle_request(client, doc_root_helper):
    status = 200
    body_content = None
    received, length = receive_on_socket(client)
    try:
        request_parser = Parser(received.decode())
    except (BadMethod, BadPath, BadVersion) as e:
        print('Parse Error:', str(e))
    else:
        print(f'Request: {request_parser.method} {request_parser.path} {request_parser.version}\n')

        if request_parser.is_file():
            try:
                body_content = doc_root_helper.get_file_content(request_parser.get_path())
            except FileNotFound:
                status = 404
                body_content = f'file {request_parser.path} not found'
        elif request_parser.is_dir():
            try:
                body_content = doc_root_helper.get_dir_index_file_content(request_parser.get_path())
            except DirectoryNotFound:
                status = 404
                body_content = f'index.html does not exist in {request_parser.path} directory'
            except Exception as e:
                print(f'Error is shouted: {e}')

    response = create_response(
        status=status,
        headers={'Content-Length': len(body_content)},
        body=body_content
    )
    client.sendall(response.encode())


def run_server(host, port, doc_root_helper):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print('Strart listening...')
    while True:
        c, a = s.accept()
        print(f'Connection from {a}')
        handle_request(client=c, doc_root_helper=doc_root_helper)
        c.close()


def main():
    server_args = parse_args()
    document_root_helper = DocumentRootHelper(document_root=os.path.join(BASE_DIR, server_args.document_root))
    run_server(host=server_args.host, port=server_args.port, doc_root_helper=document_root_helper)


if __name__ == '__main__':
    print(BASE_DIR)
    main()
