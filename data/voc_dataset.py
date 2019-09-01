# coding=utf-8
import os
import numpy as np
from skimage import io
from PIL import Image
from readxml import readxml

class VOCDataset:
    """VOC2012数据集"""
    def __init__(self, xml_dir, image_dir, transform=None):
        """
        Args:
            xml_dir (string): xml文件的路径.
            root_dir (string):图片的目录.
            transform (callable, optional): 对样本施加的变换
        """

        g_im = os.walk(image_dir)
        self.image_dir = image_dir
        self.xml_dir = xml_dir
        self.transform = transform
        _,_,self.imgList = next(g_im)
        
    def __len__(self):
        return len(self.imgList)

    def __getitem__(self, idx):
        xmlName = self.imgList[idx][0:-4] + '.xml'
        image = io.imread(os.path.join(self.image_dir,self.imgList[idx]))
        new_im = Image.fromarray(image)
        new_im = new_im.convert('RGB')
        image = np.asarray(new_im)
        category,location = readxml(os.path.join(self.xml_dir,xmlName))
        location = np.array(location)
        sample = {'image':image , 'class':category , 'location':location}
        if self.transform:
            sample = self.transform(sample)
        return sample