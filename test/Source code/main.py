from NetworkScanner.network import Network
from NetworkScanner.scanner import Scanner

if __name__ == "__main__":
    try:
        Nscan = Scanner()
        Nscan.auto_diag()
    except KeyboardInterrupt:
        print_red("\n[x] Program closed!")
        sys.exit()
