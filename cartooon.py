import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image
def read_file(image):
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

image = "resources/Fahad pic.jpeg"
img = read_file(image)

# Edge mask
def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return edges

line_size, blur_value = 7, 7
edges = edge_mask(img, line_size, blur_value)

# Reduce the color palette
def color_quantization(img, k):
    data = np.float32(img).reshape((-1, 3))
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    
    return result

img_quantiz = color_quantization(img, k=9)

# Reduce the noise
blurred = cv2.bilateralFilter(img_quantiz, d=5, sigmaColor=200, sigmaSpace=200)

# Combine edge mask with color quantized image
def cartoon(img, edges, blurred):
    cartoon_image = cv2.bitwise_and(blurred, blurred, mask=edges)
    return cartoon_image

cartoon_image = cartoon(img, edges, blurred)

# Display the original and cartoonized images
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(cartoon_image)
plt.title("Cartoonized Image")
plt.axis("off")

plt.tight_layout()
plt.show()
