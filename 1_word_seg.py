import cv2
import easyocr

import numpy as np

img = cv2.imread('img.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh, bin_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

img_h,img_w = bin_img.shape
def rem_black_frame():
    start_black = 0
    for hi in range(img_h):
        blackpixel_count = (bin_img[hi, :] == 0).sum()
        if blackpixel_count >0:
            start_black +=1
        else:
            break
    bin_img[:start_black, :] = 255

    end_black = 1
    for hi in range(img_h -1,0,-1):
        blackpixel_count = (bin_img[hi, :] == 0).sum()
        if blackpixel_count >0:
            end_black +=1
        else:
            break
    bin_img[-end_black:,:] = 255

    for wi in range(img_w):
        blackpixel_count = (bin_img[:,wi] == 0).sum()
        if blackpixel_count >0:
            start_black +=1
        else:
            break
    bin_img[:,start_black] = 255

    end_black = 1
    for wi in range(img_w -1,0,-1):
        blackpixel_count = (bin_img[:,wi] == 0).sum()
        if blackpixel_count >0:
            end_black +=1
        else:
            break
    bin_img[:,-end_black:] = 255


rem_black_frame()
whitelineList = []
blacklineList = []
whitecolList = []
blackcolList = []
def row_number():
    whiteline = 0
    blackline = 0

    flag = 255
    for hi in range(img_h):
        blackpixel_count = (bin_img[hi, :] == 0).sum()
        if blackpixel_count == 0:
            whiteline += 1
            if flag == 0:
                blacklineList.append(blackline)
                blackline = 0
            flag = 255
        else:
            blackline += 1
            if flag == 255:
                whitelineList.append(whiteline)
                whiteline = 0

            flag = 0


def column_number():
    whiteline = 0
    blackline = 0

    flag = 255
    for wi in range(img_w):
        blackpixel_count = (bin_img[:,wi] == 0).sum()
        if blackpixel_count == 0:
            whiteline += 1
            if flag == 0:
                blackcolList.append(blackline)
                blackline = 0
            flag = 255
        else:
            blackline += 1
            if flag == 255:
                whitecolList.append(whiteline)
                whiteline = 0

            flag = 0

row_number()
column_number()

print(whitelineList)
print(blacklineList)
print(whitecolList)
print(blackcolList)
read = easyocr.Reader(['ch_tra'])
if len(blacklineList)==1:
    result = read.readtext(img)
    print(result)
ocr_pic = np.zeros((800,900),np.uint8)
ocr_pic[:] = 255

for i in range(len(whitecolList)):
    if i == 0:
        start_x = whitecolList[0]
    else:
        start_x += whitecolList[i]+ blackcolList[i-1]
    for j in range(len(whitelineList)):
        if j == 0:
            start_y = whitelineList[0]
        else:
            start_y += whitelineList[j] + blacklineList[j - 1]
        ocr_pic[50+i*50:50+i*50+blacklineList[j],50+j*50:50+j*50+blackcolList[i]]= gray[start_y:start_y+blacklineList[j],start_x:start_x+blackcolList[i]]
result = read.readtext(ocr_pic,detail=0)
print(result[::-1])
cv2.imshow('ocr',ocr_pic)
cv2.waitKey(0)
cv2.destroyWindow("ocr")


