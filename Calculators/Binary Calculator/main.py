num1 = "00000001"
num2 = "00000001"

num1Split = [*num1]

print(f"Unsplit: {num1}\nSplit: {num1Split}")

def addBinary(num1, num2):
    for i in range(len(num1)):
        print(i)
        print(f"Index: {-i - 1}, Char: {[*num1][-i]}")

addBinary(num1, num2)