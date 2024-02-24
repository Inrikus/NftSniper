BM_PRICES = {
    ('Common', '1'): 1050,
    ('Common', '2'): 1150, 
    ('Common', '3'): 1250,
    ('Elite', '1'): 1300,
    ('Elite', '2'): 1450, 
    ('Elite', '3'): 1600,
    ('Epic', '1'): 2400,
    ('Epic', '2'): 2700,
    ('Epic', '3'): 3000,
    ('Epic', '4'): 3500,
    ('Legend', '1'): 5000,
    ('Legend', '2'): 5500,
    ('Legend', '3'): 6000,
    ('Legend', '4'): 7000,
}
QP_PRICES = {
    ('Elite', '2'): 0.8,
    ('Elite', '3'): 1,
    ('Epic', '3'): 2,
    ('Epic', '4'): 2.3,
    ('Legend', '3'): 4,
    ('Legend', '4'): 6,
}

async def check_bm_prices(result_dict) -> dict: 
    filtered_data = {
        title_id: item for title_id, item in result_dict.items()
        if ( 
            #item.get('GRADE') is not None and
            #item.get('Weapons') is not None and
            int(item.get('Price', 0)) <= int(BM_PRICES.get((item.get('GRADE', ''), item.get('Weapons', '')), 0))
        )
    }
    #print("Filtered BM data:\n", filtered_data, '\n')
    return filtered_data     

async def check_qp_prices(result_dict) -> dict:
    filtered_data = {
        title_id: item for title_id, item in result_dict.items()
        if ( 
            #item.get('GRADE') is not None and
            #item.get('Weapons') is not None and
            float(item.get('Price', 0)) <= float(QP_PRICES.get((item.get('GRADE', ''), item.get('Weapons', '')), 0))
        )
    }
    #print("Filtered QP data:", filtered_data)
    return filtered_data     
