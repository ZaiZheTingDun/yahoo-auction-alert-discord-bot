import requests, json
from xml.dom.minidom import parseString
from lightbulb import BotApp
from hikari import Embed, Color
from log import log


async def check_mercari(bot: BotApp, alert: dict) -> None:
    res = requests.get(
        f"https://www.fromjapan.co.jp/japan/sites/mercari/search?keyword={alert['name']}&sort=new&hits=36&page=1",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        },
    )

    content = json.loads(res.json())
    items = content["items"]

    for item in items:
        item_code = item["id"]
        price = item["price"]
        title = item["title"]
        image_url = item["imageUrl"]

        if bot.d.synced.find_one(name=item_code, channel_id=alert["channel_id"]):
            log("[mercari] already synced — up to date")
            continue

        embed = Embed()
        embed.color = Color(0x09B1BA)
        embed.title = title or "Unknown"

        if item_code:
            embed.url = (
                "https://zenmarket.jp/ja/mercariproduct.aspx?itemCode="
                + item_code
            )

        if image_url:
            embed.set_image(image_url)

        if price:
            try:
                embed.add_field("Price", price)
            except:
                pass

        embed.set_footer(f"Source: Mercari — #{item_code}")

        await bot.rest.create_message(alert["channel_id"], embed=embed)
        bot.d.synced.insert({"name": item_code, "channel_id": alert["channel_id"]})
