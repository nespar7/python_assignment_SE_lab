####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from my_package.model import InstanceSegmentationModel
from my_package.data import Dataset
from my_package.analysis import plot_visualization
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage
from PIL import Image

####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from functools import partial
import cv2 as cv
import os

# Define the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor, cwd):

	####### CODE REQUIRED (START) #######
	global segmented_image, bbox_image
	
	# opening the file that the user chooses
	try:
		filename = filedialog.askopenfilename(initialdir=cwd+"/data/imgs", title="select image")
		index = int(os.path.basename(filename)[0])
	except:
		print("Canceled file selection")
		return

	# delete the existing entry and update it to the new file name
	e.delete(0, END)
	e.insert(0, str(index)+'.jpg')

	# processing the image
	item = dataset.__getitem__(index)

	image_s = item['image']
	image_b = image_s.copy()
	pred_boxes, pred_masks, pred_class, pred_score = segmentor(image_s)

	# set an output folder to store the processed images
	output_path = cwd+'/output'
	if not os.path.isdir(output_path):
		os.mkdir(output_path)

	# using the plot visualisation function to process and store the processed images in the given output paths
	segmented_output = output_path + '/' + str(index) + '_segmented.png' 
	bbox_output = output_path + '/' + str(index) + '_bbox.png'
	plot_visualization(image_s, pred_boxes, pred_score, pred_masks, pred_class, segmented_output, "Segmentation")
	plot_visualization(image_b, pred_boxes, pred_score, pred_masks, pred_class, bbox_output, "Bounding-box")

	# reading the stored images and setting the global segmented image and box image
	new_image_s = cv.imread(segmented_output)
	segmented_image = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(new_image_s, cv.COLOR_BGR2RGB)))
	new_image_b = cv.imread(bbox_output)
	bbox_image = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(new_image_b, cv.COLOR_BGR2RGB)))
	####### CODE REQUIRED (END) #######

# Process the images and show them on the picture frame
def process(clicked):

	####### CODE REQUIRED (START) #######
	# if clicked has Segmentation, show the segmented image, else show the bbox image
	try:
		if clicked.get() == "Segmentation":
			image = Label(picture_frame, image=segmented_image).grid(row=1, column=0)		
		else:	
			image = Label(picture_frame, image=bbox_image).grid(row=1, column=0)
	except NameError:
			print("Select an image first")
	####### CODE REQUIRED (END) #######

# function to end the main loop
def close():
	exit()

# `main` function definition starts from here.
if __name__ == '__main__':

	####### CODE REQUIRED (START) ####### (2 lines)
	# Instantiate the root window.
	root = Tk()
	# Provide a title to the root window.
	root.title("Image Viewer")
	####### CODE REQUIRED (END) #######

	# Setting up the segmentor model.
	annotation_file = './data/annotations.jsonl'
	transforms = []

	# Instantiate the segmentor model.
	segmentor = InstanceSegmentationModel()
	# Instantiate the dataset.
	cwd = os.getcwd()
	dataset = Dataset(annotation_file, transforms=transforms, cwd=cwd)
	
	# Declare the options.
	options = ["Segmentation", "Bounding-box"]
	clicked = StringVar()
	clicked.set(options[0])

	e = Entry(root, width=70)
	e.grid(row=0, column=0)

	####### CODE REQUIRED (START) #######
	# Declare the file browsing button
	file_button = Button(root, text="Open Image", command=partial(fileClick, clicked, dataset, segmentor, cwd)).grid(row=0, column=1)
	####### CODE REQUIRED (END) #######

	####### CODE REQUIRED (START) #######
	# Declare the drop-down button
	drop_down_button = OptionMenu(root, clicked, *options).grid(row=0, column=2)
	####### CODE REQUIRED (END) #######

	# This is a `Process` button, check out the sample video to know about its functionality
	myButton = Button(root, text="Process", command=partial(process, clicked)).grid(row=0, column=3)

	# exit button
	close_button = Button(root, text="Close", command=close).grid(row=0, column=4)

	# Frame to show the images
	picture_frame = Frame(root).grid(row=1, column=0)
	
	####### CODE REQUIRED (START) ####### (1 line)
	# Execute with mainloop()
	root.mainloop()
	####### CODE REQUIRED (END) #######