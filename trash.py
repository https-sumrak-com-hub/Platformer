import csv
import turtle
import itertools

def func():
    nums = []
    for i in range(225, 99999):
        a = str(bin(i)[2:])

        if int(a[2:-2], 2) % 3 == 0 or int(a[1:-1], 2) % 2 == 0:
            nums.append(int(a, 2))
        else:
            continue

    print(*nums)

def tu():
    a = turtle
    a.speed(1)
    for i in range(2):
        a.forward(11)
        a.right(90)
        a.forward(17)
        a.right(90)
    a.pu()
    a.forward(7)
    a.left(90)
    a.back(1)
    a.right(90)
    a.pd()
    for i in range(2):
        a.forward(15)
        a.right(90)
        a.forward(7)
        a.right(90)

    a.exitonclick()

def second():
    print("x y z w")
    for x in 0, 1:
        for y in 0, 1:
            for z in 0, 1:
                for w in 0, 1:
                    f = x or (not y or z or not w) and (y or not z)

                    if f == 0:
                        print(x, y, z, w)


def fuuuckl():
    bolts_count = 0

    with open("автосервисы.csv", "r", newline="") as a:
        avtoservices_id = []
        for line in csv.reader(a):
            line = (line[0]).split(";")
            if line[0] != "" and line[1] == "Верх-Исетский":
                avtoservices_id.append(line[0])

    with open("запчасти.csv", "r", newline="") as z:
        bolt_article = []
        for line in csv.reader(z):
            line = (line[0]).split(";")
            if line[0] != "":
                if line[1] == "Тормозная система":
                    if "Болт" in line[2]:
                        bolt_article.append(line[0])

    with open("движение.csv", "r", newline="") as d:
        for line in csv.reader(d):
            line = (line[0][0:-5]).split(";")
            if line[0] != "":
                for i in range(1, 31):
                    if line[1] == f"0{i}.09.2023" or line[1] == f"{i}.09.2023":
                        if line[2] in avtoservices_id and line[3] in bolt_article:
                            if line[5] == "Поступление":
                                bolts_count += int(line[4])
                            else:
                                bolts_count -= int(line[4])

    print(bolts_count)

def chmo():
    nums = []
    for i in range(155, 900):
        num_2 = bin(i)[2:]

        if num_2[-4:-2] == num_2[-2:]:
            if int(num_2[:-2], 2) % 2 == 0:
                nums.append(int(num_2[:-2], 2))
        if num_2[-4] != num_2[-2] and num_2[-3] != num_2[-1]:
            if int(num_2[:-2], 2) % 3 == 0:
                nums.append(int(num_2[:-2], 2))

    print(*nums)

def daun():
    a = turtle
    for i in range(8):
        a.forward(12)
        a.right(90)


def hahaha_ya_sumasoshel_yzhe_nahui():
    letters = ['Т', 'Ь', 'Ю', 'Р', 'И', 'Н', 'Г']

    # Все шестибуквенные слова без повторений
    words = [''.join(p) for p in itertools.permutations(letters, 6)]

    vowels = {'Ю', 'И'}

    def ok(w: str) -> bool:
        for i, ch in enumerate(w):
            if ch == 'Ь':
                # 1) Нельзя в начале
                if i == 0:
                    return False
                # 2) Нельзя после гласных Ю или И
                if w[i - 1] in vowels:
                    return False
        return True

    valid = [w for w in words if ok(w)]

    print(len(words))  # 5040 — всего перестановок
    print(len(valid))  # 3120 — удовлетворяют условию

