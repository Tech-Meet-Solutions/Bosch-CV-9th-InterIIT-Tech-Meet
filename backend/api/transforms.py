import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as mpimg
import cv2


def resize(img, output_size): # Not now
    return cv2.resize(img, output_size)

def clip(img, maxI, minI = 0): # Yes Pixel
    img[np.where(img<minI)] = minI
    img[np.where(img>maxI)] = maxI
    return img

def flip(img, h=True, v=False): # Checkbox Geometric
    if h:
        img = np.flip(img,1)
    if v:
        img = np.flip(img,0)
    return img

def crop(img, x0, y0, h, w):  # Search for bounding box
    return img[x0:x0+h, y0:y0+w]

def sharpen(img, factor = 4): # Yes Colorspace
    identity = np.array([[0,0,0],[0,1,0],[0,0,0]])
    sharp = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])/4
    sharpened = sharp*np.random.random()*factor
    kernel = identity + sharpened
    return cv2.filter2D(img,-1,kernel)

def Blur2D(Image, BlurLevel):
    Kernel = np.ones((BlurLevel, BlurLevel), np.float32) / (BlurLevel * BlurLevel)
    Image = cv2.filter2D(Image, -1, Kernel)
    return Image

def BlurGauss(Image, BlurLevel):
    Image = cv2.GaussianBlur(Image, (BlurLevel, BlurLevel), 0)
    return Image

def BlurMedian(Image, BlurLevel):
    Image = cv2.medianBlur(Image, BlurLevel)
    return Image

def translate(img, x0, y0): #Done Geometric
    h, w = img.shape[:2]
    T = np.float32([[1,0,x0],[0,1,y0]])
    return cv2.warpAffine(img,T,(w,h))

def padding(img,padx = 10, pady = 10, color = (0,0,0)): #Not now
    h, w, c = img.shape
    hh = h + 2*padx
    ww = w + 2*pady
    result = np.full((hh,ww,c),color,dtype=np.uint8)
    result[padx:h+padx,pady:w+pady] = img
    return result

def rotate(image, angle): #Rotate Geometric
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def shearImage(image, shearLevelX, shearLevelY):
    # shearLevel should be between 0 and 1, float value
    h, w = image.shape[:2]
    M = np.eye(3)
    if shearLevelX:
        M = M @ np.float32([[1, 0.5 * shearLevelX, 0], [0, 1, 0], [0, 0, 1]])
    if shearLevelY:
        M = M @ np.float32([[1, 0, 0], [0.5 * shearLevelY, 1, 0], [0, 0, 1]])
    return cv2.warpPerspective(image, M, (int(w * 1.5), int(h * 1.5)))

class Cutout(object): #Not now
    def __init__(self,
                 min_size_ratio,
                 max_size_ratio,
                 channel_wise=False,
                 crop_target=True,
                 max_crop=10,
                 replacement=0):
        self.min_size_ratio = np.array(list(min_size_ratio))
        self.max_size_ratio = np.array(list(max_size_ratio))
        self.channel_wise = channel_wise
        self.max_crop = max_crop
        self.replacement = replacement

    def __call__(self, img):
        size = np.array(img.shape[:2])
        mini = self.min_size_ratio * size
        maxi = self.max_size_ratio * size
        for _ in range(self.max_crop):
            # random size
            h = np.random.randint(mini[0], maxi[0])
            w = np.random.randint(mini[1], maxi[1])
            # random place
            shift_h = np.random.randint(0, size[0] - h)
            shift_w = np.random.randint(0, size[1] - w)
            if self.channel_wise:
                c = np.random.randint(0, X.shape[-1])
                img[shift_h:shift_h+h, shift_w:shift_w+w, c] = self.replacement
            else:
                img[shift_h:shift_h+h, shift_w:shift_w+w] = self.replacement
        return img


class Leaf(object): #Npt now
    def __init__(self):
        pass
    def __call__(self, img):
        blur = cv2.GaussianBlur(img, (7, 7), 0)
        hsv_blur = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        # lower mask (0-10)
        lower_red = np.array([0,130,130])
        upper_red = np.array([20,255,255])
        mask_0 = cv2.inRange(hsv_blur, lower_red, upper_red)

        # upper mask (170-180)
        lower_red = np.array([165,130,130])
        upper_red = np.array([185,255,255])
        mask_1 = cv2.inRange(hsv_blur, lower_red, upper_red)
        hsv_blur[np.where(mask_1)] = hsv_blur[np.where(mask_1)] - np.array([165, 0, 0])

        mask = mask_0 + mask_1
        # change color
        turn_color = np.random.randint(0, 255)
        hsv_blur[np.where(mask)] = hsv_blur[np.where(mask)] + np.array([turn_color, 0, 0])
        img_blur = cv2.cvtColor(hsv_blur, cv2.COLOR_HSV2BGR)
        img[np.where(mask)] = img_blur[np.where(mask)]
        return img


class Brightness(object): #Yes Colorpsace
    def __init__(self, brightness=1):
        self.brightness = brightness

    def __call__(self, img):
        img = img + self.brightness
        return img


class Contrast(object): # Yes Colorpsace
    def __init__(self, contrast=1):
        self.contrast = contrast

    def __call__(self, img):
        img = img * (self.contrast / 127 + 1) - self.contrast
        return img

class GaussianNoise(object): # Both Pixel domain
    def __init__(self,center=0,std=50):
        self.center = center
        self.std = std

    def __call__(self, img):
        noise = np.random.normal(self.center, self.std, img.shape)
        img = img + noise
        return img

class UniformNoise(object): # Both Pixel domain
    def __init__(self, low=-50, high=50):
        self.low = low
        self.high = high

    def __call__(self, img):
        noise = np.random.uniform(self.low, self.high, img.shape)
        img = img + noise
        return img

def applyTransforms(arr, transforms):

    arr = translate(arr,transforms["translateX"],transforms["translateY"])
    arr = rotate(arr,transforms["rotate"])
    arr = flip(arr,transforms["flipH"],transforms["flipV"])
    if 'cropX' in transforms:
        arr = crop(arr,transforms["cropX"],transforms["cropY"],transforms["cropH"],transforms["cropW"])

    if 'shearX' in transforms and 'shearY' in transforms:
        arr = shearImage(arr,transforms["shearX"],transforms["shearY"])

    if 'clip_min' in transforms and 'clip_max' in transforms:
        arr = clip(arr,transforms['clip_max'],transforms['clip_min'])
    
    if 'sharpen' in transforms:
        arr = sharpen(arr,transforms["sharpen"])
    
    if 'brightness' in transforms:
        arr = Brightness(transforms["brightness"])(arr)
    
    if 'contrast' in transforms:
        arr = Contrast(transforms["contrast"])(arr)
    
    if 'blur_g' in transforms:
        arr = BlurGauss(arr,transforms["blur_g"])
    
    if 'blur_m' in transforms:
        arr = BlurMedian(arr,transforms["blur_m"])
    
    if 'blur_2d' in transforms:
        arr = Blur2D(arr,transforms["blur_2d"])
    
    if 'noise_gmean' in transforms and 'noise_gstd' in transforms:
        arr = GaussianNoise(transforms["noise_gmean"],transforms["noise_gstd"])(arr)
    
    if 'noise_ulow' in transforms and 'noise_uhigh' in transforms:
        arr = UniformNoise(transforms["noise_ulow"],transforms["noise_uhigh"])(arr)
    
    return arr