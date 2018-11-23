# import scrapy
# from scrapy.linkextractors import LinkExtractor


# class RustSpider(scrapy.Spider):
#     name = "rust"
#     allowed_domains = ["www.rust-lang.org"]
#     start_urls = (
#         'http://www.rust-lang.org/',
#     )

#     def parse(self, response):
#         extractor = LinkExtractor(allow_domains='rust-lang.org')
#         links = extractor.extract_links(response)
#         for link in links:
#             print (link.url)