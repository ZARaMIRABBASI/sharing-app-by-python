import socket
import os

def start_server(host='0.0.0.0', port=5001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        
        filename = client_socket.recv(1024).decode()
        if os.path.exists(filename):
            client_socket.send(b'EXISTS ' + str(os.path.getsize(filename)).encode())
            user_response = client_socket.recv(1024).decode()
            if user_response == 'GET':
                with open(filename, 'rb') as f:
                    bytes_to_send = f.read(1024)
                    while bytes_to_send:
                        client_socket.send(bytes_to_send)
                        bytes_to_send = f.read(1024)
                print("File transfer complete.")
        else:
            client_socket.send(b'ERR')

        client_socket.close()

if __name__ == "__main__":
    start_server()
