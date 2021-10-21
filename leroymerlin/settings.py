SPIDER_MODULES = ['leroymerlin.spiders']
NEWSPIDER_MODULE = 'leroymerlin.spiders'
USER_AGENT = 'Mozilla/5.0'
ROBOTSTXT_OBEY = False
LOG_ENABLED = True
LOG_LEVEL = 'ERROR'  # DEBUG / INFO / ERROR
LOG_FILE = 'log.txt'
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8
IMAGES_STORE = 'images'
ITEM_PIPELINES = {
   'leroymerlin.pipeline.DataBasePipeline': 300,
   'leroymerlin.pipeline.LeroyPhotosPipeline': 200,
}

