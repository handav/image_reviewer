import os
import csv
import cv2
import sys
from pathlib import Path

path_to_saved_images = '/Volumes/Seagate Backup Plus Drive/Hannah_Data/Datasets/AI_Grant/'
results_csv = 'cf_report_1230552_full.csv'

keyword_index = 14
keyword_options = ['city', 'field', 'forest', 'mountain', 'ocean', 'lake', 'road']

font = cv2.FONT_HERSHEY_SIMPLEX
corner = (10,200)
fontScale = 1
fontColor = (255,255,255)
lineType = 2

current_image_name = ''
current_image_counter = 1

def open_csv_results(csv_file):
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        results = list(reader)
    header = results[0]
    for i, item in enumerate(header):
        if header[i] == 'emotion_types':
            emotion_types_index = i 
        if header[i] == 'image_url':
            image_url_index = i
    return [results , emotion_types_index, image_url_index]

def process_url(url, keyword, emotions):
    global current_image_name
    global current_image_counter
    image_filename = url.split('.com/')[1].split('/')[1]
    if current_image_name == image_filename:
        current_image_counter = current_image_counter + 1
    else:
        current_image_counter = 1
    current_image_name = image_filename
    if len(emotions.split(',')) > 3:
        separated_emotions = [', '.join(emotions.split(',')[0:2]), ', '.join(emotions.split(',')[2:])]
        emotions = separated_emotions
        print len(emotions)

    path_to_img = path_to_saved_images + keyword + '/'+image_filename
    img = cv2.imread(path_to_img,1)
    #print len(emotions)

    if len(emotions) == 2:
        text_to_show = str(current_image_counter)+ '. '+ str(emotions[0])
        cv2.putText(img, text_to_show, corner, font, fontScale, fontColor, lineType)
        cv2.putText(img, str(emotions[1]), (corner[0], corner[1]+50), font, fontScale, fontColor, lineType)
    else:
        text_to_show = str(current_image_counter)+ '. '+ emotions
        cv2.putText(img, text_to_show, corner, font, fontScale, fontColor, lineType)
    cv2.imshow('image',img)
    cv2.waitKey(500)
    return current_image_name

def process_emotions(emotions):
    if '\n' in emotions:
        emotions = ', '.join(emotions.split('\n'))
    return emotions

results_and_indexes = open_csv_results(results_csv)
results = results_and_indexes[0]
emotion_types_index = results_and_indexes[1]
image_url_index = results_and_indexes[2]


for i, r in enumerate(results):
    #if not the first row (the header)
    if i > 0:
        keyword = ''
        for item in r:
            if item in keyword_options:
                keyword = item
        emotions = process_emotions(r[emotion_types_index])
        if keyword == '':
            sys.exit('Exit: no keyword found.')
        process_url(r[image_url_index], keyword, emotions)
