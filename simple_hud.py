from pyvit import can
from pyvit.hw import socketcan

dev = socketcan.SocketCanDev("vcan0")  # /dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0
dev.set_bitrate(500000)
dev.start()

speed = pedal_pos = 0
while True:
    frame = dev.recv()
    if frame.arb_id == 0x257:  # SG_ UIspeed_signed257 : 12|12@1+ (0.08,-40) [-40|287.6] "KPH"  Receiver
        d1 = frame.data[2]
        d2 = frame.data[1] / 16
        speed = int((d1 * 16 + d2) * 0.08 - 40)

    if frame.arb_id == 0x118:  # SG_ PedalPosition118 : 32|8@1+ (0.4,0) [0|100] "%"  Receiver
        d3 = frame.data[4]
        pedal_pos = int(d3 * 0.4)
    
    info = 'Speed:{:3d} km/h   PedalPos:{:3d} %'.format(speed, pedal_pos)
    print(info, end='\r', flush=True)
