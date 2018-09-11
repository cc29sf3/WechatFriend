# -*- coding: utf-8 -*-
import jieba
import numpy as np
import PIL.Image as Image
from wordcloud import WordCloud, ImageColorGenerator


class WordCloudGet():
    def __init__(self, nickname):
        self.nickname = nickname

    def wordcloud(self, text):
        wordlist = jieba.cut(text, cut_all=True)
        word_space_split = ' '.join(wordlist)
        coloring = np.array(Image.open('bgimage/background.png'))  # 词云的背景和颜色。这张图片在本地。

        my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=coloring, max_font_size=60,
                                 random_state=42, scale=2, font_path="C:\Windows\Fonts\simhei.ttf").generate(
            word_space_split)  # 生成词云。font_path="C:\Windows\Fonts\msyhl.ttc"指定字体，有些字不能解析中文，这种情况下会出现乱码。

        file_name_p = 'wordcloud/' + self.nickname + '.png'

        my_wordcloud.to_file(file_name_p)  # 保存图片
