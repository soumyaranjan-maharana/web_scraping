from playwright.sync_api import sync_playwright
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")

    fin_title = []
    fin_price = []
    fin_rating = []
    fin_instock = []
    while True:

        products = page.locator(".product_pod")


        price = products.locator(".price_color").all_inner_texts()


        rating = []
        title = []

        for i in range(products.count()):
            rating_map = {"One" : 1, "Two" : 2, "Three" : 3, "Four"  : 4, "Five" : 5}
            product = products.nth(i)
            loc_rating_class = product.locator(".star-rating").get_attribute("class")
            rating.append(rating_map[loc_rating_class.split()[-1]])
            title_class = product.locator("h3 a").get_attribute("title")
            title.append(title_class)

        
        instock = products.locator(".instock").all_inner_texts()

        fin_title.extend(title)
        fin_price.extend(price)
        fin_rating.extend(rating)
        fin_instock.extend(instock)

        next_btn = page.locator(".next a")

        if next_btn.is_visible():
            next_btn.click()
        else:
            break

    df = pd.DataFrame({
        "Title" : fin_title,
        "Price" : fin_price,
        "Rating" : fin_rating,
        "Availability" : fin_instock
    })

    path = r"C:\Users\Lenovo\OneDrive\Documents\dataframe files\books.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    

    browser.close()

