import asyncio
import signal

#from sys import stderr
#from loguru import logger


from data.classes import WeaponGradeData, BrowserRequester
from data.payloads import HEADERS, BM_PAYLOAD, QP_PAYLOAD, BLUR_URL
from handlers.parse_module import bm_qp_binance_request, blur_processing
from telegram_bot.send_message import send_telegram_message 



    
exit_event = asyncio.Event()

# logger.add(
#     stderr,
#     format="<white>{time:HH:mm:ss}</white>"
#     " | <level>{level: <8}</level>"
#     " | <cyan>{line}</cyan>"
#     " - <white>{message}</white>",
# )

async def main() -> None:
    bm_base = WeaponGradeData("fusionist_bm.db")
    await bm_base.initialize_data()
    qp_base = WeaponGradeData("fusionist_qp.db")
    await qp_base.initialize_data()
    blur_requester = BrowserRequester()
    
    try:
        await blur_requester.initialize_browser()
        while not exit_event.is_set():
            union_data = {}
            browser_data = await blur_requester.browser_request(BLUR_URL)
            #print(browser_data)
            blur_data = await blur_processing(browser_data, qp_base)
            #print(blur_data)
            binance_bm_data = await bm_qp_binance_request(bm_base, HEADERS, BM_PAYLOAD)
            #print(binance_bm_data, '\n')

            binance_qp_data = await bm_qp_binance_request(qp_base, HEADERS, QP_PAYLOAD)
            #print(binance_qp_data, '\n')

            if binance_bm_data:
               union_data.update(binance_bm_data)
             
            if binance_qp_data:
                 union_data.update(binance_qp_data)

            if blur_data:
                union_data.update(blur_data)   

            #print(union_data)
            if union_data:
                await send_telegram_message(union_data)

            await asyncio.sleep(60)

    
    except Exception as e:
        print(f"Error in main: {e}")

    finally:
        await blur_requester.close_browser()
        

        

def signal_handler(signum, frame):
    global exit_event
    exit_event.set()
     
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    


