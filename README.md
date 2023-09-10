# Seat Detector

## Description
This app uses a machine learning moel to detect people in videos.

## Deployment

* Install requirements: ```pip install -r requirements.txt```
* First download  yolo.weights.
* Next run, ```python3 yolo_video.py --video sample2.mov --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt```
