import requests

import pandas as pd

BASE_URL = "https://gql.tokopedia.com/graphql"

SHOP = "./shop"
PRODUCT = "./product"
CATEGORY = "./category"
SHOP_URL = f"{BASE_URL}/ReviewList"
PRODUCT_URL = f"{BASE_URL}/productReviewList"
CATEGORY_URL = f"{BASE_URL}/SearchProductQuery"
CATEGORIES_URL = f"{BASE_URL}/headerMainData"

header = {
    "authority": "gql.tokopedia.com",
    "accept": "*/*",
    "accept-language": "en",
    "content-type": "application/json",
    "origin": "https://www.tokopedia.com",
    "referer": "https://www.tokopedia.com",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "tkpd-userid": "0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "x-device": "desktop-0.0",
    "x-source": "tokopedia-lite",
    "x-tkpd-lite-service": "zeus",
    "x-version": "1fbf287",
}


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
    review_list = data[0]["data"]["productrevGetShopReviewReadingList"]["list"]

    shop_name = data[0]["data"]["productrevGetShopReviewReadingList"]["shopName"]

    return {
        "id": [item["id"] for item in review_list],
        "productID": [item["product"]["productID"] for item in review_list],
        "productName": [item["product"]["productName"] for item in review_list],
        "reviewerID": [item["reviewerID"] for item in review_list],
        "reviewerName": [item["reviewerName"] for item in review_list],
        "rating": [item["rating"] for item in review_list],
        "reviewText": [item["reviewText"] for item in review_list],
        "replyText": [item["replyText"] for item in review_list],
        "shopName": [shop_name for _ in review_list],
    }


def parse_product(
    data: dict,
    location: str,
    price: int,
    overall: int,
    total: int,
    name: str = "",
) -> dict[str, list]:
    """
    Parse product review data from a given dictionary and return a dictionary with lists of review attributes.

    Args:
        data (dict): A dictionary containing product review data. The expected structure is:
            {
                "data": {
                    "productrevGetProductReviewList": {
                        "productID": str,
                        "list": [
                            {
                                "id": str,
                                "variantName": str,
                                "message": str,
                                "productRating": int,
                                "reviewResponse": {
                                    "message": str
                                },
                                "user": {
                                    "userID": str,
                                    "fullName": str
                                }
                            },
                        ],
                        "shop": {
                            "shopID": str,
                            "name": str
                        }
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
    review_list = data[0]["data"]["productrevGetProductReviewList"]["list"]

    product_id = data[0]["data"]["productrevGetProductReviewList"]["productID"]

    shop_name = data[0]["data"]["productrevGetProductReviewList"]["shop"]["name"]

    if location and price and overall and total:
        return {
            "id": [item["id"] for item in review_list],
            "productID": [product_id for _ in review_list],
            "productName": [name for _ in review_list],
            "location": [location for _ in review_list],
            "price": [price for _ in review_list],
            "overall": [overall for _ in review_list],
            "total": [total for _ in review_list],
            "reviewerID": [item["user"]["userID"] for item in review_list],
            "reviewerName": [item["user"]["fullName"] for item in review_list],
            "rating": [item["productRating"] for item in review_list],
            "reviewText": [item["message"] for item in review_list],
            "replyText": [item["reviewResponse"]["message"] for item in review_list],
            "shopName": [shop_name for _ in review_list],
        }

    return {
        "id": [item["id"] for item in review_list],
        "productID": [product_id for _ in review_list],
        "productName": [name for _ in review_list],
        "reviewerID": [item["user"]["userID"] for item in review_list],
        "reviewerName": [item["user"]["fullName"] for item in review_list],
        "rating": [item["productRating"] for item in review_list],
        "reviewText": [item["message"] for item in review_list],
        "replyText": [item["reviewResponse"]["message"] for item in review_list],
        "shopName": [shop_name for _ in review_list],
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
                }
                rating
                reviewText
                reviewerID
                reviewerName
			    replyText
            }
            shopName
        }
    }
    """

    param = {
        "filterBy": "",
        "limit": 200,
        "page": page,
        "shopID": id,
        "sortBy": "create_time desc",
    }

    return session.post(
        SHOP_URL,
        headers=header,
        json=[{"query": query, "variables": param, "operationName": "ReviewList"}],
        timeout=(5, 15),
    ).json()


def fetch_product(id: str, page: int = 1) -> dict:
    """
    Fetches product reviews from the Tokopedia API.
    Args:
        id (str): The ID of the product to fetch reviews for.
        page (int, optional): The page number of reviews to fetch. Defaults to 1.
    Returns:
        dict: A dictionary containing the product reviews and related information.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the network request.
    """
    query = """
query productReviewList(
    $productID: String!
    $page: Int!
    $limit: Int!
    $sortBy: String
    $filterBy: String
) {
    productrevGetProductReviewList(
        productID: $productID
        page: $page
        limit: $limit
        sortBy: $sortBy
        filterBy: $filterBy
    ) {
        productID
        list {
            id: feedbackID
            variantName
            message
            productRating
            reviewResponse {
                message
            }
            user {
                userID
                fullName
            }
        }
        shop {
            shopID
            name
        }
    }
}
    """

    param = {
        "filterBy": "",
        "limit": 15,
        "page": page,
        "productID": id,
        "sortBy": "informative_score desc",
    }

    return session.post(
        PRODUCT_URL,
        headers=header,
        json=[
            {"query": query, "variables": param, "operationName": "productReviewList"}
        ],
        timeout=(5, 15),
    ).json()


def fetch_categories():
    query = """
query headerMainData($filter: String) {
  dynamicHomeIcon {
    categoryGroup {
      id
      title
      categoryRows {
        id
        name
        categoryId
      }
    }
  }
  categoryAllListLite(filter: $filter) {
    categories {
      id
      name
      children {
        id
        name
        children {
          id
          name
        }
      }
    }
  }
}
    """

    param = {
        "filter": "buyer",
    }

    return session.post(
        CATEGORIES_URL,
        headers=header,
        json=[{"query": query, "variables": param, "operationName": "headerMainData"}],
        timeout=(5, 15),
    ).json()


def fetch_category(id: str, page: int = 1):
    query = """
query SearchProductQuery($params: String, $adParams: String) {
  CategoryProducts: searchProduct(params: $params) {
    count
    data: products {
      idNumber: id
      id: id_str_auto_
      url
      imageUrl: image_url
      imageUrlLarge: image_url_700
      catIdNumber: category_id
      catId: category_id_str_auto_
      gaKey: ga_key
      countReview: count_review
      discountPercentage: discount_percentage
      preorder: is_preorder
      name
      price
      priceInt: price_int
      original_price
      rating
      wishlist
      labels {
        title
        color
      }
      badges {
        imageUrl: image_url
        show
      }
      shop {
        idNumber: id
        id: id_str_auto_
        url
        name
        goldmerchant: is_power_badge
        official: is_official
        reputation
        clover
        location
      }
      labelGroups: label_groups {
        position
        title
        type
      }
    }
  }
  displayAdsV3(displayParams: $adParams) {
    data {
      id
    }
    template 
  }
}
    """

    param = {
        "adParams": f"page={page}&page={page}&dep_id={id}&ob=&ep=product&item=40&src=directory&device=desktop&user_id=&minimum_item=40&start=1&no_autofill_range=",
        "params": f"page={page}&ob=&identifier=&sc={id}&user_id=&rows=40&start=1&source=directory&device=desktop&page=1&related=true&st=product&safe_search=false",
    }

    return session.post(
        CATEGORY_URL,
        headers=header,
        json=[
            {"query": query, "variables": param, "operationName": "SearchProductQuery"}
        ],
        timeout=(5, 15),
    ).json()


def __main__():
    print("Choose an option:")
    print("\t1.\tBy Shop ID")
    print("\t2.\tBy Product ID")
    print("\t3.\tBy Category")
    print("\t9.\tExit")

    choice = int(input("Enter your choice: "))

    match choice:
        case 1:
            try:
                shop_id = str(input("Enter the Shop ID: "))

                pages = int(input("Enter the number of pages to fetch (200/page): "))

                data_df = pd.DataFrame(
                    columns=[
                        "id",
                        "productID",
                        "productName",
                        "reviewerID",
                        "reviewerName",
                        "rating",
                        "reviewText",
                        "replyText",
                        "shopName",
                    ]
                )

                for page in range(1, pages + 1):
                    data = fetch_shop(shop_id, page)

                    data_df = pd.concat(
                        [data_df, pd.DataFrame.from_dict(parse_shop(data))]
                    )

                data_df["reviewText"] = data_df["reviewText"].apply(
                    lambda x: (
                        x.replace("\n", " ").replace("\r", " ")
                        if isinstance(x, str)
                        else x
                    )
                )
                data_df["replyText"] = data_df["replyText"].apply(
                    lambda x: (
                        x.replace("\n", " ").replace("\r", " ")
                        if isinstance(x, str)
                        else x
                    )
                )

                data_df.to_csv(f"{SHOP}/{shop_id}.csv", index=False)

                print(f"Data saved to {SHOP}/{shop_id}.csv")

            except ValueError:
                print("Invalid input. Please enter a valid Shop ID.")
        case 2:
            try:
                product_id = str(input("Enter the Product ID: "))

                pages = int(input("Enter the number of pages to fetch (15/page): "))

                data_df = pd.DataFrame(
                    columns=[
                        "id",
                        "productID",
                        "productName",
                        "reviewerID",
                        "reviewerName",
                        "rating",
                        "reviewText",
                        "replyText",
                        "shopName",
                    ]
                )

                for page in range(1, pages + 1):
                    data = fetch_product(product_id, page)

                    print(data)

                    data_df = pd.concat(
                        [data_df, pd.DataFrame.from_dict(parse_product(data))]
                    )

                data_df["reviewText"] = data_df["reviewText"].apply(
                    lambda x: (
                        x.replace("\n", " ").replace("\r", " ")
                        if isinstance(x, str)
                        else x
                    )
                )
                data_df["replyText"] = data_df["replyText"].apply(
                    lambda x: (
                        x.replace("\n", " ").replace("\r", " ")
                        if isinstance(x, str)
                        else x
                    )
                )

                data_df.to_csv(f"{PRODUCT}/{product_id}.csv", index=False)

                print(f"Data saved to {PRODUCT}/{product_id}.csv")

            except ValueError:
                print("Invalid input. Please enter a valid Shop ID.")
        case 3:
            try:
                data = fetch_categories()

                categories: list = data[0]["data"]["categoryAllListLite"]["categories"]

                print("Categories:")

                for category in categories:
                    print(f"\t{category['id']}: {category['name']}")

                category_id = int(input("Enter the Category ID: "))

                category = [
                    category for category in categories if category["id"] == category_id
                ][0]

                pages = int(input("Enter the number of pages to fetch (40/page): "))

                data_df = pd.DataFrame(
                    columns=[
                        "id",
                        "productID",
                        "productName",
                        "location",
                        "price",
                        "overall",
                        "total",
                        "reviewerID",
                        "reviewerName",
                        "rating",
                        "reviewText",
                        "replyText",
                        "shopName",
                    ]
                )

                for page in range(1, pages + 1):
                    data = fetch_category(category_id, page)

                    products = data[0]["data"]["CategoryProducts"]["data"]

                    for product in products:
                        product_id = product["id"]
                        product_name = product["name"]

                        product_data = fetch_product(product_id)

                        data_df = pd.concat(
                            [
                                data_df,
                                pd.DataFrame.from_dict(
                                    parse_product(
                                        product_data,
                                        name=product_name,
                                        location=product["shop"]["location"],
                                        price=product["priceInt"],
                                        overall=product["rating"],
                                        total=product["countReview"],
                                    )
                                ),
                            ]
                        )

                data_df["reviewText"] = data_df["reviewText"].apply(
                    lambda x: (
                        x.replace("\n", " ").replace("\r", " ")
                        if isinstance(x, str)
                        else x
                    )
                )
                data_df["replyText"] = data_df["replyText"].apply(
                    lambda x: (
                        x.replace("\n", " ").replace("\r", " ")
                        if isinstance(x, str)
                        else x
                    )
                )

                data_df.to_csv(
                    f"{CATEGORY}/{category_id}_{category["name"]}.csv", index=False
                )

                print(f"Data saved to {CATEGORY}/{category_id}_{category['name']}.csv")

            except ValueError:
                print("Invalid input. Please enter a valid Category ID.")
        case 9:
            exit(0)


if __name__ == "__main__":
    print("Fetching cookies...")

    session = requests.Session()

    response = session.get(BASE_URL, headers=header, timeout=(5, 60))

    if response.status_code == 200:
        cookies = session.cookies.get_dict()

        print(f"Cookies: {cookies}")

        cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])
    else:
        print("Failed to fetch cookies. Exiting...")

        exit(1)

    while 1:
        __main__()
