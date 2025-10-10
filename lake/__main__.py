import asyncio
import suitcase

from pathlib              import Path
from playwright.async_api import async_playwright

async def main() -> int:
        """suitcase.main
        """
        
        async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                page    = await browser.new_page()
                
                await page.goto("https://www.ospo.noaa.gov/products/land/hms.html#data", wait_until="domcontentloaded")

                handover = input("__main__.py, handover, [y/N]% ") == "y"
                
                if(not handover):
                        await browser.close()
                        
                        return -1
 
                await suitcase.session.download(await page.locator("a").evaluate_all(suitcase.scripts.read("injection.js"), suitcase.config.load()["filters"]), Path("common"), verbose=True)
                await browser.close()
        
        return 0

if __name__ == '__main__':
        asyncio.run(main())