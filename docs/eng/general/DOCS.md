# Tiger Language - Full Documentation 

> Transpiler version: **tiger v0.4.3** 
> Target language: **C++20** (compiler: g++ / MinGW-w64) 
> File extension: `.tgr` 
--- 

## Contents 

1. [What is Tiger](#1-what-is-tiger) 
2. [Run and compile](#2-run-and-compile) 
3. [Program structure](#3-program-structure) 
4. [Comments](#4-comments) 
5. [Data types](#5-data-types) 
6. [Variables](#6-variables) 
7. [Operators](#7-operators) 
8. [Lines and str.*](#8-rows-and-str) 
9. [Input and output](#9-input-and-output) 
10. [Conditions: if / elif / else](#10-conditions-if--elif--else) 
11. [Loops: while](#11-loops-while) 
12. [Cycles: for](#12-cycles-for) 
13. [Functions](#13-functions) 
14. [Lists](#14-lists) 
14.1 [Dictionaries (dict)](#141-dictionaries-dict) 
15. [Global variables](#15-global-variables) 
16. [Built-in http module](#16-built-in-module-http) 
17. [Built-in gui module](#17-built-in-gui module) 
17.1 [Advanced GUI with color and positioning](#171-advanced-gui-with-color-and-positioning-v04) 
18. [Built-in module random](#18-built-in-module-random) 
19. [Built-in time module](#19-built-in-time module) 
20. [Important nuances and limitations](#20-important-nuances-and-limitations) 
21. [Complete example programs](#21-complete-example-programs) 

--- 

## 1. What is Tiger 

Tiger is a compiled programming language with a syntax similar to Python and JavaScript. The `.tgr` source code is transpiled to C++ and then compiled by `g++` into a native `.exe` executable (Windows) or binary (Linux/Mac).
**Philosophy of language:** 
- Simple, readable syntax without unnecessary symbols 
- Static compilation - the result works without an interpreter 
- Types are inferred automatically - it is not necessary to write `int`, `string`, etc., although it is possible for debugging. 
- Everything that can be done in C++ can be expressed in Tiger 

--- 

## 2. Launch and compilation 

### Installation 

To work you need Python 3.9+ and the g++ compiler (MinGW-w64 on Windows). 

``` 
python tiger.py <file.tgr> [options] 
``` 

### Command line options 

| Option | Description | 
|-------|----------| 
| `-o <path>` | Output executable file name | 
| `--emit-cpp` | Stop after generating `.cpp`, do not compile | 
| `--cpp-out <f>` | Specify a name for the `.cpp` file | 
| `-I <dir>` | Add a folder to search for `.tgr` modules | 
| `-v` / `--verbose` | Detailed output of each step | 

### Call examples 

```bash 
# Compile hello.tgr to hello.exe 
python tiger.py hello.tgr 

# Specify the output file name 
python tiger.py hello.tgr -o myapp.exe 

# Only generate C++, do not compile 
python tiger.py hello.tgr --emit-cpp 

# View all steps 
python tiger.py hello.tgr -v 

# Add modules folder 
python tiger.py main.tgr -I ./libs 
``` 

--- 

## 3. Program structure 

Tiger supports two programming styles. 

### Style 1: With main() function - recommended 

```tiger 
# Helper functions are declared before main 
greet(name) { 
print("Hello, " + name + "!") 
} 

main() { 
greet("peace") 
} 
``` 

The `main()` function is the entry point. Everything in it is executed at startup. 

### Style 2: Script - no main()
```tiger 
var x = 10 
var y = 20 
print("Amount: " + str.to_str(x + y)) 
``` 

In scripting style, top-level operators (except `var` and functions) are executed sequentially in the generated `main()`. However, **variables at the top level become global** and are accessible from functions. 

### Order of sections in the file 

``` 
[global variables] ← var outside functions 
[functions] ← any functions except main 
[main()] ← entry point (optional) 
``` 

--- 

## 4. Comments 

Tiger only supports single-line comments: 

```tiger 
# This is a comment 

var x = 5 # comment at the end of the line 

# A multiline "block" is just a few lines with # 
# Each line starts with a hash 
# Multiline /* */ no comments 
``` 

`//` also works (C++ syntax): 

```tiger 
// This is also a comment - works the same as # 
var y = 10 // end of line 
``` 

--- 

## 5. Data types 

Tiger supports static typing. Types can be specified explicitly or omitted for automatic inference. 

### Basic types 

| Type | Syntax | Description | 
|-----|-----------|----------| 
| `int` | `var x: int = 42` | Integers | 
| `float` | `var y: float = 3.14` | Fractional numbers (in C++: `double`) | 
| `string` | `var s: string = "hello"` | Strings | 
| `bool` | `var flag: bool = true` | Boolean values ​​| 
| `null` | `var n: null = null` | No value | 
| `list` | `var lst: list = [1, 2, 3]` | Lists (default `vector<double>`) | 
| `list[T]` | `var nums: list[int]` | List with element type |
| `dict` | `var cfg: dict = {"key": 1}` | Dictionaries (`map<string, any>` in C++) | 

### Explicitly specifying types (recommended) 

```tiger 
var age: int = 25 
var price: float = 99.99 
var name: string = "Tiger" 
var active: bool = true 

var numbers: list = [1, 2, 3, 4, 5] 
var empty_list: list = [] 
``` 

### Automatic type inference (without specifying) 

```tiger 
var x = 42 # int - automatic 
var y = 3.14 # float - automatic 
var s = "hello" # string - automatically 
``` 

### Integers (int) 

```tiger 
var a = 42 
var b = -7 
var c = 1000000 
``` 

### Fractional numbers (float / double) 

```tiger 
var pi = 3.14159 
var temperature = -12.5 
var rate = 0.01 
``` 

> **Note:** The number `1.` (with a dot without digits after) is NOT a float - the lexer does not recognize such a record. Always write at least one character after the period: `1.0` 

### Strings 

```tiger 
var name = "Ivan" 
var greeting = 'Hello!' # single quotes work too 
var empty = "" 
``` 

Escaping inside strings: 

| Sequence | Symbol | 
|-----------|--------| 
| `\n` | New line | 
| `\t` | Tab | 
| `\r` | Carriage return | 
| `\\` | Backslash | 
| `\"` | Double quote | 
| `\'` | Single quote | 

```tiger 
var msg = "Line 1\nLine 2" 
var path = "C:\\Users\\Ivan" 
var quote = "He said: \"hello\"" 
``` 

### Boolean values (bool) 

```tiger 
var flag = true 
var done = false 
``` 

Keywords: `true` and `false` (lowercase). 

### Null 

```tiger 
var result = null 
``` 

Used as no value. In C++ it is transpiled to `nullptr`.
> **Caveat:** `null` cannot be compared to strings or numbers - only use it to check for `== null`. 

--- 

## 6. Variables 

### Announcement 

Variables are declared using the `var` keyword: 

```tiger 
# Without type - automatic output 
var x = 10 
var name = "Tiger" 
var active = true 

# With an explicit type - static typing 
var count: int = 10 
var price: float = 99.99 
var message: string = "Hello" 
var flag: bool = true 
var items: list = [1, 2, 3] 
``` 

### Reassignment 

There is no need for `var` after the declaration: 

```tiger 
var score = 0 
score = 100 
score = score + 50 
``` 

### Compound assignment operators 

```tiger 
varn = 10 
n += 5 # n = n + 5 → 15 
n -= 3 # n = n - 3 → 12 
n *= 2 # n = n * 2 → 24 
n /= 4 # n = n / 4 → 6 
``` 

### Scope 

- A variable declared inside a function is **local**, visible only in this function. 
- A variable declared **outside all functions** is **global**, visible everywhere. 

```tiger 
var global_count = 0 # global - visible in increment() and main() 

increment() { 
global_count += 1 # change the global variable 
} 

main() { 
increment() 
increment() 
print(str.to_str(global_count)) # will print: 2 
} 
``` 

--- 

## 7. Operators 

### Arithmetic 

| Operator | Description | Example | 
|----------|----------|--------| 
| `+` | String addition/concatenation | `5 + 3` → `8` | 
| `-` | Subtraction/unary minus | `10 - 4` → `6` | 
| `*` | Multiplication | `3 * 4` → `12` | 
| `/` | Division | `10 / 4` → `2.5` | 
| `%` | Remainder of division | `10% 3` → `1` | 

### Comparisons 

| Operator | Description |
|----------|----------| 
| `==` | Equals | 
| `!=` | Not equal | 
| `<` | Less | 
| `<=` | Less than or equal to | 
| `>` | More | 
| `>=` | Greater than or equal to | 

```tiger 
var a = 5 
var b = 10 
print(a < b) # true 
print(a == 5) # true 
print(a != b) # true 
``` 

### Logical 

| Operator | Description | Example | 
|----------|----------|--------| 
| `and` | Logical AND | `true and false` → `false` | 
| `or` | Logical OR | `true or false` → `true` | 
| `not` | Logical NOT | `not true` → `false` | 

```tiger 
var age = 25 
var has_id = true 

if (age >= 18 and has_id) { 
print("Access granted") 
} 
``` 

### String concatenation 

The `+` operator joins strings. To add a number, you must first convert it: 

```tiger 
var score = 42 
print("Score: " + str.to_str(score)) # correct 
# print("Score: " + score) # compilation error! 
``` 

### Operator precedence (highest to lowest) 

``` 
not (unary) 
*/% 
+ - 
< <= > >= 
== != 
and 
or 
``` 

--- 

## 8. Strings and str.* 

The `str` module contains built-in functions for working with strings. Called via a dot: `str.function(arguments)`. 

### str.len(s) — string length 

```tiger 
var s = "Hello" 
var n = str.len(s) 
print(str.to_str(n)) # 6 
``` 

### str.to_str(x) - number → string 

```tiger 
var pi = 3.14 
var text = "Pi equals " + str.to_str(pi) 
print(text) # Pi is 3.140000 
``` 

Works with both `int` and `float`. 

### str.to_int(s) — string → integer 

```tiger 
var s = "42" 
var n = str.to_int(s) 
print(str.to_str(n + 8)) # 50 
```
> **Tip:** If the string is not a valid number, the program will fail at runtime. Validate user input before conversion. 

### str.to_float(s) — string → fractional number 

```tiger 
var s = input("Enter a number: ") 
var x = str.to_float(s) 
print("Doubled: " + str.to_str(x * 2.0)) 
``` 

### str.upper(s) — to uppercase 

```tiger 
var s = "hello" 
print(str.upper(s)) # HELLO 
``` 

> **Note:** Works correctly only for Latin letters (ASCII). Cyrillic is not converted - C++ `std::toupper` limitation. 

### str.lower(s) — to lower case 

```tiger 
var s = "WORLD" 
print(str.lower(s)) # world 
``` 

> Same restrictions on Cyrillic as `str.upper`. 

### Full table str.* 

| Function | Arguments | Returns | Example | 
|---------|----------|------------|--------| 
| `str.len(s)` | string | int | `str.len("hi")` → `2` | 
| `str.to_str(x)` | int or float | string | `str.to_str(3.14)` → `"3.140000"` | 
| `str.to_int(s)` | string | int | `str.to_int("5")` → `5` | 
| `str.to_float(s)` | string | float | `str.to_float("1.5")` → `1.5` | 
| `str.upper(s)` | string | string | `str.upper("hi")` → `"HI"` | 
| `str.lower(s)` | string | string | `str.lower("HI")` → `"hi"` | 
| `str.trim(s)` | string | string | `str.trim(" hi ")` → `"hi"` | 
| `str.split(s)` | string | list of strings | `str.split("a,b,c")` → `["a", "b", "c"]` | 
| `str.startswith(s, prefix)` | string, prefix | bool | `str.startswith("hello", "he")` → `true` |
| `str.endswith(s, suffix)` | string, suffix | bool | `str.endswith("hello", "lo")` → `true` | 

--- 

## 9. Input and output 

### print() - output 

```tiger 
print("Hello world!") # string 
print(42) # number 
print(3.14) # fractional 
print(true) # boolean 
print() # empty line (just a line break) 
``` 

Multiple arguments are separated by a space: 

```tiger 
var name = "Ivan" 
var age = 30 
print("Name:", name, "Age:", age) 
# → Name: Ivan Age: 30 
``` 

To print a string and a number together, use concatenation: 

```tiger 
varn = 100 
print("Result: " + str.to_str(n)) # Result: 100 
``` 

> **Tip:** `print` always adds a newline at the end. Inference without wrapping is not possible in the current version of the language. 

### input() - keyboard input 

```tiger 
var name = input("What is your name?") 
print("Hello, " + name + "!") 
``` 

Without an argument - reads without a hint: 

```tiger 
var line = input() 
``` 

Important: `input()` **always returns a string**. To work with numbers, use conversion: 

```tiger 
var age_str = input("Your age: ") 
var age = str.to_int(age_str) 

if (age >= 18) { 
print("Adult") 
} else { 
print("Minor") 
} 
``` 

--- 

## 10. Conditions: if / elif / else 

### Basic form 

```tiger 
if (condition) { 
# body 
} 
``` 

### With else 

```tiger 
var x = 10 

if (x > 0) { 
print("Positive") 
} else { 
print("Zero or negative") 
} 
``` 

### With elif 

```tiger 
var score = 75 

if (score >= 90) { 
print("Excellent") 
} elif (score >= 70) {
print("Okay") 
} elif (score >= 50) { 
print("Satisfactory") 
} else { 
print("Unsatisfactory") 
} 
``` 

The number of `elif` is not limited. 

### Nested conditions 

```tiger 
var x = 5 
var y = 10 

if (x > 0) { 
if (y > 0) { 
print("Both positive") 
} else { 
print("x is positive, y is not") 
} 
} else { 
print("x is not positive") 
} 
``` 

### Important rules 

1. Parentheses around the condition are **required**: `if (x > 0)` - correct, `if x > 0` - parser error. 
2. Curly braces `{}` are always required, even for a single statement. 
3. `elif` and `else` must come **immediately after** the closing `}` of the previous block. 

```tiger 
# CORRECT: 
if (x > 0) { 
print("yes") 
} elif (x == 0) { 
print("zero") 
} else { 
print("no") 
} 

# WRONG - else on a separate line after the empty line 
if (x > 0) { 
print("yes") 
} 

else { # ← the parser will not find a connection with if 
print("no") 
} 
``` 

--- 

## 11. Loops: while 

The only type of loop in Tiger is `while`. 

### Basic form 

```tiger 
var i = 0 
while (i < 5) { 
print(str.to_str(i)) 
i += 1 
} 
# will output: 0, 1, 2, 3, 4 
``` 

### Infinite loop with exit via flag 

```tiger 
var running = true 

while (running) { 
var choice = input("Enter 'q' to exit: ") 
if (choice == "q") { 
running = false 
} else { 
print("You entered: " + choice) 
} 
} 
``` 

### Loop with counter down 

```tiger 
varn = 10 
while (n > 0) { 
print(str.to_str(n)) 
n -= 1 
} 
print("Start!") 
``` 

### Nested loops 

```tiger 
var i = 1 
while (i <= 3) { 
var j = 1 
while (j <= 3) {
print(str.to_str(i) + " x " + str.to_str(j) + " = " + str.to_str(i * j)) 
j += 1 
} 
i += 1 
} 
``` 


> **Tip:** There are no `break` or `continue` in Tiger. To exit the loop, use the flag variable `running = false` or `return` inside the function. 

--- 

## 12. Loops: for 

A for loop allows you to iterate through the elements of a list or dictionary. 

### Syntax 

```tiger 
for (item in collection) { 
# loop body 
} 
``` 

### Examples 

```tiger 
# Iterate through the list 
var nums = [1, 2, 3, 4, 5] 
for (n in nums) { 
print(str.to_str(n)) 
} 
# will output: 1 2 3 4 5 

# Iterate through a string character by character 
var text = "hello" 
for (ch in text) { 
print(ch) 
} 
``` 

### Limitations 

- The `for` loop works with: lists, strings, function calls (returning a list/string) 
- For dictionaries you can use `for (key in dict)` - it will enumerate by keys 

--- 

## 13. Functions 

### Announcement 

Functions can have explicit parameter and return types: 

```tiger 
# No types (dynamic typing) 
greet(name) { 
print("Hello, " + name + "!") 
} 

# With types (static typing) 
add(a: int, b: int): int { 
return a + b 
} 

multiply(x: float, y: float): float { 
return x * y 
} 

getName(): string { 
return "Tiger" 
} 
``` 

### Challenge 

```tiger 
var result = add(3, 4) # result = 7 
greet("World") # will output: Hello World! 
print(str.to_str(multiply(2.5, 4.0))) # 10 
``` 

### Challenge 

```tiger 
var result = add(3, 4) # result = 7 
greet("World") # will output: Hello World! 
``` 

### Return value 

```tiger 
max(a, b) { 
if (a > b) { 
return a 
}
return b 
} 

main() { 
var m = max(10, 25) 
print(str.to_str(m)) # 25 
} 
``` 

A function without `return` returns nothing (void in C++). You cannot call it as an expression. 

### Function without parameters 

```tiger 
say_hello() { 
print("Hello!") 
} 

main() { 
say_hello() 
} 
``` 

### Recursion 

```tiger 
factorial(n) { 
if (n <= 1) { 
return 1 
} 
return n * factorial(n - 1) 
} 

main() { 
print(str.to_str(factorial(6))) # 720 
} 
``` 

### Important rules 

1. Functions cannot be declared inside other functions (nested functions are prohibited). 
2. Function parameters do not have a type - they take any value. 
3. The function must be **declared before it is called**. The order of the file is important: auxiliary functions are above `main()`. 
4. `main()` is a special function. The transpiler turns it into `int main()` C++. 

--- 

## 14. Lists 

A list is an ordered collection of elements of the same type. 

### Creation 

```tiger 
var nums = [1, 2, 3, 4, 5] 
var words = ["apple", "banana", "cherry"] 
var empty = [] 
var floats = [1.0, 2.5, 3.7] 
``` 

### Access by index 

Indexes start with `0`: 

```tiger 
var fruits = ["apple", "banana", "cherry"] 
print(fruits[0]) # apple 
print(fruits[2]) # cherries 
``` 

### Changing an element 

```tiger 
var nums = [10, 20, 30] 
nums[1] = 99 
print(str.to_str(nums[1])) # 99 
``` 

###List length 

```tiger 
var nums = [1, 2, 3, 4, 5] 
var n = str.len(str.to_str(nums[0])) # not for lists! 
``` 

> **Note:** Lists do not have a built-in `.len()` method. To determine the length, you need to store it in a separate variable or calculate it manually.
### Iterate through the list 

```tiger 
var nums = [10, 20, 30, 40, 50] 
var i = 0 
var total = 0 
while (i < 5) { # 5 - manual length 
total += nums[i] 
i += 1 
} 
print("Amount: " + str.to_str(total)) # 150 
``` 

### Lists as parameters 

```tiger 
sum_list(lst, size) { 
var total = 0 
var i = 0 
while (i < size) { 
total += lst[i] 
i += 1 
} 
return total 
} 

main() { 
var nums = [1, 2, 3, 4, 5] 
var s = sum_list(nums, 5) 
print(str.to_str(s)) # 15 
} 
``` 

### List restrictions 

- All elements must be of the same type (more precisely, C++ must output `std::common_type`). 
- A list of strings and a list of numbers cannot be mixed: `[1, "hello"]` is a compilation error. 
- There are no built-in methods `.push()`, `.pop()`, `.append()` - in the current version the lists are of a fixed size. 

--- 

## 14.1 Dictionaries (dict) 

A dictionary is a collection of key-value pairs. Keys must be strings, values ​​can be of any type. 

### Creation 

```tiger 
var config = {"port": 8080, "timeout": 30} 
var empty = {} 
``` 

> **Note:** In the current version, dictionary values must be numbers (int/float). String values ​​are not supported - the dictionary is translated to `std::map<std::string, double>`. 

### Accessing elements 

```tiger 
var config = {"host": "localhost", "port": 8080} 
print(config["host"]) # localhost 
print(config["port"]) # 8080 
``` 

### Automatically change and add elements 
```tiger 
var counts = {"zen1": 0, "zen2": 0} 
counts["zen1"] = 1 # change existing key
counts["zen3"] = 2 # add new key 
``` 

### Dictionary restrictions 
- Keys must be strings 
- Values must be numbers (float/double) - string values are not supported 
- In C++ it is translated to `std::map<std::string, double>` 
- Nested dictionaries are not supported - value must be a number 

--- 

## 15. Global variables 

A variable declared **outside of any function** is global. It is visible in all file functions. 

### Announcement 

```tiger 
var counter = 0 # global int 
var app_name = "Tiger" # global string 
var pi = 3.14159 # global double 
var debug = false # global bool 
``` 

### Reading and changing from functions 

```tiger 
var score = 0 

add_score(points) { 
score += points # change the global variable directly 
} 

reset_score() { 
score = 0 
} 

main() { 
add_score(10) 
add_score(25) 
print("Score: " + str.to_str(score)) # 35 
reset_score() 
print("After reset: " + str.to_str(score)) # 0 
} 
``` 

### How global variables are transpiled 

Tiger turns top-level `vars' into true C++ global variables: 

```tiger 
var x = 42 
var name = "Tiger" 
``` 

→ generated in C++ as: 

```cpp 
int x = 42; 
std::string name = std::string("Tiger"); 
``` 

These variables live throughout the program's execution. 

### Global Variable Type Table 

| Tiger | C++ type | 
|-------|---------| 
| `var x = 42` | `int` | 
| `var x = 3.14` | `double` | 
| `var x = "hello"` | `std::string` | 
| `var x = true` | `bool` | 
| `var x = null` | `void*` |
| `var x = [1,2,3]` | `std::vector<double>` | 
| `var x` (no value) | `double` | 

> **Note:** A global variable fixes the type when declared. You cannot declare `var x = 0` (int) and then assign `x = "hello"` (string) - this is a C++ compilation error. 

> **Tip:** If a global variable is initialized with a complex expression (function call, arithmetic), the type is automatically inferred as `double`. This is the safe default for numerical calculations. 

--- 

## 16. Importing modules 

### Built-in modules 

```tiger 
import http # HTTP client 
import gui # window GUI (Windows only) 
``` 

### Import .tgr files 

```tiger 
import utils # includes utils.tgr from the same folder 
import math_ext # includes math_ext.tgr 
``` 

The functions from `utils.tgr` become available in your file. 

**Import rules for .tgr:** 
- The file is searched first in the folder of the current file, then in the folders from `-I`. 
- The `main()` function in the imported file is **ignored** - you only include auxiliary functions. 
- Cyclic imports (`A` imports `B`, `B` imports `A`) **prohibited** - the transpiler will throw an error. 
- Each file is imported only once, even if multiple files reference it. 

### Example: Modularization 

**math_utils.tgr:** 
```tiger 
abs_val(x) { 
if (x < 0) { 
return -x 
} 
return x 
} 

power(base, exp) { 
var result = 1 
var i = 0 
while (i < exp) { 
result = result * base 
i += 1 
} 
return result 
} 
``` 

**main.tgr:** 
```tiger 
import math_utils 

main() { 
print(str.to_str(abs_val(-5))) # 5
print(str.to_str(power(2, 8))) # 256 
} 
``` 

Compilation: 
```bash 
python tiger.py main.tgr -o program.exe 
``` 

--- 


## 17. Important nuances and limitations 

### Static typing (v0.3+) 

Tiger supports static typing - compile-time type checking. 

#### Advantages: 
- Type errors are found before the program starts 
- Explicit types make the code self-documenting 
- More efficient C++ code is generated 

#### Typing syntax: 

```tiger 
# Variables 
var x: int = 10 
var name: string = "Tiger" 

# Functions 
add(a: int, b: int): int { 
return a + b 
} 

# Without specifying types - dynamic typing 
var y = 20 
``` 

#### Typing errors: 

```tiger 
var x: int = "hello" # ERROR: cannot assign string to int 
``` 

### No break and continue 

To exit the loop, use the flag: 

```tiger 
var found = false 
var i = 0 
while (i < 10 and not found) { 
if (nums[i] == target) { 
found = true 
} 
i += 1 
} 
``` 

### No nested functions 

```tiger 
outer() { 
inner() { # ← ERROR: nested functions are not allowed 
print("nested") 
} 
} 
``` 

### No try/catch 

There is no exception handling. If `str.to_int("abc")` the program will crash with a C++ error. 

### print always adds \n 

You cannot display text without a line feed. 

###Order of functions is important 

The function must be declared above the call location. There are no automatic forward declarations. 

```tiger 
# CORRECT: 
helper() { 
print("helper") 
} 

main() { 
helper() # helper declared above 
} 

# WRONG: 
main() { 
helper() # helper declared BELOW - compilation error 
} 

helper() {
print("helper") 
} 
``` 

--- 

## 18. Complete sample programs 

### Example 1: Guess the number (with typing) 

```tiger 
main() { 
var secret: int = 42 
var attempts: int = 0 
var won: bool = false 

print("Guess a number from 1 to 100!") 

while (not won) { 
var guess_str = input("Your guess: ") 
var guess = str.to_int(guess_str) 
attempts += 1 

if (guess < secret) { 
print("Too little!") 
} elif (guess > secret) { 
print("Too much!") 
} else { 
won = true 
print("Correct! Attempts: " + str.to_str(attempts)) 
} 
} 
} 
``` 

--- 

### Example 2: Calculator with memory (global variable) 

```tiger 
var memory = 0.0 

calculate(a, b, op) { 
if (op == "+") { return a + b } 
elif (op == "-") { return a - b } 
elif (op == "*") { return a * b } 
elif(op == "/") { 
if (b == 0.0) { 
print("Division by zero!") 
return 0.0 
} 
return a/b 
} 
return 0.0 
} 

show_menu(mem) { 
print("") 
print("=== Calculator ===") 
print("1. Fold") 
print("2. Subtract") 
print("3. Multiply") 
print("4. Divide") 
print("5. M+ (save)") 
print("6. MR (memory: " + str.to_str(mem) + ")") 
print("7. MC (reset)") 
print("0. Exit") 
} 

main() { 
var running = true 

while (running) { 
show_menu(memory) 
var choice = input("> ") 

if (choice == "0") { 
running = false
} elif (choice == "1" or choice == "2" or choice == "3" or choice == "4") { 
var a = str.to_float(input("First number: ")) 
var b = str.to_float(input("Second number: ")) 

var op = "+" 
if (choice == "2") { op = "-" } 
elif (choice == "3") { op = "*" } 
elif (choice == "4") { op = "/" } 

var res = calculate(a, b, op) 
print("= " + str.to_str(res)) 

} elif (choice == "5") { 
var a = str.to_float(input("First: ")) 
var b = str.to_float(input("Second: ")) 
var op = input("Operator: ") 
memory = calculate(a, b, op) 
print("Saved: " + str.to_str(memory)) 

} elif (choice == "6") { 
print("Memory: " + str.to_str(memory)) 

} elif (choice == "7") { 
memory = 0.0 
print("Memory reset") 
} 
} 

print("Goodbye!") 
} 
``` 

--- 

### Example 3: Multiplication tables 

```tiger 
print_row(n) { 
var j = 1 
while (j <= 10) { 
var product = n * j 
print(str.to_str(n) + " x " + str.to_str(j) + " = " + str.to_str(product)) 
j += 1 
} 
} 

main() { 
var n_str = input("Multiplication table for the number: ") 
var n = str.to_int(n_str) 
print_row(n) 
} 
``` 

--- 

### Example 4: Recursion - Fibonacci numbers 

```tiger 
fib(n) { 
if (n <= 0) { return 0 } 
if (n == 1) { return 1 } 
return fib(n - 1) + fib(n - 2) 
} 

main() { 
var i = 0 
while (i <= 10) {
print("fib(" + str.to_str(i) + ") = " + str.to_str(fib(i))) 
i += 1 
} 
} 
``` 

--- 

### Example 5: Working with a list 

```tiger 
find_max(lst, size) { 
var max = lst[0] 
var i = 1 
while (i < size) { 
if (lst[i] > max) { 
max = lst[i] 
} 
i += 1 
} 
return max 
} 

sum_list(lst, size) { 
var total = 0.0 
var i = 0 
while (i < size) { 
total += lst[i] 
i += 1 
} 
return total 
} 

main() { 
var nums = [3.0, 7.0, 1.0, 9.0, 4.0, 6.0, 2.0, 8.0, 5.0] 
var size = 9 

var max = find_max(nums, size) 
var total = sum_list(nums, size) 

print("Maximum: " + str.to_str(max)) 
print("Amount: " + str.to_str(total)) 
print("Average: " + str.to_str(total / size)) 
} 
``` 

--- 

### Example 6: Modular program (multiple files) 

**string_utils.tgr:** 
```tiger 
# Repeats a line n times 
repeat(s, n) { 
var result = "" 
var i = 0 
while (i < n) { 
result = result + s 
i += 1 
} 
return result 
} 

# Frame of characters 
border(width, ch) { 
return repeat(ch, width) 
} 
``` 

**main.tgr:** 
```tiger 
import string_utils 

print_box(text) { 
var line = border(str.len(text) + 4, "=") 
print(line) 
print("| " + text + " |") 
print(line) 
} 

main() { 
print_box("Greetings from Tiger!") 
print_box("The language works!") 
} 
``` 

```bash 
python tiger.py main.tgr -o demo.exe 
``` 

--- 

### Example 7: Global event counter 

```tiger 
var event_count = 0 
var last_event = "no" 

log_event(name) { 
event_count += 1 
last_event = name
print("[" + str.to_str(event_count) + "] " + name) 
} 

show_stats() { 
print("Total events: " + str.to_str(event_count)) 
print("Last: " + last_event) 
} 

main() { 
log_event("Launch") 
log_event("Initialization") 
log_event("Loading data") 
log_event("Done") 
print("") 
show_stats() 
} 
``` 

Conclusion: 
``` 
[1] Launch 
[2] Initialization 
[3] Loading data 
[4] Done 

Total events: 4 
Latest: Done 
``` 

--- 

### Example 8: Working with a dictionary 

```tiger 
main() { 
var counts = {"zen1": 1, "zen2": 1, "zen3": 1} 
print("Counts: " + str.to_str(counts["zen1"])) 
}