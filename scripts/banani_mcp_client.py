import urllib.request
import json
import ssl
import sys
import time
import os

ENDPOINT = "https://app.banani.co/api/mcp/mcp"
API_KEY = "bnni_WFvLygMU9wGeQQD0QNOXX5GgrMakMHYw"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def do_mcp_call():
    # Attempting to initialize the MCP protocol and hit the tool
    # Let's see if we can just get the SSE URL
    req = urllib.request.Request(ENDPOINT, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "text/event-stream"
    })
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            for line in response:
                decoded = line.decode('utf-8').strip()
                if decoded.startswith("endpoint:"):
                    return decoded.split("endpoint:")[1].strip()
                print("SSE Line:", decoded)
                if len(decoded) > 100:
                    break
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

post_url = do_mcp_call()
print(f"POST URL from SSE: {post_url}")
