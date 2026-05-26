# cli library 

Built-in library for working with command line arguments and color output. 

## Import 

```tiger 
import cli 
``` 

## Working with arguments 

### cli.get(key, default) 
Returns the string value of the argument by key. If the argument is not found, returns the default value. 

```tiger 
var name: string = cli.get("name", "default") 
``` 

### cli.get_int(key, default) 
Returns the integer value of the key argument. If the argument is not found, returns the default value. 

```tiger 
var count: int = cli.get_int("count", 3) 
``` 

###cli.has(key) 
Checks for the presence of an argument. Returns `true` if an argument is passed. 

```tiger 
if cli.has("verbose"): 
print("Verbose mode enabled") 
``` 

### cli.is_help() 
Checks whether a help flag has been passed (`-h` or `--help`). 

```tiger 
if cli.is_help(): 
cli.help("prog", "[options]") 
``` 

## Color output 

###cli.success(msg) 
Displays a message in green (success). 

```tiger 
cli.success("Operation completed!") 
``` 

### cli.info(msg) 
Displays a message in blue (information). 

```tiger 
cli.info("Loading data...") 
``` 

### cli.warning(msg) 
Displays a message in yellow (warning). 

```tiger 
cli.warning("This is a warning") 
``` 

###cli.error(msg) 
Prints a message in red (error) to stderr. 

```tiger 
cli.error("Something went wrong!") 
``` 

###cli.debug(msg) 
Displays the message in gray (debugging). Displayed only if the `-v` or `--verbose` flag is present. 

```tiger 
cli.debug("Variable x = 42") 
``` 

## Help 

### cli.help(prog_name, usage) 
Displays a help message about the program. 

```tiger 
cli.help("myprogram", "[--name=<name>] [--count=<num>]") 
``` 

Conclusion: 
``` 
Usage: myprogram [--name=<name>] [--count=<num>] 

Options: 
-h, --help Show this help message 
-v, --verbose Enable debug output 
``` 

## Usage example 

```tiger 
import cli 

var name: string = cli.get("name", "default") 
var count: int = cli.get_int("count", 3) 

if cli.is_help() { 
cli.help("program", "[--name=<name>] [--count=<num>]") 
exit(0) 
} 
cli.success("Hello from Tiger!") 
cli.info("Loading data...") 

if cli.has("verbose") { 
cli.info("Name: " + name + ", Count: " + str.to_str(count)) 
} 
cli.warning("This is a warning") 
cli.error("Something went wrong!") 
cli.debug("Debug info (only with -v)") 
``` 

Launching the program: 
```bash 
./program --name Alice --count 5 -v # debug visible with -v 
./program --help 
```