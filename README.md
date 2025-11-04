# PyAutoGUI MCP Server

This repository contains a PyAutoGUI MCP (Model Context Protocol) server. It exposes the functionality of the PyAutoGUI library as a set of tools that can be used by a client. This allows for remote control of the mouse and keyboard, as well as screen capture and other GUI automation tasks.

## Running the server

To run the server, execute the following command:

```bash
python pyautogui-mcp.py
```

```bash
{
  "mcpServers": {
      "pyautogui": {
        "command": "python",
        "args": [
          "C:\\Users\\deept\\Desktop\\Claude\\pyautogui-mcp.py"
        ],
        "env": {}
      }
  }
}
```
