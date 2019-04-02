# -*- coding: utf-8 -*-
import RPi.GPIO as IO

#树莓派所使用的引脚   ： 最终使用 21（1 开）控制开关门；16（0获取，1不获取） 获取是否开启摄像头
#                 --   16  20  21
#                 13   19  26  --
# 

class HardWare():

    def IO_Init():
        global out_led,out_high,in_distance
        out_led = 21
        out_high = 20
        out_high1 = 26
        in_distance = 16
        IO.setmode(IO.BCM)
        IO.setwarnings(False)
        IO.setup(out_led,IO.OUT)
        IO.setup(out_high,IO.OUT)
        IO.setup(out_high1,IO.OUT)
        IO.setup(in_distance,IO.IN)
        IO.output(out_led,0)
        IO.output(out_high,1)
        IO.output(out_high1,1)

    def if_distance():
        return IO.input(in_distance)

    def openDoor():
        IO.output(out_led,1)

    def closeDoor():
        IO.output(out_led,0)

    def io_lever(pin):
        return IO.input(pin)
