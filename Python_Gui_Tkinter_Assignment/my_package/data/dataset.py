import cv2 as cv
import json
from my_package.data.transforms import blur, crop, flip, rescale, rotate


class Dataset(object):

    # Storing the transforms and the working directory to take the images from
    def __init__(self, annotation_file, transforms = None, cwd=None):
        
        self.transforms = transforms
        self.cwd = cwd
        
        # Getting the images by reading the annotation file and storing them
        image_list = []
        with open(annotation_file) as f:
            for json_obj in f:
                image_dict = json.loads(json_obj)
                image_list.append(image_dict)

        self.image_list = image_list

        

    def __len__(self):
        
        # returns the length of the image list
        return len(self.image_list)


    def __getitem__(self, idx):
        
        # Given an index, get the images, pngs and bounding boxes
        # apply given transforms on the image and return the dictionary
        image_element = self.image_list[idx]
        image_addr = image_element['img_fn']
        png_addr = image_element['png_ann_fn']
        bboxes = image_element['bboxes']

        # Paths to read for the image and png
        image_path = self.cwd + '/data/' + image_addr
        png_path = self.cwd + '/data/' + png_addr

        image = cv.imread(image_path)
        gt_png_ann = cv.imread(png_path, 0)

        # applying the transforms to the image
        for tran in self.transforms:
            image = tran(image)
            gt_png_ann = tran(gt_png_ann)
        
        # Normalising the image and png
        image = cv.normalize(image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
        gt_png_ann = cv.normalize(gt_png_ann, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
        gt_bboxes = []
        for bbox in bboxes:
            category = bbox['category']
            bbox_coords = bbox['bbox']
            bbox_coords.insert(0, category)
            gt_bboxes.append(bbox_coords)

        # Returning original image for analysis part 2 purposes
        item_dict = {'image' : image, 'gt_png_ann' : gt_png_ann, 'gt_bboxes' : gt_bboxes}

        return item_dict
