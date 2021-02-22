import cv2
import numpy as np
import pandas as pd
import torch

#Constants



#Input Functions for Sample Solution

def load_labels(file_name, image_width, image_height, frame_number=-1):
    '''
    return pandas DF when frame_number is -1
    return pytorch tensor when frame_number is a valid frame number
    '''
    data = pd.read_csv(file_name, sep=' ')

    data['X'] = data['X'].apply(lambda x: x*image_width)
    data['Y'] = data['Y'].apply(lambda x: x*image_height)
    data['Width'] = data['Width'].apply(lambda x: x*image_width)
    data['Height'] = data['Height'].apply(lambda x: x*image_height)

    if frame_number==-1:
        return data
    frame = data[(data["Frame"]==frame_number)]
    pt_frame = torch.tensor(frame[["Class","ID","X","Y","Width","Height"]].values)
    return pt_frame





#Output Functions for Sample Solution
def detect_catches(image, bbox_xyxy, classes, ids, frame_num, colorDict, frame_catch_pairs, ball_person_pairs):
    #Create a list of bbox centers and ranges
    bbox_XYranges = bbox_xyxy2XYranges(bbox_xyxy)
    

    #Detect the color of each ball and return a dictionary matching id to color
    detected_ball_colors = detect_colors(image, bbox_XYranges, classes, ids, colorDict)

    #Detect collison between balls and people
    collisions = detect_collisions(classes, ids, frame_num, bbox_XYranges, detected_ball_colors)

    #Update dictionary pairs
    frame_catch_pairs, ball_person_pairs = update_dict_pairs(frame_num, collisions, frame_catch_pairs, ball_person_pairs)
    bbox_strings = format_bbox_strings(ids, classes, detected_ball_colors, collisions)

    return (bbox_strings, frame_catch_pairs, ball_person_pairs)




def detect_colors(image, bbox_XYranges, classes, ids, colorDict):
    detected_ball_colors = {}
    bbox_offset = 5

    for i in range(len(classes)):

        #Checks if the class is a ball (1)
        if (classes[i] == 1): 
            #Extract region of interest HSV values
            #Image values are (height, width, colorchannels)
            X = bbox_XYranges[i][0]
            Y = bbox_XYranges[i][1]
            roi_bgr = image[(Y - bbox_offset):(Y + bbox_offset), (X - bbox_offset):(X + bbox_offset)]


            #Convert BGR image to HSV image
            roi_hsv = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)
            hue  = np.mean(roi_hsv[:,:,0])
            sat = np.mean(roi_hsv[:,:,1])
            val   = np.mean(roi_hsv[:,:,2])
            ball_color = (hue, sat, val)


            #Check if the color is in a specified range
            for color in colorDict:
                upper = colorDict[color][0]
                lower = colorDict[color][1]

                if (ball_color <= upper) :
                    if (ball_color >= lower) :
                        detected_ball_colors[ids[i]] = [color, bbox_XYranges[i][0], bbox_XYranges[i][1]]
                        break

    return detected_ball_colors


def bbox_xyxy2XYranges(bbox_xyxy):
    bbox_XYranges = []

    #Create list of bbox centers and ranges
    for box in bbox_xyxy:
        #Get bbox corners
        xmin = int(box[0])
        ymin = int(box[1])
        xmax = int(box[2])
        ymax = int(box[3])

        #Get center of bounding box
        X = int(((xmax - xmin) / 2) + xmin)
        Y = int(((ymax - ymin) / 2) + ymin)

        #Create a range for collison detection
        X_range = (X - ((xmax - xmin) / 2), X + ((xmax - xmin) / 2))
        Y_range = (Y - ((ymax - ymin) / 2), Y + ((ymax - ymin) / 2))

        bbox_XYranges.append([X, Y, X_range, Y_range])

    return bbox_XYranges


def format_bbox_strings(ids, classes, detected_ball_colors, collisions):
    bbox_strings = [None] * len(classes)

    for i in range(len(classes)):
        #Person bbox info
        if (ids[i] in collisions):
            color = collisions[ids[i]][0]
            txt = 'Holding {color}'.format(color = color)

        #Ball bbox info    
        elif (ids[i] in detected_ball_colors):
            color = detected_ball_colors[ids[i]][0]
            txt = 'Detected {color}'.format(color = color)

        else:
            txt = ''

        bbox_strings[i] = txt

    return bbox_strings


def detect_collisions(classes, ids, frame_num, bbox_XYranges, detected_ball_colors):
    #collisions = {'id' : color, ....}
    collisions = {}

    for i in range(len(classes)):
        #Check if a person
        if (classes[i] == 0):

            #Get persons bbox range
            person_X_range = bbox_XYranges[i][2]
            person_Y_range = bbox_XYranges[i][3]

            #Check if the center of a ball is in a persons bounding box
            #detected_ball_colors = {'id' : [color, X, Y], ...}
            for ball in detected_ball_colors:
                ball_color = detected_ball_colors[ball][0]
                ball_X = detected_ball_colors[ball][1]
                ball_Y = detected_ball_colors[ball][2]

                if (ball_X >= person_X_range[0] and ball_X <= person_X_range[1] and ball_Y >= person_Y_range[0] and ball_Y <= person_Y_range[1]):
                    collisions[ids[i]] = ball_color
                    break

    return collisions


def update_dict_pairs(frame_num, collisions, frame_catch_pairs, ball_person_pairs):
    for person in collisions:
        color = collisions[person]

        #Ball color has not been held yet
        if (color not in ball_person_pairs):
            ball_person_pairs[color] = person

        #Ball is held by a new person 
        elif (ball_person_pairs[color] != person):
            ball_person_pairs[color] = person
            frame_catch_pairs.append([frame_num, ball_person_pairs])

            print([frame_num, ball_person_pairs])

    return (frame_catch_pairs, ball_person_pairs)



    
        






