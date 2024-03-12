class Map:

    def __init__(self) -> None:
        self.coord_array = []
        self.last_array = []
        self.zenith = 2500

    def add_position (self, f3c):
        self.coord_array.append(self.f3c_to_coords(f3c))

    def get_coord_array(self):
        return self.coord_array

    
    def get_curr_coords(self):
        if self.get_curr_dim() == "the_nether":
            return [(self.coord_array[-1][0] * 8), (self.coord_array[-1][1] * 8)]
        return [self.coord_array[-1][0], self.coord_array[-1][1]]
    
    def get_curr_x(self):
        if self.get_curr_dim() == "the_nether":
            return (self.coord_array[-1][0] * 8)
        return self.coord_array[-1][0]
    
    def get_curr_z(self):
        if self.get_curr_dim() == "the_nether":
            return (self.coord_array[-1][1] * 8)
        return self.coord_array[-1][1]
    
    def get_curr_dim(self):
        return self.coord_array[-1][2]

    def get_last_coords(self):
        if self.get_last_dim() == "the_nether":
            return [(self.coord_array[-2][0] * 8), (self.coord_array[-2][1] * 8)]
        return [self.coord_array[-2][0], self.coord_array[-2][1]]
    
    def get_last_x(self):
        if self.get_last_dim() == "the_nether":
            return self.coord_array[-2][0] * 8
        return self.coord_array[-2][0]
    
    def get_last_z(self):
        if self.get_last_dim() == "the_nether":
            return self.coord_array[-2][1] * 8
        return self.coord_array[-2][1]
    
    def get_last_dim(self):
        return self.coord_array[-2][2]
    
    def get_dx(self):
        return self.get_curr_x() - self.get_last_x()

    def get_dz(self):
        return self.get_curr_z() - self.get_last_z()

    def get_color(self):
        if self.get_curr_dim() == "the_nether":
            return "#800000"
        else:
            return "#003151"

    def clear_array(self):
        self.last_array = self.coord_array
        self.coord_array = []
        self.zenith = 2500

    def f3c_to_coords(self, clipboard:str) -> list:

        clip_array = clipboard.split()

        # coords = [clip_array[6], clip_array[8]]
        # coords = list(map(float, coords))
        # coords = list(map(int, coords))

        x = clip_array[6] # get x coord from f3c
        x = x[0:(len(x) - 3)] # cut out decimals from coord
        x = int(x) # convert to integer

        z = clip_array[8] # same as above but with z coord
        z = z[0:(len(z) - 3)] 
        z = int(z) 

        dim = (clip_array[2])[10:] # get dimension from f3c and cut out "minecraft:"

        data = [x, z, dim]

        return(data)
    



# /execute in minecraft:overworld run tp @s 453.30 74.00 829.30 420.94 -31.15   