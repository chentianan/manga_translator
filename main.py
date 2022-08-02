import cv2
import easyocr
import word_seg
import tkinter as tk
import tkinter.filedialog as fd
import translator

def word_extra(filename):

    img = cv2.imread(filename)
    read = easyocr.Reader(['ch_tra'])
    place,bb = read.detect(filename)


    list_word = place[0]
    space = 3
    boxlist = []
    for x1,x2,y1,y2 in place[0]:
        i=0
        for box in boxlist:

            x11=box[0]-space
            x12=box[1]+space
            y11=box[2]-space
            y12=box[3]+space
            Lx=abs((x1 + x2) / 2 - (x11 + x12) / 2)
            Ly=abs((y1 + y2) / 2 - (y11 + y12) / 2)
            Sax=abs(x1-x2)
            Sbx=abs(x11-x12)
            Say=abs(y1-y2)
            Sby=abs(y11-y12)
            if Lx <= (Sax + Sbx) / 2 and  Ly <= (Say + Sby) / 2 :
                boxlist[i]=[min(x1,box[0]),max(x2,box[1]),min(y1,box[2]),max(y2,box[3])]
                break
            i+=1
        else:
            boxlist.append([x1,x2,y1,y2])

    image_high, image_width, rgb = img.shape



    for x in boxlist:
        if x[0] <= 0:
            x[0] = 0

        if x[1] >= image_width:
            x[1] = image_width

        if x[2] <= 0:
            x[2] = 0

        if x[3] >= image_high:
            x[3] = image_high
        print(x)

    total_number = len(boxlist)
    cv2.namedWindow('img',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img',1024,768)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    for i in boxlist:
        cv2.rectangle(img, (i[0], i[2]), (i[1], i[3]), (0, 0, 255), 2)

    cv2.imshow("img",img)

    j = 1
    for i in boxlist:

        numberOfPic.set(str(total_number)+":"+str(j))

        string1 = word_seg.word_seg(gray[i[2]:i[3],i[0]:i[1]])


        if string1 != '':
            Or_text.set(string1)
            converted_text.set(translator.translate(Or_text.get()))
            numberOfWord.set(str(len(string1)))

            root.update()
            cv2.imshow('word',img[i[2]:i[3],i[0]:i[1]])
            cv2.waitKey(0)
            cv2.destroyWindow('word')
        j+=1




#word_extra("001.jpg")
def select_file():
    file_name = fd.askopenfilename()
    file_path.set(file_name)

def translator_():
    word_extra(file_path.get())



root = tk.Tk()
root.title("WordTranslation")
root.geometry('800x600+300+100')
file_path = tk.StringVar()
tk.Label(root, text = "picture_selection").place(x=20,y=20)
t1 = tk.Entry(root,textvariable = file_path,width = 60)
t1.place(x=100,y=20)
tk.Button(root, text = "browse...",command = select_file).place(x=50,y=60)
tk.Button(root, text = "convert", command = translator_).place(x = 50,y =100)
Or_text = tk.StringVar()
converted_text = tk.StringVar()
tk.Entry(root,textvariable = Or_text,width = 100).place(x=20,y=150)

tk.Entry(root,textvariable = converted_text,width = 100).place(x=20,y=220)
numberOfWord = tk.StringVar()
numberOfPic = tk.StringVar()
tk.Entry(root,textvariable = numberOfPic).place(x=20,y=320)
tk.Entry(root,textvariable = numberOfWord).place(x=20,y=420)


root.mainloop()
cv2.destroyAllWindows()













