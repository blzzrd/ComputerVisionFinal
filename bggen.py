import numpy as np
import os
import cv2


"""
one of the traditional methods to gen a bg image is to calculate intensity of
each pixel over several slices.
Given n images, calculate mode of all. 
Time consuming. Requires large space. 


Boolean operation to determine mode

b(r,c,t) = bg pixl at (r,c) @ t
nb(r,c) = # of bg pixels at (r,c) for T

g(r,c,t) = foreground (r,c) @ t
ng(r,c,) = # of fg pixels @ (r,c)

nb(r,c) + ng(r,c) = T

For any pixel nb(r,c) > T/2



proposition 1

B = x3 AND (x1 ^ x2) OR x1 and x2



"""


def getMode(img1, img2, img3):
    # Per Paper:
    # b = (g3 and (g1 xor g2)) or (g1 and g2)
    b = (img3 & (img1^img2)) | (img1 & img2)
    return b


"""
in case numpy doesn't support big boolean
def getImageMode(img1, img2, img3):
    h, w, _ = img1.shape
    for y in range(h):
        for x in range(w):
            p1 = img1[y][x]
            p2 = img1[y][x]
"""

def backgroundGeneration(seq, L):
    """
    seq - sequence of images. (list of cv2.imread)
    L = Level 
    """

    result = []

    if L <= 0:
        print("Error, level must be a positive, nonzero number.")
        return 

    for i in range(3**(L-1) -1):
        s = np.random.choice(len(seq), 3)
        result[i] = getMode(seq[s[0]], seq[s[1]], seq[s[2]])

    for i in range(2, L):
        for j in range(3**(L-1) -1):
            img1 = result[3*j]
            img2 = result[3*j+1]
            img3 = result[3*j+2]
            result[j] = getMode(img1, img2, img3)

    return result[0]



if __name__ == "__main__":
    """ python3 bggen.py Level(int) sample/ bgimg1.py """

    path = sys.argv[1]
    resultPath = sys.argv[2]

    image_sequence = []
    for image in path:
        if os.path.isfile(image):
            img = cv2.imread(os.path.join(path, image))
            if img:
                image_sequence.append(img)

    result_img = backgroundGeneration(seq, L)
    cv2.imwrite(filename=resultPath, img=result_img)



