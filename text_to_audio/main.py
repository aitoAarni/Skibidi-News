# from engines import polly, gcp
from fastmcp import FastMCP

# import uuid

mcp = FastMCP("My MCP Server")


@mcp.tool
def synthesize(text: str) -> str:
    return "Synthesized"


# def main():
#    text = "Hey everyone on TikTok, I'm GCP and I'm here to bring you Skibidi News."
#    client = polly.PollyClient()
#    filename = f"{uuid.uuid4()}.mp3"
#    client.synthesize(text).save_as(filename)


if __name__ == "__main__":
    mcp.run()
