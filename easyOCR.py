import cv2
import pandas as pd
import easyocr
img = cv2.imread(r"boundries/im15.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
noise=cv2.medianBlur(gray,9)
cv2.imshow('frame', noise) 
thresh, image = cv2.threshold(noise, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imshow('fram', image) 
reader = easyocr.Reader(["en"])
result = reader.readtext(noise)
for (bbox, text, prob) in result:
    print(f'Text: {text}, Probability: {prob}')
df=pd.DataFrame(result)
print(df[1])
cv2.waitKey(0)
cv2.destroyAllWindows()