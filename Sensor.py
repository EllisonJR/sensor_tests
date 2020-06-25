import spidev
from gpiozero import MCP3008
from gpiozero import LED

tmp = MCP3008(channel=0, device=0)
spi = spidev.SpiDev()
spi.open(0,0)

green = LED(21)
yellow = LED(20)
red = LED(16)

#read raw output from mcp3008
#spi.xfer2 takes in a list in the form of the speed, delay, and bits passed through the spi chip
def readadc(adcnum):
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

#call the function that reads from the chip
#take the rawValue and multiply it by the reference voltage
#divide the resulting number by the digital 10bit value (1024)
#now you have the voltage relative to what the chip is reading from the lm35 sensor
#one last time, divide the number again, but by .01 as the sensor is outputting mV relative to centigrade

#then do a quikc conversion for the sake of LED switching, before we exit the function, pass the centigrade
#value out to the main value
def Readout():
    rawValue = readadc(0)
    
    temperatureInCelsius = ((rawValue * 3.3) / 1024) / 0.01
    farenheit = (temperatureInCelsius * 1.8) + 32
    if farenheit <= 79.99:
        green.on()
        red.off()
        yellow.off()
    elif farenheit >= 80.0 and farenheit <= 99.99:
        green.off()
        red.off()
        yellow.on()
    elif farenheit >= 100:
        green.off()
        red.on()
        yellow.off()
    
    return temperatureInCelsius
