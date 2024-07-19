from rich.console import Console

console = Console()


def logo():
    console.print('\t[bold white][bold yellow]© [bold cyan]Copyright By [bold red1]: [bold sky_blue2]Huỳnh Mai Nhật Minh [bold orange1]([bold green1]2005[bold orange1])')
    banner = """
        [bold cyan2]
        ███╗   ███╗██╗███╗   ██╗██╗  ██╗
        ████╗ ████║██║████╗  ██║██║  ██║
        ██╔████╔██║██║██╔██╗ ██║███████║
        ██║╚██╔╝██║██║██║╚██╗██║██╔══██║
        ██║ ╚═╝ ██║██║██║ ╚████║██║  ██║
        ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

                    [bold yellow]☢️  [bold yellow][[bold magenta] I AM ATOMIC [bold yellow]][bold white]"""
    console.print(banner, justify="center")
