import scrapy, os, zipfile

class CotSpiderSpider(scrapy.Spider):
    name = "cot_spider"
    allowed_domains = ["cftc.gov"]
    start_urls = ["https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm"]

    def parse(self, response):
        tables = [
            response.xpath('//table[1]/tbody/tr/td/a[1]/@href | //table[1]/tbody/tr/td/p/a[1]/@href').getall(),
            response.xpath('//table[3]/tbody/tr/td/a[1]/@href | //table[3]/tbody/tr/td/p/a[1]/@href').getall(),
            response.xpath('//table[5]/tbody/tr/td/a[1]/@href | //table[5]/tbody/tr/td/p/a[1]/@href').getall()
        ]
        
        for table_links in tables:
            for link in table_links:
                # if not link.endswith("2006_2016.zip"):
                #     if not link.endswith("deacot1986_2016.zip"):
                        targetlink = response.urljoin(link)
                        yield scrapy.Request(url=targetlink, callback=self.download_files)
            
            
    

    def download_files(self, response):
        path = response.url.split('/')[-1]
        dirf = r"C:\Users\ABEES_SIGNATURE\Documents\cot_data_new"
        if not os.path.exists(dirf):
            os.makedirs(dirf)
        os.chdir(dirf)
        
        # Write the downloaded file
        with open(path, 'wb') as f:
            f.write(response.body)
        
        # Check if the downloaded file is a zip file
        if path.endswith(".zip"):
            # Create a directory for extraction if it doesn't exist
            extract_dir = os.path.splitext(path)[0]  # Use the file name without the extension as the extraction directory
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)
            
            # Unzip the file
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Remove the zip file after extraction
            os.remove(path)