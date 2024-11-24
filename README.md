# Scrapping Tokopedia Review

This script is used for scrapping Tokopedia Reviews by using the Tokopedia GraphQL API endpoint. 

## How To Use

1. Clone the repository

```sh
git clone https://github.com/Shafnaa/scrapping-tokopedia-review.git
```

2. Create Virtual Environment 

```sh
python3 -m venv venv
```

3. Install dependencies

```sh
pip install -r requirements.txt
```

4. Run the program

```sh
python3 main.py
```

5. Choose the operation needed

```
Choose an option:
	1.	By Shop ID
	2.	By Product ID
	9.	Exit
Enter your choice: 1
Enter the Shop ID: 878799
Enter the number of pages to fetch (200/page): 5
Data saved to ./shop/878799.csv
```

## How it works

This script will use the Tokopedia GraphQL API used by the website directly with optimized query to only fetch the data we need. Here is the query for fetching By Shop ID:

```gql
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
```

```json
{
    "filterBy": "",
    "limit": 200,
    "page": 1,
    "shopID": "id",
    "sortBy": "create_time desc"
}
```
