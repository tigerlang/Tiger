# Библиотека time

Работа с датой и временем.

## Импорт

```tiger
import time

main() {
    print("Сейчас: " + time.now())
    print("Дата: " + time.date())
    print("Время: " + time.time_only())
    print("Timestamp: " + str.to_str(time.timestamp()))
    time.sleep(1000)  # пауза 1 секунду
}
```

## Функции

| Функция | Описание |
|---------|----------|
| `time.timestamp()` | Unix timestamp (секунды с 1970) |
| `time.now()` | Текущая дата и время "ГГГГ-ММ-ДД ЧЧ:ММ:СС" |
| `time.date()` | Только дата "ГГГГ-ММ-ДД" |
| `time.time_only()` | Только время "ЧЧ:ММ:СС" |
| `time.sleep(ms)` | Пауза на указанное количество миллисекунд |