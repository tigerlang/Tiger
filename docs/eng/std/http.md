# http library 

Windows only. Uses WinINet. 

## Import 

```tiger 
import http 
``` 

## Functions 

### http.get(url) 

Performs a GET request and returns the response body as a string. 

```tiger 
import http 

main() { 
var url = "http://api.example.com/data" 
var body = http.get(url) 
print("Server response:") 
print(body) 
} 
``` 

### http.post(url, data) 

Sends a POST request with data and returns a server response. 

```tiger 
import http 

main() { 
var response = http.post("http://httpbin.org/post", "name=John&age=30") 
print(response) 
} 
``` 

### http.get_status(url) 

Returns the HTTP status code as a string (for example, "200", "404"). 

```tiger 
import http 

main() { 
var status = http.get_status("http://example.com") 
print("Status: " + status) 
} 
```