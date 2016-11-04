import sys
import usb.core
import time

dev = usb.core.find(idVendor = 0x16c0, idProduct=0x5dc)

assert dev is not None

print dev

print hex(dev.idVendor) + ',' + hex(dev.idProduct)

mymin = 0
mymax = 0
myave = 0
mytime = time.strftime("%d-%m-%Y_%H:%M")
mycount = 0
mysum = 0
dB = 0

while True:
    ret = dev.ctrl_transfer(0xC0, 4, 0, 0,200)
    print "ret ", ret
    dB = (ret[0] + ((ret[1] & 3) * 256)) * 0.1 + 30
    print "dB ", dB

