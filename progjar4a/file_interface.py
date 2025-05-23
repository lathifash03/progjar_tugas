import os
import base64
from glob import glob
from mimetypes import guess_type

class FileInterface:
    def __init__(self):
        # Pastikan folder 'files' ada
        if not os.path.exists('files'):
            os.makedirs('files')
        os.chdir('files/')

    def list(self, params=[]):
        try:
            files = []
            for filename in glob('*.*'):
                mime_type, _ = guess_type(filename)
                files.append({
                    'name': filename,
                    'type': mime_type or 'application/octet-stream'
                })
            return {'status': 'OK', 'data': files}
        except Exception as e:
            return {'status': 'ERROR', 'data': str(e)}

    def get(self, params=[]):
        try:
            filename = params[0]
            if not os.path.exists(filename):
                return {'status': 'ERROR', 'data': 'File not found'}

            mime_type, _ = guess_type(filename)
            
            with open(filename, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                'status': 'OK',
                'data_namafile': filename,
                'data_file': file_data,
                'data_type': mime_type or 'application/octet-stream'
            }
        except Exception as e:
            return {'status': 'ERROR', 'data': str(e)}

    def upload(self, params=[]):
        try:
            if len(params) < 2:
                return {'status': 'ERROR', 'data': 'Missing parameters'}

            filename = params[0]
            file_data = params[1]

            # Validasi base64
            try:
                if len(file_data) % 4 != 0:
                    file_data += '=' * (4 - len(file_data) % 4)
                decoded_data = base64.b64decode(file_data)
            except Exception:
                return {'status': 'ERROR', 'data': 'Invalid base64 data'}

            with open(filename, 'wb') as f:
                f.write(decoded_data)

            mime_type, _ = guess_type(filename)
            
            return {
                'status': 'OK',
                'data_namafile': filename,
                'data_type': mime_type or 'application/octet-stream',
                'data': f'File {filename} uploaded successfully'
            }
        except Exception as e:
            return {'status': 'ERROR', 'data': str(e)}

    def delete(self, params=[]):
        try:
            filename = params[0]
            if not os.path.exists(filename):
                return {'status': 'ERROR', 'data': 'File not found'}

            os.remove(filename)
            return {
                'status': 'OK',
                'data_namafile': filename,
                'data': f'File {filename} deleted successfully'
            }
        except Exception as e:
            return {'status': 'ERROR', 'data': str(e)}

if __name__ == '__main__':
    fi = FileInterface()
    
    print("=== Daftar File ===")
    print(fi.list())
    
    print("\n=== Get File (donalbebek.jpg) ===")
    print(fi.get(['donalbebek.jpg']))
    
    print("\n=== Get File (rfc2616.pdf) ===")
    print(fi.get(['rfc2616.pdf']))
    
    print("\n=== Upload Test ===")
    # Contoh upload file text
    test_data = base64.b64encode(b'This is a test file').decode('utf-8')
    print(fi.upload(['test.txt', test_data]))
    
    print("\n=== Delete Test ===")
    print(fi.delete(['test.txt']))