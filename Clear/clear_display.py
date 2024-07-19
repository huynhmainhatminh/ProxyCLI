import os
import sys


class ClearDisplay:
    @staticmethod
    def clear():
        try:
            if "linux" in sys.platform.lower():
                os.system("clear")
            elif "win" in sys.platform.lower():
                os.system("cls")
            else:
                os.system("clear")
        except (Exception,):
            os.system("cls")
