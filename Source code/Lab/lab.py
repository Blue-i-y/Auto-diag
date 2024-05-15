import sys
import time
def clear_line(second):
    # Efface la ligne actuelle
    time.sleep(second)
    print("\033[A\x1b[0K\r")
    print("\033[2A ")
    time.sleep(second)

while 1 :
    print("Ceci est un texte.")
    clear_line(2)
