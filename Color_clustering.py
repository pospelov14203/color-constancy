import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from utils.data_operations import recreate_image
from sklearn.utils import shuffle
from time import time
import cv2
import k_medoids


n_colors = 2

image = cv2.imread("pictures/2.jpg")
#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

image = np.array(image, dtype=np.float32) / 100

# Load Image and transform to a 2D numpy array.
w, h, d = original_shape = tuple(image.shape)
assert d == 3
image_array = np.reshape(image, (w * h, d))

# print("Fitting model on a small sub-sample of the data")
# t0 = time()
image_array_sample = shuffle(image_array, random_state=0)[:50]
# kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
# print("done in %0.3fs." % (time() - t0))
#
# # Get labels for all points
# print("Predicting color indices on the full image (k-means)")
# t0 = time()
# labels = kmeans.predict(image_array)
# print("done in %0.3fs." % (time() - t0))

k_medoids = k_medoids.PAM(k=n_colors)
k_medoids.fit(image_array_sample)
labels = k_medoids.predict(image_array)


# Display all results, alongside original image
plt.figure(1)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Original image (96,615 colors)')
#image = np.array(image, dtype=np.float32) * 100
rgb_image = cv2.cvtColor(image, cv2.COLOR_Lab2RGB)
plt.imshow(rgb_image)

plt.figure(2)
plt.clf()
ax = plt.axes([0, 0, 1, 1])
plt.axis('off')
plt.title('Quantized image (64 colors, K-Means)')
#plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h))
final_image = recreate_image(k_medoids.cluster_medoids_, labels, w, h)
#mat_image = cv2.fromarray(final_image)
final_image = np.array(final_image, dtype=np.float32) * 100
final_image = np.array(final_image, dtype=np.uint8)
final_image = cv2.cvtColor(final_image, cv2.COLOR_Lab2RGB)
plt.imshow(final_image)

# plt.figure()
# plt.axis("off")
# plt.imshow(image)
plt.show()