import random
import string
import os


def create_large_file():
    file = '/home/rakesh/Python_Projects/externalSorting/largefile.txt'

    open(file, "w+")

    with open(file, "a") as f:
        while os.stat(file).st_size < 1024*1024*1024:
            f.write(''.join([random.choice(string.ascii_letters)
                             for n in range(random.randint(1, 56))]))
            f.write("\n")
        print(os.stat(file).st_size)


create_large_file()
