from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label
from textual import events
from .extra import calc_ideal_columns
from typing import Iterable, Any


class Select(App):
    CSS_PATH = "styles.tcss"

    def __init__(self, options: Iterable, prompt: str, multiselect: bool = False, limit: int | None = None, columns: int | None = None):
        super().__init__()

        if isinstance(options, dict):
            self.options: list = sorted(options.keys())
            self.values: list = [options[key] for key in self.options]
        elif isinstance(options, set):
            self.options: list = sorted(options)
        else:
            self.options: list = list(options)

        self.prompt: str = prompt
        self.limit: int = limit or len(self.options)
        self.columns: int = columns or calc_ideal_columns(len(self.options))
        self.multiselect: bool = multiselect
        self.selected: set[int] = set()
    
    @property
    def is_dict(self) -> bool:
        return hasattr(self, 'values')

    @property
    def current_index(self) -> int:
        return self.list_view.index or 0

    @current_index.setter
    def current_index(self, value: int):
        if value < 0:
            self.list_view.index = 0
        elif value >= len(self.list_view.children):
            self.list_view.index = len(self.list_view.children) - 1
        else:
            self.list_view.index = value

    def update_styles(self, *args, **kwargs):
        for i, item in enumerate(self.list_view.children):
            bg, fg, style = "#3B3B3B", "white", "none" # default

            if i == self.current_index and i in self.selected:
                bg, fg, style = "darkmagenta", "white", "bold"
            elif i == self.current_index:
                bg, fg, style = "darkred", "white", "bold"
            elif i in self.selected:
                bg, fg, style = "darkblue", "white", "bold"

            item.styles.background = bg
            item.styles.color = fg
            item.styles.text_style = style

    def get_results(self) -> list[Any] | Any | None:
        final_value = self.values if self.is_dict else self.options
        return [final_value[i] for i in sorted(self.selected)] if self.multiselect else final_value[self.current_index]

    async def on_key(self, event: events.Key) -> None:
        movements = {
            "up": -abs(self.columns - 1),
            "down": abs(self.columns - 1),
            "left": -1,
            "right": 1,
            "home": -self.current_index,
            "end": len(self.list_view.children) - 1,
        }
        self.current_index += movements.get(event.key, 0)

        if event.key == "space" and self.multiselect:
            if self.current_index in self.selected or len(self.selected) < self.limit:
                self.selected.symmetric_difference_update({self.current_index})

        elif event.key == "r":
            self.selected.clear()

        elif event.key == "escape":
            self.exit(None)
            return

        elif event.key in ("enter"):
            result = self.get_results()
            self.exit(result)
            return
        self.update_styles()

    def compose(self) -> ComposeResult:
        yield Label(f"{self.prompt}\n", expand=True)
        self.list_view = ListView(*[ListItem(Label(str(opt)))
                                  for opt in self.options])
        self.list_view.styles.grid_size_columns = self.columns
        self.list_view.styles.grid_columns = ("1fr " * self.columns).strip()
        yield self.list_view
        yield Label(f"\nNavigate with ↑, ↓, →, ←. {"Select and desselect with space. Restart options with \"R\"." if self.multiselect else ""} Click \"Enter\" to assign the value/s, (Esc) to not to.", expand=True)
        self.update_styles()  # Apply styles on startup

if __name__ == "__main__":

    options = { 
        f"Option {str(i).zfill(2)}": f"Value {str(i).zfill(2)}" for i in range(1, 41)
    }
    options = range(1, 41)  # Example options as a range
    # Example usage:
    # Multiselect
    selected_multi = Select(options, 'Select one or various  with space', multiselect=True, limit=3).run()
    print("Multi-selected:", selected_multi)
    # Single select
    selected_single = Select(options, 'Select an option').run()
    print("Single-selected:", selected_single)
