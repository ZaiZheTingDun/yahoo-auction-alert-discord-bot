import requests, json
from xml.dom.minidom import parseString
from lightbulb import BotApp
from hikari import Embed, Color
from log import log
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()


async def check_mercari(bot: BotApp, alert: dict) -> None:
    browser.get(f"https://zenmarket.jp/ja/mercari.aspx?q=%25e9%25ac%25bc%25e6%25bb%2585%25e3%2581%25ae%25e5%2588%2583%25e3%2581%25b1%25e3%2581%2597%25e3%2582%2583%25e3%2581%2593%25e3%2582%258c&sort=LaunchDate")
    products = browser.find_elements(By.CLASS_NAME, 'product')

    r = session.get(f"https://zenmarket.jp/ja/mercari.aspx", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    })

    content = json.loads(r.json()["d"])

    for item in products:
        linkElement = item.find_element(By.CLASS_NAME, 'product-link')
        link = linkElement.get_attribute('href')
        code = link.split("itemCode=")[1]
        imgElement = item.find_element(By.CSS_SELECTOR, 'img')
        img = imgElement.get_attribute('src')
        titleElement = item.find_element(By.CSS_SELECTOR, '.title-container .item-title')
        title = titleElement.get_attribute('title')
        priceElement = item.find_element(By.CSS_SELECTOR, '.price .current-price .amount')
        price = priceElement.get_attribute('data-jpy')

        log(link + code + img + title + price)

        if bot.d.synced.find_one(name=code, channel_id=alert["channel_id"]):
            log("[mercari] already synced — up to date")
            continue

    embed = Embed()
    embed.color = Color(0x09B1BA)
    embed.title = title or "Unknown"

    if code:
        embed.url = (
            "https://zenmarket.jp/ja/mercariproduct.aspx?itemCode="
            + code
        )

        if img:
            embed.set_image(img)

        if price:
            try:
                embed.add_field("Price", price)
            except:
                pass

    embed.set_footer(f"Source: Mercari — #{code}")

    await bot.rest.create_message(alert["channel_id"], embed=embed)
    bot.d.synced.insert({"name": code, "channel_id": alert["channel_id"]})
