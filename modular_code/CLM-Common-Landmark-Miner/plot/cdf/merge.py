import os
from PIL import Image

COL = 4 #指定拼接图片的列数
ROW = 1 #指定拼接图片的行数
UNIT_HEIGHT_SIZE = 3061 #图片高度
UNIT_WIDTH_SIZE = 4000 #图片宽度
PATH = "D:\\2022Summer\\GeoCam-Reproduction\\pictures\\cdf\\cdf\\" #需要拼接的图片所在的路径
NAME = "result.png" #拼接出的图片保存的名字
SAVE_QUALITY = 100 #保存的图片的质量 可选0-100

#进行图片的复制拼接
def concat_images(image_names, name, path):
    image_files = []
    for index in range(COL * ROW):
        image_files.append(Image.open(path + image_names[index])) #读取所有用于拼接的图片
    target = Image.new('RGB', (UNIT_WIDTH_SIZE * COL, UNIT_HEIGHT_SIZE * ROW), 'white') #创建成品图的画布
    #第一个参数RGB表示创建RGB彩色图，第二个参数传入元组指定图片大小，第三个参数可指定颜色，默认为黑色
    for row in range(ROW):
        for col in range(COL):
            #对图片进行逐行拼接
            #paste方法第一个参数指定需要拼接的图片，第二个参数为二元元组（指定复制位置的左上角坐标）
            #或四元元组（指定复制位置的左上角和右下角坐标）
            target.paste(image_files[COL*row+col], (0 + UNIT_WIDTH_SIZE*col, 0 + UNIT_HEIGHT_SIZE*row))
    target.save(path + name, quality=SAVE_QUALITY) #成品图保存

#获取需要拼接图片的名称
def get_image_names(path):
    image_names = ["result_1.png", "result_2.png", "result_3.png", "result_4.png"] #获取目标文件夹下的所有文件的文件名
    #先用list将iterator转成list，再[0]取出里面的三元元组元素，再[2]取出元组中的由文件夹名组成的列表
    #从所有文件中随机抽取需要数量的文件，可设置是否能重复抽取
    #random库中的choices函数用于可放回抽取，第一个参数指定用于抽取的对象，k参数指定抽取数量
    #sample函数用于不放回抽取，参数同上
    
    return image_names


if __name__ == '__main__':
    concat_images(get_image_names(PATH), NAME, PATH)