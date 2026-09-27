from playwright.async_api import async_playwright


class Client:
    WAIT_CONFIG = {
        "https://fundinghub.com.ua/grants": {
            "selector": 'a[href*="/grant/"]',
            "timeout": 30_000,
        },
        "https://fundinghub.com.ua/grant/": {
            "selector": "h2",
            "timeout": 30_000,
        },
        "https://grant-av.com.ua/grants/": {
            "selector": ".grant-card",
            "timeout": 15_000,
        },
    }

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=True
        )

        self.page = await self.browser.new_page()

    async def get_html(self, url: str) -> str:
        config = self._get_wait_config(url)

        await self.page.goto(
            url,
            wait_until="domcontentloaded",
        )

        await self.page.wait_for_selector(
            config["selector"],
            state="attached",
            timeout=config["timeout"],
        )

        return await self.page.content()

    async def close(self):
        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

    def _get_wait_config(self, url: str) -> dict:
        for domain, config in self.WAIT_CONFIG.items():
            if domain in url:
                return config

        raise ValueError(f"No wait config for URL: {url}")