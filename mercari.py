from lightbulb import BotApp
from hikari import Embed, Color
from selenium.webdriver.chrome.options import Options

from logger import log, error
from selenium import webdriver
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)


async def check_mercari(bot: BotApp, alert: dict) -> None:
    browser.get(f"https://zenmarket.jp/ja/mercari.aspx?q={alert['name']}&sort=LaunchDate")
    products = browser.find_elements(By.CLASS_NAME, 'product')

    for item in products:
        link_element = item.find_element(By.CLASS_NAME, 'product-link')
        link = link_element.get_attribute('href')
        code = link.split("itemCode=")[1]

        img_element = item.find_element(By.CSS_SELECTOR, 'img')
        img = img_element.get_attribute('src')

        title_element = item.find_element(By.CSS_SELECTOR, '.title-container .item-title')
        title = title_element.get_attribute('title')

        price_element = item.find_element(By.CSS_SELECTOR, '.price .current-price .amount')
        price = price_element.get_attribute('data-jpy')

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
            except Exception as e:
                error(str(e))

        embed.set_footer(f"Source: Mercari — #{code}")

        await bot.rest.create_message(alert["channel_id"], embed=embed)
        bot.d.synced.insert({"name": code, "channel_id": alert["channel_id"]})
