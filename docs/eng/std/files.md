# Library files 

Built-in library for working with the file system. 

## Import 

```tiger 
import files 
``` 

## Functions 

### files.create_dir(path) 
Creates a directory at the specified path. 

```tiger 
files.create_dir("my_folder") 
``` 

### files.create_file(path) 
Creates an empty file at the specified path. 

```tiger 
files.create_file("my_file.txt") 
``` 

### files.remove_dir(path) 
Deletes a directory at the specified path. 

```tiger 
files.remove_dir("old_folder") 
``` 

### files.remove_file(path) 
Deletes a file at the specified path. 

```tiger 
files.remove_file("old_file.txt") 
``` 

### files.list_dir(path) 
Returns a list of file and folder names within the specified directory. 

```tiger 
items = files.list_dir(".") 
for item in items: 
print(item) 
``` 

### files.read(path) 
Reads the contents of a file and returns a string. 

```tiger 
content = files.read("data.txt") 
print(content) 
``` 

### files.write(path, content) 
Writes a string to a file. 

```tiger 
files.write("output.txt", "Hello, World!") 
``` 

## Usage example 

```tiger 
import files 

# Create a folder structure 
files.create_dir("project") 
files.create_dir("project/src") 
files.create_dir("project/bin") 

# Create a configuration file 
files.write("project/config.txt", "debug=true") 

# Read the file 
config = files.read("project/config.txt") 
print(config) 

# List the contents 
items = files.list_dir("project") 
for item in items: 
print(item) 

# Cleanup 
files.remove_file("project/config.txt") 
files.remove_dir("project/src") 
files.remove_dir("project/bin") 
files.remove_dir("project") 
```