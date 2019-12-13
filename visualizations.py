import matplotlib.pyplot as plt
import os
import numpy as np 
import json
import ast
from wordcloud import WordCloud 

def readData(filename):
    f = open(filename, 'r')
    data = f.read()
    data = ast.literal_eval(data)
    f.close()
    return data

def generateWordcloud(data, filename):
    wordcloud = WordCloud(background_color='white',width=1400,height=1000).generate_from_frequencies(data)
    
    fig = plt.figure()

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    fig.savefig(filename)

def scatterCityTemps(data1, data2, filename):
    categories = list(data1.keys())
    lows = list(data1.values())
    highs = list(data2.values())

    fig = plt.figure()
    ax = fig.add_subplot(111)

    N = len(categories)
    width = 0.2
    ind = np.arange(N)

    p1 = ax.bar(ind, lows, width)
    p2 = ax.bar(ind + width, highs, width)

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(categories)
    ax.legend((p1, p2), ('Lows', 'Highs'), loc='upper left', prop= {'size': 10})
    ax.autoscale_view()

    ax.set(xlabel = 'City', ylabel = 'Temperature (F)', title = 'Average Temperatures for U.S. Cities')

    ax.grid()

    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.show()

    fig.savefig(filename)

def main():
    #avg_genre_popularity = readData('genrepopularity.txt')
    #generateWordcloud(avg_genre_popularity, 'Wordcloud of genre popularity')

    #forecast_frequency = readData('forecastfreq.txt')
    #generateWordcloud(forecast_frequency, 'Wordcloud of forecast frequency')

    avg_lows = readData('avglowtemp.txt')
    avg_highs = readData('avghightemp.txt')
    scatterCityTemps(avg_lows, avg_highs, 'Scatterplot of Average City Temps')



if __name__ == "__main__":
    main()