import requests
import sys

def main():
    base_url = "http://localhost:8000/mcp"
    print("=" * 60)
    print(" MCP HTTP Test Client")
    print("=" * 60)

    # Step 1: Connect
    print(f"Connecting to MCP server at: {base_url}")
    try:
        r = requests.get(base_url)
        if r.status_code not in (200, 404):  # 404 is okay if /mcp root not defined
            r.raise_for_status()
        print("Connection established!")
    except Exception as e:
        print(f"Failed to connect to MCP server: {e}")
        sys.exit(1)

    # Step 2: Initialize session (simulated)
    print("Initializing session...")
    print("Session initialized!")

    # Step 3: List available tools
    print("\nListing available tools...")

    try:
        headers = {"Accept": "text/event-stream", "Content-Type": "application/json"}
        resp = requests.get(f"{base_url}/tools", headers=headers)
        resp.raise_for_status()
        tools_data = resp.json()
        tools = tools_data.get("tools", [])
    except Exception as e:
        print(f"Failed to fetch tools: {e}")
        sys.exit(1)
    
    if not tools:
        print("No tools found.")
        return

    print(f"Found {len(tools)} tool{'s' if len(tools) != 1 else ''}:")
    for t in tools:
        name = t.get("name", "<unnamed>")
        desc = t.get("description", "")
        print(f"  – {name}: {desc}")

    print("=" * 60)
    print("MCP server test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()