import datetime
import datetime as dt
import os

import tesserocr
from tesserocr import PyTessBaseAPI
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

print(tesserocr.tesseract_version())  # print tesseract-ocr version
print('language', tesserocr.get_languages())  # prints tessdata path and list of available languages


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = 9999.99
    try:
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
    except Exception as e:
        print('Error = ', e)

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    # 4. Convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    #initial similar value
    s = 0
    try:
        s, a = ssim(np.array(grayA), np.array(grayB), full=True)
        print(s)
        return s
    except Exception as e:
        print('Error = ', e)
        return 0


def prepareimage(file_name):
    im = Image.open("resource/images/uploaded_images/"+file_name)
    im_gray = im.convert("L")  # แปลงให้เป็นภาพขาวดำ
    # im = Image.open('tt.jpg')
    out = 'out.png'
    im_gray.save('resource/images/out.jpg', dpi=(300, 300))
    # image_process()

    return image_process(file_name)


def fine_slip_name(file_name):
    slip_name = ''
    contrast = cv2.imread("resource/images/uploaded_images/"+file_name)
    file_filter = []
    for file in os.listdir('resource/images/master'):
        allowed_extensions = {"png", "jpg", "jpeg"}
        filename = file.lower()
        extension = filename.rsplit(".", 1)[-1]
        if extension in allowed_extensions:
            file_filter.append(file)

    for file_in_filter in file_filter:
        original = cv2.imread("resource/images/master/" + file_in_filter)
        result_compare = compare_images(original, contrast, file_in_filter)
        if result_compare >= 0.9:
            return file_in_filter.rsplit(".", 1)[0]

    return slip_name


def image_process(fileName):
    ipo = PyTessBaseAPI(path='resource/tessdata_best', lang="eng+tha")
    # ลบช่องว่างแต่ละตัวอักษร
    ipo.SetVariable('preserve_interword_spaces', '1')
    # Path ของรูปภาพ
    ipo.SetImageFile("resource/images/uploaded_images/"+fileName)

    print(ipo.GetUTF8Text())
    print("end time", dt.datetime.now())
    return ipo.GetUTF8Text()


# with PyTessBaseAPI(path='resource/tessdata_best' ,lang="eng+tha") as api:
#     # ลบช่องว่างแต่ละตัวอักษร
#     api.SetVariable('preserve_interword_spaces', '1')
#
#     # Path ของรูปภาพ
#     api.SetImageFile("resource/images/F43E458C-AC7B-44ED-98C5-BED3AFF2E119_0.jpg")
#     print(api.GetUTF8Text())
#     print("end time" , dt.datetime.now())


# Defining main function
# def main():
#     print("hey there")
#     print("start time", dt.datetime.now())
#     prepareimage()
#     return  None


# # __name__
# if __name__ == "__main__":
#     main()

# Defining main function
def main():
    print("hey there")
    print("start time", dt.datetime.now())
    prepareimage('')
# return None
