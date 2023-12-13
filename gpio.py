from caravel import *
from util import *

MPRJ_INPUT_CFG  = None
MPRJ_OUTPUT_CFG = None

def gpio_setup(gpio_mode):
    global MPRJ_INPUT_CFG, MPRJ_OUTPUT_CFG

    assert gpio_mode in ["sky130", "gf180"]

    if gpio_mode == "sky130":
        MPRJ_INPUT_CFG = 0x1801
        MPRJ_OUTPUT_CFG = 0x1800

    elif gpio_mode == "gf180":
        # mgmt_en = 1, oe_ovr = 1, ie = 1, oe = 1
        MPRJ_INPUT_CFG = 0x00F
        # mgmt_en = 0, oe_ovr = 1, ie = 1, oe = 1
        MPRJ_OUTPUT_CFG = 0x00E

def gpio_config_get(dev, idx):
    hi = caravel_read(dev, REG_GPIO_CFG_BASE+idx*2)
    lo = caravel_read(dev, REG_GPIO_CFG_BASE+idx*2+1)
    return (hi << 8) | lo

def gpio_config_set(dev, idx, cfg):
    caravel_write(dev, REG_GPIO_CFG_BASE+idx*2, cfg >> 8)
    caravel_write(dev, REG_GPIO_CFG_BASE+idx*2+1, cfg & 0xFF)

def gpio_config_push(dev):
    caravel_write(dev, REG_GPIO_CTRL, 1)

# 0 = proj input, 1 = proj output
def gpio_setmode(dev, idx, direction):
    assert MPRJ_INPUT_CFG is not None
    assert MPRJ_OUTPUT_CFG is not None
    gpio_config_set(dev, idx, MPRJ_OUTPUT_CFG if direction else MPRJ_INPUT_CFG)

def gpio_getall(dev):
    buf = caravel_read_multi(dev, REG_GPIO, 5)
    return (
        (buf[0] << 32) |
        (buf[1] << 24) |
        (buf[2] << 16) |
        (buf[3] << 8)  |
        (buf[4] << 0)
    )

def gpio_setall(dev, val):
    buf = [
        (val >> 32) & 0xFF,
        (val >> 24) & 0xFF,
        (val >> 16) & 0xFF,
        (val >> 8)  & 0xFF,
        (val >> 0)  & 0xFF,
    ]
    caravel_write(dev, REG_GPIO+0, buf)

def gpio_get(dev, idx):
    return get_bit(gpio_getall(dev), idx)

# hi/lo both inclusive, like SystemVerilog
def gpio_getrange(dev, hi, lo):
    assert hi >= lo
    dat = gpio_getall(dev)
    out = 0
    for i in list(range(lo, hi+1))[::-1]:
        out <<= 1
        out |= get_bit(dat, i)
    return out

def gpio_set(dev, idx, val):
    dat = gpio_getall(dev)
    dat &= ~(1 << idx)
    if val:
        dat |= (1 << idx)
    gpio_setall(dev, dat)

# hi/lo both inclusive, like SystemVerilog
def gpio_setrange(dev, hi, lo, val):
    assert hi >= lo
    dat = gpio_getall(dev)
    for i in range(lo, hi+1):
        dat &= ~(1 << i)
        if val & 1:
            dat |= (1 << i)
        val >>= 1
    gpio_setall(dev, dat)
