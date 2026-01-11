with open('app/__init__.py', 'r') as f:
    lines = f.readlines()

# Find the line with @app.route('/api/health'...) and find the corresponding health function
health_endpoint_start = None
health_endpoint_end = None
for i, line in enumerate(lines):
    if "@app.route('/api/health'" in line:
        health_endpoint_start = i
    # The function ends when we see a return statement or a new decorator
    if health_endpoint_start is not None and health_endpoint_end is None:
        if i > health_endpoint_start and (line.startswith('@') or (i < len(lines) - 1 and lines[i+1].startswith('@'))):
            health_endpoint_end = i
            break
        if 'return' in line and '200' in line:
            health_endpoint_end = i + 1
            break

if health_endpoint_end:
    # Insert the new health endpoint
    new_code = '''\n# Health check endpoint without API prefix\n@app.route('/health', methods=['GET'])\ndef health_simple() -> Tuple[Dict[str, Any], int]:\n    return {'status': 'ok'}, 200\n'''
    lines.insert(health_endpoint_end, new_code)
    with open('app/__init__.py', 'w') as f:
        f.writelines(lines)
    print('✅ /health endpoint added at line', health_endpoint_end)
else:
    print('❌ Could not find /api/health endpoint')
