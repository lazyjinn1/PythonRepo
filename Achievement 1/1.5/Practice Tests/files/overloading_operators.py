class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches
        
    def __str__(self):
        output = str(self.feet) + " feet, " + str(self.inches) + " inches"
        return output
    
    def __sub__(self, other):
        height_A_inches = self.inches + self.feet * 12
        height_B_inches = other.inches + other.feet * 12
        product_of_inches = height_B_inches - height_A_inches
        product_feet = product_of_inches // 12
        product_inch = product_of_inches - (product_feet * 12)
        return Height(product_feet, product_inch)
    
    def __add__(self, other):
        height_A_inches = self.inches + self.feet * 12
        height_B_inches = other.inches + other.feet * 12
        sum_of_inches = height_B_inches + height_A_inches
        sum_feet = sum_of_inches // 12
        sum_inch = sum_of_inches - (sum_feet * 12)
        return Height(sum_feet, sum_inch)
    
    def __lt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A < height_inches_B

    def __le__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A <= height_inches_B

    def __eq__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A == height_inches_B
    
    def __gt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A > height_inches_B
    
    def __ge__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A >= height_inches_B
    
    def __ne__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A != height_inches_B
    
# a = Height(4, 10)
# b = Height(5, 6)
# c = Height(7, 1)
# d = Height(5, 5)
# e = Height(6, 7)
# f = Height(5, 6)

# heights = [a, b, c, d, e, f]

# heights = sorted(heights)
# for height in heights:
#     print(height)
    
person_A_feet = int(input('What is the first person\'s height in feet? '))
person_A_inch = int(input('What is the first person\'s height in inches? '))
person_B_feet = int(input('What is the second person\'s height in feet? '))
person_B_inch = int(input('What is the second person\'s height in inches? '))
personA_height = Height(person_A_feet, person_A_inch)
personB_height = Height(person_B_feet, person_B_inch)

print("Person A's height:", personA_height)
print("Person B's height:", personB_height)

height_difference = personB_height - personA_height
height_combination = personA_height + personB_height

height_greater_than = personA_height > personB_height
height_greaterThan_equalTo = personA_height >= personB_height
height_not_equalTo = personA_height != personB_height

print("is A greater than B? : ", height_greater_than)
print("is A greater than or equal to B? : ", height_greaterThan_equalTo)
print("is A not equal to B? : ", height_not_equalTo)

