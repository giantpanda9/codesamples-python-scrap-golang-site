#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scrapy spider/scrapper to fetch and parse the first page available by this link - https://golang.org/pkg/
# Author: Nikolay Chegodaev
import scrapy
import datetime
from urlparse import urljoin
from hashlib import md5
import urllib2
from cookielib import CookieJar
from scrapy.http import HtmlResponse

class scrapGoPageSpider(scrapy.Spider):
	name = 'scrapGoPageSpider'
	allowed_domains = ['golang.org']
	start_urls = ['https://golang.org/']

	def parse(self, response):
		scrapypath = scrapy.Selector(response)
		baseurl = 'https://golang.org'
		packagespath = scrapypath.xpath('/html/body/header/nav/ul/li[2]/a/@href').get()
		projectspath = scrapypath.xpath('/html/body/header/nav/ul/li[3]/a/@href').get()
		yield response.follow(str(baseurl) + str(packagespath), self.parsePackages)
		yield response.follow(str(baseurl) + str(projectspath), self.parseProjects)
		
	def parsePackages(self, response):
		scrapypath = scrapy.Selector(response)
		baseurl = 'https://golang.org/pkg'
		packageslinklist = scrapypath.xpath('//*[contains(@class, "pkg-name")]//a/@href').extract()
		packagestextlist = scrapypath.xpath('//*[contains(@class, "pkg-name")]//a/text()').extract()
		packagesdesclist = scrapypath.xpath('//*[contains(@class, "pkg-synopsis")]/text()').extract()
		packagestextcount = len(packagestextlist)
		
		returnedArray = []
		for i in range(2, int(packagestextcount)):
			returned = {}
			returned['name'] = str(packagestextlist[i])
			if i <= len(packageslinklist):
				returned['url'] = baseurl + "/" + packageslinklist[i] 
			if i <= len(packagesdesclist):
				packagesdesclist[i] = packagesdesclist[i].replace("\n\t\t\t\t\t\t\t\t\t","")
				packagesdesclist[i] = packagesdesclist[i].replace("\n\t\t\t\t\t\t\t\t","")
				print packagesdesclist[i]
				returned['description'] = packagesdesclist[i]
			returnedArray.append(returned)
		return returnedArray

	def parseProjects(self, response):
		scrapypath = scrapy.Selector(response)
		baseurl = 'https://golang.org'
		projectsversionlinklist = scrapypath.xpath('*//a[contains(text(),"Go ")]/@href').extract()
		projectsversiontextlist = scrapypath.xpath('*//a[contains(text(),"Go ")]/text()').extract()
		projectsversiondatelist = scrapypath.xpath('*//small[contains(text(),"(")]/text()').extract()
		projectsversiontextcount = len(projectsversiontextlist)
		
		returnedArray = []
		for i in range(0, int(projectsversiontextcount)):
			returned = {}
			#returned[str(projectsversiontextlist[i])] = {}
			returned['name'] = str(projectsversiontextlist[i])
			if i <= len(projectsversionlinklist):
				returned['url'] = baseurl + "/" + projectsversionlinklist[i] 
			if i < len(projectsversiondatelist):
				projectsversiondatelist[i] = projectsversiondatelist[i].replace("(","")
				projectsversiondatelist[i] = projectsversiondatelist[i].replace(")","")
				returned['date'] = projectsversiondatelist[i]
			else:
				returned['date'] = None
			returnedArray.append(returned)
		return returnedArray
