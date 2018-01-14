# -*- coding: utf-8 -*-
from aip import AipOcr
from PIL import Image


class PythonOcr(object):
    AppID = "10689156"
    APIKey = "2Vj4t2VfgVGRnnHCTWvRhprR"
    SecretKey = "PoVonzeGr7O1rD4fOAA7nx0gF1pF1EzA"
    AppName = "pythonOcr"
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def readImgFile(self, imgPath):
        with open(imgPath, 'rb') as fp:
            return fp.read()

    def ocrChar(self, imgPath):
        # 图片数据
        image = self.readImgFile(imgPath)
        client = AipOcr(self.AppID, self.APIKey, self.SecretKey)
        return client.basicAccurate(image)

    def preConcert(self, img):  # 对图片做预处理
        width, height = img.size
        threshold = 30
        for i in range(0, width):
            for j in range(0, height):
                p = img.getpixel((i, j))  # 抽取每个像素点的像素
                r, g, b = p
                if r > threshold or g > threshold or b > threshold:
                    img.putpixel((i, j), self.WHITE)
                else:
                    img.putpixel((i, j), self.BLACK)
        # img.show()
        # img.save("preFig.jpg")
        return img

    def remove_noise(self, img, window=1):  # 对去除背景的图片做噪点处理
        if window == 1:
            window_x = [1, 0, 0, -1, 0]
            window_y = [0, 1, 0, 0, -1]
        elif window == 2:
            window_x = [-1, 0, 1, -1, 0, 1, 1, -1, 0]
            window_y = [-1, -1, -1, 1, 1, 1, 0, 0, 0]

        width, height = img.size
        for i in range(width):
            for j in range(height):
                box = []

                for k in range(len(window_x)):
                    d_x = i + window_x[k]
                    d_y = j + window_y[k]
                    try:
                        d_point = img.getpixel((d_x, d_y))
                        if d_point == self.BLACK:
                            box.append(1)
                        else:
                            box.append(0)
                    except IndexError:
                        img.putpixel((i, j), self.WHITE)
                        continue

                box.sort()
                if len(box) == len(window_x):
                    mid = box[int(len(box) / 2)]
                    if mid == 1:
                        img.putpixel((i, j), self.BLACK)
                    else:
                        img.putpixel((i, j), self.WHITE)
        img.save("mov_noise_fig.jpg")
        return img

    def ocrImg(self, orignalImg, tmpImg):
        img = Image.open(orignalImg)
        img = self.preConcert(img)
        img.save(tmpImg)
        result = self.ocrChar(tmpImg)
        words = result['words_result']
        return words[0]['words'], img


if __name__ == '__main__':
    ocr = PythonOcr()
    originalPtah = 'captcha.jpeg'
    tmpPath = 'preFile.jpg'
    print ocr.ocrImg(originalPtah, tmpPath)
