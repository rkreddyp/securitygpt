

from securitygpt.schema.schema_resource import URLResource
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from typing import List, Optional
import requests,time
from url_normalize import url_normalize
from bs4 import BeautifulSoup   # For HTML parsing
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from bs4.element import Comment
import urllib.request
import functools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


class headless_browser_utils:

    def initiate_driver_return_browser(url):
        print ( "initiate_driver_return_browser")
        opts = FirefoxOptions()

        fp = webdriver.FirefoxProfile()
        fp.set_preference("security.fileuri.strict_origin_policy", False);
        fp.set_preference("javascript.enabled", False);
        fp.update_preferences()
        opts.add_argument("--headless")
        opts.set_preference("browser.download.folderList", 2)
        opts.set_preference("browser.download.dir", "/tmp/") 
        opts.set_preference("browser.helperApps.neverAsk.saveToDisk","application/text/csv")
        #browser = webdriver.Firefox(firefox_options=opts , log_path='/tmp/geckodriver.log', executable_path = '/tmp/geckodriver', firefox_profile=fp)
        try :
            #browser = webdriver.Firefox(options=opts , log_path='/tmp/geckodriver.log', executable_path = '/tmp/geckodriver')
            browser = webdriver.Firefox(options=opts)
        except :
            time.sleep(5)
            try :
                #browser = webdriver.Firefox(options=opts , log_path='/tmp/geckodriver.log', executable_path = '/tmp/geckodriver')
                browser = webdriver.Firefox(options=opts )
            except Exception as e: print(e)

        delay = 4
        browser.set_window_size(1920,1920)
        try :
            browser.get(url)
        except Exception as e:
            print(e) 
        
        time.sleep(2)
        return browser 



class url_parse_utils:
    

    def initiate_driver_return_browser(url):
        print ( "initiate_driver_return_browser")
        opts = FirefoxOptions()

        fp = webdriver.FirefoxProfile()
        fp.set_preference("security.fileuri.strict_origin_policy", False);
        fp.set_preference("javascript.enabled", False);
        fp.update_preferences()
        opts.add_argument("--headless")
        opts.set_preference("browser.download.folderList", 2)
        opts.set_preference("browser.download.dir", "/tmp/") 
        opts.set_preference("browser.helperApps.neverAsk.saveToDisk","application/text/csv")
        #browser = webdriver.Firefox(firefox_options=opts , log_path='/tmp/geckodriver.log', executable_path = '/tmp/geckodriver', firefox_profile=fp)
        try :
            #browser = webdriver.Firefox(options=opts , log_path='/tmp/geckodriver.log', executable_path = '/tmp/geckodriver')
            browser = webdriver.Firefox(options=opts)
        except :
            time.sleep(5)
            try :
                #browser = webdriver.Firefox(options=opts , log_path='/tmp/geckodriver.log', executable_path = '/tmp/geckodriver')
                browser = webdriver.Firefox(options=opts )
            except Exception as e: print(e)

        delay = 4
        browser.set_window_size(1920,1920)
        try :
            browser.get(url)
        except Exception as e:
            print(e) 
        
        time.sleep(2)
        return browser 


    @staticmethod
    def fetch_soup(url: str) -> BeautifulSoup:
        timeout_seconds = 5
        response = requests.get(url,verify=False,timeout=timeout_seconds)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
    @staticmethod
    def fetch_title(soup: BeautifulSoup) -> str:
        title = soup.title.string
        return title
    

    @staticmethod    
    def fetch_content(soup: BeautifulSoup) -> str:
        text = soup.get_text()
        return text
    
    @staticmethod    
    def fetch_paragraphs(soup:BeautifulSoup) -> List[str]:
        paragraphs = [p.text for p in soup.find_all("p") if len(p.text) > 50]
        return paragraphs

    @staticmethod   
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    @staticmethod    
    def fetch_text(url) -> List[str]:
        text_arr = []
        try :

            browser = url_parse_utils.initiate_driver_return_browser(url)
            el = browser.find_element(By.TAG_NAME,'body')
            for text in (el.text).split('\n'):
                if len (text) > 200:
                    #print (url)
                    #print ("fetchtext --", text)
                    text_arr.append(text)
            return ".".join (text_arr)
        except Exception as e:
            print ("exceptin in fetch_text")
            return "NA"

    @staticmethod    
    def fetch_tables(soup: BeautifulSoup) -> str:
        tables = soup.find_all('table')
        return tables

    
    @staticmethod    
    def fetch_inline_images(soup: BeautifulSoup) -> str:
            
            # Find inline images and their descriptions
        image_elements = soup.find_all('img')  # Adjust the tag name as needed

        for img in image_elements:
            # Extract image source URL
            img_src = img.get('src')

            # Extract image description (if available)
            img_description = img.get('alt', '')

            # Print image source and description
            print("Image Source:", img_src)
            print("Image Description:", img_description)
            print("-" * 40)  # Separator between images

    @staticmethod    
    def fetch_tables_markdown(soup: BeautifulSoup) -> str:
        tables = soup.find_all('table')
        markdown_tables = []
    
        for table in tables:
            rows = table.find_all('tr')
            markdown_table = []
            
            for row in rows:
                cols = row.find_all(['td', 'th'])
                markdown_row = '| ' + ' | '.join([col.get_text().strip() for col in cols]) + ' |'
                markdown_table.append(markdown_row)
                
                # If this is a header row, add a line to separate headers from data
                if cols and row.find('th'):
                    markdown_table.append('| ' + ' | '.join(['---' for _ in cols]) + ' |')
                    
            markdown_tables.append('\n'.join(markdown_table))
            
        return '\n\n'.join(markdown_tables)


class BaseURL:
    def __init__(self, url: str, description: str = "NA"):
        self.url = url
        self.soup = "NA"
        self.description = description
        self.visited = False
        self.content = "NA"
        self.title = "NA"
        self.paragraphs = "NA"

class URL(BaseURL):
    def __init__(self, url: str, description: str = "NA"):
        super().__init__(url, description)
        self.soup = url_parse_utils.fetch_soup(url)
        #self.title = url_parse_utils.fetch_title(self.soup)
        self.content = url_parse_utils.fetch_content(self.soup)
        #self.paragraphs = url_parse_utils.fetch_paragraphs(self.soup)
        self.urltext = " ".join ( self.paragraphs ).replace('\n', ' ').replace('\r', '')
        self.tables = url_parse_utils.fetch_tables_markdown(self.soup)
        self.paragraphs = url_parse_utils.fetch_text(url)

class URLManager:

    def __init__(self, urls):
        if isinstance(urls, str):
            urls = [urls]  # Convert a single URL to a list with one element
        self.urls = []
        for url in urls:
            self.add_url(url) # calls URL(url, description)

    def __call__(self, url: str, description: str = "NA"):
        self.add_url(url, description)

    def add_url(self, url: str, description: str = "NA"):
        # Check if the URL already exists in the list
        existing_url = next((u for u in self.urls if u.url == url), None)
        if existing_url:
            print(f"URL '{url}' already exists. Skipping.")
        else:
            try :
                url_obj = URL(url, description)
                self.urls.append(url_obj)
            except Exception as e:
                print (e)
                pass
    def get_all_urls(self):
        return self.urls
    
    

@dataclass
class URLResourcePool():
    resources: List[URLResource] = field(default_factory=list)

    def add_url_resource(self,resource: URLResource):
        self.resources.append(resource)
        return self.resources
    
    def add_url_resource_old(self, url: str, description: str, visited: bool, content: str, title: str):
            
        self.resources.append(
                    URLResource(
                        url=url_normalize(url),
                        description=description,
                        visited=visited,
                        content=content,
                        title=title,
                    )
        )
        return self.resources

    def find(self, url: str) -> Optional[URLResource]:
        url = url_normalize(url)
        resources = [r for r in self.resources if r.url == url]
        if len(resources) == 0:
            return None
        else:
            return resources[0]


    def visit(self, url: str, content: str = "") -> None:
        resource = self.find(url)
        if resource is not None:
            resource.visited = True
            resource.content = content

    def get_all(self) -> List[URLResource]:
        return self.resources

    def get_unvisited(self) -> List[URLResource]:
        return [r for r in self.resources if not r.visited]

class URLParsers(ABC):
    @abstractmethod
    def parse(self, url: str, content: str) -> List[str]:
        pass


def fetch_content(func):
    #@functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print ('in fetch content ..., args')
        print (args, kwargs)
    return wrapper
 
def massage_content(func):
    #@functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print ('in massage content ..., args')
        print (args, kwargs)
    return wrapper

@fetch_content
#@massage_content
def parse_url2():
    print ('in parse url !!!!!!!')
    #self.content = text
    #print ( len (text) )