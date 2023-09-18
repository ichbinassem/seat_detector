# Seat Detector

A robust seat detection system built with Django, Vue.js, MySQL, CSS, and HTML.

## Duration
**June 2023 - August 2023**

## Overview

The Seat Detector project is designed to accurately identify and update seating statuses in real-time. It leverages advanced technologies and methodologies to provide a seamless experience for end-users and businesses.

### Key Features:

- **YOLO Model Fine-tuning**: Utilized a dataset of 2000 samples to enhance the YOLO model, ensuring precise seat detection.
  
- **OpenCV Integration**: Incorporated OpenCV to dynamically outline detected objects, providing a visual representation of identified seats.
  
- **High Accuracy**: Achieved over 90% accuracy in updating seating status, ensuring reliability and trustworthiness.
  
- **Continuous Database Updates**: Designed a web service that facilitates ongoing database updates using batch processing of CCTV footage. This ensures that seating statuses are always up-to-date.
  
- **Google Maps API Integration**: Leveraged the Google Maps API to dynamically display restaurant seat availability, resulting in a 60% faster response time for users seeking available seating.

## Technologies Used

- **Backend**: Django
- **Frontend**: CSS, HTML
- **Database**: MySQL
- **Machine Learning**: YOLO model
- **Computer Vision**: OpenCV
- **API**: Google Maps API

## Deployment

* Install requirements: ```pip install -r requirements.txt```
* First download  yolo.weights.
* Next run, ```python3 yolo_video.py --video sample2.mov --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt```
