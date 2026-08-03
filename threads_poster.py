import os
import json
import urllib.request
import urllib.parse

def load_env(env_path='.env'):
    """Simple parser to load .env file into os.environ"""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

class ThreadsAPI:
    def __init__(self, access_token=None, user_id=None, app_id=None, app_secret=None):
        load_env()
        self.app_id = app_id or os.getenv('THREADS_APP_ID')
        self.app_secret = app_secret or os.getenv('THREADS_APP_SECRET')
        self.access_token = access_token or os.getenv('THREADS_ACCESS_TOKEN')
        self.user_id = user_id or os.getenv('THREADS_USER_ID', 'me')
        self.base_url = "https://graph.threads.net/v1.0"

    def verify_token(self):
        """Test if the Threads access token is valid and active"""
        if not self.access_token or self.access_token == "your_threads_access_token_here":
            print("[-] THREADS_ACCESS_TOKEN belum diisi di file .env")
            if self.app_id and self.app_secret:
                print(f"[i] App ID: {self.app_id}")
                print(f"[i] App Secret: {self.app_secret[:4]}***{self.app_secret[-4:]}")
                print("\n[!] PERHATIAN: App Secret (Rahasia Aplikasi) BUKAN Access Token pengguna!")
                print("[!] Untuk mengirim postingan ke Threads API, Anda membutuhkan 'User Access Token'.")
            return False, "Token belum diisi"

        url = f"{self.base_url}/me?fields=id,username,name,threads_profile_picture_url&access_token={urllib.parse.quote(self.access_token)}"
        req = urllib.request.Request(url, method='GET')

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"[+] Token VALID!")
                print(f"    User ID : {result.get('id')}")
                print(f"    Username: @{result.get('username')}")
                if result.get('name'):
                    print(f"    Nama    : {result.get('name')}")
                return True, result
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            try:
                err_json = json.loads(err_body)
                err_msg = err_json.get('error', {}).get('message', err_body)
            except Exception:
                err_msg = err_body
            print(f"[-] Token INVALID atau GAGAL! (HTTP Status {e.code})")
            print(f"    Detail Error: {err_msg}")
            return False, err_msg
        except Exception as e:
            print(f"[-] Terjadi kesalahan koneksi: {str(e)}")
            return False, str(e)

    def create_container(self, text, media_type="TEXT", image_url=None):
        """Step 1: Create a Threads post container"""
        if not self.access_token:
            raise ValueError("Threads Access Token is missing. Please set THREADS_ACCESS_TOKEN in .env")

        url = f"{self.base_url}/{self.user_id}/threads"
        data = {
            'media_type': media_type,
            'text': text,
            'access_token': self.access_token
        }
        if media_type == "IMAGE" and image_url:
            data['image_url'] = image_url

        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data=encoded_data, method='POST')

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('id')
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            print(f"Error creating container: {err_body}")
            return None

    def publish_container(self, creation_id):
        """Step 2: Publish the created Threads container"""
        if not creation_id:
            return None

        url = f"{self.base_url}/{self.user_id}/threads_publish"
        data = {
            'creation_id': creation_id,
            'access_token': self.access_token
        }

        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data=encoded_data, method='POST')

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('id')
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            print(f"Error publishing container: {err_body}")
            return None

    def post_text(self, text):
        """Post simple text/link post to Threads"""
        print("Creating Threads post container...")
        creation_id = self.create_container(text=text, media_type="TEXT")
        if creation_id:
            print(f"Container created ID: {creation_id}. Publishing...")
            post_id = self.publish_container(creation_id)
            if post_id:
                print(f"Successfully published post to Threads! Post ID: {post_id}")
                return post_id
        return None

if __name__ == '__main__':
    import sys
    print("=== Testing Threads API Access Token ===")
    token_input = sys.argv[1] if len(sys.argv) > 1 else None
    api = ThreadsAPI(access_token=token_input)
    api.verify_token()
