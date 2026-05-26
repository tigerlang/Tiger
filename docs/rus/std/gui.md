# Библиотека gui

Создаёт нативные Windows-окна через WinAPI. Только Windows.

## Импорт

```tiger
import gui
```

## Базовые функции

### gui.window(title, width, height)

Создаёт окно с заголовком и размерами в пикселях.

### gui.button(text)

Добавляет кнопку в окно. Кнопки располагаются вертикально с шагом 40px, начиная от координаты (20, 20).

### gui.label(text)

Добавляет текстовую метку в окно.

```tiger
gui.label("Привет, мир!")
```

### gui.entry(name)

Добавляет поле ввода текста.

```tiger
gui.entry("username")
```

### gui.run()

Запускает цикл обработки сообщений. Программа остановится здесь до закрытия окна.

> **Нюанс:** GUI-функции работают только после вызова `gui.window()`.

## Расширенный GUI с цветом и позиционированием

### Цветные виджеты

Помимо базовых функций `gui.button()` и `gui.label()`, доступны расширенные функции с цветом:

```tiger
gui.button_colored(text, bgColor, textColor, callback)
gui.label_colored(text, textColor, bgColor)
```

**Цвета (строки):**
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

### Позиционирование виджетов

Для точного позиционирования используйте функции с явными координатами:

```tiger
gui.button_ex(x, y, width, height, text, bgColor, textColor, callback)
gui.label_ex(x, y, width, height, text, textColor, bgColor)
```

```tiger
import gui

main() {
    gui.window("Positioned", 500, 400)
    
    # Кнопка в координатах (50, 50) размером 120x40
    gui.button_ex(50, 50, 120, 40, "OK", "green", "white", handleOk)
    
    # Метка в координатах (50, 120)
    gui.label_ex(50, 120, 200, 30, "Status: ready", "blue", "white")
    
    gui.run()
}
```

### Обратные вызовы (callback) для кнопок

Кнопки могут выполнять функцию при нажатии через callback:

```tiger
import gui

handleClick() {
    print("Кнопка нажата!")
}

main() {
    gui.window("Callback Demo", 300, 200)
    gui.button_colored("Press me", "blue", "white", handleClick)
    gui.run()
}
```

## Полный список функций GUI

| Функция | Параметры | Описание |
|---------|-----------|----------|
| `gui.window(title, w, h)` | title, width, height | Создаёт окно |
| `gui.button(text)` | text | Добавляет кнопку (по умолчанию) |
| `gui.label(text)` | text | Добавляет метку (по умолчанию) |
| `gui.entry(name)` | name | Поле ввода |
| `gui.run()` | — | Запускает цикл сообщений |
| `gui.button_colored(t, bg, fg, cb)` | text, bgColor, textColor, callback | Цветная кнопка |
| `gui.label_colored(t, fg, bg)` | text, textColor, bgColor | Цветная метка |
| `gui.button_ex(x,y,w,h,t,bg,fg,cb)` | координаты, размеры, цвета | Кнопка с позицией |
| `gui.label_ex(x,y,w,h,t,fg,bg)` | координаты, размеры, цвета | Метка с позицией |