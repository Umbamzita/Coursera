from bs4 import BeautifulSoup
from decimal import Decimal
import requests


def value(soup):
    return Decimal(soup.find_next_sibling('Value').string.replace(',','.'))

def nominal(soup):
    return Decimal(soup.find_next_sibling('Nominal').string.replace(',','.'))
    

def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp',
                            params = {
                                    'date_req' : date
                                    })      # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')
    if cur_from != 'RUR':
        soup_from = soup.find('CharCode', text=cur_from)
        value_from=value(soup_from)
        nominal_from=nominal(soup_from)
    else:
        value_from=Decimal('1')
        nominal_from=1
    
    
    soup_to = soup.find('CharCode', text=cur_to)
    value_to = value(soup_to)
    nominal_to = nominal(soup_to)
    
    
    result=Decimal(value_from/nominal_from*amount)/(value_to/nominal_to)
    return result.quantize(Decimal("1.0000"))