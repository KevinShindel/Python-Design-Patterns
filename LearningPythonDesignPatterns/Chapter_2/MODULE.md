

````python
singletone.py

only_one_var = "I'm only one!"
````

````python
module1.py

import singletone

print(singletone.only_one_var)
singletone.only_one_var += ' after the modification'
import module2
````

````python
module2.py
import singletone
print(singletone.only_one_var)
````