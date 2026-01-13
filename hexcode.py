
def encode(ip):
    tmp = ip.split('.')
    output = ''
    for i in tmp:
        output += hex(int(i))[2:]
    return output

def decode(hexin):
    ip1 = int(hexin[0:2], 16)
    ip2 = int(hexin[2:4], 16)
    ip3 = int(hexin[4:6], 16)
    ip4 = int(hexin[6:8], 16)
    out = f"{ip1}.{ip2}.{ip3}.{ip4}"
    return out