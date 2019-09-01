# coding=utf-8
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class_list = ['background','person','bird', 'cat', 'cow', 'dog', 'horse', 'sheep','aeroplane', 'bicycle', 'boat', 'bus', 'car', 'motorbike', 'train','bottle', 'chair', 'diningtable', 'pottedplant', 'sofa','tvmonitor']

#编写一个可以展示图片以及目标边界框的函数
def show_groundBox(image, classse = [], locations = []):
    if type(image) == type('./data'):
        image = plt.imread(image)
    colorList = ['b', 'g', 'r', 'c', 'm', 'y']
    fig,ax = plt.subplots(1)
    ax.imshow(image)
    for i,ele in enumerate(locations):
        if classse[i] == -1:
            break
        c = classse[i]%6
        rect = patches.Rectangle((ele[0],ele[1]),ele[2]-ele[0],ele[3]-ele[1],
                                 linewidth=2,edgecolor=colorList[c],facecolor='none')
        ax.add_patch(rect)
        ax.text(ele[0]+3, ele[1]-3, class_list[classse[i]],backgroundcolor = colorList[c],color = 'w')
