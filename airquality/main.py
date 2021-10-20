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
import sounddevice as sd

#### LOCAL IMPORTS ####
import ipc

#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
TRANSMISSION_PORT = 10001
SOUND_DEVICE = 0
SAMPLE_INTERVAL = 1 # seconds
NOISE_SAMPLE_DUR = 0.5 # seconds
TRANSMIT_AQ_DATA_EVENT = 'air-data'
TRANSMIT_AQ_STATUS_EVENT = 'air-status'
LOG_GAS_DATA = True
LOG_FILE_SUFFIX = '1'

#### CREATE NOISE OBJECT ####
sd.default.device = SOUND_DEVICE
noise = Noise(duration=NOISE_SAMPLE_DUR)

log_gas_file = None
start_time = None

def main(argv):
    # Establish IPC
    ipc.init()

    heating = True
    ipc.msg_transmission(TRANSMIT_AQ_STATUS_EVENT,{'heating': heating})

    if(LOG_GAS_DATA):
        log_gas_file = open('log_gas'+LOG_FILE_SUFFIX+'.txt','rw')
        log_gas_file.write('time,oxidising,reducing,ammonia\n')

        start_time = time.time()
    
    heating = False

    while(True):
         
        gas_data = gas.read_all()
        temp = bme280.get_temperature()

        """ data = {'temperature':temp,'pressure':bme280.get_pressure(), # May need to add 
        'humidity':bme280.get_humidity(),'light':ltr559.get_lux(),
        'ox_gas':gas_data.oxidising/1000,'red_gas':gas_data.reducing/1000,
        'amm_gas':gas_data.nh3/1000,'noise_low':amp_low,
        'noise_mid':amp_mid,'noise_high':amp_high} """
        data = {'temperature':temp,'pressure':bme280.get_pressure(), # May need to add 
        'humidity':bme280.get_humidity(),'light':ltr559.get_lux(),
        'ox_gas':gas_data.oxidising/1000,'red_gas':gas_data.reducing/1000,
        'amm_gas':gas_data.nh3/1000}
        # GCS needs  
        if(LOG_GAS_DATA):
            log_gas_file.write((time.time()-start_time) + ',' + gas_data.oxidising + ',' + gas_data.reducing + ',' + gas_data.nh3 + '\n')

        ipc.msg_transmission(TRANSMIT_AQ_DATA_EVENT,data)
        ipc.msg_transmission(TRANSMIT_AQ_STATUS_EVENT,{'heating': heating})
        ipc.msg_lcd(TRANSMIT_AQ_DATA_EVENT,{'temperature':temp})

        time.sleep(SAMPLE_INTERVAL)

#### ENTRY POINT ####
if __name__ == "__main__":
    main(sys.argv[1:])
