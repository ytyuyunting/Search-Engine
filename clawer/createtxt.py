import pandas as pd
import numpy as np

# Compile stats: fetch.csv
fetch = pd.read_csv("/Users/like/Desktop/cs572/hw2/createtxt/fetch_wsj.csv", header=None)

attempted = fetch.shape[0]
code_data = fetch.loc[:, [1]]
code = np.array(code_data)
success = 0
failure = 0
for elem in code:
    if elem[0] < 300:
        success += 1
    else:
        failure += 1

dict_of_status = fetch.groupby(fetch.columns[1]).count().to_dict()
dict_of_status = dict_of_status[0]


# Compile stats: visit.csv
visit = pd.read_csv("/Users/like/Desktop/cs572/hw2/createtxt/visit_wsj.csv", header=None)

total_extracted = visit[visit.columns[2]].sum()

# Size is in bytes
dict_of_size = visit.groupby(visit.columns[1]).count().to_dict()
dict_of_size = dict_of_size[0]

size_data = visit.loc[:, [1]]
size = np.array(size_data)
less_1kb = 0
less_10kb = 0
less_100kb = 0
less_1mb = 0
greater_1mb = 0

for elem in size:
    if elem[0] < 1024:
        less_1kb += 1
    elif elem[0] < 10 * 1024:
        less_10kb += 1
    elif elem[0] < 100 * 1024:
        less_100kb += 1
    elif elem[0] < 1024 * 1024:
        less_1mb += 1
    else:
        greater_1mb += 1

dict_of_ct = visit.groupby(visit.columns[3]).count().to_dict()
dict_of_ct = dict_of_ct[0]  # Have to clip top 1/2 when outputting to file

# Compile stats: urls.csv
urls = pd.read_csv("/Users/like/Desktop/cs572/hw2/createtxt/urls_wsj.csv", header=None)

unique_extracted = urls.shape[0]

extracted_data = urls.loc[:, [1]]
extracted = np.array(extracted_data)
unique_within = 0
uinque_outside = 0

for elem in extracted:
    if elem[0] == ' OK':
        unique_within += 1
    else:
        uinque_outside += 1
# Output to file
out = "Name: Ke Li\n"
out += "USC ID: 3444143924\n"
out += "News site crawled: wsj.com\n"
out += "\n"
out += "Fetch Statistics\n"
out += "================\n"
out += "# fetches attempted: " + str(attempted) + "\n"
out += "# fetches succeeded: " + str(success) + " \n"
out += "# fetches failed or aborted: " + str(failure) + "\n"
out += "\n\n\n"
out += "Outgoing URLs:\n"
out += "==============\n"
out += "Total URLs extracted: " + str(total_extracted) + "\n"
out += "# unique URLs extracted: " + str(unique_extracted) + "\n"
out += "# unique URLs within News Site: " + str(unique_within) + "\n"
out += "# unique URLs outside News Site: " + str(uinque_outside) + "\n"
out += "\n"
out += "Status Codes:\n"
out += "=============\n"
for key in dict_of_status:
    out += str(key) + ": " + str(dict_of_status[key]) + "\n"
out += "\n"
out += "File Sizes:\n"
out += "===========\n"
out += "< 1KB: " + str(less_1kb) + "\n"
out += "1KB ~ <10KB: " + str(less_10kb) + "\n"
out += "10KB ~ <100KB: " + str(less_100kb) + "\n"
out += "100KB ~ <1MB: " + str(less_1mb) + "\n"
out += ">= 1MB: " + str(greater_1mb) + "\n"
out += "\n"
out += "Content Types:\n"
out += "==============\n"
for key in dict_of_ct:
    out += key.split(";")[0] + ": " + str(dict_of_ct[key]) + "\n"

out = out[:-1]  # Cut the last new-line

with open('CrawlReport_wsj.txt', 'w') as fp:
    fp.write(out)
