# xkcd-pi-printer
Raspberry Pi + XKCD + Thermal Printer goodness. For use with the [Adafruit thermal printer](https://www.adafruit.com/product/2751)

# Demo
See my blog post about it at http://jamish.github.io/pi/python/hardware/3dprint/2017/05/11/pi-printer.html

# Dependencies
1. [XKCD](https://pypi.python.org/pypi/xkcd/) library
2. [PIL](http://www.pythonware.com/products/pil/) library
3. [Python-Thermal-Printer](https://github.com/adafruit/Python-Thermal-Printer) library from Adafruit

# Usage
Either just run ./run.sh whenever you feel like it, or create a crontab entry with `crontab -e` to fetch a new comic every day:
```
0 9 * * * /home/pi/Documents/Python/xkcd/run.sh >> /home/pi/Documents/Python/xkcd/output.log 2>&1
```
