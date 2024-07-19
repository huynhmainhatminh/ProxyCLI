from data.display_proxies import *
from collections import deque
from data.checker_api import CheckAPI
from aiohttp import ClientSession, TCPConnector
from Display import home
import time


class CheckerFraudScore:
    def __init__(self, list_proxy: list[str], layout: Layout) -> None:
        self.list_proxy = list_proxy
        self.messages = deque(maxlen=height - 13)
        self.messages_time = deque(maxlen=height - 13)
        self.layout = layout

        self.internet_send = Progress("{task.description}", TextColumn(""))
        self.send = self.internet_send.add_task(
            "\n[bold yellow1][ [bold sky_blue1]IN USE [bold yellow1]] ", vertical="top"
            )

        self.internet_receive = Progress("{task.description}", TextColumn(""))
        self.receive = self.internet_receive.add_task(
            "\n[bold yellow1][ [bold sky_blue1]SPEED [bold yellow1]] ",
            vertical="top"
            )

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
        self.internet_table.add_row(
            Panel(
                Group(self.cpu_progress, self.internet_receive), border_style="bold medium_spring_green",
                padding=(1, 1), )
            )

        self.memory_progress = Progress(
            "{task.description}",
            BarColumn(style="bold spring_green2"),
            TextColumn("[progress.percentage][bold violet]{task.percentage:>3.0f}%"),
        )
        self.memory_progress.add_task(
            "[bold yellow1][ [bold sky_blue1]MEMORY [bold yellow1]]", total=100,
            vertical="top"
            )

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
            "[bold yellow1][ [bold sky_blue1]ALL JOBS [bold yellow1]]", total=len(self.list_proxy)
        )

        self.progress_table = Table.grid(expand=True)
        self.progress_table.add_row(
            Panel(
                self.overall_progress,
                border_style="bold medium_spring_green",
                padding=(3, 3),
            )
        )

        self.stats = {
            "h": 0, "m": 0, "l": 0, "completed": 0,
        }

    async def fetch(self, host: str, port: str, session) -> None:
        async with semaphore:
            checker_proxy = await CheckAPI(host, session).fetch_fraud_score()
            if checker_proxy in {1, 2, 3}:
                self.stats[{3: "h", 2: "m"}.get(checker_proxy, "l")] += 1
            self.stats["completed"] += 1
            self.messages.append(f"[bold bright_white]{host}:{port}")
            self.messages_time.append(f"[bold bright_white]{time.asctime()}")
            self.layout["t1"].update(DisplayProxies().generate_table(self.messages))
            self.layout["info_settings"].update(DisplayProxies().generate_table_time(self.messages_time))
            self.layout["type_anonymity"].update(
                DisplayProxies().update_type_score(self.stats["h"], self.stats["m"], self.stats["l"])
                )
            self.overall_progress.update(self.overall_task, completed=self.stats["completed"])

    async def run(self):
        self.layout["progress_all"].update(self.progress_table)
        self.layout["f2"].update(self.performance_table)
        self.layout["k2"].update(self.internet_table)
        self.layout["k1"].update(self.panel_time)
        self.layout["header"].update(Header("CHECKER FRAUD SCORE"))

        set_tasks: set = set()
        async with ClientSession(connector=TCPConnector(limit=50)) as session:
            for proxy in self.list_proxy:
                if len(set_tasks) >= 5000:
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
                set_tasks.add(asyncio.create_task(self.fetch(data_proxy[0], data_proxy[1], session,)))
            await asyncio.gather(*set_tasks)
            await asyncio.sleep(3)
            self.layout["progress_all"].update(
                home.DisplayHome().update_frame("[bold yellow1][ [bold spring_green2]COMPLETE PROCESS [bold yellow1]]")
                )
            await asyncio.sleep(5)
