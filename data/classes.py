import aiosqlite
import sys
from playwright.async_api import async_playwright

class BrowserRequester:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    async def initialize_browser(self):
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
    
    async def close_browser(self):
        if self.playwright:
            await self.playwright.stop()
        
    async def browser_request(self, url):
        try:
            if self.page:
                response = await self.page.goto(url)
                if response:
                    print(f"Browser Response status: {response.status}")
                    data = await response.json()
                    return data
                else:
                    print('Empty response')
                    return None
            else:
                print('Browser or page not initialized')
                return None

        except Exception as e:
            print(f"SomeError playwright {e}")
            return None


class WeaponGradeData:
    def __init__(self, db_file: str):
        self._db_file = db_file
        self._weapons_grade_data = {}

    async def initialize_data(self):
        # Инициализация данных из базы данных
        try:
            async with aiosqlite.connect(self._db_file) as conn:
                cursor = await conn.cursor()
                await cursor.execute("SELECT tokenid, Weapons, GRADE FROM fusionist_data")
                rows = await cursor.fetchall()
                
                # Заполнение данных в виде кортежей (tokenid: (Weapons, GRADE))
                self._weapons_grade_data = {row[0]: (row[1], row[2]) for row in rows}
        
        except aiosqlite.OperationalError as e:
            print(f"OperationalError initializing data: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"SystemError: {e}")
            sys.exit(1)
    
    def get_weapons_and_grade_by_tokenid(self, tokenid: int):
        # Поиск данных по tokenid
        return self._weapons_grade_data.get(tokenid, (None, None))

# Использование:
# data = WeaponGradeData.get_data_by_tokenid(123)  # Получение данных для tokenid=123
# weapons_value = data["Weapons"]
# grade_value = data["GRADE"]