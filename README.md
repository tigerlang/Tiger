# Tiger Programming Language

> **Version 0.4.3** – A simple, compiled language with Python‑like syntax that transpiles to C++.

Tiger is a statically typed (but optionally) language designed for small to medium scripts and GUI applications.  
Your `.tgr` source is translated to C++20 and then compiled into a native executable.

---

## ✨ Features

- **Familiar syntax** – like Python but with optional braces and parentheses.
- **Static typing** (optional) – use `x: int = 5` for early error detection.
- **Built‑in modules** – `http` (Windows), `gui` (Windows), `random`, `time`, `files`, `cli`.
- **Lists & dictionaries** – `[1,2,3]` and `{"key": value}` (any value type).
- **For loops** – `for item in collection` over lists, strings and dict keys.
- **No complex setup** – one Python script + g++ produces an `.exe`.

---

## 🚀 Quick Start

### 1. Install dependencies

- **Python 3.9+**  
- **g++** (MinGW‑w64 on Windows, GCC on Linux/Mac)

### 2. Write `hello.tgr`

```tiger
main() {
    print("Hello, Tiger!")
}
```

### 3. Compile and run

```bash
python tiger.py hello.tgr
./hello
```

Output: `Hello, Tiger!`

---

## 📘 Basic Syntax

### Variables

```tiger
var x = 10                # inferred integer
var name: string = "Tiger"  # explicit type
var pi = 3.14             # float
var active = true
```

### Functions

```tiger
add(a: int, b: int): int {
    return a + b
}

main() {
    var result = add(3, 4)   # 7
    print(str.to_str(result))
}
```

### Conditionals & Loops

```tiger
if score >= 90 {
    print("Excellent")
} elif score >= 60 {
    print("Pass")
} else {
    print("Fail")
}

var i = 0
while i < 5 {
    print(str.to_str(i))
    i += 1
}

for item in ["apple", "banana"] {
    print(item)
}
```

### Lists & Dictionaries

```tiger
var nums = [1, 2, 3]
nums[1] = 99

var config = {"host": "localhost", "port": 8080}
print(config["host"])
```

---

## 📦 Standard Library

| Module    | Functions (examples)                                 |
|-----------|------------------------------------------------------|
| `str`     | `len()`, `to_str()`, `to_int()`, `trim()`, `split()`|
| `http`    | `get(url)`, `post(url, data)`, `get_status(url)`    |
| `gui`     | `window()`, `button()`, `label()`, `entry()`, `run()`|
| `random`  | `randint()`, `int_range()`, `float_range()`, `seed()`|
| `time`    | `now()`, `date()`, `sleep(ms)`, `timestamp()`        |
| `files`   | `read()`, `write()`, `create_dir()`, `list_dir()`    |
| `cli`     | `get()`, `has()`, `success()`, `error()`, `help()`   |

Example using `files`:

```tiger
import files

main() {
    files.write("data.txt", "Hello")
    var content = files.read("data.txt")
    print(content)
}
```

---

## 🧪 More Examples

### Guess the number

### GUI window (Windows only)

```tiger
import gui

handleClick() {
    print("Button clicked!")
}

main() {
    gui.window("My App", 400, 300)
    gui.button_colored("Click me", "blue", "white", handleClick)
    gui.run()
}
```

---

## ⚙️ Compiler Options

```bash
python tiger.py source.tgr -o output.exe   # set output name
python tiger.py source.tgr --emit-cpp      # only generate .cpp
python tiger.py source.tgr -I ./libs       # add import search path
python tiger.py source.tgr -v              # verbose output
```

---

## ⚠️ Notes

- Tiger **requires `g++`** (MinGW on Windows) – no other compiler is supported.
- The `gui` module works **only on Windows** (uses WinAPI).
- No `break`/`continue` – use flag variables to exit loops.
- Functions must be declared **before** they are called.
- For full details, see the `DOCS.md` file included in the SDK.

---

## 📄 License

Tiger is free to use under the MIT License.
