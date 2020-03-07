# codesamples-python-scrap-golang-site
Depends on Scrapy module for Python 2.7
Using Python 2.7 because Scrapy stable package available for Python 2.x for now

Scrapy installation (based on https://linoxide.com/ubuntu-how-to/scrapy-install-ubuntu/):
1) (optional, mandatory only if not installed) install pip: sudo apt-get install python-pip
2) (optional, mandatory only if not installed) install development libraries: sudo apt-get install python-dev
3) (mandatory) intall Scrapy module itself: sudo pip install scrapy

How to run?
1) cd codesampleScrapGoSite
2) scrapy crawl scrapGoPageSpider -o /home/nik/scrapyOutput/output/output.json
