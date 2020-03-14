import numpy as np
import sys
import os
import cv2
import pdb


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
            img1 = result[3*j]
            img2 = result[3*j+1]
            img3 = result[3*j+2]
            result[j] = get_mode(img1, img2, img3)

    return result[0]


def mc_get_mode(frames):
    w, h, p = frames[0].shape
    f = np.zeros((frames[0].shape))

    for y in range(w):
        for x in range(h):
            for c in range(p):
                #bit = 1
                n = 0
                while n < 8: # bit < 0b11111111:
                    diff = 0
                    for frame in frames:
                        pix = frame[y][x][c]
                        if pix & (1<<n): #np.bitwise_xor(pix,bit) > 0:
                            diff += 1
                        else:
                            diff -= 1
                    if diff > 0:
                        f[y][x][c] += (1<<n)#bit
                    n += 1
                    #bit <<= 1
                    
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

    N = len(seq)
    arrF = []

    for i in range(S**L):
        r = np.random.randint(N-1)
        arrF.append(seq[r])

    for l in range(L):
        b = 0
        for i in range(S):
            f = mc_get_mode(seq[b:b+S])
            b += S
            arrF[i] = f

    return arrF[0]

import numpy as np

def median_filter(seq,n):
    '''
    Median filter method for background subtraction.
    
    ARGS:
        seq - The sequence of image frames
        n - a parameter for the number of frames
    
    RETURNS:
        An numpy array that outputs the image of the background
    '''
    
    if n <= 0:
        print('Error, level must be a positive, nonzero number')
        return None
    
    s = np.random.choice(len(seq), n, replace=True)
    
    img = []
    
        
    h,w,_ = seq[0].shape
    
    result = np.zeros([h,w])
    
    for y in range(h):
        for x in range(w):
            img = []
            for i in range(n):
                img.append(seq[s[i]][y][x])
            result[y][x] = np.median(img,axis = 0)
    
    return(result)
            


if __name__ == "__main__":
    """ python3 bggen.py sample/ bgimg1.png """

    path = sys.argv[1]
    result_path = sys.argv[2]

    image_sequence = []
    for image in os.listdir(path):
        image_path = os.path.join(path, image)
        if os.path.isfile(image_path):
            img = cv2.imread(image_path)
            if img is not None:
                image_sequence.append(img)
    tfrgb_result = tf_background_generation(image_sequence, L=6)
    if tfrgb_result is not None:
        cv2.imwrite(filename='tfrgb'+result_path, img=tfrgb_result)

    mcrgb_result = mc_background_generation(image_sequence, S=9, L=6)
    if mcrgb_result is not None:
        cv2.imwrite(filename='mcrgb'+result_path, img=mcrgb_result)

    median_result = median_filter(image_sequence,n = 10)
    if median_result is not None:
        cv2.imwrite(filename='median'+result_path, img=median_result)
    """
    ## HSV TIME
    hsv_seq = [] 
    for image in image_sequence:
        hsv_seq.append(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))

    tfhsv_result = tf_background_generation(hsv_seq, L=6)
    if tfhsv_result is not None:
        tfhsvrgb_result = cv2.cvtColor(tfhsv_result, cv2.COLOR_HSV2BGR)
        cv2.imwrite(filename='tfhsv'+result_path, img=tfhsvrgb_result)

    mchsv_result = mc_background_generation(hsv_seq, S=3, L=3)
    if mchsv_result is not None:
        mchsvrgb_result = cv2.cvtColor(mchsv_result.astype('float32'), cv2.COLOR_HSV2BGR)
        cv2.imwrite(filename='mchsv'+result_path, img=mchsvrgb_result)
    """

