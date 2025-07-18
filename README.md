# select_options

select_options is a Python library for creating interactive selection menus in terminal applications. Designed for personal use, but open to proposals and contributions.

## Overview

A simple library to make a beautiful appearance on the console to select one or various options.

## Features

- Interactive selection menus
- Multiselect support
- Customizable prompts
- Adjustable columns (auto between 2-5, manual control planned)
- Limit selection in multiselect menus
- Future: color customization

## Installation

Install via pip:

```bash
pip install select_options
```

Or install from source:

```bash
git clone https://github.com/Gerry1402/select.git
cd select
pip install .
```

## Usage

For every type of iterable except `dict`, the menu shows the string representation of each item. If items are not stringifiable, use a `dict` where the key is the displayed content and the value is the result.

Example:

```python
from select_options import Select
options = ["Option 1", "Option 2", "Option 3"]

selected = Select(options, prompt="Choose an option")

single = selected.run()
print(f"You selected: {single_selected}")

select.prompt = "Choose one or various options"
selected.multiselect = True

multi = selected.run()

```

## Parameters

- **Title**: Purpose of the selection, instructions shown below the table.
- **Multiselect**: Allows multiple selections.
- **Limit**: Restricts the number of selections in multiselect menus.
- **Columns**: Auto-adjusts columns (2-5); manual control planned.

## Compatibility

Tested on Windows 11. Compatibility with other OS/environments is not guaranteed.

## Requirements

- Python >= 3.7
- textual

## License

MIT License

##

Gerard Vello  
Email: gerard.vello@gmail.com

---

## Roadmap

- Manual column control
- Color customization

## Screenshots
![Base color selection](image\README\1752244777712.png)
This is the base color for Multi-select and Single-select.

![Color of selected ones with current position over a selected](image\README\1752244868055.png)
This are the colors that appear on the Multi-select, the blue are the selected ones and the purple is the current position over a selected option.

Contributions, suggestions, and issues are welcome. Feel free to open a pull request or issue on GitHub.
