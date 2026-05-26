# Time library 

Working with date and time. 

## Import 

```tiger 
import time 

main() { 
print("Now: " + time.now()) 
print("Date: " + time.date()) 
print("Time: " + time.time_only()) 
print("Timestamp: " + str.to_str(time.timestamp())) 
time.sleep(1000) # pause 1 second 
} 
``` 

## Functions 

| Function | Description | 
|---------|----------| 
| `time.timestamp()` | Unix timestamp (seconds since 1970) | 
| `time.now()` | Current date and time "YYYY-MM-DD HH:MM:SS" | 
| `time.date()` | Date only "YYYY-MM-DD" | 
| `time.time_only()` | Only time "HH:MM:SS" | 
| `time.sleep(ms)` | Pause for the specified number of milliseconds |