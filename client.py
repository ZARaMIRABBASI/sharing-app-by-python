import socket
from tkinter import Tk, Button, Label, filedialog

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        filename = file_path.split('/')[-1]
        send_file(file_path, filename)

def send_file(file_path, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Enter the server IP address: ")  # آدرس IP سرور را وارد کنید
    server_port = 5001  # پورت سرور

    try:
        client_socket.connect((server_ip, server_port))
        client_socket.send(filename.encode())

        response = client_socket.recv(1024).decode()
        if response.startswith('EXISTS'):
            filesize = response.split()[1]
            print(f"File exists, size: {filesize} bytes.")
            client_socket.send(b'GET')

            with open(file_path, 'rb') as f:
                bytes_to_send = f.read(1024)
                while bytes_to_send:
                    client_socket.send(bytes_to_send)
                    bytes_to_send = f.read(1024)
            print("File sent successfully.")
        else:
            print("File does not exist on the server.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client_socket.close()

def main():
    root = Tk()
    root.title("File Sharing Client")

    Label(root, text="Select a file to send:").pack(pady=10)
    Button(root, text="Browse", command=select_file).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
