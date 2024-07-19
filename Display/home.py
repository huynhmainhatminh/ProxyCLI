from rich.layout import Layout
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich import box


class DisplayHome:
    def __init__(self) -> None:
        self.option_to_function = {
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
            "n1": "[bold yellow1][ [bold green_yellow]INFORMATION [bold yellow1]]",
            "n2": "[bold yellow1][ [bold green_yellow]TERMS OF USE [bold yellow1]]",
        }

        self.layout: Layout = self.make_layout_home()

    @classmethod
    def make_layout_home(cls) -> Layout:
        layout = Layout(name="root")

        layout.split_column(
            Layout(name="main", ratio=1),
            Layout(name="footer", size=10),
        )
        layout["main"].split_column(
            Layout(name="type_anonymity1"),
            Layout(name="type_anonymity2"),
            Layout(name="type_anonymity3"),
            Layout(name="type_anonymity4"),
        )
        layout["main"]["type_anonymity1"].split_row(
            Layout(name="func1"),
            Layout(name="func2"),
            Layout(name="func3"),
        )
        layout["main"]["type_anonymity2"].split_row(
            Layout(name="func4"),
            Layout(name="func5"),
            Layout(name="func6"),
        )
        layout["main"]["type_anonymity3"].split_row(
            Layout(name="func7"),
            Layout(name="func8"),
            Layout(name="func9"),
        )
        layout["main"]["type_anonymity4"].split_row(
            Layout(name="func10"),
            Layout(name="func11"),
            Layout(name="func12"),
        )
        layout["footer"].split_row(
            Layout(name="n1"),
            Layout(name="n2"),
        )
        return layout

    @classmethod
    def update_frame(cls, title_func: str) -> Panel:
        sponsor_message = Table.grid(padding=0)
        sponsor_message.add_column(style="green", justify="center")
        sponsor_message.add_row(title_func)

        additional_message = ""
        style = "bold medium_spring_green"
        padding = (1, 1)

        if "INFORMATION" in title_func:
            additional_message = (
                "\n[bold turquoise2]Author [bold yellow2]: [bold bright_cyan]Huỳnh Mai Nhật Minh\n"
                "[bold turquoise2]Telegram [bold yellow2]: [bold bright_cyan]https://t.me/MarkJethro"
            )
        elif "TERMS OF USE" in title_func:
            additional_message = (
                "\n[bold indian_red1]It's made for just testing purpose. We are not responsible for any abuse or damage caused by this program. Only for Educational Purpose. Thanks."
            )
        elif "COMPLETE PROCESS" in title_func:
            padding = (3, 3)
            style = "bold medium_spring_green"

        if additional_message:
            sponsor_message.add_row(additional_message)

        message_panel = Panel(
            Align.center(sponsor_message, vertical="top"),
            box=box.ROUNDED,
            padding=padding,
            style=style
        )
        return message_panel

    def update_layout(self) -> None:
        for option in self.option_to_function:
            self.layout[option].update(self.update_frame(self.option_to_function[option]))

    def run_display_home(self) -> Layout:
        self.update_layout()
        return self.layout
