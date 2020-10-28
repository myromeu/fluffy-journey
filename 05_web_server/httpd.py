import os
import argparse
import socket
import threading

from document_root import DocumentRootHelper, FileNotFound, DirectoryNotFound
from request import (
    receive_on_socket,
    RequestParser,
    EmptyRecievedError,
    BadVersion,
    BadPath,
    Forbidden,
    BadMethod
)

from response import (
    Response,
    create_response,
    empty_handler,
    get_handler,
    post_handler,
    head_handler
)

from status import STATUS_TO_CODE

HTTP_HANDLERS = {
    'GET': get_handler,
    'POST': post_handler,
    'HEAD': head_handler,
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


def handle_request(client, doc_root_helper):
    response_obj = Response()
    headers = None
    received, length = receive_on_socket(client)
    try:
        request_parser = RequestParser(received.decode())
    except Forbidden as e:
        response_obj = Response(status=403)
    except (EmptyRecievedError, BadMethod, BadPath, BadVersion) as e:
        print('Parse Error:', str(e))
    else:
        print(f'Request: {request_parser.method} {request_parser.path} {request_parser.version}\n')
        handler = HTTP_HANDLERS.get(request_parser.method, empty_handler)

        response_obj, headers = handler(method=request_parser.method,
                                        request_parser=request_parser,
                                        doc_root_helper=doc_root_helper)

    response = create_response(
        status=response_obj.status,
        headers=headers,
        body=response_obj.body
    )
    client.sendall(response.encode())
    client.close()


def run_server(host, port, doc_root_helper):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print('Start listening...')
    requests = 0
    while True:
        # print(f'Running threads {len(threading.enumerate())}')
        c, a = s.accept()
        requests += 1
        print(f'request {requests}')
        handle_request(c, doc_root_helper)
        # thread_handler = threading.Thread(
        #     target=handle_request,
        #     kwargs={'client': c, 'doc_root_helper': doc_root_helper}
        # )
        # # todo: current working threads
        # thread_handler.start()


def main():
    server_args = parse_args()
    document_root_helper = DocumentRootHelper(document_root=os.path.join(BASE_DIR, server_args.document_root))
    run_server(host=server_args.host, port=server_args.port, doc_root_helper=document_root_helper)


if __name__ == '__main__':
    main()
