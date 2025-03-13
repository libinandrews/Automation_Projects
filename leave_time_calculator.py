# -*- coding: utf-8 -*-
"""
Author: Libin Andrews

This tool calculates future times based on a given start time and a list of time additions.
It also determines the elapsed time since a specified log time.
Formatted output is provided using the Rich library for better readability.
"""

from datetime import datetime, timedelta
from rich.console import Console
from rich.align import Align
from typing import List, Tuple

class TimeCalculator:
    """Handles time calculations including addition and elapsed time."""
    
    @staticmethod
    def add_time(hours: int, minutes: int, add_hours: int = 0, add_minutes: int = 0) -> str:
        """Adds hours and minutes to a given time."""
        initial_time = datetime.strptime(f"{hours}:{minutes}", "%H:%M")
        new_time = initial_time + timedelta(hours=add_hours, minutes=add_minutes)
        return new_time.strftime("%I:%M %p")

    @staticmethod
    def time_elapsed_since(hours: int, minutes: int) -> Tuple[int, int]:
        """Calculates time elapsed since a given hour and minute."""
        now = datetime.now()
        initial_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        
        if now < initial_time:
            initial_time -= timedelta(days=1)
        
        elapsed_time = now - initial_time
        elapsed_hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        elapsed_minutes, _ = divmod(remainder, 60)
        return int(elapsed_hours), int(elapsed_minutes)

class ConsolePrinter:
    """Handles console output formatting using rich."""
    
    def __init__(self) -> None:
        self.console = Console()
    
    def print_time_addition(self, h: int, m: int, times_to_add: List[Tuple[int, int]]) -> None:
        """Prints time calculations for added hours and minutes."""
        for add_hours, add_minutes in times_to_add:
            new_time = TimeCalculator.add_time(h, m, add_hours, add_minutes)
            if add_hours == 9 and add_minutes == 36:
                self._print_important(f"{add_hours} hours {add_minutes} min from {h}:{m} is [bold yellow]{new_time}[/bold yellow]")
            else:
                self._print_normal(f"{add_hours} hours {add_minutes} min from {h}:{m} is [bold yellow]{new_time}[/bold yellow]")
    
    def print_elapsed_time(self, h: int, m: int) -> None:
        """Prints elapsed time since a given hour and minute."""
        elapsed_hours, elapsed_minutes = TimeCalculator.time_elapsed_since(h, m)
        self._print_normal(f"Time since log is [bold yellow]{elapsed_hours} hours and {elapsed_minutes} minutes[/bold yellow]")
    
    def _print_normal(self, text: str) -> None:
        self.console.print(Align.center(f"[bold]{text}[/bold]"))
    
    def _print_important(self, text: str) -> None:
        self.console.print(Align.center(f"[bold red]{text}[/bold red]"))

def main() -> None:
    """Main function to execute the time calculations and display results."""
    h, m = 9, 30
    times_to_add = [(7, 10), (8, 0), (9, 0), (9, 36), (10, 0)]
    
    printer = ConsolePrinter()
    print("-" * 50 + " Start of Tool " + "-" * 50)
    printer.print_time_addition(h, m, times_to_add)
    printer.print_elapsed_time(h, m)
    print("\n" + "-" * 50 + " End of Tool " + "-" * 50)

if __name__ == "__main__":
    main()
