import requests
import concurrent.futures
from bs4 import BeautifulSoup
import json
import re

"""
webmapper program v1.0

Uses multi-threading to recursively create 
a webmap from a base url up to a specified depth 
"""

# Define the number of threads for parallel processing
MAX_THREADS = 50

class mapper:
    
    ###
    # Class Constructor
    ###
    def __init__(self, base_url):
        self.base_url = base_url
        self.output = {}

    ###
    # get_data method that sends a GET request to a URL
    # No redirects, responses time out after 5 seconds
    ###
    @staticmethod
    def get_data(url): 
        try:
            response = requests.get(url, allow_redirects=False, timeout=5)
        except:
            response = []

        return response

    ###
    # downloads function that multithreads the use of get_data
    ###
    def downloads(self, urls):
        responses = []
        threads = min(MAX_THREADS, len(urls))

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            result = executor.map(self.get_data, urls)
            
        for r in result:
            responses.append(r)
        return responses

    ###
    # dict_converter that changes flat dictionary into nested structure
    # {child_url_1:root_url, child_url_2:root_url} becomes {root_url:[child_url_1, child_url_2]} 
    # Example Shown:
    # a
    # ├── b
    # │   ├── d
    # │   ├── e
    # │   │   ├── g
    # │   │   └── h
    # │   └── f
    # └── c
    ###
    @staticmethod
    def dict_converter(final_dict):
        # final_dict of form {'b': 'a', 'c': 'a', 'd': 'b', 'e': 'b', 'f': 'b', 'g': 'e', 'h': 'e'}
        result = {}
        for key in final_dict.values():
            result[key]=[]
        for item in final_dict.items():
            result[item[1]].append(item[0])

        # now condensed to parent/children {'a': ['b', 'c'], 'b': ['d', 'e', 'f'], 'e': ['g', 'h']}

        # find locations for substitution
        keys = []
        loc = []
        tags = []
        for key in result.keys():
            for item in result.items():
                if key in item[1]:
                    keys.append(item[0])
                    loc.append(item[1].index(key))
                    tags.append(key)

        keys.reverse()
        loc.reverse()
        tags.reverse()

        for i in range(len(keys)):
            result[keys[i]][loc[i]] = {tags[i]:result[tags[i]]}

        # children substituted {'a': [{'b': ['d', {'e': ['g', 'h']}, 'f']}, 'c'], 'b': ['d', {'e': ['g', 'h']}, 'f'], 'e': ['g', 'h']}

        keys = list(result.keys())
        for i in range(len(keys)):
            if i > 0:
                result.pop(keys[i]) 

        # final result condensed to {'a': [{'b': ['d', {'e': ['g', 'h']}, 'f']}, 'c']}

        return(result)

    ###
    # get_urls_from_response method to extract/validate responses from urls
    ###
    @staticmethod
    def get_urls_from_response(base_url, response):
    
        if response is None:
            return []

        if type(response) is list:
            return []
            
        if 'content-type' not in response.headers.keys():
            return []

        content_type = response.headers['content-type']

        if "text/html" not in content_type:
            return []

        urls = []
        soup = BeautifulSoup(response.text, 'html.parser')
        for url in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            urls.append(url.get('href'))

        return urls

    ###
    # map function that recursively crawls links for other links and so on up to a specified depth
    ###
    def map(self, max_depth: int):

        final_dict = {}

        url_pool = [[] for _ in range(0, max_depth + 1)]
        url_pool[0].append(self.base_url)

        for depth_index in range(0, max_depth):
            urls = url_pool[depth_index]
            if len(urls) == 0:
                break
            
            responses = self.downloads(urls)

            for i in range(len(urls)):
                parsed = self.get_urls_from_response(urls[i], responses[i])
                
                for link in parsed:

                    if link not in final_dict.values():
                        if link.startswith('https'):
                            url_pool[depth_index + 1].append(link)
                            final_dict[link] = urls[i]

        self.output = self.dict_converter(final_dict)
        return 

    ###
    # printJSON function to print the outputted dictionary to a JSON format
    ###
    def printJSON(self, indentJSON = 3):
        print(json.dumps(self.output, indent = indentJSON))
        return

    ###
    # saveJSON function to save the outputted dictionary to a JSON format
    ###
    def saveJSON(self, filename = 'map.json', indentJSON = 3):
        with open(filename, 'w') as f:
            json.dump(self.output, f, indent = indentJSON)
        return
        