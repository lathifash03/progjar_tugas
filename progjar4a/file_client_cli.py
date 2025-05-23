import socket
import json
import base64
import logging
import argparse

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)

def send_command(command_str, server_address, timeout=10):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect(server_address)
            logging.info(f"Mengirim perintah: {command_str[:50]}...")  # Log potongan perintah
            sock.sendall(command_str.encode())
            
            data_received = ""
            while True:
                data = sock.recv(8192)  # Buffer lebih besar untuk file besar
                if not data:
                    break
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            
            return json.loads(data_received)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"status": "ERROR", "data": str(e)}

def remote_list(server_address):
    response = send_command("LIST", server_address)
    if response['status'] == 'OK':
        print("\nDaftar file di server:")
        for file in response['data']:
            print(f"- {file}")
    else:
        print(f"\nError: {response['data']}")

def remote_get(filename, server_address):
    response = send_command(f"GET {filename}", server_address)
    if response['status'] == 'OK':
        try:
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(response['data_file']))
            print(f"\nFile '{filename}' berhasil didownload.")
        except Exception as e:
            print(f"\nError menyimpan file: {str(e)}")
    else:
        print(f"\nError: {response['data']}")

def remote_upload(filename, server_address):
    try:
        with open(filename, 'rb') as f:
            file_data = base64.b64encode(f.read()).decode()
        response = send_command(f"UPLOAD {filename} {file_data}", server_address)
        if response['status'] == 'OK':
            print(f"\n{response['data']}")
        else:
            print(f"\nError: {response['data']}")
    except FileNotFoundError:
        print(f"\nError: File '{filename}' tidak ditemukan di lokal.")
    except Exception as e:
        print(f"\nError: {str(e)}")

def remote_delete(filename, server_address):
    response = send_command(f"DELETE {filename}", server_address)
    if response['status'] == 'OK':
        print(f"\n{response['data']}")
    else:
        print(f"\nError: {response['data']}")

def main():
    parser = argparse.ArgumentParser(description="File Client CLI")
    parser.add_argument('--host', default='172.16.16.101', help="Alamat IP server")
    parser.add_argument('--port', type=int, default=7777, help="Port server")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subcommand: list
    list_parser = subparsers.add_parser('list', help='List file di server')

    # Subcommand: get
    get_parser = subparsers.add_parser('get', help='Download file dari server')
    get_parser.add_argument('filename', help='Nama file yang akan didownload')

    # Subcommand: upload
    upload_parser = subparsers.add_parser('upload', help='Upload file ke server')
    upload_parser.add_argument('filename', help='Nama file yang akan diupload')

    # Subcommand: delete
    delete_parser = subparsers.add_parser('delete', help='Hapus file di server')
    delete_parser.add_argument('filename', help='Nama file yang akan dihapus')

    args = parser.parse_args()
    server_address = (args.host, args.port)

    if args.command == 'list':
        remote_list(server_address)
    elif args.command == 'get':
        remote_get(args.filename, server_address)
    elif args.command == 'upload':
        remote_upload(args.filename, server_address)
    elif args.command == 'delete':
        remote_delete(args.filename, server_address)

if __name__ == '__main__':
    main()

    # List file
# python file_client_cli.py list --host 172.16.16.101 --port 7777

# Download file
# python file_client_cli.py get donalbebek.jpg --host 172.16.16.101

# Upload file
# python file_client_cli.py upload tugas3.txt --port 7777

# Delete file
# python file_client_cli.py delete tugas3.txt
