import cv2
import numpy as np

def resize(img, output_size):
    # output_size = (width, height)
    return cv2.resize(img, output_size)

def clip(img, maxI, minI=0):
    img[np.where(img < minI)] = minI
    img[np.where(img > maxI)] = maxI
    return img

def flip(img, horizontal=True, vertical=False):
    # param = (min, max, default, type)
    # horizontal = (TRUE / FALSE), vertical = (TRUE / FALSE)
    if horizontal:
        img = np.flip(img, 1)
    if vertical:
        img = np.flip(img, 0)
    return img

def crop(img, r1, c1, h, w):
    return img[r1:r1 + h, c1:c1 + w]

def sharpen(img, factor=4):
    # param = (min, max, default, type)
    # level = (0, 4, 0, float)
    sharp = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    kernel = sharp * factor / 4
    kernel[1, 1] += 1
    return cv2.filter2D(img, -1, kernel)

def blur(img, level):
    # param = (min, max, default, type)
    # level = (1, 11, 1, odd int)
    level = int(level / 2) * 2 + 1
    img = cv2.GaussianBlur(img, (level, level), 0)
    return img

def translate(img, r1, c1):
    # param = (min, max, default, type)
    # r1 = (-20, 20, 0, int), c1 = (-20, 20, 0, int)
    height, width = img.shape[:2]
    T = np.float32([[1, 0, r1], [0, 1, c1]])
    return cv2.warpAffine(img, T, (width, height))

def padding(img, padX=10, padY=10):
    # param = (min, max, default, type)
    # padX = (0, 20, 0, int), padY = (0, 20, 0, int)
    color = (0, 0, 0)
    height, width, c = img.shape
    heightNew = height + 2 * padX
    widthNew = width + 2 * padY
    result = np.full((heightNew, widthNew, c), color, dtype=np.uint8)
    result[padX:height + padX, padY:width + padY] = img
    return result

def rotate(img, angle=0):
    # param = (min, max, default, type)
    # angle = (-25, 25, 0, int)
    imgCenter = tuple(np.array(img.shape[1::-1]) / 2)
    rotMat = cv2.getRotationMatrix2D(imgCenter, angle, 1.0)
    result = cv2.warpAffine(img, rotMat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def shear(img, shearLevelX, shearLevelY):
    # param = (min, max, default, type)
    # shearLevelX = (0, 1, 0, float), shearLevelY = (0, 1, 0, float)
    height, width = img.shape[:2]
    matrix = np.eye(3)
    if shearLevelX:
        matrix[0, 1] = 0.5 * shearLevelX
    if shearLevelY:
        matrix[1, 0] = 0.5 * shearLevelY
    matrix[0, 2] = -matrix[0, 1] * width / 2
    matrix[1, 2] = -matrix[1, 0] * height / 2
    img2 = cv2.warpPerspective(img, matrix, (int(width), int(height)))
    return resize(img2, (width, height))

def brightness(img, alpha, beta):
    # param = (min, max, default, type)
    # alpha = (0.5, 2, 1, float), beta = (-20, 20, 0, int)
    alpha = np.array([alpha])
    beta = np.array([beta, beta, beta])
    img = np.clip(img * alpha, 0, 255)
    img = np.clip(img + beta, 0, 255)

    return img.astype("uint8")

def gamma(img, gamma):
    # param = (min, max, default, type)
    # gamma = (0.5, 2, 1, float)
    Lab = cv2.split(cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2LAB))
    Lab[0] = (((Lab[0] / 255.0)**gamma) * 255.0).astype('uint8')
    return cv2.cvtColor(cv2.merge(Lab), cv2.COLOR_LAB2BGR)

def noise(img, level):
    # param = (min, max, default, type)
    # level = (0, 50, 0, int)
    noise = np.random.normal(0, level, img.shape)
    return np.clip(img + noise, 0, 255).astype("uint8")

def histEqual(img):
    # param = (True or False)
    Lab = cv2.split(cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2LAB))
    Lab[0] = cv2.equalizeHist(Lab[0])
    return cv2.cvtColor(cv2.merge(Lab), cv2.COLOR_LAB2BGR)

def Clahe(img, size=8):
    # param = (min, max, default, type)
    # size = (1, 11, 1, int)
    clip = 2.0
    Clahe = cv2.createCLAHE(clipLimit=float(clip), tileGridSize=(int(size), int(size)))
    Lab = cv2.split(cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2LAB))
    Lab[0] = Clahe.apply(Lab[0])
    return cv2.cvtColor(cv2.merge(Lab), cv2.COLOR_LAB2BGR)

def LensDistortion(img):
    # param = (True or False)
    d_coef = (0.15, 0.15, 0.1, 0.1, 0.05)
    amount = 1
    h, w = img.shape[:2]
    f = (h ** 2 + w ** 2) ** 0.5
    K = np.array([[f, 0, w / 2],
                  [0, f, h / 2],
                  [0, 0, 1]])
    d_coef = d_coef * amount
    d_coef = d_coef * (2 * (np.random.random(5) < 0.5) - 1)
    M, _ = cv2.getOptimalNewCameraMatrix(K, d_coef, (w, h), 0)
    remap = cv2.initUndistortRectifyMap(K, d_coef, None, M, (w, h), 5)
    img = cv2.remap(img, *remap, cv2.INTER_LINEAR)
    return img


if __name__ == "__main__":
    img = cv2.imread("1.png")
    img2 = LensDistortion(img)
    cv2.imshow("img", img)
    cv2.imshow("img2", img2)
    cv2.waitKey(5000)
    # for i in range(20, 130):
    #     print(i)
    #     img2 = Clahe(img, 2.0, i / 10.0)
    #     cv2.imshow("img", img)
    #     cv2.imshow("img2", img2)
    #     # cv2.imwrite("result/img " + str(i) + ".png", img2)
    #     cv2.waitKey(2000)
