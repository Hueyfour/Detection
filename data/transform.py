# coding=utf-8
import numpy as np
import random
import torch
from skimage import transform, exposure
from PIL import Image


class RandomCrop:
    """
    随机裁剪图像.
    """
    def __call__(self, sample):
        image,category,bboxes = sample['image'], sample['class'], sample['location']
        h_img, w_img, _ = image.shape
        # 得到可以包含所有bbox的最大bbox
        max_bbox = np.concatenate([np.min(bboxes[:, 0:2], axis=0), np.max(bboxes[:, 2:4], axis=0)], axis=-1)
        max_l_trans = max_bbox[0]
        max_u_trans = max_bbox[1]
        max_r_trans = w_img - max_bbox[2]
        max_d_trans = h_img - max_bbox[3]
        
        
        crop_xmin = max(0, int(max_bbox[0] - random.uniform(0, max_l_trans)))
        crop_ymin = max(0, int(max_bbox[1] - random.uniform(0, max_u_trans)))
        crop_xmax = max(w_img, int(max_bbox[2] + random.uniform(0, max_r_trans)))
        crop_ymax = max(h_img, int(max_bbox[3] + random.uniform(0, max_d_trans)))
        
        image = image[crop_ymin : crop_ymax, crop_xmin : crop_xmax]
 
        bboxes[:, [0, 2]] = bboxes[:, [0, 2]] - crop_xmin
        bboxes[:, [1, 3]] = bboxes[:, [1, 3]] - crop_ymin

        return {'image':image , 'class':category , 'location':bboxes}
    
        
class Expand:
    
    def __init__(self, prob = 0.5):
        self.prob = prob
    
    def __call__(self, sample):        
        image,category,location = sample['image'], sample['class'], sample['location']
        location = location.copy()
        h, w, d = image.shape
        if h>w:
            length = (h-w)/2
            expand_image = np.full((h,int(2*length+w), d),122,dtype=image.dtype)
            expand_image[0:h, int(length):int(length + w)] = image
            location[:,0] += (int(length))
            location[:,2] += (int(length))
            
        else:
            length = (w-h)/2
            expand_image = np.full((int(2*length+h),w, d),122,dtype=image.dtype)
            expand_image[int(length):int(length + h),0:w] = image
            location[:,1] += (int(length))
            location[:,3] += (int(length))        
        image = expand_image
        
        if np.random.random_sample() < self.prob:
            h, w, d = image.shape
            l = random.randint(h,3*h)
            expand_image = np.full((l,l, d),122,dtype=image.dtype)
            c = random.randint(0,l-h)
            d = random.randint(0,l-h)
            expand_image[c:c+h, d:d+w] = image
            image = expand_image
            location[:,0] += (d)
            location[:,1] += (c)
            location[:,2] += (d)
            location[:,3] += (c)

        return {'image':image , 'class':category , 'location':location}
       

class Rescale:
    """缩放图像为给定大小.

    参数:
        output_size (tuple or int): 描述缩放为正方形的大小. 
    """
    def __init__(self, output_size):
        #assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image,category,location = sample['image'], sample['class'], sample['location']
        h, w = image.shape[:2]        
        new_h, new_w = self.output_size,self.output_size
        image = transform.resize(image, (new_h, new_w))
        location = location * [new_w / w, new_h / h, new_w / w, new_h / h]
        return {'image':image, 'class':category , 'location':location}
    

class RandomFlip:
    """
    随机水平翻转图像.
    参数：翻转概率
    """
    def __init__(self, probability = 0.3):
        self.probability = probability
    def __call__(self, sample): 
        image,category,location = sample['image'], sample['class'], sample['location']
        h, w = image.shape[:2]
        if np.random.random_sample() < self.probability:
            new_im = Image.fromarray(image)
            new_im = new_im.transpose(Image.FLIP_LEFT_RIGHT)
            image = np.asarray(new_im)
            for coordinate in location:
                coordinate[0],coordinate[2] = w - coordinate[2],w - coordinate[0]
        return {'image':image , 'class':category , 'location':location}
    
    
class ColorDistortion:
    """
    随机调整图像亮度.
    参数：调整概率
    """
    def __init__(self, probability = 0.3):
        self.probability = probability
    def __call__(self, sample): 
        image,category,location = sample['image'], sample['class'], sample['location']
        if np.random.random_sample() < self.probability:
            gamma = np.random.uniform(0.2,1.7,1)
            image = exposure.adjust_gamma(image,gamma)
        return {'image':image , 'class':category , 'location':location} 
    
    
class Extend:
    """
    填充名称列表和位置数组，以便使用dataloader
    类填充为-1，坐标填充为0，0，0，0
    参数： 填充的长度
    """
    def __init__(self,length = 60):
        self.length = length
        
    def __call__(self,sample):
        image,category,location = sample['image'], sample['class'], sample['location']
        zeros = np.zeros((self.length-len(category),4))
        category = category + [-1]*(self.length-len(category))
        location = np.row_stack((location,zeros))
        return {'image':image , 'class':category , 'location':location}
    
class ToTensor:
    """
    从 ndarrays 转换为 Tensors.
    """

    def __call__(self, sample):
        image,category,location = sample['image'], sample['class'], sample['location']
        # 需要转换轴，因为
        # numpy image: H x W x C
        # torch image: C X H X W
        image = image.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image),
                'class': torch.from_numpy(np.array(category)),
                'location': torch.from_numpy(location).type(torch.FloatTensor)}