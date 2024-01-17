import logging
from enum import IntEnum, unique

from flags import zero_bit, sign_bit, carry_bit, parity_bit, get_bit

@unique
class RegID(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    H = 5
    L = 6

class DRegID(IntEnum):
    BC = 1
    DE = 3
    HL = 5
    M = 5
    SP = 7
    PC = 8

def flags(value):
    return {
        'z': zero_bit(value), 
        's': sign_bit(value), 
        'cy': carry_bit(value), 
        'p': parity_bit(value)
    }

class Registers:
    logger = logging.getLogger('Registers')

    def __init__(self):
        self._items = bytearray(7)

    def get(self, reg_id):
        """Get the value of a register."""
        return self._items[reg_id]

    def set(self, reg_id, value):
        """Set the value of a register."""
        self._items[reg_id] = value & 0xff

    def perform_operation(self, reg_id, value, operation):
        """Perform an operation on a register and return the flags."""
        result = operation(self._items[reg_id], value)
        self.set(reg_id, result)
        return flags(result)

    def increment(self, reg_id, value):
        """Increment a register by a value and return the flags."""
        if value < 0:
            raise ValueError('Must be a positive value')

        return self.perform_operation(reg_id, value, lambda x, y: x + y)

    def decrement(self, reg_id, value):
        """Decrement a register by a value and return the flags."""
        if value < 0:
            raise ValueError('Must be a positive value')

        return self.perform_operation(reg_id, value, lambda x, y: x - y)

    def bitwise_operation(self, reg_id, value, operation):
        """Perform a bitwise operation on a register and return the flags."""
        result = operation(self._items[reg_id], value)
        self.set(reg_id, result)
        return flags(result)

    def and_(self, reg_id, value):
        """Perform a bitwise AND operation on a register and return the flags."""
        return self.bitwise_operation(reg_id, value, lambda x, y: x & y)

    def or_(self, reg_id, value):
        """Perform a bitwise OR operation on a register and return the flags."""
        return self.bitwise_operation(reg_id, value, lambda x, y: x | y)

    def xor_(self, reg_id, value):
        """Perform a bitwise XOR operation on a register and return the flags."""
        return self.bitwise_operation(reg_id, value, lambda x, y: x ^ y)

    def not_(self, reg_id):
        """Perform a bitwise NOT operation on a register and return the flags."""
        result = self._items[reg_id] ^ 0xff
        self.set(reg_id, result)
        return flags(result)

    def shift_left(self, reg_id):
        """Shift a register to the left and return the flags."""
        result = (self._items[reg_id] << 1) | (self._items[reg_id] >> 7)
        self.set(reg_id, result)
        return flags(result)

    def shift_left_carry(self, reg_id, carry):
        """Shift a register to the left with carry and return the carry flag."""
        tmp = self._items[reg_id]
        result = (tmp << 1) | carry
        carry_flag = bool(get_bit(tmp, 7))
        self.set(reg_id, result)
        return {'cy': carry_flag}

    def shift_right(self, reg_id):
        """Shift a register to the right and return the flags."""
        tmp = self._items[reg_id]
        result = (tmp >> 1) | (tmp << 7)
        carry_flag = bool(get_bit(tmp, 0))
        self.set(reg_id, result)
        return {'cy': carry_flag}

    def shift_right_carry(self, reg_id, carry):
        """Shift a register to the right with carry and return the carry flag."""
        tmp = self._items[reg_id]
        result = (tmp >> 1) | (carry << 7)
        carry_flag = bool(get_bit(tmp, 0))
        self.set(reg_id, result)
        return {'cy': carry_flag}

    def get_pair(self, dreg_id):
        """Get the value of a pair of registers."""
        start = dreg_id
        end = dreg_id + 2
        return int.from_bytes(self._items[start:end], byteorder='big', signed=False)

    def set_pair(self, dreg_id, value):
        """Set the value of a pair of registers."""
        value = value & 0xffff  # Ensure value is within 16-bit range
        self._items[dreg_id] = value >> 8  # Set high byte
        self._items[dreg_id + 1] = value & 0xff  # Set low byte

    def increment_pair(self, dreg_id, value):
        """Increment a pair of registers by a value and return the flags."""
        if value < 0:
            raise ValueError('Must be a positive value')

        current_value = self.get_pair(dreg_id)
        result = current_value + value
        self.set_pair(dreg_id, result)
        return flags(result)

    def decrement_pair(self, dreg_id, value):
        """Decrement a pair of registers by a value and return the flags."""
        if value < 0:
            raise ValueError('Must be a positive value')

        current_value = self.get_pair(dreg_id)
        result = current_value - value
        self.set_pair(dreg_id, result)
        return flags(result)
