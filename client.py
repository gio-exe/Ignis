import os
import requests
import hashlib
from urllib.parse import quote

class UploadProgress:
    def __init__(self, fileobj, filesize, progress_callback):
        self.fileobj = fileobj
        self.filesize = filesize
        self.progress_callback = progress_callback
        self.read_bytes = 0

    def read(self, size=-1):
        data = self.fileobj.read(size)
        if data:
            self.read_bytes += len(data)
            self.progress_callback(self.read_bytes, self.filesize)
        return data

class B2:
    def __init__(self, kid, ak, bid, bucket_name):
        self.kid = kid
        self.ak = ak
        self.bid = bid
        self.bucket_name = bucket_name
        self.au = None
        self.du = None
        self.tk = None

    def auth(self):
        r = requests.get(
            "https://api.backblazeb2.com/b2api/v2/b2_authorize_account",
            auth=(self.kid, self.ak)
        )
        r.raise_for_status()
        d = r.json()
        self.au = d['apiUrl']
        self.du = d['downloadUrl']
        self.tk = d['authorizationToken']

    def get_upload_url(self):
        r = requests.post(
            f"{self.au}/b2api/v2/b2_get_upload_url",
            headers={'Authorization': self.tk},
            json={'bucketId': self.bid}
        )
        r.raise_for_status()
        return r.json()

    def sha1(self, data):
        h = hashlib.sha1()
        h.update(data)
        return h.hexdigest()

    def upload(self, filepath, progress_callback=None):
        filesize = os.path.getsize(filepath)
        with open(filepath, 'rb') as f:
            data_for_hash = f.read()
            sha1_hash = self.sha1(data_for_hash)

        upload_info = self.get_upload_url()
        raw_filename = os.path.basename(filepath)
        encoded_filename = quote(raw_filename, safe='')

        headers = {
            'Authorization': upload_info['authorizationToken'],
            'X-Bz-File-Name': encoded_filename,
            'Content-Type': 'b2/x-auto',
            'X-Bz-Content-Sha1': sha1_hash,
            'Content-Length': str(filesize),
        }

        with open(filepath, 'rb') as f:
            data_to_send = UploadProgress(f, filesize, progress_callback) if progress_callback else f
            r = requests.post(
                upload_info['uploadUrl'],
                headers=headers,
                data=data_to_send
            )
        r.raise_for_status()
        return r.json()

    def list_files(self, max_files=100):
        r = requests.post(
            f"{self.au}/b2api/v2/b2_list_file_versions",
            headers={'Authorization': self.tk},
            json={'bucketId': self.bid, 'maxFileCount': max_files}
        )
        r.raise_for_status()
        return r.json().get('files', [])

    def download(self, filename, dest_path):
        files = self.list_files(1000)
        file_info = next((f for f in files if f['fileName'] == filename), None)
        if not file_info:
            raise FileNotFoundError(f"File '{filename}' not found.")
        url = f"{self.du}/file/{self.bucket_name}/{filename}"
        r = requests.get(url, headers={'Authorization': self.tk}, stream=True)
        r.raise_for_status()
        os.makedirs(os.path.dirname(dest_path) or '.', exist_ok=True)
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return dest_path

    def delete(self, filename):
        files = self.list_files(1000)
        file_info = next((f for f in files if f['fileName'] == filename), None)
        if not file_info:
            raise FileNotFoundError(f"File '{filename}' not found for deletion.")
        r = requests.post(
            f"{self.au}/b2api/v2/b2_delete_file_version",
            headers={'Authorization': self.tk},
            json={'fileName': file_info['fileName'], 'fileId': file_info['fileId']}
        )
        r.raise_for_status()
        return r.json()
