"""
Add error handling to all chart creation functions
"""

with open('static/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add try-catch and logging to chart functions
chart_functions = [
    'createTopMedicinesChart',
    'createInventoryChart', 
    'createCategoryChart',
    'createRevenueChart',
    'createPredictionChart'
]

for func_name in chart_functions:
    # Find the function
    start_marker = f'function {func_name}('
    if start_marker in content:
        # Find where function starts
        func_start = content.find(start_marker)
        # Find the opening brace
        brace_start = content.find('{', func_start)
        # Find the closing brace (simplified - assumes no nested functions)
        brace_count = 1
        pos = brace_start + 1
        while brace_count > 0 and pos < len(content):
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
            pos += 1
        
        # Extract function body
        func_body = content[brace_start+1:pos-1]
        
        # Wrap in try-catch if not already wrapped
        if 'try {' not in func_body[:20]:
            new_body = f'''{{
    try {{
{func_body}
        console.log('{func_name} created');
    }} catch (error) {{
        console.error('Error in {func_name}:', error);
    }}
}}'''
            # Replace in content
            content = content[:brace_start] + new_body + content[pos:]
            print(f'✅ Added error handling to {func_name}')

with open('static/js/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('\n✅ All chart functions updated with error handling!')
