planet_name = str(input("What is the name of the planet? "))
distance = float(input("What is the distance from this planet? "))
axial_tilt = float(input("What is the axial tilt of the planet? "))

if(distance > 0.38 and axial_tilt < 24.5):
    print(planet_name, "is habitable.")
else:
    print(planet_name, "is not habitable.")