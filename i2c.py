from smbus import SMBus
import time

bus = SMBus(1)
#address = 0x60
address = 0x40
data = [1,2,3,4,5,6,7,8]
#bus.write_i2c_block_data(address, 0, data)

def fun_data():
        data1 = bus.write_byte_data(address, 1, 1)

        return data1

def bearing3599():
        bear1 = bus.read_byte_data(address,2)
        bear2 = bus.read_byte_data(address, 3)
        bear = (bear1 << 8)
        bear = bear/10.0
        return bear

while True:
         bearing = bearing3599()     #this returns the value to 1 decimal place in degrees.
         time.sleep(0.5) 
         data1 = fun_data()      #this returns the value as a byte between 0 and 255. 
         print (data1)
        
         time.sleep(0.5) 