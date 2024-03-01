from pymetasploit3.msfrpc import *

client = MsfRpcClient("Auto-Diag", server="0.0.0.0", port=55553)

for m in dir(client): 
    print(m)
