from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label
from textual import events
from .extra import calc_ideal_columns


class Select(App):
    CSS = """
    Screen { align: center middle; }
    ListView {
        width: 100%;
        height: auto;
        max-height: 80%;
        background: #222222;
    }
    Label {
        text-align: center;
        width: 100%;
    }
    ListView {
        height: auto;
        layout: grid;
        grid-gutter: 1 2;
        padding: 1 2;
        background: #222222;
    }
    ListItem {
        min-height: 3;
        color: #ccccff;
        align: center middle;
        background: #222222;
        padding: 0 1;
    }
    ListItem:focus {
        background: orange;
        color: black;
    }
    .selected {
        color: black;
        text-style: bold;
        background: red;
    }
    .selected Label:focus, ListItem:focus.selected Label {
        background: yellow;
        color: black;
        text-style: bold;
    }
    """

    def __init__(self, options: list[str] | dict, title: str, multiselect: bool = False, limit: int | None = None):
        super().__init__()
        self.OPTIONS: list[str] = options if isinstance(
            options, list) else sorted(list(options.keys()))
        if isinstance(options, dict):
            self.VALUES = [options[key] for key in self.OPTIONS]
        self.is_dict: bool = isinstance(options, dict)
        self.title: str = title
        self.limit: int = limit if limit is not None else len(self.OPTIONS)
        self.columns: int = calc_ideal_columns(len(self.OPTIONS))
        self.rows: int = (len(self.OPTIONS) // self.columns) + (1 if len(self.OPTIONS) % self.columns > 0 else 0)
        self.selected: set[int] = set()
        self.multiselect: bool = multiselect

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

    async def on_key(self, event: events.Key) -> None:
        movements = {
            "up": -abs(self.columns - 1),
            "down": abs(self.columns - 1),
            "left": -1,
            "right": 1,
            "home": 0,
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
            if self.is_dict:
                result = [self.VALUES[i] for i in sorted(self.selected)] if self.multiselect else self.VALUES[self.current_index]
            else:
                result = sorted(self.selected) if self.multiselect else self.current_index
            self.exit(result)
            return
        self.update_styles()

    def compose(self) -> ComposeResult:
        yield Label(f"{self.title}\n", expand=True)
        self.list_view = ListView(*[ListItem(Label(opt))
                                  for opt in self.OPTIONS])
        self.list_view.styles.grid_size_columns = self.columns
        self.list_view.styles.grid_columns = ("1fr " * self.columns).strip()
        yield self.list_view
        yield Label(f"\nNavigate with ↑, ↓, →, ←. {"Select and desselect with space. Restart options with \"R\"." if self.multiselect else ""} Click enter to assign the value/s, (Esc) to not to.", expand=True)
        self.update_styles()  # Apply styles on startup

if __name__ == "__main__":

    options = ["holaaa"]*12
    # Example usage:
    # Multiselect
    selected_multi = Select(options, 'Select one or various  with space', multiselect=True, limit=3).run()
    print("Multi-selected:", selected_multi)
    # Single select
    selected_single = Select(options, 'Select an option').run()
    print("Single-selected:", selected_single)
