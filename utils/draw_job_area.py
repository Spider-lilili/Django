# _*_coding:utf-8 _*_
"""
    @Time　　: 2020/4/4   16:04 
    @Author　 : Guoli
    @ File　　  : draw_job_area.py
    @Software  : PyCharm
    @Description : 
"""
from matplotlib import pyplot as plt
from matplotlib import font_manager
from math import ceil, floor
import os
my_font = font_manager.FontProperties(fname='/System/Library/Fonts/Hiragino Sans GB.ttc')


class JobArea():
    def __init__(self, job_area):
        self.job_area = job_area
        self._id = 459
        self.y_list = []
        self.x_list = []

    def figure(self):
        for job in self.job_area:
            self.y_list.append(float(job.rate))
            self.x_list.append(job.province)
            self._id = job.school_id

    def draw(self):
        plt.figure(figsize=(20, 16), dpi=80)
        plt.title("毕业生签约地区流向", fontproperties=my_font, fontsize=30)
        plt.xlabel("签约地区", fontproperties=my_font, fontsize=20)
        plt.ylabel("占比", fontproperties=my_font, fontsize=20)
        plt.bar(range(len(self.x_list)), self.y_list, width=0.3)
        plt.xticks(range(len(self.x_list)), self.x_list, fontproperties=my_font, rotation=90)
        plt.tick_params(labelsize=15)
        path = os.path.abspath(os.path.join(os.getcwd(), 'media', 'job_area'))
        if not os.path.exists(path):
            os.makedirs(path)
        img_path = os.path.join(path, str(self._id) + '.png')
        plt.savefig(img_path)
        sql_path = '/media/job_area/{}.png'.format(self._id)
        return sql_path


    def main(self):
        self.figure()
        sql_path = self.draw()
        return sql_path


if __name__ == '__main__':
    job_area = JobArea()
    job_area.main()



