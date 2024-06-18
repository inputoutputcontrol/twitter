import asyncio
import json
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
        await page.goto("https://x.com/") # replace with the user you want to export from
        await page.wait_for_timeout(1000)
        requests = [request for request in xhrrequests if "UserTweets" in request.url]
        for request in requests:
            response = await request.response()
            data = await response.text()
            try:
                parsed = json.loads(data)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("error could not parse data")
        await browser.close()
asyncio.run(main())
