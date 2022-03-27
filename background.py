from app import Car, Dealer, create_car, create_dealer
import vin_generator
import requests
import base64
import PyPDF2
import io
from pdfminer.high_level import extract_text

def scrape_vin(vin):
    SOLD_TO = "SOLD TO:"
    SHIPPED_TO = "SHIPPED TO:"
    MODEL = "MODEL:"
    ENGINE = "ENGINE:"
    PORT_OF_ENTRY = "PORT OF ENTRY:"
    EXT_COLOR = "EXTERIOR COLOR:"
    INT_COLOR = "INTERIOR/SEAT COLOR:"
    TRANSPORT = "TRANSPORT:"
    ACCESSORY = "ACCESSORY WEIGHT:"
    PRICE = "Total Price :$"
    GOVERNMENT = "GOVERNMENT 5-STAR SAFETY RATINGS"
    url = f'https://hyundai-sticker.dealerfire.com/new/{vin}'
    r = requests.get(url)
    if r.status_code != 200:
        return None, None
    f = io.BytesIO(base64.b64decode(r.content))
    p = PyPDF2.PdfFileReader(f)
    pdf_text = p.getPage(0).extractText()
    pdf_text2 = extract_text(f)
    start = pdf_text2.index(SOLD_TO) + len(SOLD_TO) + 1
    end = pdf_text2.index(SHIPPED_TO)
    sold_to = pdf_text2[start:end].strip()
    start = pdf_text.index(SOLD_TO) + len(SOLD_TO)
    end = pdf_text.index(SHIPPED_TO)
    if sold_to.split('\n')[0] != pdf_text[start:end]:
        sold_to = pdf_text[start:end] + '\n' + sold_to

    start = pdf_text2.index(SHIPPED_TO) + len(SHIPPED_TO) + 1
    end = pdf_text2.index(GOVERNMENT)
    shipped_to = pdf_text2[start:end].strip()

    start = pdf_text.index(MODEL) + len(MODEL)
    end = pdf_text.index(ENGINE)
    model = pdf_text[start:end]

    start = pdf_text.index(ENGINE) + len(ENGINE)
    end = pdf_text.index(PORT_OF_ENTRY)
    engine = pdf_text[start:end]

    start = pdf_text.index(PORT_OF_ENTRY) + len(PORT_OF_ENTRY)
    end = pdf_text.index(EXT_COLOR)
    port_of_entry = pdf_text[start:end]

    start = pdf_text.index(EXT_COLOR) + len(EXT_COLOR)
    end = pdf_text.index(INT_COLOR)
    ext_color = pdf_text[start:end]

    start = pdf_text.index(INT_COLOR) + len(INT_COLOR)
    end = pdf_text.index(TRANSPORT)
    int_color = pdf_text[start:end]

    start = pdf_text.index(TRANSPORT) + len(TRANSPORT)
    end = pdf_text.index(ACCESSORY)
    transport = pdf_text[start:end]

    start = pdf_text.index(PRICE) + len(PRICE)
    end = pdf_text.find(".", start)
    price = int(pdf_text[start:end].replace(',', ''))
    
    car = Car(vin, int(vin[-6:]), model, engine, port_of_entry, ext_color, int_color, transport, sold_to.split("\n")[0], shipped_to.split("\n")[0], price)
    dealer = Dealer(sold_to.split('\n')[0], '\n'.join(sold_to.split('\n')[1:]))
    return car, dealer

serial = 0
consecutive_fails = 0
while True:
    if serial > 999999:
        serial = 0
        consecutive_fails = 0
    car, dealer = scrape_vin(vin_generator.get_vin_from_serial(serial))
    if dealer is not None:
        create_dealer(dealer)
    if car is not None:
        create_car(car)
        print(str(serial) + " success.")
    if (car is None) and (dealer is None):
        consecutive_fails += 1
        print(str(serial) + " fail.")
    else:
        consecutive_fails = 0
    if consecutive_fails >= 1000:
        serial = 0
        consecutive_fails = 0
    else:
        serial += 1

    
