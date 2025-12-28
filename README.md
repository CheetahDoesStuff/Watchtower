# Watchtower
A task manager & system monitor - done right

## Features
### Implemented features
* Resource usage (updating live)
* Disk space (Used and availble)
* List of all processes running (updates every second)
  * Show individual process resource usage
  * Ability to kill (nuke) any process
  * Advanced statistics on processes disk usage, uptime etc
  * Sorting the processlist by ram and cpu usage
  * Searching the processlist
* Customization through themes (config based)
* Config with a growing amount of values to configure

### Planned features
* last 24h/1w wrapped showing:
  * process with most instances
  * process with most cpu/ram usage
  * process with most read/write usage
  * how long your computer has been running
  * how many times youve opened watchtower
  * how long youve had watchtower open

## Installation
**Note: This will not work until the first release of watchtower, you can still manually install the source from the repo but i recommend you wait for a release!**
You can install it from pypi using a tool of your choice, some examples are:
* pip: `pip install watchtower`
* pipx: `pipx install watchtower`
* uv: `uv tool install watchtower`

then you can launch the app by running `watchtower` in your terminal!
**Note: launching through an application launcher / start menu is coming soon**

## Configuration
### Where are the config files?
The path can very depending on operating system, so to ensure that you have the right folder, launch watchtower through the terminal using `watchtower` after installation, this will log out the now created themes and config files.

### config.toml
Here is a full config.toml config with description on what everything means:
```toml
[misc]
default-sort = "cpu" # ram or cpu - the sorting option that will be set on startup
default-theme = "Modern" # must be one of the themes in themes.toml - theme to be loaded on startup
```
**More configuration will come as i add more features, so dont worry that its not that much yet!**

### themes.toml
The themes file will automatically add the 2 default themes ("Modern" and "Modern (Light)") if the themes.toml file doesnt exist or is empty.
Lets have a look at one of the default themes and what the different colors represent:
```toml
["Modern"]
bg = "#191c24" # Background of the window(s)
fg-1 = "#1F232D" # Foreground 1 - Background of the windows different sections
fg-2 = "#242935" # Foreground 2 - Background of the Meters, Processes, Buttons and Searchbars inside a section
fg-3 = "#2A2F3C" # Foreground 3 - Background of the handle in the process sections scrollbar
text = "hsl(0, 0%, 75%)" # Color of most of the text
text-header = "hsl(0, 0%, 85%)" # Color of the bigger text in Meters and Topbars
border = "rgb(46, 50, 66)" # Border of almost everything
button-bg = "rgb(44, 50, 63)" # Background of buttons in the process elements (except the NUKE button)
button-kill-bg = "#a32626" # Color of the NUKE button
bar-meter = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(230,120,120), stop:1 rgb(231,89,236))" # Color of the filled part in the meters, by default a nice gradient yoinked from my website, ch0.dev
```
