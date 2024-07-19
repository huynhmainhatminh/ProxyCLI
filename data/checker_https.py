from data.display_proxies import *
from collections import deque
from data import checker_proxies
from Display import home


class CheckerProxyType:
    def __init__(self, *args) -> None:
        self.files = open("data/proxies.txt").read().strip().split("\n")
        self.args = args
        self.messages = deque(maxlen=height-13)

        self.internet_send = Progress("{task.description}", TextColumn(""))
        self.send = self.internet_send.add_task("\n[bold yellow1][ [bold sky_blue1]IN USE [bold yellow1]] ", vertical="top")

        self.internet_receive = Progress("{task.description}", TextColumn(""))
        self.receive = self.internet_receive.add_task("\n[bold yellow1][ [bold sky_blue1]SPEED [bold yellow1]] ",
                                                      vertical="top")

        self.time_progress = Progress(BarColumn(style="bold sky_blue1"))
        self.time_progress.add_task("", total=None)
        self.time_progress_2 = Progress("{task.description}", TimeElapsedColumn(), SynchronizedEmojiColumn())
        self.time_progress_2.add_task(" [bold yellow1][ [bold sky_blue1]TIME [bold yellow1]]", vertical="top")
        self.panel_time = Panel(
             Group(self.time_progress_2, self.time_progress),
             border_style="bold medium_spring_green",
             padding=(1, 1),
             title=f"[bold yellow1][ [bold sky_blue1]PERFORMANCE [bold yellow1]]"
         )

        self.cpu_progress = Progress(
            "{task.description}",
            BarColumn(style="bold spring_green2"),
            TextColumn("[progress.percentage][bold violet]{task.percentage:>3.0f}%"),
        )
        self.cpu_progress.add_task("[bold yellow1][ [bold sky_blue1]CPU [bold yellow1]]", total=100, vertical="top")

        self.internet_table = Table.grid(expand=True)
        self.internet_table.add_row(Panel(Group(self.cpu_progress, self.internet_receive), border_style="bold medium_spring_green", padding=(1, 1),))

        self.memory_progress = Progress(
            "{task.description}",
            BarColumn(style="bold spring_green2"),
            TextColumn("[progress.percentage][bold violet]{task.percentage:>3.0f}%"),
        )
        self.memory_progress.add_task("[bold yellow1][ [bold sky_blue1]MEMORY [bold yellow1]]", total=100,
                                      vertical="top")

        self.performance_table = Table.grid(expand=True)
        self.performance_table.add_row(
            Panel(
                Group(self.memory_progress, self.internet_send),
                border_style="bold medium_spring_green",
                padding=(1, 1),
            )
        )

        self.overall_progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            BarColumn(style="bold spring_green2"),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            TextColumn("[progress.percentage][bold sky_blue1]{task.percentage:>3.0f}%"),
        )
        self.overall_task = self.overall_progress.add_task(
            "[bold yellow1][ [bold sky_blue1]ALL JOBS [bold yellow1]]", total=len(self.files) * len(self.args[7])
        )

        self.progress_table = Table.grid(expand=True)
        self.progress_table.add_row(
            Panel(
                self.overall_progress,
                border_style="bold medium_spring_green",
                padding=(3, 3),
            )
        )
        self.layout = self.args[0]
        self.stats = {
            "live": 0, "die": 0, "completed": 0,
            "e": 0, "t": 0, "a": 0,
            "http": 0, "socks4": 0, "socks5": 0
        }

        self.live_http = {"e": [], "t": [], "a": [], "all": []}
        self.live_socks4 = {"e": [], "t": [], "a": [], "all": []}
        self.live_socks5 = {"e": [], "t": [], "a": [], "all": []}

        self.proxy_map = {
            'http': self.live_http,
            'socks4': self.live_socks4,
            'socks5': self.live_socks5
        }

    @staticmethod
    def _append_proxy(proxy_list: dict, key: str, host: str, port: int) -> None:
        proxy_list[key].append(f"{host}:{port}")
        proxy_list["all"].append(f"{host}:{port}")

    def update_stats_proxy(self, type_proxy: str, host: str, port: int, checker_proxy: int) -> None:
        if type_proxy == "http":
            self.stats["http"] += 1
            self._append_proxy(self.live_http, {3: "e", 2: "a"}.get(checker_proxy, "t"), host, port)
        elif type_proxy == "socks4":
            self.stats["socks4"] += 1
            self._append_proxy(self.live_socks4, {3: "e", 2: "a"}.get(checker_proxy, "t"), host, port)
        else:
            self.stats["socks5"] += 1
            self._append_proxy(self.live_socks5, {3: "e", 2: "a"}.get(checker_proxy, "t"), host, port)

    async def fetch(self, *args) -> None:
        async with semaphore:
            checker_proxy = await checker_proxies.CheckerProxies(
                args[0], args[1], args[2], args[3], args[4], args[5], args[6]
            ).run()
            if checker_proxy in {1, 2, 3}:
                self.stats["live"] += 1
                self.stats[{3: "e", 2: "a"}.get(checker_proxy, "t")] += 1
                self.update_stats_proxy(args[6], args[0], args[1], checker_proxy)
            else:
                self.stats["die"] += 1
            self.stats["completed"] += 1
            self.messages.append(f"[bold bright_white]{args[0]}:{args[1]}")
            self.layout["t1"].update(DisplayProxies().generate_table(self.messages))
            self.layout["type_proxy"].update(DisplayProxies().update_type_proxy(self.stats["live"], self.stats["die"]))
            if len(args[7]) == 1:
                self.layout["type_anonymity"].update(DisplayProxies().update_type_anonymity(self.stats["e"], self.stats["t"], self.stats["a"]))
            else:
                self.layout["type_anonymity"].update(DisplayProxies().update_type_proxies(self.stats["http"], self.stats["socks4"], self.stats["socks5"]))
            self.overall_progress.update(self.overall_task, completed=self.stats["completed"])

    async def run(self):
        self.layout["progress_all"].update(self.progress_table)
        self.layout["f2"].update(self.performance_table)
        self.layout["k2"].update(self.internet_table)
        self.layout["k1"].update(self.panel_time)
        self.layout["header"].update(Header(self.args[5]))

        set_tasks: set = set()

        for proxy in self.files:
            for type_proxy in self.args[7]:
                if len(set_tasks) >= self.args[1]:
                    _done, set_tasks = await asyncio.wait(set_tasks, return_when=asyncio.FIRST_COMPLETED)
                    performance: tuple = DisplayProxies().get_progress_performance()
                    self.memory_progress.update(self.overall_task, completed=performance[0])
                    self.cpu_progress.update(self.overall_task, completed=performance[1])
                    self.internet_receive.update(
                        self.receive,
                        description=f"\n[bold yellow1][ [bold sky_blue1]SPEED [bold yellow1]] [bold violet"
                                    f"]{performance[3]}"
                    )
                    self.internet_send.update(
                        self.send,
                        description=f"\n[bold yellow1][ [bold sky_blue1]IN USE [bold yellow1]] [bold violet]"
                                    f"{performance[2]}"
                    )
                data_proxy: list = proxy.strip().split(':')
                set_tasks.add(asyncio.create_task(self.fetch(
                    data_proxy[0],
                    data_proxy[1],
                    self.args[2],
                    self.args[3],
                    self.args[4],
                    self.args[6],
                    type_proxy,
                    self.args[7]
                )))

        await asyncio.gather(*set_tasks)
        await asyncio.sleep(3)
        self.layout["progress_all"].update(home.DisplayHome().update_frame("[bold yellow1][ [bold spring_green2]COMPLETE PROCESS [bold yellow1]]"))
        await asyncio.sleep(5)
        if len(self.args[7]) == 1:
            return self.proxy_map.get(self.args[7][0])
        else:
            return self.live_http, self.live_socks4, self.live_socks5


