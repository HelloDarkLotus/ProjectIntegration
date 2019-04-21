import os
import configparser
import csv
import requests
from bs4 import BeautifulSoup


class PipeLine(object):
    def __init__(self):
        self.userName = ""
        self.passWord = ""
        self.versionNumber = ""
        self.projectName = ""
        self.baseUrl = ""
        self.basePath = ""
        self.targetPath = ""
        self.gitRepo = ""
        self.session = ""
        self.headers = ""

    # return configure file's path
    def GetConfigPath(self):
        return os.getcwd() + r'\config.ini'

    # parser configure file than get configure parameters
    def ConfigMethod(self, fileName):
        config = configparser.ConfigParser()
        config.read(fileName)
        self.userName = config.get("RedmineInfo", "username")
        self.passWord = config.get("RedmineInfo", "password")
        self.baseUrl = config.get("RedmineInfo", "baseurl")        
        self.versionNumber = config.get("ProjectInfo", "version")
        self.projectName = config.get("ProjectInfo", "projname")
        self.basePath = config.get("CompileInfo", "basepath")
        self.targetPath = config.get("CompileInfo", "targetpath")
        self.gitRepo = config.get("CompileInfo", "gitrepo")

    # generate HTTP request header
    def GenHeader(self):
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        accept_encoding = 'gzip,deflate,sdch'
        accept_language = 'zh-CN,zh;q=0.8'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

        self.headers = {
            'Accept': accept,
            'Accept-Encoding': accept_encoding,
            'Accept-Language': accept_language,
            'User-Agent': user_agent,
        }

    # get token string for login authentication
    def GetLoginToken(self):
        loginUrl = self.baseUrl + r'login'
        self.session = requests.Session()
        r = self.session.get(loginUrl, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup.find('input', {'name': 'authenticity_token'})['value']

    # login redmine
    def LoginMethod(self):
        token = self.GetLoginToken()
        if token is not None:
            post_data = {
                'username': self.userName,
                'password': self.passWord,
                'authenticity_token': token,
            }

            # because redmine login successful will redirect, so should forbidden it
            self.session.post(self.baseUrl + r'login', data=post_data, headers=self.headers, allow_redirects=False)

    # spider bug information and store into list
    def SpiderMethod(self):
        roadmapUrl = self.baseUrl + r'projects/' + self.projectName.lower() + r'/roadmap'
        r = self.session.get(roadmapUrl)
        soup = BeautifulSoup(r.text, 'lxml')
        href = soup.find('a', {'name': self.versionNumber})['href']
        siUrl = r'http://192.168.100.103' + href

        # get all bug information
        r = self.session.get(siUrl)
        soup = BeautifulSoup(r.text, 'lxml')
        bugNumLst = list()
        for issue in soup.find_all('tr', {'class': 'issue hascontextmenu'}):
            bugNumLst.append(issue.find('input')['value'])

        # enter into each bug tickets then get its information
        bugInfo = list()
        for bugNum in bugNumLst:
            url = self.baseUrl + r'issues/' + bugNum
            r = self.session.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            # bug title
            bugTtl = soup.find('div', {'class': 'subject'}).find('h3').text
            # bug status
            bugSts = soup.find('div', {'class': 'status attribute'}).find('div', {'class': 'value'}).text
            # bug processor
            bugPrssr = soup.find('div', {'class': 'assigned-to attribute'}).find('a', {'class': 'user active'}).text
            # bug process start time
            bugStrt = soup.find('div', {'class': 'start-date attribute'}).find('div', {'class': 'value'}).text
            # bug progress
            bugPrgrss = soup.find('div', {'class': 'progress attribute'}).find('p', {'class': 'percent'}).text            
            bugInfo.append((bugNum, bugTtl, bugSts, bugPrssr, bugStrt, bugPrgrss))

        return bugInfo

    def StoreData(self, *kargs):
        with open('tmp.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([r'Redmine票号', r'问题标题', r'问题状态', r'问题处理人', r'开始时间', r'处理进度'])
            for bugItem in kargs:
                writer.writerows([bugItem])