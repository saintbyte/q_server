import argparse
import socket
import time

NEW_LINE = "\n"


def get_command_line_arguments():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--host", help="host to connect")
    parser.add_argument("--request", help="request")
    parser.add_argument("--command", default="", help="command")
    parser.add_argument("--data", help="data")
    parser.add_argument("--wait", type=bool, default=False, help="wait for result")
    args = parser.parse_args()
    if not any([args.request, args.host, args.data]):
        parser.print_help()
        quit()
    return args


def get_port(src):
    if ":" in src:
        return int(src.split(":")[1])
    return 1234


def get_host(src):
    if ":" in src:
        return src.split(":")[0]
    return src


def get_socket_data_for_send(request, command, data):
    return f"{request}{NEW_LINE}{command}{data}{NEW_LINE}".encode()


def main():
    args = get_command_line_arguments()
    sock = socket.socket()
    sock.connect((get_host(args.host), get_port(args.host)))
    sock.send(get_socket_data_for_send(args.request, args.command, args.data))
    task_id = sock.recv(1024)
    task_id = task_id.strip()
    print(task_id.decode("utf-8") + NEW_LINE)
    cnt = 0
    max_wait = 40
    if args.wait:
        while True:
            sock.send(get_socket_data_for_send("STATUS", task_id))
            cnt = cnt + 1
            if cnt > max_wait:
                print("reached max ")
                break
            time.sleep(1)
    sock.close()


if __name__ == "__main__":
    main()
