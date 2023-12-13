def set_bit(x, bit):
    return x | (1 << bit)

def set_bits(bits):
    x = 0
    for bit in bits:
        x |= (1 << bit)
    return x

def get_bit(x, bit):
    return (x & (1 << bit)) >> bit

def get_bits(x):
    i = 0
    bits = []
    while x != 0:
        if x & 0x1:
            bits.append(i)
        x = x >> 1
        i += 1
