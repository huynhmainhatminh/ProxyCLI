import keyboard
from Display import home
from Display import selecte_home
from rich.live import Live
from Clear import clear_display


def main():
    clear_display.ClearDisplay().clear()
    layout_home = home.DisplayHome().run_display_home()
    selecte_home.SelecteHome(layout_home, live=None).highlight_selected()
    with Live(layout_home, refresh_per_second=1000) as live:
        try:
            keyboard.on_press(selecte_home.SelecteHome(layout_home, live).handle_key_press)
            keyboard.wait("esc")
        except(KeyboardInterrupt, ):
            pass


if __name__ == '__main__':
    main()
