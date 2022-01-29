from my_package.model import InstanceSegmentationModel
from my_package.data import Dataset
from my_package.analysis import plot_visualization
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage
import os

cwd = os.getcwd()

def experiment(annotation_file, segmentor, transforms, outputs, index = -1, exp_name = ""):
    #Create the instance of the dataset.
    
    new_ann_file = cwd+'/'+annotation_file
    D = Dataset(annotation_file=new_ann_file, transforms=transforms, cwd=cwd)

    #Iterate over all data items.

    data_set = []
    # If the index is not specified, do the experiment for 
    # all the images, else do the experiment for only 
    if index == -1:
        for idx in range(D.__len__()):
            item_dict = D.__getitem__(idx)
            data_set.append(item_dict)

    else:
        item_dict = D.__getitem__(index)
        data_set.append(item_dict)

    #Get the predictions from the segmentor.
    prediction_list = []
    if index == -1:
            i = 0
            new_path = outputs+'/boxes.txt'
            file = open(new_path, 'w')
        
    # If index is -1(all images are searched) we write the prediction boxes
    # to the boxes.txt file
    for data in data_set:
        pred_boxes, pred_maps, pred_class, pred_scores = segmentor(data['image'])
        prediction_list.append([pred_boxes, pred_maps, pred_class, pred_scores])
        if index == -1:
            file.write('box ' + str(i) + ' : ' + str(pred_boxes) + "\n")
            i = i+1

    if index == -1:
        print('saved boxes')

    #Draw the segmentation maps on the image and save them.
    for i in range(len(data_set)):
        image = data_set[i]['image']
        # If no experiment name is given store as "i.png"
        if exp_name == "":
            output = outputs + '/' + str(i) + '.png'
        else:
            output = outputs + '/' + exp_name + '.png'
        plot_visualization(image, pred_boxes=prediction_list[i][0], pred_scores=prediction_list[i][3], pred_maps=prediction_list[i][1], pred_classes=prediction_list[i][2], output=output)


def main():
    segmentor = InstanceSegmentationModel()
    # making a folder 'output' for sample experiment
    path = cwd+'/output'
    if not os.path.isdir(path):
        os.mkdir(path)
    annotation_file = './data/annotations.jsonl'
    experiment(annotation_file, segmentor, [FlipImage(), BlurImage(7)], path) # Sample arguments to call experiment()
    print("sample experiment completed")
    # making a new folder for analysis task 2 
    path = path + '/ana_task_2'
    if not os.path.isdir(path):
        os.mkdir(path)
    # experiment with original image
    experiment(annotation_file, segmentor, [], path, 8, "original")
    print("Experiment with original image completed")
    # experiment with Horizontally flipped image
    experiment(annotation_file, segmentor, [FlipImage()], path, 8, "flipped")
    print("experiment with Horizontally flipped image completed")
    # experiment with blurred image
    experiment(annotation_file, segmentor, [BlurImage(7)], path, 8, "blurred")
    print("experiment with blurred image completed")
    # experiment with twice scaled image
    experiment(annotation_file, segmentor, [RescaleImage(2)], path, 8, "twice")
    print("experiment with twice scaled image completed")
    # experiment with half scaled image
    experiment(annotation_file, segmentor, [RescaleImage(0.5)], path, 8, "half")
    print("experiment with half scaled image completed")
    # experiment with 90 degree right rotated image
    experiment(annotation_file, segmentor, [RotateImage(270)], path, 8, "right")
    print("experiment with 90 degree right rotated image completed")
    # experiment with 45 degree rotated image
    experiment(annotation_file, segmentor, [RotateImage(45)], path, 8, "left")
    print("experiment with 45 degree rotated image completed")


if __name__ == '__main__':
    main()
