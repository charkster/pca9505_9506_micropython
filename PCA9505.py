import machine

class PCA9505():

    def __init__(self, i2c, slave_address):

        self.i2c              = i2c
        self.slave_address    = slave_address
        self.OUTPUT_BASE_ADDR = 0x08
        self.IO_BASE_ADDR     = 0x18
        self.INPUT_BASE_ADDR  = 0x00
        self.NUM_BANKS        = 5
        self.MULTI_BYTE       = 0x80

    def init_all_outputs(self):
        self.i2c.writeto_mem(self.slave_address, self.OUTPUT_BASE_ADDR + self.MULTI_BYTE, bytearray([0x00] * 5)) # all low values
        self.i2c.writeto_mem(self.slave_address, self.IO_BASE_ADDR     + self.MULTI_BYTE, bytearray([0x00] * 5)) # all outputs

    def set_io(self, bank=0, pin=0, value=0):
        orig_value = int.from_bytes(self.i2c.readfrom_mem(self.slave_address, (self.OUTPUT_BASE_ADDR + bank), 1))
        new_value  = (orig_value & (~(1 << pin))) + (value << pin)
        self.i2c.writeto_mem(self.slave_address, self.OUTPUT_BASE_ADDR + bank, new_value.to_bytes())

    def get_io(self, bank=0, pin=0):
        return (int.from_bytes(self.i2c.readfrom_mem(self.slave_address, self.INPUT_BASE_ADDR + bank, 1)) & (1 << pin)) >> pin
    
    def set_all_io(self, bit_list=[]): # bit_list is an list of 40 numbers, each either 1 or 0
        list_of_bytes = []
        for offset in range(0,40,8):
            byte = 0
            for bit in range(0,8):
                byte += bit_list[offset+bit] << bit
            list_of_bytes.append(byte)
        self.i2c.writeto_mem(self.slave_address, self.OUTPUT_BASE_ADDR + self.MULTI_BYTE, bytearray(list_of_bytes))
    
    def read_all_io(self):
        result = []
        for byte in list(self.i2c.readfrom_mem(self.slave_address, self.INPUT_BASE_ADDR + self.MULTI_BYTE, 5)):
            result += [(byte >> bit) & 1 for bit in range(0, 8)]
        return result