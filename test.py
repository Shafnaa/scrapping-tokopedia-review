import json
import os
import asyncio
import requests

import pandas as pd

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

BASE_URL = "https://gql.tokopedia.com/graphql"

SHOP = "./shop"
PRODUCT = "./product"
SHOP_URL = f"{BASE_URL}/ReviewList"
PRODUCT_URL = f"{BASE_URL}/prodcutReviewList"

def load_json(src: str) -> dict:
    """
    Load shop data from a JSON file.

    Args:1
        src (str): The file path to the JSON file containing shop data.

    Returns:
        dict: A dictionary containing the shop data loaded from the JSON file.
    """
    with open(src, "r") as f:
        return json.load(f)
    
def parse_shop(data: dict) -> dict[str, list]:
    """
    Parses shop review data from a given dictionary and returns a dictionary with lists of review attributes.
    Args:
        data (dict): A dictionary containing shop review data. The expected structure is:
            {
                "data": {
                    "productrevGetProductReviewList": {
                        "list": [
                            {
                                "id": str,
                                "product": {
                                    "productID": str,
                                    "productName": str
                                },
                                "reviewerID": str,
                                "reviewerName": str,
                                "rating": int,
                                "reviewText": str,
                                "replyText": str
                            },
                            ...
                        ],
                        "shopName": str,
                        ...
                    }
                }
            }
    Returns:
        dict[str, list]: A dictionary where each key corresponds to a review attribute and each value is a list of those attributes from all reviews. The keys are:
            - "id": List of review IDs.
            - "productID": List of product IDs.
            - "productName": List of product names.
            - "reviewerID": List of reviewer IDs.
            - "reviewerName": List of reviewer names.
            - "rating": List of ratings.
            - "reviewText": List of review texts.
            - "replyText": List of reply texts.
            - "shopName": List of shop names (repeated for each review).
    """
    print(data)
    
    review_list = data[0]["data"]["productrevGetShopReviewReadingList"]["list"]
    
    shop_name = data[0]["data"]["productrevGetShopReviewReadingList"]["shopName"]
    
    return{
        "id": [item["id"] for item in review_list],
        "productID": [item["product"]["productID"] for item in review_list],
        "productName": [item["product"]["productName"] for item in review_list],
        "reviewerID": [item["reviewerID"] for item in review_list],
        "reviewerName": [item["reviewerName"] for item in review_list],
        "rating": [item["rating"] for item in review_list],
        "reviewText": [item["reviewText"] for item in review_list],
        "replyText": [item["replyText"] for item in review_list],
        "shopName": [shop_name for _ in review_list]
    }

def fetch_shop(id: str, page: int = 1) -> dict:
    """
    Fetch shop data from the Tokopedia API.

    Args:
        id (str): The ID of the shop to fetch data for.
        page (int): The page number of the shop data to fetch.

    Returns:
        dict: The shop data fetched from the Tokopedia API.
    """
    transport = AIOHTTPTransport(
        url=SHOP_URL,
        headers={
            'authority': 'gql.tokopedia.com',
            'accept': '*/*',
            'accept-language': 'en',
            'content-type': 'application/json',
            'origin': 'https://www.tokopedia.com',
            'referer': 'https://www.tokopedia.com',
            'cookie': cookie_header,
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'tkpd-userid': '0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'x-device': 'desktop-0.0',
            'x-source': 'tokopedia-lite',
            'x-tkpd-lite-service': 'zeus',
            'x-version': '1fbf287'
        },
    )
    
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = """
    query ReviewList(
        $shopID: String!
        $limit: Int!
        $page: Int!
        $filterBy: String
        $sortBy: String
    ) {
        productrevGetShopReviewReadingList(
            shopID: $shopID
            limit: $limit
            page: $page
            filterBy: $filterBy
            sortBy: $sortBy
        ) {
            list {
                id: reviewID
                product {
                    productID
                    productName
                    productImageURL
                    productPageURL
                    productStatus
                    isDeletedProduct
                    productVariant {
                        variantID
                        variantName
                        __typename
                    }
                    __typename
                }
                rating
                reviewTime
                reviewText
                reviewerID
                reviewerName
                avatar
                replyText
                replyTime
                attachments {
                    attachmentID
                    thumbnailURL
                    fullsizeURL
                    __typename
                }
                videoAttachments {
                    attachmentID
                    videoUrl
                    __typename
                }
                state {
                    isReportable
                    isAnonymous
                    __typename
                }
                likeDislike {
                    totalLike
                    likeStatus
                    __typename
                }
                badRatingReasonFmt
                __typename
            }
            hasNext
            shopName
            totalReviews
            __typename
        }
    }
    """    
    
    param = {
        "filterBy": "",
        "limit": 200,
        "page": page,
        "shopID": id,
        "sortBy": "create_time desc"
    }
        
    return client.execute(gql(query), variable_values=param)

def operation_shop():    
    print("Choose an option:")
    print("\t1.\tFetch shop data")
    print("\t2.\tConvert all shop data to csv")
    print("\t9.\tExit")
    
    match int(input()):
        case 1:
            try:
                shop_id = str(input("Enter the Shop ID: "))
                
                pages = int(input("Enter the number of pages to fetch (200/page): "))
                
                data_df = pd.DataFrame(columns=["id", "productID", "productName", "reviewerID", "reviewerName", "rating", "reviewText", "replyText", "shopName"])
                
                for page in range(1, pages + 1):    
                    data = fetch_shop(shop_id, page)
                    
                    data_df = pd.concat([data_df, pd.DataFrame.from_dict(parse_shop(data))])
                    
                data_df.to_csv(f"{SHOP}/{shop_id}.csv", index=False)
                    
            except ValueError:
                print("Invalid input. Please enter a valid Shop ID.")
        case 2:
            pass
        case 9:
            return

def __main__():
    print("Choose an option:")
    print("\t1.\tBy Shop ID")
    print("\t2.\tBy Product ID")
    print("\t9.\tExit")
    
    match int(input()):
        case 1:
            operation_shop()
        case 2:
            pass
        case 9:
            return
        
if __name__ == "__main__":   
    print("Fetching cookies...")
    
    session = requests.Session()
    
    response = session.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=(5, 60))
    
    print("masuk sini kaga?")
    
    if response.status_code == 200:
        cookies = session.cookies.get_dict()
        
        print(f"Cookies: {cookies}")        
        
        cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])
    else:
        print("Failed to fetch cookies. Exiting...")
        
        exit(1)
    
    while 1:
        __main__()