# First, install the Google Generative AI library
$ pip install google-genai rich

# Save the code to code-execution.py
# Then run the program with Python
$ python code-execution.py
Okay, I can help you find the sum of the first 50 prime numbers. Here's how I'll approach this:                                       
 1 Generate a list of the first 50 prime numbers. I'll need an efficient way to identify prime numbers. I can use the Sieve of        
   Eratosthenes method or a simpler trial division approach.                                                                          
 2 Sum the prime numbers. Once I have the list, I'll simply add them up.                                                              
Here's the Python code to accomplish this:                                                                                            
---
╭─────────────────────────────────────────────────────────────── Code ───────────────────────────────────────────────────────────────╮
│    1 def is_prime(n):                                                                                                              │
│    2     """Efficiently determine if a number is prime."""                                                                         │
│    3     if n <= 1:                                                                                                                │
│    4         return False                                                                                                          │
│    5     if n <= 3:                                                                                                                │
│    6         return True                                                                                                           │
│    7     if n % 2 == 0 or n % 3 == 0:                                                                                              │
│    8         return False                                                                                                          │
│    9     i = 5                                                                                                                     │
│   10     while i * i <= n:                                                                                                         │
│   11         if n % i == 0 or n % (i + 2) == 0:                                                                                    │
│   12             return False                                                                                                      │
│   13         i += 6                                                                                                                │
│   14     return True                                                                                                               │
│   15                                                                                                                               │
│   16 primes = []                                                                                                                   │
│   17 num = 2                                                                                                                       │
│   18 while len(primes) < 50:                                                                                                       │
│   19     if is_prime(num):                                                                                                         │
│   20         primes.append(num)                                                                                                    │
│   21     num += 1                                                                                                                  │
│   22                                                                                                                               │
│   23 print(f'{primes=}')                                                                                                           │
│   24 print(f'{sum(primes)=}')                                                                                                      │
│   25                                                                                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
---
╭────────────────────────────────────────────────────────────── Output ──────────────────────────────────────────────────────────────╮
│ primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,   │
│ 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229]                                │
│ sum(primes)=5117                                                                                                                   │
│                                                                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
---
The sum of the first 50 prime numbers is 5117.                                                                                        
---
