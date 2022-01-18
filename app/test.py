import time

for i in range(1, 20):
    time.sleep(0.5)
    print(f'\rИтерация # {i}', end="")


# for x in range(10):
#     time.sleep(0.5) # shows how its working
#     print("\r {}".format(x), end="")