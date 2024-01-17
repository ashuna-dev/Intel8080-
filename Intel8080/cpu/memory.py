


class InvalidMemoryAddressError(Exception):
    """Raised when a memory address is out of bounds."""
    pass


class Memory:
    def __init__(self) -> None:
        """Initialize Memory with a buffer of 0xffff bytes."""
        self._buffer = bytearray(0xffff)

    def _check_address(self, address: int) -> None:
        """Check if the given address is within the valid range."""
        if not (0x0 <= address <= 0xffff):
            msg = f'Memory operation out of bounds: {address:06x}'
            raise InvalidMemoryAddressError(msg)

    def read_byte(self, address: int) -> int:
        """Read a single byte from the specified memory address."""
        self._check_address(address)
        return self._buffer[address]

    def write_byte(self, address: int, value: int) -> None:
        """Write a single byte to the specified memory address."""
        self._check_address(address)
        self._buffer[address] = value

    def read_double_byte(self, address: int) -> int:
        """Read a double-byte (16-bit) value from the specified memory address."""
        self._check_address(address)
        self._check_address(address + 1)
        return int.from_bytes(self._buffer[address:address + 2], byteorder='little', signed=False)

    def write_double_byte(self, address: int, value: int) -> None:
        """Write a double-byte (16-bit) value to the specified memory address."""
        self._check_address(address)
        self._check_address(address + 1)
        self._buffer[address:address + 2] = value.to_bytes(2, byteorder='little', signed=False)