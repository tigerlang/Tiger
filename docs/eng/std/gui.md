# gui library 

Creates native Windows windows via WinAPI. Windows only. 

## Import 

```tiger 
import gui 
``` 

## Basic functions 

### gui.window(title, width, height) 

Creates a window with a title and dimensions in pixels. 

###gui.button(text) 

Adds a button to a window. The buttons are positioned vertically in 40px increments, starting from coordinates (20, 20). 

###gui.label(text) 

Adds a text label to the window. 

```tiger 
gui.label("Hello world!") 
``` 

###gui.entry(name) 

Adds a text input field. 

```tiger 
gui.entry("username") 
``` 

###gui.run() 

Starts the message processing loop. The program will stop here until the window closes. 

> **Note:** GUI functions only work after calling `gui.window()`. 

## Advanced GUI with color and positioning 

### Colored widgets 

In addition to the basic `gui.button()` and `gui.label()` functions, advanced color functions are available: 

```tiger 
gui.button_colored(text, bgColor, textColor, callback) 
gui.label_colored(text, textColor, bgColor) 
``` 

**Colors (strings):** 
- `"white"`, `"black"`, `"red"`, `"green"`, `"blue"` 
- `"yellow"`, `"cyan"`, `"magenta"`, `"gray"`, `"orange"` 

```tiger 
import gui 

main() { 
gui.window("Colored App", 400, 300) 
gui.label_colored("Hello!", "red", "white") 
gui.button_colored("Click", "blue", "white", handleClick) 
gui.run() 
} 
``` 

### Positioning widgets 

For precise positioning, use functions with explicit coordinates: 

```tiger 
gui.button_ex(x, y, width, height, text, bgColor, textColor, callback) 
gui.label_ex(x, y, width, height, text, textColor, bgColor) 
``` 

```tiger 
import gui 

main() { 
gui.window("Positioned", 500, 400) 

# Button at coordinates (50, 50) size 120x40 
gui.button_ex(50, 50, 120, 40, "OK", "green", "white", handleOk) 

# Label at coordinates (50, 120) 
gui.label_ex(50, 120, 200, 30, "Status: ready", "blue", "white") 

gui.run() 
} 
``` 

### Callbacks for buttons 

Buttons can perform a function when clicked via a callback: 

```tiger 
import gui 

handleClick() { 
print("Button pressed!") 
} 

main() { 
gui.window("Callback Demo", 300, 200) 
gui.button_colored("Press me", "blue", "white", handleClick) 
gui.run() 
} 
``` 

## Complete list of GUI functions 

| Function | Options | Description | 
|---------|----------|----------| 
| `gui.window(title, w, h)` | title, width, height | Creates a window | 
| `gui.button(text)` | text | Adds a button (default) | 
| `gui.label(text)` | text | Adds a label (default) | 
| `gui.entry(name)` | name | Input field | 
| `gui.run()` | — | Starts a message loop | 
| `gui.button_colored(t, bg, fg, cb)` | text, bgColor, textColor, callback | Colored button | 
| `gui.label_colored(t, fg, bg)` | text, textColor, bgColor | Color mark | 
| `gui.button_ex(x,y,w,h,t,bg,fg,cb)` | coordinates, sizes, colors | Position button | 
| `gui.label_ex(x,y,w,h,t,fg,bg)` | coordinates, sizes, colors | Label with position |