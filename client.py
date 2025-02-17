import socket
import time
import platform
import subprocess
import argparse

def get_clipboard_content():
    commands = {
        "Windows": "powershell Get-Clipboard",
        "Darwin": "pbpaste",
        "Linux": "xclip -o"
    }
    return subprocess.check_output(commands[platform.system()], shell=True).decode('utf-8').strip()

def send_clipboard_content(sock):
    last_content = ""
    while True:
        try:
            current_content = get_clipboard_content()
            if current_content != last_content:
                last_content = current_content
                sock.sendall(current_content.encode('utf-8'))
            time.sleep(1)
        except Exception as e:
            print(f"{e}")
            time.sleep(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str, help='IP Address')
    parser.add_argument('--port', type=int, default=65432, help='(default: 65432)')

    args = parser.parse_args()
    HOST = args.host
    PORT = args.port

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print(f"Connected to {HOST}:{PORT}")
                send_clipboard_content(s)
        except Exception as e:
            print(f"{e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
