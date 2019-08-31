import numpy as np
import matplotlib.pyplot as plt
import cv2
from tqdm import trange

width, height = (100, 100)
# grid = np.zeros((width, height))
grid = (np.random.randint(0,3,(width, height)) < 1).astype(np.float32)
# grid[40:60:4, 40:60:4] = 1.0
# grid[48:52, 48:52] = 1.0
# grid[52:56, 48:52] = 1.0

offsets = np.array([[0,-1],[0, 1],[-1, 0],[1, 0]])
conway_offsets = np.append(offsets, [[1, 1], [1,-1], [-1, 1], [-1, -1]], axis=0)
print(conway_offsets.shape)

step = 0

img_grid = np.zeros_like(grid)

for _ in trange(1000):
    tmp_grid = np.zeros_like(grid)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            nghb = 0
            idxy = np.array([i,j])

            for offset in conway_offsets:
                try:
                    iy, ix = idxy + offset
                    nghb += grid[iy, ix]
                except:
                    pass

            # pretty:single offsets
            # if nghb == 2 and grid[i, j] < 1.0:
            #     tmp_grid[i, j] = 1.0
            # elif grid[i, j] == 1.0:
            #     tmp_grid[i, j] = 2.0
            # elif grid[i, j] == 2.0:
            #     tmp_grid[i, j] = 0.0

            if nghb == 3 and grid[i, j] == 0.0:
                tmp_grid[i, j] = 1.0
            elif (nghb == 2 or nghb == 3) and grid[i, j] == 1.0: 
                tmp_grid[i, j] = 1.0
            else:
                tmp_grid[i, j] = 0.0

    grid = tmp_grid
    img_grid = 0.7 * img_grid + 0.3*grid
    # plt.imsave('./ca_out/{}.png'.format(str(step).zfill(4)), cv2.resize(grid, (400, 400), interpolation=cv2.INTER_NEAREST))
    cv2.imshow('brian'.format(step), cv2.resize(grid * 255., (200,200)))
    cv2.waitKey(1)

    step += 1

