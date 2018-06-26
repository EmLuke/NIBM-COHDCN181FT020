import sys

def cal():
    if sum >= 2000:
        discount = sum * 0.10
        x = sum - discount
        print("Discocunt : ", discount)
        print("Total Cost : ", x)
        return file1(x, discount)

    elif sum >= 1500:
        discount = sum * 0.07
        x = sum - discount
        print("Discocunt : ", discount)
        print("Total Cost : ", x)
        return file1(x, discount)



    elif sum >= 1000:
        discount = sum * 0.05
        x = sum - discount
        print("Discocunt : ", discount)
        print("Total Cost : ", x)
        return file1(x, discount)



    elif sum < 1000:
        discount = 0
        x = sum
        print("Discocunt", discount)
        print("Total Cost : ", x)
        return file1(x, discount)

    else:
        print("not valid")
        exit()


def file1(x, discount):
    f = open("abc.txt", 'a+')
    f.write("\n")
    f.write(str(discount))
    f.write("\n")
    f.write(str(x))
    f.write("\n")
    f.close()


def file():
    f = open("abc.txt", 'a+')
    f.write("\n")
    f.write(str(price))
    f.write("\n")
    f.close()
sum=0
count=0

price = input("enter item price or press enter to quit: ")

while price:
    count += 1
    no = price
    try:
        no = float(price)
        sum += float(no)
        file()
        errorvalue = False

    except ValueError:
        error = sys.exc_info()[1]
        print("invalid input")
        print(error)
        errorvalue = True

    if errorvalue:
        print("You entered invalid value, Please try again!")

    price = input("enter item price or press enter to quit: ")

cal()
