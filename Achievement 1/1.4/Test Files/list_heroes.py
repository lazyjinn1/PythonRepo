def display(file):
    heroes = []

    for line in file:
        line = line.rstrip('\n')

        hero_name = line.split(', ')[0]
        firstYear = line.split(', ')[1]

        heroes.append([hero_name, firstYear])

    heroes.sort(key = lambda hero: hero[1])

    for hero in heroes:
        print("--------------------")
        print("Superhero: " + hero[0])
        print("First Year: " + hero[1])

filename = input("Enter the filename with all the superheroes: ")

try:
    file = open(filename, 'r')
    display(file)
except FileNotFoundError:
    print('File does not exist - exiting, please try again later')
except:
    print('An unexpected error occurred.')
else:
    file.close()
finally:
    print('Goodbye!')