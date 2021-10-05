#### EXTERNAL MODULE IMPORTS ####
import time # time.sleep()
try:
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
bme280 = BME280()
from enviroplus import gas
from enviroplus.noise import Noise
import sys

#### LOCAL IMPORTS ####
import airquality.ipc

#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
TRANSMISSION_PORT = 10001
SAMPLE_INTERVAL = 1 # seconds
NOISE_SAMPLE_DUR = 0.5 # seconds
TRANSMIT_AQ_DATA_EVENT = 'air-data'
TRANSMIT_AQ_STATUS_EVENT = 'air-status'

#### CREATE NOISE OBJECT ####
noise = Noise(duration=NOISE_SAMPLE_DUR)

def main(argv):
    # Establish IPC
    air_quality.ipc.init()

    air_quality.ipc.msg_transmission(TRANSMIT_AQ_STATUS_EVENT,{'heating': True})

    air_quality.ipc.msg_transmission(TRANSMIT_AQ_STATUS_EVENT,{'heating': False})

    while(True):
        # Microphone will block for up to half a seocond
        amp_low, amp_mid, amp_high, amp_total = noise.get_noise_profile()
         
        gas_data = gas.read_all()
        temp = bme280.get_temperature()

        data = {'temperature':temp,'pressure':bme280.get_pressure(), # May need to add 
        'humidity':bme280.get_humidity(),'light':ltr559.get_lux(),
        'ox_gas':gas_data.oxidising/1000,'red_gas':gas_data.reducing/1000,
        'amm_gas':gas_data.nh3/1000,'noise_low':amp_low,
        'noise_mid':amp_mid,'noise_high':amp_high}

        air_quality.ipc.msg_transmission(TRANSMIT_AQ_DATA_EVENT,data)
        air_quality.ipc.msg_lcd(TRANSMIT_AQ_DATA_EVENT,{'temperature':temp})

        time.sleep(SAMPLE_INTERVAL-NOISE_SAMPLE_DUR)

#### ENTRY POINT ####
if __name__ == "__main__":
    main(sys.argv[1:])
