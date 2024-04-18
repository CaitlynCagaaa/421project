import imutils
import cv2
import requests
import yaml
url = "http://192.168.1.22:8080/drawer0/conf.yaml"
# Retrieve the file content from the URL
response = requests.get(url, allow_redirects=True)
# Convert bytes to string
content = response.content.decode("utf-8")
# Load the yaml
content = yaml.safe_load(content)
print(content)
url = "http://192.168.1.22:8080/drawer0/tool_1_1.jpg"
image =imutils.url_to_image(url)
cv2.imshow("check",image)
cv2.waitKey(0)