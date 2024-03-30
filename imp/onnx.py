	
import cv2
import numpy as np
onnx_model_path = "hiline_class.onnx" 
sample_image = r"drawer0/tool_3_2.jpg"
 
#The Magic:
net =  cv2.dnn.readNetFromONNX(onnx_model_path) 
image = cv2.imread(sample_image)

normalized_image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
net.setInput(cv2.dnn.blobFromImage(normalized_image, size=(224, 224), swapRB=False, crop=True))
detection = net.forward()
#cv2.imwrite('output1.jpg',img) # Uncomment this line to save the output

print(detection)
print(detection.shape)
print(detection.data)
#cv2.imshow("Object Detection", blobb)