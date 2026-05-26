# Библиотека cli

Встроенная библиотека для работы с аргументами командной строки и цветным выводом.

## Импорт

```tiger
import cli
```

## Работа с аргументами

### cli.get(key, default)
Возвращает строковое значение аргумента по ключу. Если аргумент не найден, возвращает значение по умолчанию.

```tiger
var name: string = cli.get("name", "default")
```

### cli.get_int(key, default)
Возвращает целочисленное значение аргумента по кключу. Если аргумент не найден, возвращает значение по умолчанию.

```tiger
var count: int = cli.get_int("count", 3)
```

### cli.has(key)
Проверяет наличие аргумента. Возвращает `true`, если аргумент передан.

```tiger
if cli.has("verbose"):
    print("Verbose mode enabled")
```

### cli.is_help()
Проверяет, передан ли флаг помощи (`-h` или `--help`).

```tiger
if cli.is_help():
    cli.help("prog", "[options]")
```

## Цветной вывод

### cli.success(msg)
Выводит сообщение зеленым цветом (успех).

```tiger
cli.success("Operation completed!")
```

### cli.info(msg)
Выводит сообщение синим цветом (информация).

```tiger
cli.info("Loading data...")
```

### cli.warning(msg)
Выводит сообщение желтым цветом (предупреждение).

```tiger
cli.warning("This is a warning")
```

### cli.error(msg)
Выводит сообщение красным цветом (ошибка) в stderr.

```tiger
cli.error("Something went wrong!")
```

### cli.debug(msg)
Выводит сообщение серым цветом (отладка). Отображается только при наличии флага `-v` или `--verbose`.

```tiger
cli.debug("Variable x = 42")
```

## Справка

### cli.help(prog_name, usage)
Выводит справочное сообщение о программе.

```tiger
cli.help("myprogram", "[--name=<name>] [--count=<num>]")
```

Вывод:
```
Usage: myprogram [--name=<name>] [--count=<num>]

Options:
  -h, --help     Show this help message
  -v, --verbose  Enable debug output
```

## Пример использования

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

Запуск программы:
```bash
./program --name Alice --count 5 -v    # debug виден с -v
./program --help
```