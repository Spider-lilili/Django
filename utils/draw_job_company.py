# _*_coding:utf-8 _*_
"""
    @Time　　: 2020/4/4   16:05 
    @Author　 : Guoli
    @ File　　  : draw_job_company.py
    @Software  : PyCharm
    @Description : 
"""

from matplotlib import pyplot as plt
from matplotlib import font_manager
import os
my_font = font_manager.FontProperties(fname='/System/Library/Fonts/Hiragino Sans GB.ttc')


class JobCompany():
    def __init__(self, _id, x_y):
        # self.x_y = '国有企业,35.21; 金融,14.00; 三资企业,4.73; 科研设计单位,2.47; 机关,1.97; 中初教育单位,1.28; 医疗卫生单位,0.89; 部队,0.10; 高等教育单位,0.10; 其他事业单位,6.51; 其他企业,32.74'
        # self._id = 459
        self._id = _id
        self.x_y = x_y
        self.x_list = []
        self.y_list = []

    def figure(self):
        for i in self.x_y.split(";"):
            x, y = i.split(",")
            self.x_list.append(x.replace(" ", ""))
            self.y_list.append(float(y.replace(" ", "")))

    def draw(self):
        # print(self.x_list)
        # print(self.y_list)
        plt.figure(figsize=(20, 16),dpi=80)

        plt.title("毕业生签约单位性质",fontproperties=my_font,fontsize=30)
        plt.xlabel("签约单位类型",fontproperties=my_font,fontsize=20)
        plt.ylabel("占比",fontproperties=my_font,fontsize=20)

        plt.bar(range(len(self.x_list)),self.y_list,width=0.3)
        plt.xticks(range(len(self.x_list)),self.x_list,fontproperties=my_font)
        plt.tick_params(labelsize=15)
        path = os.path.abspath(os.path.join(os.getcwd(), 'media', 'job_company'))
        if not os.path.exists(path):
            os.makedirs(path)
        img_path = os.path.join(path, str(self._id)+'.png')
        plt.savefig(img_path)
        sql_path = '/media/job_company/{}.png'.format(self._id)
        return sql_path


    def main(self):
        self.figure()
        sql_path = self.draw()
        return sql_path

if __name__ == '__main__':
    job = JobCompany()
    job.main()

