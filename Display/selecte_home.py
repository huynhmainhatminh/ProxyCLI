import keyboard
from Display.home import *
from Clear import clear_display
from data import setting
from data.display_proxies import *
from data import checker_https
from data import get_proxies
from data import checker_fraud_score
from data import checker_api
from data import input_api


class SelecteHome:
    def __init__(self, layout: Layout, live) -> None:
        self.option_to_function: dict[str] = {
            "func1": "[bold yellow1][ [bold sky_blue1]CHECKER PROXY HTTP/s [bold yellow1]]",
            "func2": "[bold yellow1][ [bold sky_blue1]CHECKER FRAUD SCORE [bold yellow1]]",
            "func3": "[bold yellow1][ [bold sky_blue1]HELP TOOLS PROXIES [bold yellow1]]",
            "func4": "[bold yellow1][ [bold sky_blue1]CHECKER PROXY SOCKS4 [bold yellow1]]",
            "func5": "[bold yellow1][ [bold sky_blue1]GET ALL PROXIES FREE [bold yellow1]]",
            "func6": "[bold yellow1][ [bold sky_blue1]CHECKER FRAUD SCORE [bold yellow1]]",
            "func7": "[bold yellow1][ [bold sky_blue1]CHECKER PROXY SOCKS5 [bold yellow1]]",
            "func8": "[bold yellow1][ [bold sky_blue1]PROXIES DETECTION [bold yellow1]]",
            "func9": "[bold yellow1][ [bold sky_blue1]CLEAR & CLEAN TOOLS [bold yellow1]]",
            "func10": "[bold yellow1][ [bold sky_blue1]CHECKER LIVE/DIE [bold yellow1]]",
            "func11": "[bold yellow1][ [bold sky_blue1]TCP PING PROXIES [bold yellow1]]",
            "func12": "[bold yellow1][ [bold sky_blue1]SETTING CHECKER [bold yellow1]]",
        }
        self.make_layout: Layout = layout
        self.layout: Layout = layout
        self.selected_index: int = 0
        self.update_frame = DisplayHome()
        self.live = live
        self.options: list[str] = list(self.option_to_function.keys())
        self.block_display: bool = False

        self.loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(self.loop)

        self.data = json.load(open("data/settings.json", "r"))
        self.threads: int = self.data["threads"]
        self.urls: str = self.data["urls"]
        self.timeout: int = self.data["timeout"]
        self.retries: int = self.data["retries"]

        self.file_maps = {
            'http': {
                'e': "output/http_s/elite.txt",
                'a': "output/http_s/anonymous.txt",
                't': "output/http_s/transparent.txt",
                'all': "output/http_s/all.txt"
            },
            'socks4': {
                'e': "output/socks4/elite.txt",
                'a': "output/socks4/anonymous.txt",
                't': "output/socks4/transparent.txt",
                'all': "output/socks4/all.txt"
            },
            'socks5': {
                'e': "output/socks5/elite.txt",
                'a': "output/socks5/anonymous.txt",
                't': "output/socks5/transparent.txt",
                'all': "output/socks5/all.txt"
            }
        }

        if "keywords" in str(self.data):
            self.keywords = self.data["keywords"]
        else:
            self.keywords = None

    @staticmethod
    def write_proxies_to_files(proxies, file_map):
        for key, file_path in file_map.items():
            with open(file_path, "a") as f:
                for proxy in proxies[key]:
                    f.write(proxy + "\n")

    def highlight_selected(self) -> None:
        for i, option in enumerate(self.option_to_function):
            if i == self.selected_index:
                highlight_table = Table.grid(padding=0)

                highlight_table.add_column()
                highlight_table.add_row(self.option_to_function[option])
                panel = Panel(
                    Align.center(highlight_table, vertical="top"),
                    box=box.ROUNDED,
                    padding=(1, 1),
                    style="bold medium_orchid1"
                )
                self.layout[option].update(panel)
            else:
                self.layout[option].update(self.update_frame.update_frame(self.option_to_function[option]))

    def handle_key_press(self, event) -> None:
        if event.name == "down" and self.block_display is False:
            self.selected_index = (self.selected_index + 3) % len(self.options)
        elif event.name == "up" and self.block_display is False:
            self.selected_index = (self.selected_index - 3) % len(self.options)
        elif event.name == "right" and self.block_display is False:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif event.name == "left" and self.block_display is False:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif event.name == "space" and self.block_display is False:

            # check http/s
            if self.options[self.selected_index] == "func1":
                self.block_display = True
                clear_display.ClearDisplay().clear()
                self.layout = DisplayProxies().run_display_https()
                self.live.update(self.layout)
                live_https = self.loop.run_until_complete(checker_https.CheckerProxyType(
                        self.layout, self.threads, self.urls, self.timeout, self.retries,
                        "CHECKER PROXY HTTP/s", self.keywords, ["http"]).run())

                self.write_proxies_to_files(live_https, self.file_maps['http'])
                self.layout = self.make_layout
                self.live.update(self.layout)

            # check socks4
            elif self.options[self.selected_index] == "func4":
                self.block_display = True
                clear_display.ClearDisplay().clear()
                self.layout = DisplayProxies().run_display_https()
                self.live.update(self.layout)
                live_socks4 = self.loop.run_until_complete(checker_https.CheckerProxyType(
                        self.layout, self.threads, self.urls, self.timeout, self.retries,
                        "CHECKER PROXY SOCKS4", self.keywords, ["socks4"]).run())

                self.write_proxies_to_files(live_socks4, self.file_maps['socks4'])
                self.layout = self.make_layout
                self.live.update(self.layout)

            # check socks5
            elif self.options[self.selected_index] == "func7":
                self.block_display = True
                clear_display.ClearDisplay().clear()
                self.layout = DisplayProxies().run_display_https()
                self.live.update(self.layout)
                live_socks5 = self.loop.run_until_complete(
                    checker_https.CheckerProxyType(
                        self.layout, self.threads, self.urls,
                        self.timeout, self.retries,
                        "CHECKER PROXY SOCKS5", self.keywords, ["socks5"]).run())
                self.write_proxies_to_files(live_socks5, self.file_maps['socks5'])
                self.layout = self.make_layout
                self.live.update(self.layout)

            elif self.options[self.selected_index] == "func10":
                self.block_display = True
                clear_display.ClearDisplay().clear()
                self.layout = DisplayProxies().run_display_https()
                self.live.update(self.layout)
                live_die = self.loop.run_until_complete(
                    checker_https.CheckerProxyType(
                        self.layout, self.threads, self.urls,
                        self.timeout, self.retries,
                        "CHECKER LIVE/DIE", self.keywords, ["http", "socks4", "socks5"]).run())
                proxy_http = live_die[0]
                proxy_socks4 = live_die[1]
                proxy_socks5 = live_die[2]

                self.write_proxies_to_files(proxy_http, self.file_maps['http'])
                self.write_proxies_to_files(proxy_socks4, self.file_maps['socks4'])
                self.write_proxies_to_files(proxy_socks5, self.file_maps['socks5'])

                self.layout = self.make_layout
                self.live.update(self.layout)

            elif self.options[self.selected_index] == "func2":
                self.block_display = True
                self.live.stop()
                clear_display.ClearDisplay().clear()
                keyboard.send('backspace')
                list_proxy = input_api.InputAPI().run()
                self.highlight_selected()
                self.live.start()
                self.live.refresh()

                clear_display.ClearDisplay().clear()
                self.layout = DisplayProxies().make_layout_api()
                self.live.update(self.layout)
                self.loop.run_until_complete(checker_fraud_score.CheckerFraudScore(list_proxy, self.layout).run())
                self.layout = self.make_layout
                self.live.update(self.layout)

            # get all proxy
            elif self.options[self.selected_index] == "func5":
                self.block_display = True
                self.live.stop()
                clear_display.ClearDisplay().clear()
                keyboard.send('backspace')
                self.loop.run_until_complete(get_proxies.get_proxy())
                self.highlight_selected()
                self.live.start()
                self.live.refresh()

            # setting proxy
            elif self.options[self.selected_index] == "func12":
                self.block_display = True
                self.live.stop()
                clear_display.ClearDisplay().clear()
                keyboard.send('backspace')
                setting.settings()
                self.highlight_selected()
                self.live.start()
                self.live.refresh()

        elif event.name == "f12":
            self.block_display = False

        self.highlight_selected()
        self.live.update(self.layout)
