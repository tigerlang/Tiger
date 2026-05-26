# Random library 

Random number generation. 

## Import 

```tiger 
import random 

main() { 
print(str.to_str(random.randint(100))) # 0-99 
print(str.to_str(random.int_range(1, 6))) # 1-6 (for games) 
print(str.to_str(random.float_range(0.0, 1.0))) # 0.0-1.0 
print(str.to_str(random.random())) # 0.0-1.0 (short) 
random.seed(42) # commit seed 
} 
``` 

## Functions 

| Function | Description | 
|---------|----------| 
| `random.randint(n)` | Random int from 0 to n-1 | 
| `random.int_range(a, b)` | Random int from a to b inclusive | 
| `random.float_range(a, b)` | Random float from a to b | 
| `random.random()` | Random float from 0.0 to 1.0 | 
| `random.seed(n)` | Set seed for reproducible results |