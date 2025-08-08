<h1 align="center">Ignis</h1>
<p align="center">
  <img width="459" height="395" alt="2-removebg-preview" src="https://github.com/user-attachments/assets/174650c5-4561-42ab-8775-ad843d6a186e" />
</p>
Ignis is a lightweight and easy to use command line tool that makes managing Backblaze B2 cloud storage simpler. Since the official Backblaze CLI can be harder to install and use, Ignis simplifies the process. Just enter your credentials during setup to connect to your buckets.
## Features

- **Upload files** directly to Backblaze B2 buckets  
- **List files** stored
- **Download files** to your local machine  
- **Delete files** from buckets  
- **Easy configuration and setup** with credentials and bucket details  

---

## Setup

    git clone https://github.com/gio-exe/Ignis

    cd Ignis

    chmod +x ./run.sh

    ./run.sh

---

## Usage

- **1. Upload**

  Upload a file to your Backblaze B2 bucket.

      > 1
      File path: /path/to/file.txt
      Uploaded file.txt

- **2. List**

  List all files currently stored in your bucket.

      > 2
      Files:
      ID#0: file.txt (1024 bytes)
      ID#1: image.png (200000 bytes)

- **3. Download**

  Download a file from your bucket to a local directory.

      > 3
      File ID to download: 0
      Folder path to download into (default current dir): /home/user/downloads
      Downloaded 'file.txt' to /home/user/downloads/file.txt

- **4. Delete**

  Delete a file from your bucket.

      > 4
      File ID to delete: 1
      Deleted 'example.txt'

- **5. View**

  View the contents of a file.

      > 5
      File ID to view: 0

      ------ FILE CONTENT START ------

      Content of file.txt. Hello world!

      ------- FILE CONTENT END -------

- **6. Exit**

  Exit the application.

      > 6
      Goodbye!
