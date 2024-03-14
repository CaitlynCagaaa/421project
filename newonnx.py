import cv2
import numpy as np
import onnx
import onnxruntime as ort

# Load the ONNX model
def load_model(model_path):
    return ort.InferenceSession(model_path)

# Perform inference on an image
def infer_image(image, session, input_name, output_name):
    # Preprocess the image
    input_img = cv2.resize(image, (224, 224))
    input_img = np.transpose(input_img, (2, 0, 1)).astype(np.float32)
    input_img = np.expand_dims(input_img, axis=0)
    input_img /= 255.0

    # Run inference
    input_feed = {input_name: input_img}
    outputs = session.run([output_name], input_feed=input_feed)

    return outputs[0]

# Draw bounding boxes and labels on the image
def draw_boxes(image, boxes, labels):
    for box, label in zip(boxes, labels):
        x1, y1, x2, y2 = box.astype(int)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Main function to process an image
def process_image(image_path, model_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to read image.")
        return

    model = load_model(model_path)
    input_name = model.get_inputs()[0].name
    output_name = model.get_outputs()[0].name

    outputs = infer_image(image, model, input_name, output_name)
    print(outputs)

    boxes = outputs[:, :4]
    print(boxes)
    scores = outputs[:, 4]
    labels = outputs[:, 5]
    print(labels)

    # Filter boxes based on confidence score threshold
    threshold = 0.5
    filtered_boxes = boxes[scores > threshold]
    print(filtered_boxes)
    filtered_labels = labels[scores > threshold]

    draw_boxes(image, filtered_boxes, filtered_labels)

    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = r"hammer/hammer01.jpg" # Change this to your image file
    model_path = r"hiline_class.onnx" # Change this to your ONNX model file
    process_image(image_path, model_path)