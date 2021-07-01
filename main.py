import calendar
import requests
from datetime import datetime, timedelta
import csv
import time


def current_date():
    return str(datetime.now().date())[0:7] + '-01'


def generator_name(name_of_table):
    now = calendar.month_name[int(current_date()[5:7])][0:3]
    return 'WB_' + name_of_table + '_' + current_date()[0:4] + '-' + now + '.csv'


def request_deliveries():
    url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/incomes?' \
          f'dateFrom={current_date()}T21%3A00%3A00.000Z&key={api_key}'
    response = requests.get(url)
    column = ['income', 'Number', 'Date', 'lastChangeDate', 'SupplierArticle', 'TechSize', 'Barcode', 'Quantity',
              'totalPrice', 'dateClose', 'warehouseName', 'mid', 'status']
    with open(f'{path}deliveries\{generator_name("deliveries")}', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column)
        for row in range(len(response.json())):
            writer.writerow(response.json()[row].values())


def request_warehouse():
    url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?' \
          f'dateFrom={current_date()}T21%3A00%3A00.000Z&key={api_key}'
    response = requests.get(url)
    column = ['lastChangeDate', 'supplierArticle', 'techSize', 'barcode', 'quantity',
              'isSupply', 'isRealization', 'quantityFull', 'quantityNotInOrders', 'warehouseName',
              'inWayToClient', 'inWayFromClient', 'nmId', 'subject', 'category',
              'daysOnSite', 'brand', 'SCCode']
    with open(f'{path}warehouse\{generator_name("warehouse")}', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column)
        for row in range(len(response.json())):
            temp = response.json()[row]
            [temp.pop(k) for k in ['Price', 'Discount']]
            writer.writerow(temp.values())


def request_orders():
    url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders?' \
          f'dateFrom={current_date()}T21%3A00%3A00.000Z&flag=0&key={api_key}'
    response = requests.get(url)
    column = ['number', 'date', 'lastChangeDate', 'supplierArticle', 'techSize', 'barcode', 'quantity',
              'totalPrice', 'discountPercent', 'warehouseName', 'oblast', 'incomeID', 'odid', 'nmId',
              'subject', 'category', 'brand', 'isCancel', 'cancel_dt']
    with open(f'{path}orders\{generator_name("orders")}', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column)
        for row in range(len(response.json())):
            temp = response.json()[row]
            temp.pop('gNumber')
            writer.writerow(temp.values())


def request_sales():
    url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/sales?' \
          f'dateFrom={current_date()}T21:00:00.000Z&key={api_key}'
    response = requests.get(url)
    column = ['number', 'date', 'lastChangeDate', 'supplierArticle', 'techSize', 'barcode', 'quantity',
              'totalPrice', 'discountPercent', 'isSupply', 'isRealization', 'orderId', 'promoCodeDiscount',
              'warehouseName', 'countryName', 'oblastOkrugName', 'regionName', 'incomeID', 'saleID',
              'odid', 'spp', 'forpay', 'finished_price', 'nmId', 'subject', 'category',
              'brand', 'IsStorno']
    with open(f'{path}sales\{generator_name("sales")}', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column)
        for row in range(len(response.json())):
            temp = response.json()[row]
            [temp.pop(k) for k in ['priceWithDisc', 'gNumber']]
            writer.writerow(temp.values())


def request_salesreports():
    now_date = str(datetime.now().date())
    url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/reportDetailByPeriod?' \
          f'dateFrom={current_date()}&key={api_key}&limit=1000&rrdid=0&dateto={now_date}'
    response = requests.get(url)
    column = ['realizationreport_id', 'suppliercontract_code', 'rrd_id', 'gi_id', 'subject_name',
              'NM_id', 'brand_name', 'sa_name', 'ts_name', 'barcode', 'doc_type_name', 'quantity',
              'nds', 'cost_amount', 'retail_price', 'retail_amount', 'retail_commission', 'sale_percent',
              'commission_percent', 'customer_reward', 'supplier_reward', 'office_name', 'supplier_oper_name',
              'order_dt', 'sale_dt', 'rr_dt', 'shk_id', 'retail_price_withdisc_rub', 'for_pay', 'for_pay_nds',
              'delivery_amount', 'return_amount', 'delivery_rub', 'gi_box_type_name',
              'product_discount_for_report', 'supplier_promo', 'supplier_spp']
    with open(f'{path}salesreports\{generator_name("salesreports")}', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column)
        for row in range(len(response.json())):
            temp = response.json()[row]
            temp.pop('rid')
            writer.writerow(temp.values())


if __name__ == '__main__':

    global api_key
    api_key = '----'
    global path
    path = '----'

    year = int(str(datetime.now().date())[0:4])
    month = int(str(datetime.now().date())[5:7])
    day = int(str(datetime.now().date())[8:10])

    next_start_morning = datetime(year, month, day, 8, 0, 0)
    if datetime(year, month, day, 16, 0, 0) > datetime.now():
        next_start_evening = datetime(year, month, day, 16, 0, 0)
    else:
        next_start_evening = datetime(year, month, day, 16, 0, 0) + timedelta(1)
    while True:
        dtn = datetime.now()
        if dtn >= next_start_morning or dtn >= next_start_evening:
            if dtn >= next_start_morning:
                next_start_morning += timedelta(1)
                while True:
                    try:
                        request_deliveries()
                        time.sleep(2)
                        request_sales()
                        time.sleep(2)
                        request_warehouse()
                        time.sleep(2)
                        request_orders()
                        time.sleep(2)
                        request_salesreports()
                        break
                    except:
                        time.sleep(300)
            else:
                next_start_evening += timedelta(1)
                while True:
                    try:
                        request_deliveries()
                        time.sleep(2)
                        request_sales()
                        time.sleep(2)
                        request_warehouse()
                        time.sleep(2)
                        request_orders()
                        time.sleep(2)
                        request_salesreports()
                        break
                    except:
                        time.sleep(300)
        time_delta = min(next_start_morning, next_start_evening) - dtn
        if 0 >= (min(next_start_morning, next_start_evening) - dtn).seconds <= 60:
            continue
        time.sleep(time_delta.seconds)
