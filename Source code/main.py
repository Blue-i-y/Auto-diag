import sys

from network import Network
from scanner import Scanner

if __name__ == "__main__":
    try:
        Nscan = Scanner()
        Nscan.Auto_Diag()
    except KeyboardInterrupt:
        print("\n[x] Program closed!")
        sys.exit()
