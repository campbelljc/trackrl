

# Rounds an integer down to the given power of 2. y must be a power of 2.
def floor2(x, y):
    return x & ~(y - 1)

COORDS_Z_STEP = 8
MAX_TRACK_HEIGHT = 254 * COORDS_Z_STEP
COORDS_Z_PER_TINY_Z = 16

class CoordsXYRangedZ:
    def __init__(self, a, b, c, d):
        self.x, self.y = a, b
        self.baseZ = c
        self.clearanceZ = d

SubpositionTranslationDistances = [
    #// For a base length of 8716 (0x220C) on the horizontal and 6554 (0x199A) on the vertical, use the Pythagoras theorem and round up.
    0,      # no movement
    8716,   # X translation
    8716,   # Y translation
    12327,  # XY translation
    6554,   # Z translation
    10905,  # XZ translation
    10905,  # YZ translation
    13961,  # XYZ translation
    #// For the reverser car, multiply the horizontal distance by 2.5 and the vertical distance by 4.072.
    0,      # no movement
    21790,  # X translation
    21790,  # Y translation
    30817,  # Z translation
    16385,  # XY translation
    27262,  # XZ translation
    27262,  # YZ translation
    34902,  # XYZ translation
]

word_9A2A60 = [ # dist between cars on train(?)
    [ 0, 16 ],
    [ 16, 31 ],
    [ 31, 16 ],
    [ 16, 0 ],
    [ 16, 16 ],
    [ 64, 64 ],
    [ 64, -32 ],
    [ -32, -32 ],
    [ -32, 64 ],
]
