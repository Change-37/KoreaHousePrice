import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def makeGraph(df, x, y):
    dataX = df[x]
    dataY = df[y]
    plt.plot(dataX,dataY,'o-')
    notokr = fm.FontProperties(fname=getFont())
    plt.rcParams['font.family'] = notokr.get_name()
    plt.rcParams['font.size'] = 20
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title('월별 평균 거래가격 변화')
    plt.show()


def getFont():
    font_file_path_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    print(len(font_file_path_list))

    fav_font_file_path_lst = filter(lambda x: True if "NotoSansKR" in x else False, font_file_path_list)

    print()
    for font_file_path in fav_font_file_path_lst:
        if 'Regular' in font_file_path:
            return font_file_path