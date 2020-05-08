from scrapy.cmdline import execute

# scrapy crawl template
execute(
    [
        "scrapy",
        "crawl",
        "template",
        "-akeyword=template_keyword",
        "-apage=1",
        "-sMONGO_URL=mongodb://localhost:27017/",
        "-sSPIDER_NAME=templatespider",
        "-sTASK_ID=001",
        "-sJOB_ID=002",
    ]
)

