import sys
import logo
from time import sleep

red = "\033[1;31m"
yellow = "\033[1;33m"
cyan = "\033[1;36m"
bold = "\033[1;97m"
green = "\033[1;32m"
sky_blue2 = "\033[1;38;5;111m"
medium_spring_green = "\033[1;38;5;48m"


def run(z):
    for i in z:
        sys.stdout.write(i)
        sys.stdout.flush()
        sleep(0.01)


def error_input():
    print(f"\n{yellow}[{red}!{yellow}] {red}Invalid value {bold}")

