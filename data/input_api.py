import re
from data.extra import *


class InputAPI:
    @staticmethod
    def filter_text(text):
        def filter_ip(proxy):
            regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
            _ = proxy.split(':')[0]
            if re.search(regex, _):
                if len(proxy.split(':')[1]) > 5:
                    return False
                else:
                    if len(proxy.split(':')[1]) == 1:
                        return False
                    else:
                        return True
            else:
                return False

        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+'
        match = re.search(pattern, text)
        if match:
            host_port = match.group()
            filter_ip(host_port)
            if filter_ip(host_port) is True:
                return host_port

    def run(self) -> list[str]:
        print("\n")
        logo.logo()
        all_proxy = []
        while True:
            try:
                run(f"\n{bold}{yellow}[{cyan}●{yellow}] {sky_blue2}ENTER PROXIES FILE PATH {bold}: ")
                file_path = open(input(), encoding='UTF-8').read().strip().split('\n')
                for proxy_all in file_path:
                    text_filter = self.filter_text(proxy_all.strip())
                    if text_filter:
                        all_proxy.append(text_filter)
                break
            except(FileNotFoundError, PermissionError):
                error_input()
                continue

        all_proxy = list(set(all_proxy))
        print(f"\n{red}[{yellow}!{red}] {medium_spring_green}All Available Proxies{bold}: {sky_blue2}{len(all_proxy)}")
        sleep(5)
        return all_proxy