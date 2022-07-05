# Standard library imports

# Related third party imports
from panda3d.core import *

# Constants
INPUT = 'greetings/Greetz_8K.png'
OUTPUT = 'models/greetings.png'

my_image = PNMImage(Filename(INPUT))
for x in range(my_image.getXSize()):
    for y in range(my_image.getYSize()):
        xel_a = my_image.getXelA(x, y)
        new_xel_a = LVecBase4f(0, 0, 0, 1-(xel_a[0]+xel_a[1]+xel_a[2])/3)
        # print(f'{xel_a} -> {new_xel_a}')
        my_image.setXelA(x, y, new_xel_a)
my_image.write(Filename(OUTPUT))

# convert tex_dmg_480x120.png tex_dmg_480x120.png tex_dmg_480x120.png tex_dmg_480x120.png tex_dmg_480x120.png tex_dmg_480x120.png tex_dmg_480x120.png tex_dmg_480x120.png -append tex_dmg_mosaic.png
#


