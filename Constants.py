import pyaudio

HEADER = '\033[95m'
INFO = '\033[94m'
SUCCESS = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

STATION = 0
ROUTER = 1

DATA_SIZE = 8
SLEEP_TIME = 1
CHANNELS = 2
RATE = 44100
FORMAT = pyaudio.paInt16
CHUNK = 1024
THRESHOLD = 5000
NOISE = '1'
SILENCE = '0'
SECONDS = 12
TIME_ATT = 1
MESSAGE_SIZE = SECONDS
MACHINE_A = '00'
MACHINE_B = '01'
MACHINE_C = '10'
MACHINE_D = '11'

VALIDATE_BITS = 'Values not recognized (0s and 1s only)'
VALIDATE_CONTROL_BITS = 'Control bits not found (must be 1)'
VALIDATE_MESSAGE_LENGHT = 'Incorrect message lenght (must be {})'.format(MESSAGE_SIZE)
