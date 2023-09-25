

from schema.schema_resource import URLResource
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from typing import List, Optional
import requests
from url_normalize import url_normalize
from bs4 import BeautifulSoup   # For HTML parsing
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation

import requests
from bs4 import BeautifulSoup

import functools

class url_parse_utils:
    
    @staticmethod
    def fetch_soup(url: str) -> BeautifulSoup:
        response = requests.get(url)
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
    def fetch_tables(soup: BeautifulSoup) -> str:
        tables = soup.find_all('table')
        return tables
    
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

class URL(BaseURL):
    def __init__(self, url: str, description: str = "NA"):
        super().__init__(url, description)
        self.soup = url_parse_utils.fetch_soup(url)
        #self.title = url_parse_utils.fetch_title(self.soup)
        self.content = url_parse_utils.fetch_content(self.soup)
        self.paragraphs = url_parse_utils.fetch_paragraphs(self.soup)
        self.tables = url_parse_utils.fetch_tables_markdown(self.soup)

class URLManager:

    def __init__(self, urls):
        if isinstance(urls, str):
            urls = [urls]  # Convert a single URL to a list with one element
        self.urls = []
        for url in urls:
            self.add_url(url)

    def __call__(self, url: str, description: str = "NA"):
        self.add_url(url, description)

    def add_url(self, url: str, description: str = "NA"):
        # Check if the URL already exists in the list
        existing_url = next((u for u in self.urls if u.url == url), None)
        if existing_url:
            print(f"URL '{url}' already exists. Skipping.")
        else:
            url_obj = URL(url, description)
            self.urls.append(url_obj)

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

class URLOld() :

    def __init__(self, url: str, description: str = "NA", visited: bool = False, content: str = "NA", title: str = "NA"):
        self.url = url
        self.description = description
        self.visited = visited
        self.content = content
        self.title = title

    def __str__(self):
        return f"URL(url={self.url}, description={self.description}, visited={self.visited}, content={self.content}, title={self.title})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)

    def visit(self, content: str = "") -> None:
        self.visited = True
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "description": self.description,
            "visited": self.visited,
            "content": self.content,
            "title": self.title,
        }

    

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "URL":
        return URL(
            url=d["url"],
            description=d["description"],
            visited=d["visited"],
            content=d["content"],
            title=d["title"],
        )

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