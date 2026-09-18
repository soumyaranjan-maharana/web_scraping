from playwright.async_api import async_playwright
import pandas as pd
import asyncio
import math

async def mult_scrape(page, urls):
    res = []
    for index ,url in urls:
        await page.goto(url, wait_until="domcontentloaded", timeout = 60000)

        try:
            description_text = await page.locator(".woocommerce-product-details__short-description p").text_content() if await page.locator(".woocommerce-product-details__short-description p").count() > 0 else None
            sku_text = await page.locator(".sku").text_content() if await page.locator(".sku").count() > 0 else None
            stock_raw = await page.locator(".stock").text_content() if await page.locator(".stock").count() > 0 else None

        except Exception as e:
            description_text, sku_text, stock_raw = None, None, None
            print(f"Skipped {u}: {e}")

        res.append((index,description_text, sku_text, stock_raw))

    return res




async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        await page.goto("https://scrapeme.live/shop/")

        title = []
        price = []
        img_url = []
        product_url = []
        

        while True:
            products = page.locator(".product")
            title_raw = await products.locator("h2").all_text_contents()
            price_raw = await products.locator(".price").all_text_contents()
            count = await products.count()
            for i in range(count):
                product = products.nth(i)
                img_loc = await product.locator("img").get_attribute("src")
                pro_loc = await product.get_by_role("link").get_attribute("href")
                img_url.append(img_loc)
                product_url.append(pro_loc)


            title.extend(title_raw)
            price.extend(price_raw)

            




            nxt_btn = page.locator("a.next").first

            if await nxt_btn.is_visible():
               await nxt_btn.click()
               await page.wait_for_load_state("domcontentloaded")
            else:
                break

        worker = 4
        pages = []
        batch_size = math.ceil(len(product_url) / worker)
        batches = []

        for i in range(worker):
            pages.append(await browser.new_page())
            start = batch_size * i
            end = batch_size * (i+1)
            batch = list(enumerate(product_url))[start:end]
            batches.append(batch)

        result = await asyncio.gather(*[
            mult_scrape(pages[i], batches[i]) for i in range(worker)
        ]
        )

    



        data = {
            "Title" : title,
            "Price" : price,
            "Image URL" : img_url,
            "Product URL" : product_url,
            "Description" : None,
            "SKU" : None,
            "Stock" : None
        }


        df = pd.DataFrame(data)

        for r in result:
            for i, description, sku, stock in r:
                df.loc[i, "Description"] = description  
                df.loc[i, "SKU"] = sku
                df.loc[i, "Stock"] = stock

        
        df.to_csv(r"C:\Users\Lenovo\OneDrive\Documents\dataframe files\product.csv", index=False, encoding="utf-8-sig")

        await browser.close()



if __name__ == "__main__":
    asyncio.run(scrape())