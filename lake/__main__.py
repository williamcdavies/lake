import asyncio
import suitcase
import tempfile
import zipfile

import geopandas as gpd

from pathlib              import Path
from playwright.async_api import async_playwright
from sqlalchemy           import create_engine

_COMMON_PATH = Path(Path(__file__).parent.parent / "common")

async def scrape(
                url: str 
        ) -> int:
        """__main__.scrape
        """

        async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                page    = await browser.new_page()
                
                await page.goto(url, wait_until="domcontentloaded")
                
                if(not input("[y|N]: ") == "y"):
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

def main() -> int:
        """__main__.main
        """

        engine     = create_engine("postgresql://williamchuter-davies@localhost:5432/spatial")
        table_dict = {
                "hms_fire": "hms_fires",
                "hms_smoke": "hms_smokes"
        }

        for path in _COMMON_PATH.glob("*.zip"):
                try:
                        with zipfile.ZipFile(path, 'r') as zf:
                                shp_files = [f for f in zf.namelist() if f.endswith(".shp")]
                        
                                if not shp_files:
                                        continue
                                
                                shp_file = shp_files[0]
                                
                                with tempfile.TemporaryDirectory(dir=_COMMON_PATH) as buffer:
                                        zf.extractall(buffer)

                                        stem  = Path(shp_file).stem.lower()
                                        table = next((v for k, v in table_dict.items() if k in stem), None)

                                        if not table:
                                                continue
                                        
                                        try:
                                                gdf = gpd.read_file(Path(buffer) / shp_file, on_invalid="fix")
                                        
                                        except Exception as e:
                                                print(f"Insertion of {shp_file} from {buffer} to {table}: Failed with {e}")
                                                
                                                continue

                                        if table:
                                                print(f"Insertion of {shp_file} from {buffer} to {table}: Success")
                                                gdf.to_postgis(table, engine, if_exists="append", index=False, chunksize=1024)
               
                except zipfile.BadZipFile as e:
                        print(f"Open {path} as ZipFile: Failed with {e}")
                        
                        continue
        
        return 0

if __name__ == '__main__':
        main()