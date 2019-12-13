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

def boxplotGenrePops(data, filename):
    categories = list(data.keys())

    data_to_plot = []
    for genre in data:
        data_to_plot.append(data[genre])
    
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.boxplot(data_to_plot)

    ax.set_xticklabels(categories)
    ax.autoscale_view()
    ax.set(xlabel = 'Genre', ylabel = 'Popularity', title = 'Boxplot of Popularities for Genre')

    x = [0, 100]
    plt.yticks(np.arange(min(x), max(x)+1, 10))
    plt.xticks(rotation=90)
    plt.tight_layout()

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

def welcomeUser():
    print('Which visualization would you like to see?')
    print('(1) Wordcloud of Spotify genre popularity')
    print('(2) Wordcloud of forecast frequency')
    print('(3) Bar graph of average city temperatures')
    print('(4) Boxplot of genre popularities')
    usr_response = input('Select a number. [1-4]')
    return usr_response

def user_response():
    usr_response = input("Would you like to see another visualization? [y/n]")
    if usr_response.lower() == 'y':
        return main()
    elif usr_response.lower() == "n":
        print("Thanks for your time!")
        return
    else:
        print("Invalid input. Please try again.")
        return user_response()

def main():
    usr_response = welcomeUser()
    if usr_response == '1':
        avg_genre_popularity = readData('genrepopularity.txt')
        generateWordcloud(avg_genre_popularity, 'Wordcloud of genre popularity')
    elif usr_response == '2':
        forecast_frequency = readData('forecastfreq.txt')
        generateWordcloud(forecast_frequency, 'Wordcloud of forecast frequency')
    elif usr_response == '3':
        avg_lows = readData('avglowtemp.txt')
        avg_highs = readData('avghightemp.txt')
        scatterCityTemps(avg_lows, avg_highs, 'Bar plot of Average City Temps')
    elif usr_response == '4':
        genredata = readData('genresummary.txt')
        boxplotGenrePops(genredata, 'Boxplot of Genre popularities')
    else:
        print('Invalid input. Please try again.\n')
        return main()

    user_response()

    return

if __name__ == "__main__":
    main()