import machine
from PCA9505 import PCA9505

i2c = machine.I2C(1,sda=machine.Pin(6), scl=machine.Pin(7), freq=400000) # rp2040/rp2350 xiao
io1 = PCA9505(i2c=i2c, slave_address=0x21)

io1.init_all_outputs()
io1.set_all_io([0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0])
io1.read_all_io()
io1.get_io(bank=0,pin=3)
io1.get_io(bank=0,pin=4)
io1.set_io(bank=0,pin=4,value=1)
io1.get_io(bank=0,pin=4)