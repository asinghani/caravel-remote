## Utility functions for accessing Caravel
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController
from io import StringIO

CARAVEL_PASSTHRU = 0xC4
CARAVEL_STREAM_READ = 0x40
CARAVEL_STREAM_WRITE = 0x80
CARAVEL_REG_READ = 0x48
CARAVEL_REG_WRITE = 0x88

def caravel_setup():
    s = StringIO()
    Ftdi.show_devices(out=s)
    devlist = s.getvalue().splitlines()[1:-1]
    gooddevs = []
    for dev in devlist:
        url = dev.split('(')[0].strip()
        name = '(' + dev.split('(')[1]
        gooddevs.append(url)
    if len(gooddevs) == 0:
        print('Error:  No matching FTDI devices on USB bus!')
        sys.exit(1)
    elif len(gooddevs) > 1:
        print('Error:  Too many matching FTDI devices on USB bus!')
        Ftdi.show_devices()
        sys.exit(1)
    else:
        print('Success: Found one matching FTDI device at ' + gooddevs[0])

    spi = SpiController(cs_count=2)
    spi.configure(gooddevs[0])
    dev = spi.get_port(cs=0)
    return dev

def caravel_read(dev, reg):
    return caravel_read_multi(dev, reg, 1)[0]

def caravel_read_multi(dev, reg, len_):
    assert len_ > 0
    cmd = CARAVEL_REG_READ if len_ == 1 else CARAVEL_STREAM_READ
    return dev.exchange([cmd, reg], len_)

def caravel_write(dev, reg, data):
    if isinstance(data, int):
        data = [data]
    cmd = CARAVEL_REG_WRITE if len(data) == 1 else CARAVEL_STREAM_WRITE
    dev.exchange([cmd, reg, *data])

REG_SPI_STATUS     = 0x00 # len = 1
REG_MFG_ID         = 0x01 # len = 2
REG_PROD_ID        = 0x03 # len = 1
REG_MASK_REV       = 0x04 # len = 4
REG_RESET          = 0x0B # len = 1
REG_GPIO_CTRL      = 0x13 # len = 1
REG_GPIO_CFG_BASE  = 0x1D
REG_GPIO           = 0x69

def caravel_mfg_id(dev):
    return int(caravel_read_multi(dev, REG_MFG_ID, 2).hex(), 16)

def caravel_prod_id(dev):
    return int(caravel_read_multi(dev, REG_PROD_ID, 1).hex(), 16)

def caravel_proj_id(dev):
    return int(("{:032b}".format(int(caravel_read_multi(dev, REG_MASK_REV, 4).hex(), 16)))[::-1], 2)

def caravel_reset(dev, rst):
    caravel_write(dev, REG_RESET, rst)
