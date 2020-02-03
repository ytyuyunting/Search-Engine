import csv

from bs4 import BeautifulSoup
import time
from time import sleep
import requests
from random import randint
from html.parser import HTMLParser
import json
import random
from collections import OrderedDict
import math
import pandas as pd

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome '
                            '/ 61.0.3163.100 Safari / 537.36'}
SEARCH_URL = "http://www.bing.com/search?q="
SEARCH_SELECTOR = ("li", {"class": "b_algo"})
# SEARCH_URL = "http://www.search.yahoo.com/search?p="
# SEARCH_SELECTOR = ("li", {"class": "ac-algo fz-l ac-21th lh-24"})

class SearchEngine:
    @staticmethod
    def de_duplicate(val):
        length = len(val)
        if length > 1:
            for k in range(length - 1):
                if val[k] is None:
                    continue
                else:
                    for j in range(k + 1, length):
                        if val[j] is None:
                            continue
                        else:
                            url_1 = val[k].replace("https://", "").replace("http://", "")
                            url_2 = val[j].replace("https://", "").replace("http://", "")
                            if url_1.endswith("/"):
                                url_1 = url_1[:-1]
                            if url_2.endswith("/"):
                                url_2 = url_2[:-1]
                            if url_1.lower() == url_2.lower():
                                val[j] = None
        val = list(filter(None, val))
        return val


    @staticmethod
    def search(query, sleep=True):
        print()
        print("start")
        if sleep:  # Prevents loading too many pages too soon
            time.sleep(randint(10, 29))
            temp_url = '+'.join(query.split())  # for adding + between words for the query
            url = SEARCH_URL + temp_url
            print(url)
            soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
            new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        # raw_results = soup.find_all("li", attrs = {"class" : "b_algo"})
        raw_results = soup.find_all(*SEARCH_SELECTOR)
        results = []
        # implement a check to get only 10 results and also check that URLs must not be duplicated
        for result in raw_results:
            link = result.find('a').get('href')
            if len(results) >= 10:
                break
            print(link)
            results.append(link)
        results = SearchEngine.de_duplicate(results)
        return results


class create_dictionary(dict):

    # __init__ function
    def __init__(self):
        self = OrderedDict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value


def readtxtfile():
    with open('100QueriesSet1.txt') as input_file:
        lines = []
        i = 0
        for line in input_file:
            line = line[:-3]
            lines.append(line)
            i = i + 1
            if i == 2:
                break
    return lines


def readjsonfile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def spearman(array):
    sums = 0
    for overlap in array:
        d = overlap[1] - overlap[0]
        sums = sums + math.pow(d, 2)
    n = len(array)
    try:
        p = 1 - (6 * sums) / (n * (n * n - 1))
        p = round(p, 2)
    except ZeroDivisionError as ze:
        # see piazza @10 for explanation.
        if n == 1 and array[0][0] == array[0][1]:
            # case where n=1 (exactly one overlap) and google_rank == ask_rank
            p = 1
        else:
            # case when n=0 (zero overlaps) OR ( n=1 (exactly 1 overlap) and google_rank != ask_rank )
            p = 0
    return p


def check_overlap(link1, link2):
    link1 = link1.replace("https://", "").replace("http://", "")
    link2 = link2.replace("https://", "").replace("http://", "")
    if link1.endswith("/"):
        link1 = link1[:-1]
    if link2.endswith("/"):
        link2 = link2[:-1]
    if link1.lower() == link2.lower():
        return True
    return False


def compare_overlap():
    res_com = []
    data_google = readjsonfile('Google_Result1.json')
    data_bing = readjsonfile('hw1.json')
    k = 0
    num_ave = 0
    percent_ave = 0.0
    coe_ave = 0.00
    for g in data_bing:
        k += 1
        bing_arr = data_bing[g]
        google_arr = data_google[g]
        overlap_num = 0
        overlap = []
        single_com = []
        for i in range(len(bing_arr)):
            for j in range(len(google_arr)):
                if check_overlap(bing_arr[i], google_arr[j]):
                    overlap_num += 1
                    overlap.append([i, j])
                    break
        string = 'Query ' + str(k)

        single_com.append(string)
        single_com.append(overlap_num)
        overlap_precent = float(overlap_num * 100 / 10)
        overlap_precent = round(overlap_precent, 1)
        single_com.append(overlap_precent)
        spearman_coe = spearman(overlap)
        single_com.append(spearman_coe)

        # calculate average
        num_ave += overlap_num
        percent_ave += overlap_precent
        coe_ave += spearman_coe
        res_com.append(single_com)
    num_ave = num_ave / k
    num_ave = round(num_ave, 0)
    percent_ave = num_ave*100/ 10
    percent_ave = round(percent_ave, 1)
    coe_ave = coe_ave / k
    coe_ave = round(coe_ave, 2)
    row_ave = ['Averages', num_ave, percent_ave, coe_ave]
    res_com.append(row_ave)
    return res_com


#############Driver code############
queries = readtxtfile()
dict_obj = create_dictionary()
for query in queries:
    res_link = SearchEngine.search(query)
    dict_obj.add(query, res_link)

with open('hw1.json', 'w') as outfile:
    json.dump(dict_obj, outfile)
print("start2:")
# readjsonfile and compare

compare_result = compare_overlap()

with open('hw1.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    header = ["Queries", " Number of Overlapping Results", " Percent Overlap", " Spearman Coefficient"]
    writer.writerow(header)
    for row in compare_result:
        for i in range(1, 4):
            temp = str(row[i])
            row[i] = ' ' + temp
        writer.writerow(row)
print("Finished generating CSV file.")
####################################
