import json
import scrapy
from ..items import YahooquestionsItem


categories_ids = ['396545012', '396545144', '396545013', '396545311', '396545660', '396545014',
                  '396545327', '396545015', '396545016', '396545451', '396545433', '396545367',
                  '396545019', '396545018', '396545394', '396545401', '396545439', '396545443',
                  '396545444', '396546046', '396545122', '396545301', '396545454', '396545213',
                  '396545469', '396546089'
                  ]


class YahooQuestions(scrapy.Spider):
    name = "question"

    # API URL
    start_urls = 'https://answers.yahoo.com/_reservice_/'
    # API headers
    api_headers = {
        'content-type': 'application/json'
    }

    # HTTP PUT request payload
    payload = {
        "type": "CALL_RESERVICE",
        "payload": {
            # change the category ID to retrieve proper questions
            # e.g. you have URL: https://answers.yahoo.com/dir/index/discover?sid=396545443
            # so you need to look at "?sid=396545443" string query parameter
            # and extract the number 396545443 to use it as the "categoryId" below
            "categoryId": '396545012',
            "lang": "en-US",
            "count": 20,
            "offset": "pc00~p:0"
        },
        "reservice": {
            "name": "FETCH_DISCOVER_STREAMS_END",
            "start": "FETCH_DISCOVER_STREAMS_START",
            "state": "CREATED"
        }
    }

    # data offset
    data_offset = 0

    # crawler's entry point
    def start_requests(self):
        # make HTTP PUT request to API URL
        # for i in categories_ids:
        #     self.payload["payload"]["categoryId"] = i
        for i in categories_ids:
            self.payload["payload"]["categoryId"] = i
            yield scrapy.Request(
                url=self.start_urls,
                method='PUT',
                headers=self.api_headers,
                body=json.dumps(self.payload),
                callback=self.parse
        )

    # parse callback method
    def parse(self, response):
        items = YahooquestionsItem()
        json_data = json.loads(response.text)
        for question in json_data['payload']['questions']:
            items['qid'] = question['qid']
            items['title'] = question['title']
            items['detail'] = question['detail']
            items['answerscount'] = question['answersCount']
            items['thumbUpsCount'] = question['thumbUpsCount']
            items['CreatedTime'] = question['createdTime']
            items['categoryname'] = question['category']['name']
            items['main_category'] = self.payload['payload']['categoryId']
            yield items
        # check if next bunch of data available
        if json_data['payload']['canLoadMore'] == True:
            # update data offset
            self.data_offset += 20

            # update payload offset
            self.payload['payload']['offset'] = 'pc' + str(self.data_offset) + '~p:0'

            # crawl next bunch of data
            # for i in categories_ids:
            #     self.payload["payload"]["categoryId"] = i
            for i in categories_ids:
                self.payload["payload"]["categoryId"] = i
                yield scrapy.Request(
                    url=self.start_urls,
                    method='PUT',
                    headers=self.api_headers,
                    body=json.dumps(self.payload),
                    callback=self.parse
                )
