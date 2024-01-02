import json, paramiko,time,
from threading import Thread
from ftplib import FTP

class Scanner(Network):
    def __init__(self):
        super().__init__()

    def cve_finder(self):
        # ... (your existing code)

    def ssh_connect(self, ip, username, password, port=22):
        # ... (your existing code)

    def ftp_connect(self, ip, user, password):
        # ... (your existing code)

    def bruteforce(self, ip, type):
        # ... (your existing code)

    def service_detection(self, host):
        # ... (your existing code)

    def Auto_Diag(self):
        # ... (your existing code)
