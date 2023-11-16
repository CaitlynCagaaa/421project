import cv2

# how are you turning it into a black and white photo to find countous
# must be one of cv2 color conversion codes, and must turn it into grayscale
# do not reccomend changing
grayscale = cv2.COLOR_BGR2GRAY

# how is the program finding the threshold, aka how is it turning it into just white and black to find contours
# must be one of cv2 thresholding varaibles
# Reccomendations :if draw has dark barkground use THRESH_BINARY_INV, if light background use THRESH_BINARY
threshType = cv2.THRESH_BINARY_INV

# the minumum value for thresholding, the larger the difference in grayscale betweeen the background and the object in 
# the picture the bigger the value 
# should be an interger between 0 and 256
# do not recommend changing
minThreshValue = 90

# minimum number of pixels that make up the width of an object
# increase to remove small non-objects
# decrease to find small objects 
minWidth = 4

#minimum number of pixels that make up the height of an object
# increase to remove small non-objects
# decrease to find small objects
minHeight = 4


