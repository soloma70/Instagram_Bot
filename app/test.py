from time import sleep
from random import randrange

# for i in range(1, 20):
#     time.sleep(0.5)
#     print(f'\rИтерация # {i}', end="")


# for x in range(10):
#     time.sleep(0.5) # shows how its working
#     print("\r {}".format(x), end="")

delay = 10

while delay:
    print(f'\rЗадержка {delay - 1} с.', end='')
    sleep(1)
    delay -= 1

print('Hello World!')
