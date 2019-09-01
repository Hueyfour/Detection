# coding=utf-8
import xml.dom.minidom
from xml.dom.minidom import parse
class_list = ['background','person','bird', 'cat', 'cow', 'dog', 'horse', 'sheep','aeroplane', 'bicycle', 'boat', 'bus', 'car', 'motorbike', 'train','bottle', 'chair', 'diningtable', 'pottedplant', 'sofa','tvmonitor']

#该函数根据CLASS_LIST的内容，读取xml文件，返回物体类别和标记的框位置
def readxml(addr):
    global class_list
    clas = []
    loca = []
    DOMTree = xml.dom.minidom.parse(addr)
    collection = DOMTree.documentElement
    node =  collection.getElementsByTagName('object')
    for element in node:
        objName = element.getElementsByTagName('name')[0].childNodes[0].nodeValue
        if objName not in class_list:
            continue
        else:
            bndbox = []
            clas.append(objName)
            objBox = element.getElementsByTagName('bndbox')[0]
            bndbox.append(objBox.getElementsByTagName('xmin')[0].childNodes[0].nodeValue)
            bndbox.append(objBox.getElementsByTagName('ymin')[0].childNodes[0].nodeValue)
            bndbox.append(objBox.getElementsByTagName('xmax')[0].childNodes[0].nodeValue)
            bndbox.append(objBox.getElementsByTagName('ymax')[0].childNodes[0].nodeValue)
            bndbox = [int(eval(p)) for p in bndbox]
            loca.append(bndbox)
    clas = [class_list.index(i) for i in clas]
    return clas , loca