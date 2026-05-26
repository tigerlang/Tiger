# Библиотека random

Генерация случайных чисел.

## Импорт

```tiger
import random

main() {
    print(str.to_str(random.randint(100)))           # 0-99
    print(str.to_str(random.int_range(1, 6)))         # 1-6 (для игр)
    print(str.to_str(random.float_range(0.0, 1.0)))   # 0.0-1.0
    print(str.to_str(random.random()))                # 0.0-1.0 (коротко)
    random.seed(42)                                  # фиксировать seed
}
```

## Функции

| Функция | Описание |
|---------|----------|
| `random.randint(n)` | Случайное int от 0 до n-1 |
| `random.int_range(a, b)` | Случайное int от a до b включительно |
| `random.float_range(a, b)` | Случайное float от a до b |
| `random.random()` | Случайное float от 0.0 до 1.0 |
| `random.seed(n)` | Установить seed для воспроизводимых результатов |