import cv2
import easyocr

import numpy as np
def word_seg(gray):
#img = cv2.imread('img.png')


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

        start_black = 0
        for wi in range(img_w):
            blackpixel_count = (bin_img[:,wi] == 0).sum()
            if blackpixel_count >0:
                start_black +=1
            else:
                break
        bin_img[:,:start_black] = 255

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

    read = easyocr.Reader(['ch_tra'])
    if len(blacklineList) == 1:
        ocr_pic = np.zeros((100+img_h,100+img_w),np.uint8)
        ocr_pic[:]= 255
        ocr_pic[50:50+img_h,50:50+img_w] = gray

        result = read.readtext(ocr_pic)
        print(result)
        if result[0][2]>0.1:
            return result[0][1]
        else:
            return ''
    elif len(blacklineList) == 0:
        return ''


    column_number()


    def new_list(white, black, size):
        if len(black) <2:
            return white,black
        min_white = 100
        max_black = max(black)

        ix = black.index(max_black)
        templist = white+[100000]
        templist[0] = 999999
        j = -1
        for i in range(black.count(max_black)):
            j = black.index(max_black,j+1)
            min_white = min(min_white,templist[j],templist[j+1])
        j = -1

        for i in range(black.count(max_black-1)):
            j = black.index(max_black-1, j + 1)
            min_white = min(min_white, templist[j], templist[j + 1])

        if black.count(max_black)+black.count(max_black-1)<2:
            hight = black[0]+white[1]+black[1]
            if abs(hight-size)<=5:

                max_black = hight
                if len(black)>2:
                    min_white = white[2]
                else:
                    min_white = 2
                ix = 0





        def list_pos(white, black):
            white_list_new = []
            black_list_new = []
            ah1 = 0
            for i in range(0,len(black)):
                if black[i] <= max_black - 2:
                    ah1 += black[i] + white[i]
                    if ah1 >= max_black + min_white +2:
                        white_list_new.append(min_white)
                        black_list_new.append(max_black)
                        ah1 = ah1 - (max_black+min_white)

                    if -2 < ah1-min_white-max_black < 1:
                        black_list_new.append(max_black)
                        white_list_new.append(ah1-max_black)
                        ah1 = 0

                    elif i == len(black)-1:
                        white_list_new.append(min_white)
                        black_list_new.append(ah1-min_white)


                else:
                    if ah1 > 0:
                        white_list_new.append(min_white)
                        black_list_new.append(max_black)
                        white_list_new.append(ah1+white[i]-max_black-min_white)

                    else:
                        white_list_new.append(white[i])
                    black_list_new.append(black[i])
                    ah1 = 0

            return (white_list_new,black_list_new)
        white1 = white[ix:]
        black1 = black[ix:]
        white_after_max,black_after_max = list_pos(white1,black1)
        black2 = black[ix::-1]
        if ix == len(black)-1:
            white2 = [min_white]+white[:0:-1]
        else:
            white2 = white[ix+1:0:-1]
        white_before_max,black_before_max = list_pos(white2,black2)


        white_list_new = [white[0]]+white_before_max[:0:-1] + white_after_max[1:]
        black_list_new = black_before_max[:0:-1] + black_after_max

        return  white_list_new , black_list_new

    max_hight = max(blacklineList)
    max_width = max(blackcolList)
    whitelineList,blacklineList = new_list(whitelineList,blacklineList,max_width)
    whitecolList,blackcolList = new_list(whitecolList,blackcolList,max_hight)










    ocr_pic = np.zeros((160+len(blackcolList)*(max_hight+20),100+len(blacklineList)*(max_width+6)),np.uint8)
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
            ocr_pic[80+i*(max_hight+20):80+i*(max_hight+20)+blacklineList[j],50+j*(max_width+6):50+j*(max_width+6)+blackcolList[i]]= gray[start_y:start_y+blacklineList[j],start_x:start_x+blackcolList[i]]
    result = read.readtext(ocr_pic)[::-1]
    str1 = ''
    for item in result:
        if item[2] > 0.2:
            str1 += item[1]


    return (str1)



