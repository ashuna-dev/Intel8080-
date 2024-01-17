def get_bit(value, index):
    return (value >> index) & 1

def zero_bit(value):
    return value == 0

def sign_bit(value):
    return value < 0

def carry_bit(value):
    return value < 0 or value > 0xFF

def parity_bit(value):
    return bin(value).count('1') % 2 == 0

class ConditionFlags:
    def __init__(self):
        self.s = False  
        self.z = False  
        self.p = False  
        self.cy = False  
        self.ac = False  
        self.pad = False
