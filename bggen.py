import numpy as np
import sys
import os
import cv2


""" 
TEKNOMO-FERNANDEZ ALGORITHM FOR BACKGROUND GENERATION 
ADAPTED BY ALEJANDRO CASTANEDA AND RENEE WU
CREATED FOR COMPUTER VISION 410, FENG LIU
"""

def get_mode(img1, img2, img3):
    """
    get_mode
    Boolean Operation to Determine the Mode.
    Compares three images and gets the binary value for the value that occurs
    most frequently in the images.

    ARGS --
    img1, img2, img3 - A series of input images (created by cv2.imread)

    RETURNS --
    b - The resultant numpy array of the values through the boolean equation.

    Returns the background 
    """

    # Per Paper: b = (g3 and (g1 xor g2)) or (g1 and g2)
    b = (img3 & (img1^img2)) | (img1 & img2)
    return b


def background_generation(seq, L):
    """
    background_generation
    
    Generates the background by iterating through a sequence of frames
    a certain amount of time. 

    ARGS --
    seq - The sequence of image frames (list of images read by cv2.imread)
    L - The amount of times the procedure is repeated until the level L.

    RETURNS --
    Returns an np array ready for cv2 to imwrite.
    """
    result = []

    if L <= 0:
        print("Error, level must be a positive, nonzero number.")
        return None

    for i in range(3**(L-1) -1):
        s = np.random.choice(len(seq), 3, replace=False)
        result.append(get_mode(seq[s[0]], seq[s[1]], seq[s[2]]))


    print(len(result))
    for i in range(2, L):
        for j in range(3**(L-i)-1):
            print(j, 3*j, 3*j+1, 3*j+2)
            img1 = result[3*j]
            img2 = result[3*j+1]
            img3 = result[3*j+2]
            result[j] = get_mode(img1, img2, img3)

    return result[0]


if __name__ == "__main__":
    """ python3 bggen.py Level(int) sample/ bgimg1.py """

    path = sys.argv[1]
    resultPath = sys.argv[2]

    image_sequence = []
    for image in os.listdir(path):
        image_path = os.path.join(path, image)
        if os.path.isfile(image_path):
            img = cv2.imread(image_path)
            if img is not None:
                image_sequence.append(img)

    result_img = background_generation(image_sequence, L=6)

    if result_img is not None:
        cv2.imwrite(filename=resultPath, img=result_img)

