import asyncio
import json
import psutil
import datetime
import os
from rich.layout import Layout
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich import box
from datetime import datetime
from itertools import cycle
from rich.text import Text
from rich.console import Group
from rich.progress import (
    BarColumn, Progress, SpinnerColumn, TimeRemainingColumn,
    MofNCompleteColumn, TimeElapsedColumn, TextColumn, ProgressColumn
)

height = os.get_terminal_size()[1]
semaphore = asyncio.Semaphore(1500)


class SynchronizedEmojiColumn(ProgressColumn):
    def __init__(self):
        super().__init__()
        self.emojis = cycle(["ʕ•ﻌ•ʔ", "ʕ•ᴥ<ʔ", "ʕ>ᴥ•ʔ", "ʕ>ᴥ<ʔ", "ʕ♥ᴥ♥ʔ"])
        self.current_emoji = next(self.emojis)
        self.last_update = 0

    def render(self, task):
        elapsed_seconds = int(task.elapsed)
        if elapsed_seconds > self.last_update:
            self.current_emoji = next(self.emojis)
            self.last_update = elapsed_seconds
        text = Text(
            f"[ {self.current_emoji} ]",
            style="bold yellow1"
        )
        text.stylize("bold sky_blue1", 2, 3 + len(self.current_emoji))
        return text


class Header:

    def __init__(self, name_title: str):
        self.name_title = name_title

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            f"[bold salmon1]{self.name_title}", f"[bold magenta1]{datetime.now().ctime()}",
        )
        return Panel(grid, border_style="bold medium_spring_green")


class DisplayProxies:
    def __init__(self) -> None:
        self.layout: Layout = self.make_layout_home()
        self.max_cpu_freq = psutil.cpu_freq().max / 1000
        self.count_cpu = psutil.cpu_count(logical=True)
        self.json_file = open("data/settings.json")
        self.json_data = json.load(self.json_file)

    def get_progress_performance(self) -> tuple:
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        composite_metric = round((memory_percent * self.count_cpu) / 100, 2)

        return (
            memory_percent,
            composite_metric,
            f"{memory.used / (1024 ** 3):.2f}/{memory.total / (1024 ** 3):.2f} GB",
            f"{composite_metric * self.max_cpu_freq / self.count_cpu:.2f}/{self.max_cpu_freq:.2f} GHz",
        )

    @staticmethod
    def make_layout_api() -> Layout:
        layout = Layout(name="root")

        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=9),
        )
        layout["main"].split_row(
            Layout(name="side"),
            Layout(name="body", ratio=2, minimum_size=60),
        )
        layout["footer"].split_row(
            Layout(name="type_anonymity"),
            Layout(name="progress_all", ratio=2, minimum_size=50),
        )
        layout["main"]["side"].split_column(
            Layout(name="info_settings"),
        )
        layout["main"]["body"].split_row(
            Layout(name="t1"),
            Layout(name="t2"),
        )
        layout["main"]["body"]["t2"].split_column(
            Layout(name="f1"),
            Layout(name="f2", size=7),
        )
        layout["main"]["body"]["t2"]["f1"].split_column(
            Layout(name="k1"),
            Layout(name="k2"),
        )
        return layout

    @staticmethod
    def make_layout_home() -> Layout:
        layout = Layout(name="root")

        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=9),
        )
        layout["main"].split_row(
            Layout(name="side"),
            Layout(name="body", ratio=2, minimum_size=60),
        )
        layout["footer"].split_row(
            Layout(name="type_anonymity"),
            Layout(name="progress_all", ratio=2, minimum_size=50),
        )
        layout["main"]["side"].split_column(
            Layout(name="info_settings"),
            Layout(name="type_proxy", size=7),
        )
        layout["main"]["body"].split_row(
            Layout(name="t1"),
            Layout(name="t2"),
        )
        layout["main"]["body"]["t2"].split_column(
            Layout(name="f1"),
            Layout(name="f2", size=7),
        )
        layout["main"]["body"]["t2"]["f1"].split_column(
            Layout(name="k1"),
            Layout(name="k2"),
        )
        return layout

    def update_info_settings(self) -> Panel:

        sponsor_message = Table.grid(padding=1)
        sponsor_message.add_column(style="green", justify="left")
        sponsor_message.add_column(no_wrap=False)
        sponsor_message.add_row(
            "[bold turquoise2]THREADS[bold yellow2]:", f'[bold violet]{str(self.json_data["threads"])}'
        )
        sponsor_message.add_row(
            "[bold turquoise2]TIMEOUT[bold yellow2]:", f'[bold violet]{str(self.json_data["timeout"])}'
        )
        sponsor_message.add_row(
            "[bold turquoise2]RETRIES[bold yellow2]:", f'[bold violet]{str(self.json_data["retries"])}'
        )
        sponsor_message.add_row(
            "[bold turquoise2]URLS[bold yellow2]:", f'[bold dark_slate_gray2]{str(self.json_data["urls"])}'
        )
        if str("keywords") in str(self.json_data):
            sponsor_message.add_row(
                "[bold turquoise2]KEYWORDS[bold yellow2]:", f'[bold spring_green2]TRUE'
            )
        else:
            sponsor_message.add_row(
                "[bold turquoise2]KEYWORDS[bold yellow2]:", f'[bold deep_pink2]FALSE'
            )

        message = Table.grid(padding=0)
        message.add_column()
        message.add_column(no_wrap=False)
        message.add_row(sponsor_message)

        message_panel = Panel(
            Align.left(sponsor_message, vertical="top"),
            box=box.ROUNDED,
            padding=(1, 2),
            title="[bold yellow1][ [bold sky_blue1]SETTING CHECKER [bold yellow1]]",
            border_style="bold medium_spring_green",
        )
        return message_panel

    @staticmethod
    def update_type_anonymity(elite: int = 0, transparent: int = 0, anonymous: int = 0) -> Panel:
        sponsor_message = Table.grid(padding=1)
        sponsor_message.add_column(style="green", justify="left")
        sponsor_message.add_column(no_wrap=False)
        sponsor_message.add_row(
            "[bold turquoise2]ELITE[bold yellow2]:", f'[bold violet]{str(elite)}'
        )
        sponsor_message.add_row(
            "[bold turquoise2]TRANSPARENT[bold yellow2]:", f'[bold violet]{str(transparent)}'
        )
        sponsor_message.add_row(
            "[bold turquoise2]ANONYMOUS[bold yellow2]:", f'[bold violet]{str(anonymous)}'
        )

        message = Table.grid(padding=0)
        message.add_column()
        message.add_column(no_wrap=False)
        message.add_row(sponsor_message)

        message_panel = Panel(
            Align.left(sponsor_message, vertical="top", ),
            box=box.ROUNDED,
            padding=(1, 2),
            border_style="bold medium_spring_green",
        )
        return message_panel

    @staticmethod
    def update_type_proxies(count_http: int = 0, count_socks4: int = 0, count_socks5: int = 0) -> Panel:
        sponsor_message = Table.grid(padding=1)
        sponsor_message.add_column(style="green", justify="left")
        sponsor_message.add_column(no_wrap=False)
        sponsor_message.add_row(
            "[bold turquoise2]PROXIES HTTP/s[bold yellow2]:", f'[bold violet]{str(count_http)}'
        )
        sponsor_message.add_row(
            "[bold turquoise2]PROXIES SOCKS4[bold yellow2]:", f'[bold violet]{str(count_socks4)}'
        )
        sponsor_message.add_row(
            "[bold turquoise2]PROXIES SOCKS5[bold yellow2]:", f'[bold violet]{str(count_socks5)}'
        )

        message = Table.grid(padding=0)
        message.add_column()
        message.add_column(no_wrap=False)
        message.add_row(sponsor_message)

        message_panel = Panel(
            Align.left(sponsor_message, vertical="top", ),
            box=box.ROUNDED,
            padding=(1, 2),
            border_style="bold medium_spring_green",
        )
        return message_panel

    @staticmethod
    def update_type_score(h: int = 0, m: int = 0, l: int = 0) -> Panel:
        sponsor_message = Table.grid(padding=1)
        sponsor_message.add_column(style="green", justify="left")
        sponsor_message.add_column(no_wrap=False)
        sponsor_message.add_row(
            "[bold red1]HIGH[bold yellow2]:", f'[bold violet]{str(h)}'
        )
        sponsor_message.add_row(
            "[bold yellow1]MODERATE[bold yellow2]:", f'[bold violet]{str(m)}'
        )
        sponsor_message.add_row(
            "[bold medium_spring_green]LOW[bold yellow2]:", f'[bold violet]{str(l)}'
        )

        message = Table.grid(padding=0)
        message.add_column()
        message.add_column(no_wrap=False)
        message.add_row(sponsor_message)

        message_panel = Panel(
            Align.left(sponsor_message, vertical="top", ),
            box=box.ROUNDED,
            padding=(1, 2),
            border_style="bold medium_spring_green",
        )
        return message_panel

    @staticmethod
    def update_type_none() -> Panel:
        sponsor_message = Table.grid(padding=1)
        sponsor_message.add_column(style="green", justify="left")
        sponsor_message.add_column(no_wrap=False)
        sponsor_message.add_row(
            "[bold turquoise2]NONE[bold yellow2]:", f'[bold violet]0'
        )
        sponsor_message.add_row(
            "[bold turquoise2]NONE[bold yellow2]:", f'[bold violet]0'
        )
        sponsor_message.add_row(
            "[bold turquoise2]NONE[bold yellow2]:", f'[bold violet]0'
        )

        message = Table.grid(padding=0)
        message.add_column()
        message.add_column(no_wrap=False)
        message.add_row(sponsor_message)

        message_panel = Panel(
            Align.left(sponsor_message, vertical="top", ),
            box=box.ROUNDED,
            padding=(1, 2),
            border_style="bold medium_spring_green",
        )
        return message_panel

    @staticmethod
    def update_type_proxy(live: int = 0, die: int = 0):
        sponsor_message = Table.grid(padding=1)
        sponsor_message.add_column(style="green", justify="left")
        sponsor_message.add_column(no_wrap=False)
        sponsor_message.add_row(
            "[bold spring_green2]LIVE PROXIES[bold yellow2]:", f'[bold violet]{str(live)}'
        )
        sponsor_message.add_row(
            "[bold deep_pink2]DIED PROXIES[bold yellow2]:", f'[bold violet]{str(die)}'
        )

        message = Table.grid(padding=1)
        message.add_column()
        message.add_column(no_wrap=False)
        message.add_row(sponsor_message)

        message_panel = Panel(
            Align.left(sponsor_message, vertical="top", ),
            box=box.ROUNDED,
            padding=(1, 2),
            border_style="bold medium_spring_green",
        )
        return message_panel

    @staticmethod
    def generate_table(rows) -> Panel:
        table_string = "\n".join([str(row) for row in rows])
        message_panel = Panel(
            table_string,
            padding=1,
            border_style="bold medium_spring_green",
            title=f"[bold yellow1][ [bold sky_blue1]PROCESSES [bold yellow1]]"
        )
        return message_panel

    @staticmethod
    def generate_table_time(rows) -> Panel:
        table_string = "\n".join([str(row) for row in rows])
        message_panel = Panel(
            table_string,
            padding=1,
            border_style="bold medium_spring_green",
            title=f"[bold yellow1][ [bold sky_blue1]TIME PROCESSES[bold yellow1]]"
        )
        return message_panel

    def run_display_https(self):

        self.layout["info_settings"].update(self.update_info_settings())
        self.layout["type_anonymity"].update(self.update_type_none())
        self.layout["type_proxy"].update(self.update_type_proxy())
        return self.layout
