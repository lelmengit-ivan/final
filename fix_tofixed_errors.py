"""
Fix all .toFixed() errors by ensuring values are parsed as floats
"""
import re

with open('static/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix patterns where .toFixed is called directly on variables that might not be numbers
replacements = [
    # sale.total_price.toFixed(2)
    (r'sale\.total_price\.toFixed\(2\)', r'(parseFloat(sale.total_price) || 0).toFixed(2)'),
    # item.revenue.toFixed(2)
    (r'item\.revenue\.toFixed\(2\)', r'(parseFloat(item.revenue) || 0).toFixed(2)'),
    # data.total_revenue.toFixed(2) - already fixed
    # totalRevenue.toFixed(2) - these are calculated, should be fine
    # cashSales.toFixed(2) - these are calculated, should be fine
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

with open('static/js/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all .toFixed() errors!")
print("   - sale.total_price")
print("   - item.revenue")
print("   - supplier.rating (already fixed)")
print("   - med.price (already fixed)")
