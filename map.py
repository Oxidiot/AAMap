class Map:

    def __init__(self) -> None:
        self.coord_array = []

    def add_position (self, f3c):
        self.coord_array.append(self.f3c_to_coords(f3c))

    def f3c_to_coords(self, clipboard) -> list:
        clipArray = clipboard.split()
        x = clipArray[6]
        z = clipArray[8]
        dim = clipArray[2]
        return([x, z, dim])
    



# /execute in minecraft:overworld run tp @s 453.30 74.00 829.30 420.94 -31.15   