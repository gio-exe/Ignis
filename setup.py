import subprocess
import sys
import os

def install_requests():
    try:
        import requests
    except ImportError:
        print("requests package not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])

def write_config(kid, ak, bid, bucket_name):
    content = f"""

KID = '{kid}'
AK = '{ak}'
BID = '{bid}'
BUCKET_NAME = '{bucket_name}'
"""
    with open('config.py', 'w') as f:
        f.write(content)
    print("config.py created with keys and bucket name.")

def main():
    install_requests()
    print("=== Ignis Configuration ===")
    kid = input("Enter your Backblaze Key ID (KID): ").strip()
    ak = input("Enter your Backblaze Application Key (AK): ").strip()
    bid = input("Enter your Backblaze Bucket ID (BID): ").strip()
    bucket_name = input("Enter your Backblaze Bucket Name: ").strip()

    write_config(kid, ak, bid, bucket_name)

    print("\nRunning main.py...\n")
    subprocess.run([sys.executable, 'main.py'])

if __name__ == '__main__':
    main()
