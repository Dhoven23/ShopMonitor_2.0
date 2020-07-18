import cv2
import time
import numpy as np

StudentID = 20481553

screen = np.zeros((1080,1920,3))

def main():
    face = cv2.imread(f"{StudentID}.jpg")

    screen[0:640,0:480] = face
    cv2.imshow('test', face)
    cv2.imshow('blank', screen)
    cv2.waitKey()
    print(np.shape(face))


if __name__ == '__main__':
    main()
