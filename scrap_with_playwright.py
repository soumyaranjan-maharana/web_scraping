import time
from playwright.sync_api import sync_playwright
import pandas as pd


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False,slow_mo=500)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/js")

    final_auth = []
    final_text = []
    while True:

        auth = page.locator("small.author").all_inner_texts()
        text = page.locator("span.text").all_inner_texts()

        final_text.extend(text)
        final_auth.extend(auth)

        next_page = page.locator("li.next a")

        if next_page.is_visible():
            next_page.click()
            page.wait_for_selector(".quote")
        else:
            break


    df = pd.DataFrame({
        "Author" : final_auth,
        "Quotes" : final_text
    })

   
    df.to_csv(r"C:\Users\Lenovo\OneDrive\Documents\dataframe files\quotes2.csv", index=False, encoding="utf-8-sig")
    browser.close()
    