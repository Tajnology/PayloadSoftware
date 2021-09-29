#### EXTERNAL MODULE IMPORTS ####
try:
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
bme280 = BME280()
from enviroplus import gas

#### LOCAL IMPORTS ####
import ipc

#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
TRANSMISSION_PORT = 10001
SAMPLE_INTERVAL = 1 # seconds


class Data:
    def __init__(self,temperature,pressure,humidity,light,ox_gas,red_gas,amm_gas,noise_level):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.light = light
        self.ox_gas = ox_gas
        self.red_gas = red_gas
        self.amm_gas = amm_gas
        self.noise_level = noise_level


def main(argv):
    # Establish IPC
    ipc.init()

    ipc.msg_transmission('status',{'heating': True})


#### ENTRY POINT ####
if __name__ == "__main__":
    main(sys.argv[1:])
