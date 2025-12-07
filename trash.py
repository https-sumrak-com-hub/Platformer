def A_a(N):
    primes = ""
    shagi = 0
    for i in range(2, N + 1):
        is_prime = True
        for j in range(2, i):
            shagi += 1
            if i % j == 0:
                is_prime = False
                break


        if is_prime:
            primes += f"{i}, "


    return shagi

def A_b(N):
    primes = ""
    shagi = 0
    if N < 2:
        return []

    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(N ** (1/2)) + 1):
        if is_prime[i]:
            for j in range(i * i, N + 1, i):
                is_prime[j] = False
                shagi += 1

    for i in range(N+1):
        if is_prime[i]:
            primes += f"{i}, "


    return shagi

l = [100, 1000, 2000, 3000, 4000, 5000]

def A(n):
    start_num = 1
    finish_num = n
    if finish_num > 0:
        for i in range(start_num, finish_num+1):
            start_num *= i
    else:
        start_num = 0
    return start_num


def B(file_name):
    integers = []
    with open(f"{file_name}.txt", "r") as txt_file:
        for integer in txt_file.readlines():
            if "\n" in integer:
                integers.append(int(integer[:-1]))
            else:
                integers.append(int(integer))

    integers_mult = integers[0]
    for i in range(1, len(integers)):
        integers_mult *= integers[i]

    integers_divide = integers[0]
    for i in range(1, len(integers)):
        integers_divide /= integers[i]

    integers_whole = int((str(integers_divide).split("."))[0])
    integers_remainder = "0."+(str(integers_divide).split("."))[1]

    print(f"Умножение: {integers_mult}, целое частное: {integers_whole}, остаток от деления: {integers_remainder}")

def C():
    with open("filee.txt", "r") as file:
        print(int(file.readline().replace("\n", ""))**(1/2))

