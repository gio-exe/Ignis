import os
import sys
import tempfile
from client import B2
import config

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_progress(uploaded, total):
    percent = uploaded / total * 100
    bar_len = 40
    filled_len = int(bar_len * uploaded // total)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write(f"\rUploading.. [{bar}] {percent:6.2f}%")
    sys.stdout.flush()
    if uploaded == total:
        print()

def main():
    clear_screen()
    print("\n-- Ignis --")

    c = B2(config.KID, config.AK, config.BID, config.BUCKET_NAME)
    try:
        c.auth()
    except Exception as e:
        print(f"Auth error: {e}")
        return

    files = []

    while True:
        print("\n1.Upload\n2.List\n3.Download\n4.Delete\n5.View\n6.Exit")
        choice = input("> ")

        if choice == '1':
            path = input("File path: ")
            if not os.path.exists(path):
                print("File not found.")
                continue
            try:
                resp = c.upload(path, progress_callback=print_progress)
                print(f"Uploaded {os.path.basename(path)}")
            except Exception as e:
                print(f"\nUpload error: {e}")

        elif choice == '2':
            try:
                files = c.list_files()
                if not files:
                    print("\nNo files found.\n")
                    continue
                print("\nFiles:")
                for i, f in enumerate(files):
                    print(f"ID#{i}: {f['fileName']} ({f['contentLength']} bytes)")
            except Exception as e:
                print(f"List error: {e}")

        elif choice == '3':
            if not files:
                print("Files not yet listed.")
                continue
            try:
                file_id_str = input("File ID to download: ")
                file_id = int(file_id_str)
                if file_id < 0 or file_id >= len(files):
                    print("Invalid file ID.")
                    continue
                fname = files[file_id]['fileName']
                folder = input("Folder path to download into (default current dir): ") or '.'
                dest = os.path.join(folder, fname)
                c.download(fname, dest)
                print(f"Downloaded '{fname}' to {dest}")
            except ValueError:
                print("Invalid input. Please enter a valid file ID.")
            except Exception as e:
                print(f"Download error: {e}")

        elif choice == '4':
            if not files:
                print("Files not yet listed.")
                continue
            try:
                file_id_str = input("File ID to delete: ")
                file_id = int(file_id_str)
                if file_id < 0 or file_id >= len(files):
                    print("Invalid file ID.")
                    continue
                fname = files[file_id]['fileName']
                c.delete(fname)
                print(f"Deleted '{fname}'")
                files.pop(file_id)
            except ValueError:
                print("Invalid input. Please enter a valid file ID.")
            except Exception as e:
                print(f"Delete error: {e}")

        elif choice == '5':
            if not files:
                print("Files not yet listed.")
                continue
            try:
                file_id_str = input("File ID to view: ")
                file_id = int(file_id_str)
                if file_id < 0 or file_id >= len(files):
                    print("Invalid file ID.")
                    continue
                fname = files[file_id]['fileName']
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp_path = tmp.name
                c.download(fname, tmp_path)
                print("\n------ FILE CONTENT START ------\n")
                with open(tmp_path, 'r', encoding='utf-8', errors='replace') as f:
                    print(f.read())
                print("\n------- FILE CONTENT END -------\n")
                os.unlink(tmp_path)
            except ValueError:
                print("Invalid input. Please enter a valid file ID.")
            except Exception as e:
                print(f"View error: {e}")

        elif choice == '6':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()
