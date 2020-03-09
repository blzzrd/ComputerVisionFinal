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


def tf_background_generation(seq, L):
    """
    tf_background_generation
    
    Generates the background by iterating through a sequence of frames
    a certain amount of time. Collected from the Teknomo Fernandez Algorithm
    located on https://arxiv.org/abs/1510.00889.

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


    for i in range(2, L):
        for j in range(3**(L-i)-1):
            print(j, 3*j, 3*j+1, 3*j+2)
            img1 = result[3*j]
            img2 = result[3*j+1]
            img3 = result[3*j+2]
            result[j] = get_mode(img1, img2, img3)

    return result[0]


def mc_get_mode(frames):
    w, h, _ = frames[0].shape
    f = np.zeros((frames[0].shape))

    for i in range(h):
        for j in range(w):
            bit = 1
            f[y][x] = 0
            while bit < 0b11111111:
                diff = 0
                for frame in frames:
                    pix = frame[y][x]
                    if pix^bit > 0:
                        diff += 1
                    else:
                        diff -= 1
                if diff > 0:
                    f[y][x] += bit
                bit <<= 1
    
    return f

def mc_background_generation(seq, S, L):
    """
    mc_background_generation
    
    Generates the background by iterating through a sequence of frames
    a certain amount of time. Collected from the Monte Carlo inspired RCF Algorithm
    located on https://www.researchgate.net/publication/282155172_A_Monte-Carlo-based_Algorithm_for_Background_Generation.

    ARGS --
    seq - The sequence of image frames (list of images read by cv2.imread)
    S - Sampling size. Adjustable by user.
    L - The amount of times the procedure is repeated until the level L.

    RETURNS --
    Returns an np array ready for cv2 to imwrite.
    """
    result = []

    if L <= 0:
        print("Error, level must be a positive, nonzero number.")
        return None

    S = len(seq)
    arrF = []

    for i in range(S**L - 1):
        r = np.random.randint(S-1)
        arrF.append(seq[r])


    for i in range(L-1):
        b = 0
        for j in range(S - 1):
            f = mc_get_mode(seq)
            b += S
        arrF[i] = f

    return arrF[0]


def rgb_to_hsv(frame):
    norm = frame / 255
    r,g,b = frame[:,:,0], frame[:,:,1], frame[:,:,2]

    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn

    if diff == 0:
        h = 0
    elif mx in r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif mx in g:
        h = (60 * ((g - b) / diff) + 120) % 360
    elif mx in b:
        h = (60 * ((g - b) / diff) + 240) % 360
    
    if mx == 0:
        s = 0
    else:
        s = diff / mx * 100

    v = mx * 100
    






if __name__ == "__main__":
    """ python3 bggen.py sample/ bgimg1.png """

    path = sys.argv[1]
    resultPathString = path + '.png'

    image_sequence = []
    for image in os.listdir(path):
        image_path = os.path.join(path, image)
        if os.path.isfile(image_path):
            img = cv2.imread(image_path)
            if img is not None:
                image_sequence.append(img)

    tfrgb_result = tf_background_generation(image_sequence, L=6)

    if tfrgb_result is not None:
        cv2.imwrite(filename='tfrgb'+resultPath, img=result_img)


    tfrgb_result = tf_background_generation(image_sequence, L=6)

    if tfrgb_result is not None:
        cv2.imwrite(filename='tfrgb'+resultPath, img=result_img)



