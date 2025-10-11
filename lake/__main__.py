import asyncio
import suitcase

from pathlib              import Path
from playwright.async_api import async_playwright

async def scrape(
                url: str 
        ) -> int:
        """__main__.scrape
        """

        async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                page    = await browser.new_page()
                
                await page.goto(url, wait_until="domcontentloaded")
                
                if(not input("") == ""):
                        await browser.close()
                        
                        return -1
 
                await suitcase.session.download(
                        await page.locator("a").evaluate_all(
                                suitcase.scripts.read("injection.js"), 
                                suitcase.config.load()["filters"]
                        ), 
                        Path("common"), 
                        verbose=True
                )
        
        return 0

async def main() -> int:
        """__main__.main
        """
        
        return 0

if __name__ == '__main__':
        asyncio.run(main())