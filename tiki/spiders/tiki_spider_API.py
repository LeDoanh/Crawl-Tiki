import scrapy
import json
import datetime
from tiki.items import Tiki_Product


class tiki(scrapy.Spider):
    # Define Spider
    name = "tiki"

    # Urls
    start_url = 'https://www.tiki.vn/'
    list_product_url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=48&include=advertisement&aggregations=2&trackity_id=eea44a7b-5e01-1476-9270-eda9acca7784&category={category_number}&page={page}&urlKey={key}"
    product_url = "https://tiki.vn/api/v2/products/{product_id}?platform=web&spid={web_spid}"

    # Customize crawl options:
    keyword = "Điện thoại Smartphone"
    start_page = 1
    _id = 1
    
    # Save CSV:
    custom_settings = {"FEEDS": {"Tiki_crawl_result.json": {"format": "json"}}}

    # Start request:
    def start_requests(self):
        yield scrapy.Request(url = self.start_url, callback = self.parse_category)
    
    # Get url and request category API page:
    def parse_category(self, response):
        category_url = response.xpath("//a[contains(text(), '" + self.keyword + "')]/@href").get()
        url_key = category_url.split('/')[3]
        category_num = category_url[-4:]
        yield scrapy.Request(url = self.list_product_url.format(category_number = category_num, page = self.start_page, key = url_key), callback = self.parse)

    # Get product url, request product API page and request next page:
    def parse(self, response):
        data = json.loads(response.body)
        products = data['data']
        for product in products:
            url_product = product["url_path"]
            id_p = product["id"]
            web_s = url_product.split("-")[-1].split(".")[-1].split("=")[-1]
            yield scrapy.Request(url = self.product_url.format(product_id = id_p, web_spid = web_s), callback = self.parse_product)

        # Request next page:
        last_page = data['paging']['last_page']
        page = data['paging']['current_page']
        if page < (last_page + 1):
            next_page_url = response.urljoin(response.url.replace("&page=" + str(page), "&page=" + str(page + 1)))
            yield scrapy.Request(url = next_page_url, callback = self.parse)

    # Get response and take product data:
    def parse_product(self, response):
        Product_detail = json.loads(response.body)
        Product = Tiki_Product()

        # Product data:
        Product['Id'] = self._id
        self._id += 1
        
        Product['Name'] = Product_detail["name"]
        Product['Sku'] = Product_detail["sku"]
        Product['Current_price'] = Product_detail["price"]
        Product['List_price'] = Product_detail["list_price"]
        Product['Original_price'] = Product_detail["original_price"]
        Product['Discount'] = Product_detail["discount"]
        Product['Discount_rate'] = Product_detail["discount_rate"]
        Product['Rating_average'] = Product_detail["rating_average"]
        Product['Review_count'] = Product_detail["review_count"]
        Product['Favourite_count'] = Product_detail["favourite_count"]
        Product['Inventory_status'] = Product_detail["inventory_status"]
        Product['Inventory_type'] = Product_detail["inventory_type"]
        Product['Day_ago_created'] = (datetime.date.today() + datetime.timedelta(days = - Product_detail["day_ago_created"])).strftime("%d/%m/%Y")
        Product['Brand'] = Product_detail["brand"]["name"]
        Product['Current_seller'] = Product_detail["current_seller"]["name"]

        # All_time_quantity_sold
        try:
            Product['All_time_quantity_sold'] = Product_detail["all_time_quantity_sold"]
        except:
            Product['All_time_quantity_sold'] = "No record"

        # Other_sellers
        try:
            Product['Other_sellers'] = Product_detail["other_sellers"]
        except:
            Product['Other_sellers'] = "No"

        # Ranks
        try:
            Product['Rank'] = Product_detail["ranks"]["rank"]
        except:
            Product['Rank'] = "No"

        # Seller_specifications
        try:
            Product['Seller_specifications'] = Product_detail["seller_specifications"]["name"]
        except:
            Product['Seller_specifications'] = "No"

        Product['Description'] = Product_detail["description"]
        return Product