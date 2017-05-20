#-*- coding: UTF-8 -*-

# tripadvisor Scrapper - use this one to scrape hotels

# importing libraries
from bs4 import BeautifulSoup
import urllib
import os
import urllib.request
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
import csv
import ssl

WebSitesNew = []
for i in range(1, 60):
    website = "http://www.tripadvisor.ca/Hotel_Review-g155021-d278031-Reviews-or" + str(i*10) + \
              "-Hampton_Inn_Suites_by_Hilton_Windsor-Windsor_Ontario.html#REVIEWS"
    WebSitesNew.append(website)
    WebSitesNew.append("http://www.tripadvisor.ca/Hotel_Review-g155021-d278031-Reviews-Hampton_Inn_Suites_by_Hilton_Windsor-Windsor_Ontario.html#REVIEWS")

# List the first page of the reviews (ends with "#REVIEWS") - separate the websites with ,
WebSites = [
    "http://www.tripadvisor.ca/Hotel_Review-g155021-d278031-Reviews-or10-Hampton_Inn_Suites_by_Hilton_Windsor-Windsor_Ontario.html#REVIEWS",
    # "http://www.tripadvisor.ca/Hotel_Review-g155021-d278031-Reviews-or50-Hampton_Inn_Suites_by_Hilton_Windsor-Windsor_Ontario.html#REVIEWS",
    "http://www.tripadvisor.ca/Hotel_Review-g155021-d278031-Reviews-or610-Hampton_Inn_Suites_by_Hilton_Windsor-Windsor_Ontario.html#REVIEWS",
    # "https://www.tripadvisor.ca/Hotel_Review-g190479-d3587956-Reviews-or960-The_Thief-Oslo_Eastern_Norway.html#REVIEWS",
    # "https://www.tripadvisor.ca/Hotel_Review-g190479-d3587956-Reviews-or20-The_Thief-Oslo_Eastern_Norway.html#REVIEWS",
    # "https://www.tripadvisor.ca/Hotel_Review-g190479-d3587956-Reviews-or10-The_Thief-Oslo_Eastern_Norway.html#REVIEWS",
]


def crawlToCSV(theurl):

    placeHolder = []

    thepage = urllib.request.urlopen(theurl)
    soup = BeautifulSoup(thepage, "html.parser")
    # extract the help count, restaurant review count, attraction review count and hotel review count
    a = b = 0
    helpcountarray = restaurantarray = attractionarray = hotelarray = ""

    for profile in soup.findAll(attrs={"class": "memberBadging g10n"}):
        image = profile.text.replace("\n", "|||||").strip()
        if image.find("helpful vote") > 0:
            # counter = image.split("helpful vote", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
            counter = image.split("helpful vote", 1)[0].split()[-1].replace('reviews','')
            if len(helpcountarray) == 0:
                helpcountarray = [counter]
            else:
                helpcountarray.append(counter)
        elif image.find("helpful vote") < 0:
            if len(helpcountarray) == 0:
                helpcountarray = ["0"]
            else:
                helpcountarray.append("0")

        if image.find("attraction") > 0:
            counter = image.split("attraction", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
            if len(attractionarray) == 0:
                attractionarray = [counter]
            else:
                attractionarray.append(counter)
        elif image.find("attraction") < 0:
            if len(attractionarray) == 0:
                attractionarray = ["0"]
            else:
                attractionarray.append("0")

        if image.find("restaurant") > 0:
            counter = image.split("restaurant", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
            if len(restaurantarray) == 0:
                restaurantarray = [counter]
            else:
                restaurantarray.append(counter)
        elif image.find("restaurant") < 0:
            if len(restaurantarray) == 0:
                restaurantarray = ["0"]
            else:
                restaurantarray.append("0")

        if image.find("hotel") > 0:
            counter = image.split("helpful vote", 1)[0].split()[-3].replace('reviews','')
            if len(hotelarray) == 0:
                hotelarray = [counter]
            else:
                hotelarray.append(counter)
        elif image.find("hotel") < 0:
            if len(hotelarray) == 0:
                hotelarray = ["0"]
            else:
                hotelarray.append("0")

# extract the rating count for each user review
    altarray = ""
    # for rating in soup.findAll(attrs={"class": "rating reviewItemInline"}):
    #     alt = rating.find('img', alt=True)['alt']
    #     if alt[-5:] == 'stars':
    #         if len(altarray) == 0:
    #             altarray = [alt]
    #         else:
    #             altarray.append(alt)
    for rating in soup.findAll(attrs={"class": "rating reviewItemInline"}):
        if rating.contents:
            for ele in rating.contents:
                bubble_style = {'bubble_50':"5", 'bubble_40':"4", 'bubble_30':"3", 'bubble_20':"2", 'bubble_10':"1", 'bubble_0':"0"}
                if rating.contents[0].attrs['class']:
                    if rating.contents[0].attrs['class'][1] in bubble_style:
                        alt = bubble_style[rating.contents[0].attrs['class'][1]]
                        if len(altarray) == 0:
                            altarray = [alt]
                        else:
                            altarray.append(alt)
        else:
            altarray.append("")
    if soup.find(attrs={"class": "heading_name"}) and soup.find(attrs={"class": "heading_name"}).text:
        Organization = soup.find(attrs={"class": "heading_name"}).text.replace('"', ' ').replace('Review of',' ').strip()
    else:
        Organization = "Unknown Organization"

    if soup.findAll(attrs={"class": "format_address"}) and len(soup.findAll(attrs={"class": "format_address"})) > 0:
        Address = soup.findAll(attrs={"class": "format_address"})[0].text.replace(',', '').replace('\n', '').strip()
    else:
        Address = "Unknown Address"







    # Loop through each review on the page
    for x in range(0, len(hotelarray)):
        try:
            Reviewer = soup.findAll(attrs={"class": "username mo"})[x].text
        except:
            Reviewer = "N/A"
            continue

        Reviewer = Reviewer.replace(',', ' ').replace('”', '').replace('“', '').replace('"', '').strip()
        if soup.findAll(attrs={"class": "reviewerBadge badge"}) and len(soup.findAll(attrs={"class": "reviewerBadge badge"})) > x:
            ReviewCount = soup.findAll(attrs={"class": "reviewerBadge badge"})[x].text.split(' ', 1)[0].strip()
        else:
            ReviewCount = '0'
        if soup.findAll(attrs={"class": "location"}) and len(soup.findAll(attrs={"class": "location"})) > x:
            Location = soup.findAll(attrs={"class": "location"})[x].text.replace(',', ' ').strip()
        else:
            Location = ''
        if soup.findAll(attrs={"class": "quote"}) and len(soup.findAll(attrs={"class": "quote"})) > x:
            ReviewTitle = soup.findAll(attrs={"class": "quote"})[x].text.replace(',', ' ').replace('”', '').replace('“','').replace('"', '').replace('é', 'e').strip()
        else:
            ReviewTitle = ''
        if soup.findAll(attrs={"class": "entry"}) and len(soup.findAll(attrs={"class": "entry"})) > x:
            Review = soup.findAll(attrs={"class": "entry"})[x].text.replace(',', ' ').replace('\n', ' ').strip()
        else:
            Review = ''
        if soup.findAll(attrs={"class": "ratingDate"}) and len(soup.findAll(attrs={"class": "ratingDate"})) > x:
            RatingDate = soup.findAll(attrs={"class": "ratingDate"})[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip()
        else:
            RatingDate = ''

        Rating = altarray[x][:1]
        HelpCount = helpcountarray[x]
        AttractionCount = attractionarray[x]
        Restaurant = restaurantarray[x]
        Hotel = hotelarray[x]

        Record = []
        # Record = Organization + "," + Address + "," + Reviewer + "," + ReviewTitle + "," + Review + "," + ReviewCount + "," + HelpCount + "," + AttractionCount + "," + Restaurant + "," + Hotel + "," + Location + "," + RatingDate + "," + Rating
        # Record = Organization + "," + Address + "," + Reviewer + "," + ReviewTitle + "," + Review + "," + str(ReviewCount) + "," + str(HelpCount) + "," + str(AttractionCount) + "," + Restaurant + "," + Hotel + "," + Location + "," + RatingDate + "," + str(Rating)
        Record.append(Organization)
        Record.append(Address)
        Record.append(Reviewer)
        Record.append(ReviewTitle)
        Record.append(Review)
        Record.append(str(ReviewCount))
        Record.append(str(HelpCount))
        Record.append(str(AttractionCount))
        Record.append(Restaurant)
        Record.append(Hotel)
        Record.append(Location)
        Record.append(RatingDate)
        Record.append(str(Rating))

        # placeHolder.append(Record)
        placeHolder.append(Record)
    return placeHolder



if __name__=='__main__':

    pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
    results = pool.map(crawlToCSV, WebSitesNew)  # results is a list of all the placeHolder lists returned from each call to crawlToCSV
    # creating CSV file to be used
    pool.close()
    pool.join()

    # Single process
    # results = []
    # for url in WebSites:
    #     results.append(crawlToCSV(url))

    # file = open("Output.csv", "wb")
    # file.write(
    #     b"Organization,Address,Reviewer,Review Title,Review,Review Count,Help Count,Attraction Count,Restaurant Count,Hotel Count,Location,Rating Date,Rating" + b"\n")
    # file.close()

    # with open(r"~/Desktop/TripAdviser Reviews.csv", "ab") as f:
    with open("Windsor.csv", "wt", newline='') as f:
        writeFile = csv.writer(f)
        writeFile.writerow(
            ["Organization", "Address", "Reviewer", "Review Title", "Review", "Review Count", "Help Count",
             "Attraction Count", "Restaurant Count", "Hotel Count", "Location", "Rating Date", "Rating"])

        for result in results:
            try:
                writeFile.writerows(result)
            except Exception as e:
                continue

# looping through each site until it hits a break
# for theurl in WebSites:
#
#         file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")

    # link = soup.find_all(attrs={"class": "nav next rndBtn ui_button primary taLnk"})
    # print(Organization)
    # if len(link) == 0:
    #     break
    # else:
    #     WebSites.append("http://www.tripadvisor.com" + link[0].get('href'))
    #     soup = BeautifulSoup(urllib.request.urlopen("http://www.tripadvisor.com" + link[0].get('href')),"html.parser")
    #     print(link[0].get('href'))
    #     Checker = link[0].get('href')[-7:]

# file.close()
