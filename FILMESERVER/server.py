from http.server import HTTPServer
from api.endpoints import MyHandler

def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Servidor rodando em http://localhost:8000')
    httpd.serve_forever()

if __name__ == "__main__":
    main()
