import sys
import pathlib
import os
import json
from i2c_handler import I2C_Trinity
from rich.console import Console
from rich import print


i2c = I2C_Trinity(1)

class MainMenu:
    def __init__(self):
        self.console = Console()
        self.config_path = os.path.join(pathlib.Path(__file__).parent.resolve(),'config.json')
        self.load_config()

    def start(self):
        while(1):
            options_name = ["start_test", "setup_count", "setup_interval", "exit_program"]
            options_function = [self.start_test, self.setup_count, self.setup_interval, self.exit_program]

            os.system('clear')
            print(f"  [bold green]Current Config[/bold green]")
            print(f"[bold cyan]Count[/bold cyan]          : [bold magenta]{self.count}[/bold magenta]")
            print(f"[bold cyan]Interval (sec)[/bold cyan] : [bold magenta]{self.interval}[/bold magenta]")
            print()

            self.console.print("[bold]Menu options_name:[/bold]")
            for i, option in enumerate(options_name):
                self.console.print(f"  {i}. [cyan]{option}[/cyan]")
            user_option = self.get_user_choice(0, len(options_name) - 1)
            selected_function = options_function[user_option]
            selected_function()

    def get_user_choice(self, lower_bound=0, upper_bound=0, is_having_boundary=True):
        while True:
            try:
                if is_having_boundary:
                    prompt = f"Enter your choice ({lower_bound}-{upper_bound}): "
                else:
                    prompt = "Enter your choice: "

                choice = int(input(prompt))

                if not is_having_boundary or (lower_bound <= choice <= upper_bound):
                    return choice
                else:
                    print("[bold red]Invalid choice.[/bold red]")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def load_config(self):
        f = open(self.config_path)
        data_dict = json.loads(f.read())
        self.count = data_dict["count"]
        self.interval = data_dict["interval"] 

    def save_config(self, var_name, value):
        f = open(self.config_path)
        data_dict = json.loads(f.read())
        data_dict[var_name] = value

        with open(self.config_path, 'w') as f:
            json.dump(data_dict, f)

    def start_test(self):
        os.system('clear')

    def setup_count(self):
        os.system('clear')
        print("[cyan]Enter the interval (in seconds) between each sensor data:[/cyan]")
        self.count = self.get_user_choice(is_having_boundary=False)
        self.save_config("count", self.count)
        self.start()

    def setup_interval(self):
        os.system('clear')
        print("[cyan]Enter the quantity of data points: [/cyan]")
        self.interval = self.get_user_choice(is_having_boundary=False)
        self.save_config("interval", self.interval)
        self.start()

    def exit_program(self):
        os.system('clear')
        print("[bold green]Goodbye![/bold green] \U0001F60A")
        sys.exit()

def main():
    main_menu = MainMenu()
    main_menu.start()

if __name__ == '__main__':
    main()