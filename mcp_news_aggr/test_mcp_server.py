import requests
import sys
import json

def main():
    base_url = "http://localhost:8000/mcp"
    print("=" * 60)
    print(" MCP Streamable HTTP Test Client")
    print("=" * 60)

    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json"
    }

    # JSON-RPC payload to call your get_summary tool
    payload = {
        "jsonrpc": "2.0",
        "method": "get_summary",
        "params": {},
        "id": 1
    }

    try:
        resp = requests.post(base_url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        summary = data.get("result", {}).get("summary", "No summary returned")
        print("\n=== News Summary ===\n")
        print(summary)

    except Exception as e:
        print(f"Failed to connect or call MCP server: {e}")
        sys.exit(1)

    print("\n============================================================")
    print("MCP server test completed successfully!")
    print("============================================================")

if __name__ == "__main__":
    main()
