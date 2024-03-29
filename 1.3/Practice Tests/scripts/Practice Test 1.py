a = int(input("What is your first number? "))
b = int(input("What is your second number? "))
addOrSubtract = str(input("Would you like to add or subtract? "))

if addOrSubtract == "add":
    print(a + b)
elif addOrSubtract == "subtract":
    print(a - b)
else:
    print("Choices are invalid")