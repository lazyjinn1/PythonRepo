fruit = input("I have an apple, an orange and a banana! " \
    + "Which fruit would you like to have? : ")

if fruit == ("apple") or fruit == ("orange"):
    print("Here, have an " + fruit + ".")

    number_of_fruits = int(input("How many " + fruit + "s do you have now?: "))
    if number_of_fruits > 0:
        print("You have some " + fruit + "s.")

        if number_of_fruits > 3:
            print("But you've got way too many!")

    else:
        print("You have no " + fruit + "s.")
elif fruit == "banana":
    print("Here, have a " + fruit + ".")

    number_of_fruits = int(input("How many " + fruit + "s do you have now?: "))
    if number_of_fruits > 0:
        print("You have some " + fruit + "s.")

        if number_of_fruits > 3:
            print("But you've got way too many!")

    else:
        print("You have no " + fruit + "s.")
else:
    print("Oh no, I don't have any " + fruit +  "s!")



