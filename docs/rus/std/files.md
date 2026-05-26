# Библиотека files

Встроенная библиотека для работы с файловой системой.

## Импорт

```tiger
import files
```

## Функции

### files.create_dir(path)
Создаёт директорию по указанному пути.

```tiger
files.create_dir("my_folder")
```

### files.create_file(path)
Создаёт пустой файл по указанному пути.

```tiger
files.create_file("my_file.txt")
```

### files.remove_dir(path)
Удаляет директорию по указанному пути.

```tiger
files.remove_dir("old_folder")
```

### files.remove_file(path)
Удаляет файл по указанному пути.

```tiger
files.remove_file("old_file.txt")
```

### files.list_dir(path)
Возвращает список имён файлов и папок внутри указанной директории.

```tiger
items = files.list_dir(".")
for item in items:
    print(item)
```

### files.read(path)
Читает содержимое файла и возвращает строку.

```tiger
content = files.read("data.txt")
print(content)
```

### files.write(path, content)
Записывает строку в файл.

```tiger
files.write("output.txt", "Hello, World!")
```

## Пример использования

```tiger
import files

# Создаём структуру папок
files.create_dir("project")
files.create_dir("project/src")
files.create_dir("project/bin")

# Создаём файл конфигурации
files.write("project/config.txt", "debug=true")

# Читаем файл
config = files.read("project/config.txt")
print(config)

# Перечисляем содержимое
items = files.list_dir("project")
for item in items:
    print(item)

# Очистка
files.remove_file("project/config.txt")
files.remove_dir("project/src")
files.remove_dir("project/bin")
files.remove_dir("project")
```