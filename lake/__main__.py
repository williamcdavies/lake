import asyncio
import re
import suitcase
import tempfile
import zipfile

import geopandas as gpd

from pathlib              import Path
from playwright.async_api import async_playwright
from sqlalchemy           import create_engine

_COMMON_PATH = Path(Path(__file__).parent.parent / "common")

# async def scrape(
#                 url: str 
#         ) -> int:
#         """__main__.scrape
#         """

#         async with async_playwright() as p:
#                 browser = await p.chromium.launch(headless=False)
#                 page    = await browser.new_page()
                
#                 await page.goto(url, wait_until="domcontentloaded")
                
#                 if(not input("[y|N]: ") == "y"):
#                         await browser.close()
                        
#                         return -1
 
#                 await suitcase.session.download(
#                         await page.locator("a").evaluate_all(
#                                 suitcase.scripts.read("injection.js"), 
#                                 suitcase.config.load()["filters"]
#                         ), 
#                         Path("common"), 
#                         verbose=True
#                 )
        
#         return 0

def main() -> int:
        """__main__.main
        """
    
        engine = create_engine("postgresql://williamchuter-davies@localhost:5432/spatial")

        # FOR HydroLAKES_[points | polys]_v10_shp ZipFile(s)

        # gdf = gpd.read_file(Path(_COMMON_PATH / "HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10.shp"), on_invalid="fix")
        # gdf.to_postgis("lakes_polys", engine, if_exists="append", index=False, chunksize=1024)

        # FOR HM_FIRE20XXMMDD ZipFile(s)

        # table_dict = {
        #         "hms_fire": "hms_fires",
        #         "hms_smoke": "hms_smokes"
        # }

        # for path in sorted(_COMMON_PATH.glob("*.zip")):
        #         try:
        #                 with zipfile.ZipFile(path, 'r') as zf:
        #                         shp_files = [f for f in zf.namelist() if f.endswith(".shp")]
                        
        #                         if not shp_files:
        #                                 continue

        #                         shp_file = shp_files[0]

        #                         with tempfile.TemporaryDirectory(dir=_COMMON_PATH) as buffer:
        #                                 zf.extractall(buffer)

        #                                 stem = Path(shp_file).stem.lower()
        #                                 key  = next((k for k in table_dict if k in stem), None)
                        
        #                                 if not key:
        #                                         continue

        #                                 year  = re.search(r"(\d{4})", stem)
        #                                 table = f"{table_dict[key]}{year.group(1) if year else "unknown"}"

        #                                 try:
        #                                         gdf = gpd.read_file(Path(buffer) / shp_file, on_invalid="fix")
                                        
        #                                 except Exception as e:
        #                                         print(f"Insertion of {shp_file} from {buffer} to {table}: Failed with {e}")
                                                
        #                                         continue

        #                                 print(f"Insertion of {shp_file} from {buffer} to {table}: Success")
        #                                 gdf.to_postgis(table, engine, if_exists="append", index=False, chunksize=1024)

        #         except zipfile.BadZipFile as e:
        #         print(f"Attempt to open {path} as ZipFile: Failed with {e}")
                
        #         continue

        return 0

if __name__ == '__main__':
        main()