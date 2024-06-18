# way to export the data and post it to a DISCORD webhook
import asyncio
import json
import aiohttp
from datetime import datetime
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.route("**/*", lambda route: route.continue_())
        xhrrequests = []
        def resquesthandler(request):
            if request.resource_type == "xhr":
                xhrrequests.append(request)
        page.on("request", resquesthandler)
        await page.goto("https://x.com/") # twitter/x handle here 
        await page.wait_for_timeout(100)
        requests = [request for request in xhrrequests if "UserTweets" in request.url]
        for request in requests:
            response = await request.response()
            data = await response.text()
            try:
                parsed = json.loads(data)                
                currenttime = datetime.now().strftime("%B%d%Y_%I%M%p").lower()
                filename = f"{currenttime}.json"
                with open(filename, "w") as f:
                    json.dump(parsed, f, indent=2)
                webhook = "" # your discord webhook here
                payload = {
                    "file1": open(filename, "rb"),
                    "payload_json": json.dumps({"embeds": [{"title": "tweet data dumped"}]})
                }
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.post(webhook, data=payload) as resp:
                            print(f"webhook response: {resp.status}")
                    except aiohttp.ClientError as e:
                        print(f"error sending data to webhook: {e}")
            except json.JSONDecodeError:
                print("error could not parse data")
        await browser.close()
asyncio.run(main())
