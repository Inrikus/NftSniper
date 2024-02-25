import re
import aiohttp
import sys
#import asyncio

from handlers.check_prices import check_bm_prices, check_qp_prices

async def blur_processing(data, weapon_grade_data):
    nft_list = None
    result_dict = {}    
    
    if data.get('tokens'):
        nft_list = data['tokens']
    
    if nft_list:
        for nft in nft_list:
            token_id = int(nft.get('tokenId', ''))
            link = f"https://blur.io/asset/0xd396e2018b67446b134c30a89166487a8b2abd2e/{token_id}"
            price = nft['price']['amount']       
            weapons_value, grade_value = weapon_grade_data.get_weapons_and_grade_by_tokenid(token_id)
            
            result_dict[token_id] = {
                "Link": link,
                "GRADE": grade_value,
                "Weapons": weapons_value,
                "Price": price,
            }
        #print(await check_qp_prices(result_dict))
        return await check_qp_prices(result_dict)

    else: 
        print("Empty data-rows/No NFTs")
        return None

#
#async def browser_request(url, weapon_grade_data):   try:
#        async with async_playwright() as p:
#            browser = await p.chromium.launch(headless=False)
#            context = await browser.new_context()
#            page = await context.new_page()
#            response = await page.goto(url)
#            if response: 
#                print(f"Browser Response status: {response.status}")
#                data = await response.json()
#                return data
#                #return await blur_processing(data, weapon_grade_data)
#            else: 
#                print('Empty response')
#                return None
#    
#    except Exception as e:
#        print(f"SomeError playwright {e}")
#        return None       
#    

async def binance_processing(data, weapon_grade_data):
    nft_list = None
    result_dict = {}
    if data.get('data') and data['data'].get('rows'):
        #print(data['data'].get('rows'))
        nft_list = data['data']['rows']  
    
    if nft_list:
        collection_name = nft_list[0].get('collectionName', '')
        for nft in nft_list:
            id = nft['nftInfoId'] #Create Binance-Link
            link = f"https://www.binance.com/ru/nft/item/{id}"
            currency = nft['currency']
            
            if 'title' in nft:  
                title = nft.get('title', '')
                regex_match = re.search(r'\d+', title)   # Получение числовой части из поля "title"
                token_id = int(regex_match.group()) if regex_match else None
                weapons_value, grade_value = weapon_grade_data.get_weapons_and_grade_by_tokenid(token_id) # Получение данных Weapons и GRADE из объекта WeaponGradeData
                price = nft['amount']
                
                if currency == 'BNB':
                    #price = await get_binance_bnb_price()
                    price = float(price) * 350                                  
                
                result_dict[token_id] = {
                    'Link': link,
                    'GRADE': grade_value,
                    'Weapons': weapons_value,
                    'Price': price,
                }
            else: 
                print("Empty title")
                return None
        
        #print("All_In_Mechs:", result_dict)
        if collection_name == 'Fusionist - Bi·Mech':  
            return await check_bm_prices(result_dict)
        elif collection_name == 'Fusionist - Quartan Primes': 
            return await check_qp_prices(result_dict)
        else:
            print("Incorrect NFT-Type")    
            return None
    else: 
        print("Empty data-rows/No NFTs")
        return None


async def bm_qp_binance_request(weapon_grade_data, headers, payload) :
    url = "https://www.binance.com/bapi/nft/v1/friendly/nft/asset/market/asset-list"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                print(f"Binance Response status: {response.status}")
                data = await response.json()
                filtered_data = await binance_processing(data, weapon_grade_data)
                return filtered_data
                
    except aiohttp.ClientConnectionError as connection_error:
        print(f"VPN ERROR: {connection_error}")
        return None
        #sys.exit(1)
    
    except Exception as e:
        print(f"GLOBAL ERROR: {e}")
        sys.exit(1)

#
#async def get_binance_bnb_price():
#    url = "https://api.binance.com/api/v3/ticker/price"
#    params = {"symbol": "BNBUSDT"}  # Символ BNB к USDT
#
#    try:
#        async with aiohttp.ClientSession() as session:
#            async with session.get(url, params=params) as response:
#                data = await response.json()
#
#                if "price" in data:
#                    bnb_price = data["price"]
#                    print(f"Текущая цена BNB: {bnb_price} USDT\n")
#                    return bnb_price
#                else:
#                    print("Не удалось получить цену BNB.")
#                    return None
#    
#    except aiohttp.ClientConnectionError as connection_error:
#        print(f"VPN ERROR: {connection_error}")
#        return 300
#