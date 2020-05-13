from django.http import HttpResponse
from django.shortcuts import render

import cv2


def index(request):
    return render(request, "build/index.html")


def capture_image(request):
    capture = cv2.VideoCapture(0)  # TODO: checkout camera device num
    ret, frame = capture.read()
    print(ret)
    print(frame)
    capture.release()
    return HttpResponse('Done')
