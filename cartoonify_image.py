# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import cv2
import numpy as np
import imageio
import matplotlib.pyplot as plt
import easygui


# %%
import os
import sys


# %%
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


# %%
top=tk.Tk()
top.geometry('400x300')
top.title('Let us make you into a cartoon !')
top.configure(background='white')
label=Label(top,background='#9edee7', font=('Arial',20,'bold'))


# %%
def upload():
    imagePath = easygui.fileopenbox()
    cartoonify(imagePath)


# %%
def cartoonify(imagePath):
    Img = cv2.imread(imagePath)
    Img = cv2.cvtColor(Img,cv2.COLOR_BGR2RGB)

    if Img is None:
        print("Can not be found. Choose an appropriate image")
        sys.exit()

    Resize1=cv2.resize(Img, (800,330))

    #convert image to grayscale
    grayScaleImage=cv2.cvtColor(Img,cv2.COLOR_BGR2GRAY)
    Resize2=cv2.resize(grayScaleImage, (800, 330))

    #blur the image
    #use  medianblur 
    blurredScaleImage=cv2.medianBlur(grayScaleImage, 9)
    Resize3=cv2.resize(blurredScaleImage,  (800, 330))

    #retrieving the edges of the image
    #use the threshold technique`
    edgeScaleImage=cv2.adaptiveThreshold(blurredScaleImage,125,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,12)
    Resize4=cv2.resize(edgeScaleImage,(800,330))

    #applying bilateral filter to image
    #adding a water paint effect
    colorImage=cv2.bilateralFilter(Img,15, 80, 80)
    Resize5=cv2.resize(colorImage,(800,330))

    #applying cartoon effects
    #using bitwise_and to add blackness or defined edges to water paint image
    maskedImage=cv2.bitwise_and(colorImage,colorImage,mask=edgeScaleImage)
    Resize6=cv2.resize(maskedImage, (960,500))
    
    images=[Resize1, Resize2, Resize3, Resize4, Resize5, Resize6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    #making a save button
    save1=Button(top,text='Save the cartoonized image',command=lambda:save(imagePath, Resize6))
    save1.configure(background='#ff1493')
    save1.pack(side=TOP, pady=60)

    plt.show()



# %%
#saving the image
def save(Resize6, imagePath):
    newName="cartoonified image"
    path1=os.path.dirname(imagePath)
    extension=os.path.splitext(imagePath)
    path=os.path.join(path1,newName+extension)
    cv2.imwrite(path, cv2.cvtColor(Resize6,cv2.COLOR_RGB2BGR))

    text = 'image'+ newName +'saved at'+ path
    tk.messagebox.showinfo(title='Ta da!', message = text)


# %%
upload = Button(top,text='Cartoonify',padx=6,pady=4,command=upload,)
upload.configure(background='#ff1493', font=('Arial',26,'bold'))
upload.pack(side=TOP,pady=40)


# %%
top.mainloop()


