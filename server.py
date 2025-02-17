import socket
import platform
import subprocess
import argparse

def get_local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
    finally:
        sock.close()
    return local_ip

def set_clipboard_content(content):
    commands = {
        "Windows": "powershell Set-Clipboard",
        "Darwin": "pbcopy",
        "Linux": "xclip -selection clipboard"
    }
    subprocess.run(commands[platform.system()], input=content, text=True, shell=True)

def receive_clipboard_content(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            content = data.decode('utf-8')
            set_clipboard_content(content)
        except Exception as e:
            print(f"{e}")
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=65432, help='(default: 65432)')

    args = parser.parse_args()
    HOST = get_local_ip()
    PORT = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")

        while True:
            try:
                conn, addr = s.accept()
                print(f"Connection from {addr}")
                receive_clipboard_content(conn)
            except Exception as e:
                print(f"{e}")

if __name__ == "__main__":
    main()
