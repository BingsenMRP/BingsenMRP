#-*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib
import os
import urllib.request
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
import csv
import ssl

# product = input("Your interested item ASIN number:" )
products = input("Your interested items ASIN number:" )
products = products.split(',')


WebSitesNew = []
for j in products:
    for i in range(1, 51):
        # website = "https://www.amazon.ca/product-reviews/FX38B0117R/ref=cm_cr_getr_d_paging_btm_" + str(i) + "?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent&pageNumber=" + str(i)
        # website = "https://www.amazon.ca/product-reviews/"+ product +"/ref=cm_cr_getr_d_paging_btm_" + str(i) + "?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent&pageNumber=" + str(i)
        website = "https://www.amazon.ca/product-reviews/" + j + "/ref=cm_cr_getr_d_paging_btm_" + str(
            i) + "?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent&pageNumber=" + str(i)

        WebSitesNew.append(website)


# for i in range(1, 51):
#     # website = "https://www.amazon.ca/product-reviews/FX38B0117R/ref=cm_cr_getr_d_paging_btm_" + str(i) + "?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent&pageNumber=" + str(i)
#     # website = "https://www.amazon.ca/product-reviews/"+ product +"/ref=cm_cr_getr_d_paging_btm_" + str(i) + "?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent&pageNumber=" + str(i)
#     website = "https://www.amazon.ca/product-reviews/"+ j +"/ref=cm_cr_getr_d_paging_btm_" + str(i) + "?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=recent&pageNumber=" + str(i)
#
#     WebSitesNew.append(website)
    # WebSitesNew.append("http://www.tripadvisor.ca/Hotel_Review-g155021-d278031-Reviews-Hampton_Inn_Suites_by_Hilton_Windsor-Windsor_Ontario.html#REVIEWS")




def crawlToCSV(theurl):
    from google.cloud import language
    language_client = language.Client()
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    from textblob import TextBlob

    import time
    # time.sleep(1)
    placeHolder = []

    thispage = urllib.request.Request(theurl,data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    thepage = urllib.request.urlopen(thispage)
    time.sleep(0.1)
    soup = BeautifulSoup(thepage, "html.parser")






    if soup.findAll(attrs={"class": "a-row product-title"}):
        title = soup.findAll(attrs={"class": "a-row product-title"})[0].text
    else:
        title = ''

    if soup.findAll(attrs={"class": "a-row product-price-line"}):
        price = soup.findAll(attrs={"class": "a-color-price arp-price"})[0].text.replace('$','')
    else:
        price = ''
    # Loop through each review on the page


    for x in range(0, len(  soup.findAll(attrs={"class": "a-row review-data"}))):




        if soup.findAll(attrs={"class": "a-row review-data"}) and len(soup.findAll(attrs={"class": "a-size-base review-text"})) > x:
            Review = soup.findAll(attrs={"class": "a-size-base review-text"})[x].text.replace('\n', ' ').strip().lower()
            document = language_client.document_from_text(Review)
            try:
                SentimentScoreGoogle = document.analyze_sentiment().sentiment.score
            except:
                continue
            SentimentScoreVader = analyzer.polarity_scores(Review).get('compound')
            SentimentScoreTextBlob = TextBlob(Review).sentiment.polarity

            # print('>>>>>>>>>', Review, '<<<<<<\n')
            # print(SentimentScoreGoogle)
            # print(SentimentScoreVader)
            # print(SentimentScoreTextBlob)
        else:
            Review = ''

        if soup.findAll(attrs={"class": "a-section celwidget"}):
            star_text = soup.findAll(attrs={"class": "a-section celwidget"})[x].find(attrs={"class": "a-icon-alt"}).text
            if star_text:
                stars = star_text.replace(' out of 5 stars','')
        else:
            stars = ''

        Record = []

        Record.append(title)
        Record.append(Review)
        Record.append(price)
        Record.append(stars)
        Record.append(SentimentScoreGoogle)
        Record.append(SentimentScoreVader)
        Record.append(SentimentScoreTextBlob)

        # placeHolder.append(Record)
        placeHolder.append(Record)
    return placeHolder

if __name__=='__main__':

    pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
    results = pool.map(crawlToCSV, WebSitesNew)  # results is a list of all the placeHolder lists returned from each call to crawlToCSV
    # creating CSV file to be used
    pool.close()
    pool.join()


    with open(products + ".csv", "wt", newline='', encoding="utf8") as f:
        writeFile = csv.writer(f)
        writeFile.writerow(
            ["ProductTitle","Review","price","Rating","SentimentScoreGoogle","SentimentScoreVader","SentimentScoreTextBlob"])

        for result in results:
            try:
                writeFile.writerows(result)
            except Exception as e:
                continue


