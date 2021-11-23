import numpy as np
from numpy import rot90
from tqdm import tqdm

def rotate24(tensor): #rotates a 3d tensor in all possible ways 
    ax = [(0,2),(0,2),(0,2),(1,2),(0,2),(0,2)] #yeah bitch
    for i in range(6):
        tensor = rot90(tensor,axes=ax[i])
        for j in range(4):
            tensor = rot90(tensor,axes=(0,1))
            yield tensor

dim = int(input("Find all polycubes up to: "))-1#computes all n-cubes up to dim


onecube = np.array([[[1 if i==j==k==3 else 0 for i in range(7)] for j in range(7)] for k in range(7)])#start from onecube
spaces = [] #spaces holds all n-cubes 
spaces.append(onecube)

np.save(f"1-cubes", spaces)
print(f'There is 1 n-cube')

faces = [(1,0,0), (0,1,0),(0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)]#all faces of a cube with its center at the origin, will be useful later


for n in range(dim):

    possible = []#don't mind these two for now
    bounding_boxes = []#i'll explain later i swear

    for space in spaces: #for each (n-1)-cube

        a = np.where(space == 1)
        coordinates = [[a[0][i],a[1][i],a[2][i]] for i,j in enumerate(a[0])] #return all of its cubes

        for i in coordinates: #for each cube in each (n-1)-cube, try adding a block on each face. 
            for f in faces:
                try:
                    target = space.copy()
                    #if target cube adjacent to that face is empty, cube indices are not negative and we're not outside the grid
                    if target[i[0]+f[0]][i[1]+f[1]][i[2]+f[2]] != 1 and i[0]+f[0] >= 0 and i[1]+f[1] >= 0 and i[2]+f[2] >= 0:
                        target[i[0]+f[0]][i[1]+f[1]][i[2]+f[2]] = 1
                        possible.append(target) #then the resulting n-cube is a valid candidate
                except: 
                    pass

    
    for p in possible: #for each candidate, generate the smallest possible tensor which contains it

        a = np.where(p == 1)
        coordinates = np.array([[a[0][i],a[1][i],a[2][i]] for i,j in enumerate(a[0])])

        min_x = coordinates[:,0][np.where(coordinates[:,0] ==  min(coordinates[:,0]))[0][0]]
        max_x = coordinates[:,0][np.where(coordinates[:,0] ==  max(coordinates[:,0]))[0][0]]+1
        min_y = coordinates[:,1][np.where(coordinates[:,1] ==  min(coordinates[:,1]))[0][0]]
        max_y = coordinates[:,1][np.where(coordinates[:,1] ==  max(coordinates[:,1]))[0][0]]+1
        min_z = coordinates[:,2][np.where(coordinates[:,2] ==  min(coordinates[:,2]))[0][0]]
        max_z = coordinates[:,2][np.where(coordinates[:,2] ==  max(coordinates[:,2]))[0][0]]+1
        bounding_boxes.append(p[min_x:max_x,min_y:max_y,min_z:max_z])

    l = len(bounding_boxes)  
    polycubes = []

    for i in tqdm(reversed(range(l)), desc=f'Total {n+2}-cubes candidates to check: {l}, '):#for each of the i candidates(top->bottom)
        duplicate = False
        for j in range(i): #check for duplicates amongst all other j candidates (with j<i)
            for r in rotate24(bounding_boxes[i]): #by rotating them in all 24 possible ways
                if np.array_equal(bounding_boxes[j],r):
                    duplicate = True

        if not duplicate:#if no duplicates were found across all j candidates, the ith candidate is a valid polycube
            polycubes.append(possible[i])

    print(f'There are {len(polycubes)} {n+2}-cubes')
    np.save(f"{n+2}-cubes", polycubes)
    spaces = polycubes.copy()
