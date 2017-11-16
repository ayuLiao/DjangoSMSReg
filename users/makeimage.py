from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random,time,string

from SMSReg.settings import STATICFILES_DIRS,MEDIA_ROOT

class Picture(object):
    '''
    图片类，用于图片验证码
    '''
    def __init__(self, text_str, size, background):
        '''
        text_str: 验证码显示的字符组成的字符串
        size:  图片大小
        background: 背景颜色
        '''
        self.text_list = list(text_str)
        self.size = size
        self.background = background

    def create_pic(self):
        '''
        创建一张图片
        '''
        self.width, self.height = self.size
        self.img = Image.new("RGB", self.size, self.background)
        # 实例化画笔
        self.draw = ImageDraw.Draw(self.img)

    def create_point(self, num, color):
        '''
        num: 画点的数量
        color: 点的颜色
        功能：画点
        '''
        for i in range(num):
            self.draw.point(
                (random.randint(0, self.width), random.randint(0, self.height)),
                fill=color
            )

    def create_line(self, num, color):
        '''
        num: 线条的数量
        color: 线条的颜色
        功能：画线条
        '''
        for i in range(num):
            self.draw.line(
                [
                    (random.randint(0, self.width), random.randint(0, self.height)),
                    (random.randint(0, self.width), random.randint(0, self.height))
                ],
                fill=color
            )

    def create_text(self, font_type, font_size, font_color, font_num, start_xy):
        '''
        font_type: 字体
        font_size: 文字大小
        font_color: 文字颜色
        font_num:  文字数量
        start_xy:  第一个字左上角坐标,元组类型，如 (5,5)
        功能： 画文字
        '''
        font = ImageFont.truetype(font_type, font_size)
        ran_text = " ".join(random.sample(self.text_list, font_num))
        self.draw.text(start_xy, ran_text, font=font, fill=font_color)
        return ran_text

    def opera(self):
        '''
        功能：给画出来的线条，文字，扭曲一下，缩放一下，位移一下，滤镜一下。
        就是让它看起来有点歪，有点扭。
        '''
        params = [
            1 - float(random.randint(1, 2)) / 100,
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500
        ]
        self.img = self.img.transform(self.size, Image.PERSPECTIVE, params)
        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)


def GetImageCode():
    '''
    获得图片验证码
    :return: right_text:正确答案  code_id:验证码唯一ID
    '''
    strings = "abcdefghjkmnpqrstwxyz23456789ABCDEFGHJKLMNPQRSTWXYZ"
    size = (150, 50)
    background = 'white'
    pic = Picture(strings, size, background)
    pic.create_pic()
    pic.create_point(500, (220, 220, 220))
    pic.create_line(30, (220, 220, 220))
    # 加载simsun.ttc字体文件，用于生产图片中的内容
    right_text = pic.create_text(STATICFILES_DIRS[0] + "/simsun.ttc", 24, (0, 0, 205), 4, (7, 7))
    pic.opera()
    # pic.img.show()
    # 随机字符串：随机字符+时间戳
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16)) + str(int(time.time()))
    pic.img.save(MEDIA_ROOT + '/codeimage/' + ran_str + '.png')
    return {'right_text':right_text,'code_id':ran_str}


if __name__ == '__main__':
    GetImageCode()