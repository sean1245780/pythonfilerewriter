import socket
import PythonHtmlCon

LISTEN_PORT = 8910 # The port

HTML_DATA = {"header": "Welcome to the example!", "color": "red", "txt": "Having fun!",
             "type": "span", "var": False, "var2": False, "n1": False} # You can play around these


def rewrite(data: str, vars: dict = {}):
    edited_file = PythonHtmlCon.DataConnection()
    edited_file = edited_file.edit_variables_data(data, vars)
    return edited_file


def analise_request(request: str):
    if "GET" in request or "POST" in request and "HTTP" in request:
        with open(".\\somehtml.html", "r") as f:
            return "HTTP/1.1 200 OK\nContent-Type: text/html\n\n{}".format(rewrite(f.read(), HTML_DATA)) # Builds the response
    return "HTTP/1.1 404 NOT FOUND\nConnection: close\n\nClosed!"


# To connect to the server please enter to the url of your browser: localhost:port ~ Default is 8910
def main():
    # A server for helping out with the library
    listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("localhost", LISTEN_PORT)
    listening_sock.bind(server_address)

    listening_sock.listen(5)

    while True:
        client_soc, client_address = listening_sock.accept()
        print("Client Connected!")

        client_msg = client_soc.recv(2048).decode()

        client_soc.sendall(analise_request(client_msg).encode())

        client_soc.close()

    listening_sock.close()


if __name__ == '__main__':
    main()
