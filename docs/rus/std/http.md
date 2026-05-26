# Библиотека http

Только для Windows. Использует WinINet.

## Импорт

```tiger
import http
```

## Функции

### http.get(url)

Выполняет GET-запрос и возвращает тело ответа как строку.

```tiger
import http

main() {
    var url = "http://api.example.com/data"
    var body = http.get(url)
    print("Ответ сервера:")
    print(body)
}
```

### http.post(url, data)

Отправляет POST-запрос с данными и возвращает ответ сервера.

```tiger
import http

main() {
    var response = http.post("http://httpbin.org/post", "name=John&age=30")
    print(response)
}
```

### http.get_status(url)

Возвращает HTTP-статус код в виде строки (например, "200", "404").

```tiger
import http

main() {
    var status = http.get_status("http://example.com")
    print("Статус: " + status)
}
```