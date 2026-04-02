import json
from bs4 import BeautifulSoup

def to_float(val):
    if val is None:
        return 1.0
    return float(val.replace(',', '.'))

def parse_items(html):
    soup = BeautifulSoup(html, 'html.parser')
    seen = set()
    items = []
    for span in soup.find_all('span', attrs={'data-art-description': True}):
        key = (span.get('data-art-description'), span.get('data-unit-price'))
        if key in seen:
            continue
        seen.add(key)
        quantity = to_float(span.get('data-art-quantity'))
        unit_price = to_float(span.get('data-unit-price'))
        items.append({
            'name': span.get('data-art-description'),
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': round(quantity * unit_price, 2),
            'tax_type': span.get('data-tax-type'),
        })
    return items

with open('lidl_receipts.json') as f:
    raw = json.load(f)

receipts = []
for r in raw:
    ticket = r['ticket']
    html = ticket.get('htmlPrintedReceipt', '')
    items = parse_items(html)
    if not items:
        continue
    total = round(sum(i['total_price'] for i in items), 2)
    receipts.append({
        'id': ticket['id'],
        'date': ticket['date'][:10],
        'store': ticket['store']['name'],
        'address': ticket['store']['address'],
        'total': total,
        'items': items,
    })

receipts.sort(key=lambda x: x['date'])

with open('lidl_clean.json', 'w', encoding='utf-8') as f:
    json.dump(receipts, f, ensure_ascii=False, indent=2)

print(f"Processed {len(receipts)} receipts")
print(f"Date range: {receipts[0]['date']} to {receipts[-1]['date']}")
print(f"Total spent: €{sum(r['total'] for r in receipts):.2f}")
print(f"Total items purchased: {sum(len(r['items']) for r in receipts)}")
