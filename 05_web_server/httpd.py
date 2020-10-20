import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='workers', type=int, help='count of workers')
    parser.add_argument('-r', dest='document_root', type=str, help='path to DOCUMENT_ROOT')
    parser.add_argument('-H', dest='host', type=str, help='host', default='localhost')
    parser.add_argument('-p', dest='port', type=str, help='port', default='8080')
    args = parser.parse_args()
    print(args.__dict__)
    return args


def main():
    server_args = parse_args()
    run_server()


if __name__ == '__main__':
    main()
