import random
import cv2 as cv
from my_package.data.transforms import BlurImage, FlipImage, RescaleImage, RotateImage, CropImage
from matplotlib import pyplot as plt
import numpy as np

def plot_visualization(image, pred_boxes, pred_scores, pred_maps, pred_classes, output, mode): # Write the required arguments

  img = image

  # Finding the indices of the first 3 maps with highest scores
  b = pred_scores[:]
  indices = []
  number = min(3, len(pred_scores))
  for i in range(number):
    max_index = b.index(max(b))
    indices.append(max_index)
    b[max_index] = -1

  fig, (ax1, ax2) = plt.subplots(1, 2)
  plt.subplot(1, 2, 1)
  plt.imshow((img*255).astype(np.uint8)[:,:,[2,1,0]])

  # For each of the three indices, add the masks to the image
  if mode == "Segmentation":
    for i in indices:
      box = pred_boxes[i]
      mask = pred_maps[i][0]*255
      # The colors are random for each mask
      c1 = random.uniform(0, 1)
      c2 = random.uniform(0, 1)
      c3 = random.uniform(0, 1)
      for j in range(int(box[0][0]), int(box[1][0])):
        for k in range(int(box[0][1]), int(box[1][1])):
          if mask[k][j] >= 200:
            img[k][j] = (img[k][j][0]*c1, img[k][j][1]*c2, img[k][j][2]*c3)
      

  else:  
    for i in indices:
      box = pred_boxes[i]
      c1 = random.uniform(0, 1)
      c2 = random.uniform(0, 1)
      c3 = random.uniform(0, 1)
      # Drawing the bounding box on the image
      cv.rectangle(img, box[0], box[1], (c1*255, c2*255, c3*255), 3)

  plt.subplot(1, 2, 2)
  plt.imshow((image*255).astype(np.uint8)[:,:,[2,1,0]])

  # Saving the output image to the output folder
  plt.savefig(output, dpi = 250, bbox_inches = 'tight', pad_inches = 0)
    