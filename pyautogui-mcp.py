#!/usr/bin/env python3
"""
PyAutoGUI MCP Server

An MCP (Model Context Protocol) server that provides PyAutoGUI automation capabilities
through a standardized interface.

Available tools:
- Mouse control: click, move, drag, scroll
- Keyboard input: type, press, hotkey
- Screen capture: screenshot, locate images
- Window management: get active window, list windows
- Position tracking: get mouse position, pixel colors
- User prompts: alert, confirm, prompt, password
"""

import pyautogui
from mcp.server.fastmcp import FastMCP
from typing import Any, Optional, List, Dict
import os
import io
import base64
import ast

# Initialize the FastMCP server
server = FastMCP(
    name="PyAutoGUI",
    instructions="""This server provides PyAutoGUI automation capabilities.
PyAutoGUI lets your Python scripts control the mouse and keyboard to automate
interactions with other applications.

Key features:
- Mouse control: move, click, drag, scroll
- Keyboard input: type text, press keys, key combinations
- Screen capture: take screenshots, locate images on screen
- Window management: find windows, get window titles
- Position tracking: get mouse position, check pixel colors
- User interaction: show alerts, prompts, confirmations

WARNING: This will control your computer! Always test carefully and have a failsafe.
Move mouse to a corner of the screen or press Ctrl+C to abort if needed.""",
    debug=False,
)

# Configure PyAutoGUI
pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
pyautogui.PAUSE = 0.1  # Small pause between actions (0.1 seconds)

# ====================
# MOUSE CONTROL TOOLS
# ====================

@server.tool()
def move_mouse(x: int, y: int, duration: float = 0.0) -> Dict[str, Any]:
    """Move mouse cursor to specified coordinates.

    Args:
        x: X coordinate (pixels from left)
        y: Y coordinate (pixels from top)
        duration: Time to take for the move (seconds, default 0 for instant)

    Returns:
        Dictionary with x, y coordinates
    """
    try:
        pyautogui.moveTo(x, y, duration=duration)
        return {"x": x, "y": y, "message": f"Mouse moved to ({x}, {y})"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def move_mouse_relative(dx: int, dy: int, duration: float = 0.0) -> Dict[str, Any]:
    """Move mouse cursor by a relative amount.

    Args:
        dx: Change in X (pixels, positive = right, negative = left)
        dy: Change in Y (pixels, positive = down, negative = up)
        duration: Time to take for the move (seconds)

    Returns:
        Dictionary with dx, dy values
    """
    try:
        pyautogui.moveRel(dx, dy, duration=duration)
        return {"dx": dx, "dy": dy, "message": f"Mouse moved relative by ({dx}, {dy})"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def click(
    x: Optional[int] = None,
    y: Optional[int] = None,
    clicks: int = 1,
    interval: float = 0.0,
    button: str = "left"
) -> Dict[str, Any]:
    """Click at current position or specified coordinates.

    Args:
        x: X coordinate (optional, uses current position if None)
        y: Y coordinate (optional, uses current position if None)
        clicks: Number of clicks (default 1)
        interval: Time between clicks in seconds (default 0)
        button: Mouse button ('left', 'middle', 'right', default 'left')

    Returns:
        Dictionary with click details
    """
    try:
        pyautogui.click(x=x, y=y, clicks=clicks, interval=interval, button=button)
        click_location = f"at ({x}, {y})" if x is not None and y is not None else "at current mouse position"
        return {
            "x": x,
            "y": y,
            "clicks": clicks,
            "button": button,
            "message": f"Clicked {button} button {clicks} time(s) {click_location}"
        }
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def double_click(x: Optional[int] = None, y: Optional[int] = None, button: str = "left") -> Dict[str, Any]:
    """Double-click at current position or specified coordinates.

    Args:
        x: X coordinate (optional)
        y: Y coordinate (optional)
        button: Mouse button ('left', 'middle', 'right')

    Returns:
        Dictionary with click details
    """
    try:
        pyautogui.doubleClick(x=x, y=y, button=button)
        return {"x": x, "y": y, "button": button, "message": f"Double-clicked {button} button"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def right_click(x: Optional[int] = None, y: Optional[int] = None) -> Dict[str, Any]:
    """Right-click at current position or specified coordinates.

    Args:
        x: X coordinate (optional)
        y: Y coordinate (optional)

    Returns:
        Dictionary with click details
    """
    try:
        pyautogui.rightClick(x=x, y=y)
        return {"x": x, "y": y, "message": "Right-clicked"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def drag_to(x: int, y: int, duration: float = 0.0, button: str = "left") -> Dict[str, Any]:
    """Drag mouse from current position to specified coordinates.

    Args:
        x: X coordinate to drag to
        y: Y coordinate to drag to
        duration: Time for drag (seconds)
        button: Mouse button to hold

    Returns:
        Dictionary with destination coordinates
    """
    try:
        pyautogui.dragTo(x, y, duration=duration, button=button)
        return {"x": x, "y": y, "duration": duration, "message": f"Dragged to ({x}, {y})"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def drag_relative(dx: int, dy: int, duration: float = 0.0, button: str = "left") -> Dict[str, Any]:
    """Drag mouse by a relative amount from current position.

    Args:
        dx: Change in X (pixels)
        dy: Change in Y (pixels)
        duration: Time for drag (seconds)
        button: Mouse button to hold

    Returns:
        Dictionary with relative movement
    """
    try:
        pyautogui.dragRel(dx, dy, duration=duration, button=button)
        return {"dx": dx, "dy": dy, "message": f"Dragged relative by ({dx}, {dy})"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def scroll(clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> Dict[str, Any]:
    """Scroll mouse wheel.

    Args:
        clicks: Number of scroll clicks (positive = up, negative = down)
        x: X coordinate to scroll at (optional)
        y: Y coordinate to scroll at (optional)

    Returns:
        Dictionary with scroll details
    """
    try:
        pyautogui.scroll(clicks, x=x, y=y)
        return {"clicks": clicks, "x": x, "y": y, "message": f"Scrolled {clicks} clicks"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def get_mouse_position() -> Dict[str, int]:
    """Get current mouse cursor position.

    Returns:
        Dictionary with x, y coordinates
    """
    try:
        x, y = pyautogui.position()
        return {"x": x, "y": y}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


# ====================
# KEYBOARD TOOLS
# ====================

@server.tool()
def type_text(text: str, interval: float = 0.0) -> Dict[str, str]:
    """Type text using keyboard.

    Args:
        text: Text to type
        interval: Time between keystrokes (seconds)

    Returns:
        Dictionary with status
    """
    try:
        pyautogui.write(text, interval=interval)
        return {"text": text, "message": f"Typed text: {text[:50]}..."}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def press_key(key: str) -> Dict[str, str]:
    """Press and release a key.

    Args:
        key: Key to press (e.g., 'enter', 'esc', 'space', 'a', '1', 'f1')

    Returns:
        Dictionary with key pressed
    """
    try:
        pyautogui.press(key)
        return {"key": key, "message": f"Pressed key: {key}"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def key_down(key: str) -> Dict[str, str]:
    """Hold down a key.

    Args:
        key: Key to hold down

    Returns:
        Dictionary with key
    """
    try:
        pyautogui.keyDown(key)
        return {"key": key, "message": f"Key held down: {key}"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def key_up(key: str) -> Dict[str, str]:
    """Release a key.

    Args:
        key: Key to release

    Returns:
        Dictionary with key
    """
    try:
        pyautogui.keyUp(key)
        return {"key": key, "message": f"Key released: {key}"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def hotkey(*keys: str) -> Dict[str, Any]:
    """Press key combination (e.g., Ctrl+C).

    Args:
        *keys: Keys to press together (e.g., 'ctrl', 'c' or 'ctrl', 'shift', 'esc')

    Returns:
        Dictionary with keys pressed
    """
    try:
        pyautogui.hotkey(*keys)
        return {"keys": list(keys), "message": f"Pressed hotkey: {'+'.join(keys)}"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


# ====================
# SCREEN CAPTURE TOOLS
# ====================

@server.tool()
def screenshot(filename: Optional[str] = None, region: Optional[List[int]] = None) -> Dict[str, Any]:
    """Take a screenshot of the entire screen or a region.

    Args:
        filename: Optional filename to save screenshot (e.g., 'screenshot.png')
        region: Optional [left, top, width, height] to screenshot specific area

    Returns:
        Dictionary with screenshot info. If no filename is provided, the image
        is returned as a base64 encoded string.
    """
    try:
        img = pyautogui.screenshot(region=region)
        if filename is None:
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return {"message": "Screenshot taken", "region": region, "image_base64": img_str}
        else:
            # Security: Sanitize filename and save to a dedicated directory
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            safe_filename = os.path.basename(filename)
            save_path = os.path.join(screenshots_dir, safe_filename)
            img.save(save_path)
            return {"filename": save_path, "region": region, "message": f"Screenshot saved to {save_path}"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def locate_on_screen(image_path: str, region: Optional[List[int]] = None, confidence: float = 0.9) -> Dict[str, Any]:
    """Find an image on the screen.

    Args:
        image_path: Path to image file to find
        region: Optional [left, top, width, height] to search in
        confidence: Confidence level (0.0 to 1.0, default 0.9)

    Returns:
        Dictionary with location (left, top, width, height) or error message
    """
    try:

        if region:
            pos = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        else:
            pos = pyautogui.locateOnScreen(image_path, confidence=confidence)

        if pos:
            return {
                "found": True,
                "left": pos.left,
                "top": pos.top,
                "width": pos.width,
                "height": pos.height,
                "message": f"Found image at ({pos.left}, {pos.top})"
            }
        else:
            return {"found": False, "message": "Image not found on screen"}
    except Exception as e:
        return {"found": False, "error": str(e), "message": f"Error finding image: {e}"}


@server.tool()
def locate_center_on_screen(image_path: str, region: Optional[List[int]] = None, confidence: float = 0.9) -> Dict[str, Any]:
    """Find center point of an image on the screen.

    Args:
        image_path: Path to image file to find
        region: Optional [left, top, width, height] to search in
        confidence: Confidence level (0.0 to 1.0, default 0.9)

    Returns:
        Dictionary with x, y coordinates or error message
    """
    try:

        if region:
            pos = pyautogui.locateCenterOnScreen(image_path, region=region, confidence=confidence)
        else:
            pos = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)

        if pos:
            return {
                "found": True,
                "x": pos.x,
                "y": pos.y,
                "message": f"Found image center at ({pos.x}, {pos.y})"
            }
        else:
            return {"found": False, "message": "Image not found on screen"}
    except Exception as e:
        return {"found": False, "error": str(e), "message": f"Error finding image: {e}"}


@server.tool()
def get_pixel_color(x: int, y: int) -> Dict[str, str]:
    """Get RGB color of pixel at coordinates.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        Dictionary with r, g, b values
    """
    try:
        r, g, b = pyautogui.pixel(x, y)
        return {"x": x, "y": y, "r": r, "g": g, "b": b, "hex": f"#{r:02x}{g:02x}{b:02x}"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def pixel_matches_color(x: int, y: int, color: str, tolerance: int = 0) -> Dict[str, Any]:
    """Check if pixel at coordinates matches expected color.

    Args:
        x: X coordinate
        y: Y coordinate
        color: Color string (e.g., '(255, 0, 0)' or '#FF0000')
        tolerance: Color tolerance (0-255, default 0)

    Returns:
        Dictionary with match result
    """
    try:
        rgb_tuple = None
        if color.startswith('#'):
            hex_color = color.lstrip('#')
            if len(hex_color) == 6:
                rgb_tuple = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                raise ValueError("Hex color must be in #RRGGBB format.")
        elif color.startswith('('):
            color_values = color.strip('() ').split(',')
            if len(color_values) == 3:
                rgb_tuple = tuple(int(c.strip()) for c in color_values)
            else:
                raise ValueError("RGB color must be a tuple/list of 3 integers.")
        else:
            raise ValueError("Invalid color format. Use '#RRGGBB' or '(R, G, B)'.")

        matches = pyautogui.pixelMatchesColor(x, y, rgb_tuple, tolerance=tolerance)
        return {"x": x, "y": y, "color": color, "matches": matches}
    except Exception as e:
        return {"error": f"Failed to process color '{color}': {e}"}


# ====================
# WINDOW MANAGEMENT
# ====================

@server.tool()
def get_screen_size() -> Dict[str, int]:
    """Get screen width and height in pixels.

    Returns:
        Dictionary with width, height
    """
    try:
        width, height = pyautogui.size()
        return {"width": width, "height": height}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def get_active_window_title() -> Dict[str, Any]:
    """Get title of currently active window.

    Returns:
        Dictionary with window title
    """
    try:
        title = pyautogui.getActiveWindowTitle()
        return {"title": title if title else "None"}
    except pyautogui.PyAutoGUIException as e:
        return {"title": None, "error": str(e)}


@server.tool()
def get_all_window_titles() -> Dict[str, List[str]]:
    """Get list of all visible window titles.

    Returns:
        Dictionary with list of titles
    """
    try:
        titles = pyautogui.getAllTitles()
        return {"titles": titles, "count": len(titles)}
    except pyautogui.PyAutoGUIException as e:
        return {"titles": [], "count": 0, "error": str(e)}


@server.tool()
def get_windows_with_title(title_fragment: str) -> Dict[str, List[Dict[str, str]]]:
    """Find windows with titles containing specified text.

    Args:
        title_fragment: Text to search for in window titles

    Returns:
        Dictionary with matching windows
    """
    try:
        windows = pyautogui.getWindowsWithTitle(title_fragment)
        result = [
            {"title": win.title, "left": win.left, "top": win.top, "width": win.width, "height": win.height}
            for win in windows
        ]
        return {"windows": result, "count": len(result)}
    except pyautogui.PyAutoGUIException as e:
        return {"windows": [], "count": 0, "error": str(e)}


# ====================
# USER INTERACTION TOOLS
# ====================

@server.tool()
def alert(message: str, title: str = "Alert") -> Dict[str, str]:
    """Show an alert dialog.

    Args:
        message: Message to display
        title: Dialog title

    Returns:
        Dictionary with message
    """
    try:
        result = pyautogui.alert(message, title)
        return {"message": message, "title": title, "result": result}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def confirm(message: str, title: str = "Confirm", options: Optional[List[str]] = None) -> Dict[str, str]:
    """Show a confirmation dialog with OK/Cancel or custom options.

    Args:
        message: Message to display
        title: Dialog title
        options: List of button options (default: ['OK', 'Cancel'])

    Returns:
        Dictionary with result
    """
    try:
        if options:
            result = pyautogui.confirm(message, title, options)
        else:
            result = pyautogui.confirm(message, title)
        return {"message": message, "title": title, "options": options or ['OK', 'Cancel'], "result": result}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def prompt(message: str, title: str = "Prompt", default: str = "") -> Dict[str, str]:
    """Show a prompt dialog for user input.

    Args:
        message: Message to display
        title: Dialog title
        default: Default text

    Returns:
        Dictionary with result
    """
    try:
        result = pyautogui.prompt(message, title, default)
        return {"message": message, "title": title, "default": default, "result": result}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def password(message: str, title: str = "Password", mask: str = "*") -> Dict[str, str]:
    """Show a password input dialog.

    Args:
        message: Message to display
        title: Dialog title
        mask: Character to mask password (default '*')

    Returns:
        Dictionary with result (password hidden in logs)
    """
    try:
        result = pyautogui.password(message, title, mask)
        # Never return the actual password, even in case of success.
        return {"message": message, "title": title, "mask": mask, "result": "[REDACTED]" if result else None}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


# ====================
# UTILITY TOOLS
# ====================

@server.tool()
def countdown(seconds: int) -> Dict[str, int]:
    """Show a countdown timer on screen.

    Args:
        seconds: Number of seconds to count down

    Returns:
        Dictionary with countdown duration
    """
    try:
        pyautogui.countdown(seconds)
        return {"seconds": seconds, "message": f"Countdown completed for {seconds} seconds"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def display_mouse_position(seconds: int = 5) -> Dict[str, Any]:
    """Display current mouse position for specified seconds.

    Args:
        seconds: Number of seconds to display (default 5)

    Returns:
        Dictionary with a confirmation message.
    """
    try:
        # This function runs a loop, so it\'s better to run it in a separate process
        # if the server needs to remain responsive. For now, it will block.
        pyautogui.displayMousePosition(seconds)
        return {"seconds": seconds, "message": f"Mouse position displayed for {seconds} seconds"}
    except pyautogui.PyAutoGUIException as e:
        return {"error": str(e)}


@server.tool()
def fail_safe_check() -> Dict[str, bool]:
    """Check if PyAutoGUI failsafe is enabled.

    Returns:
        Dictionary with failsafe status
    """
    enabled = pyautogui.FAILSAFE
    return {"enabled": enabled, "message": "Failsafe enabled" if enabled else "Failsafe disabled"}


# Main entry point
if __name__ == "__main__":
    import sys

    # Check if PyAutoGUI is properly installed
    try:
        import pyautogui
        print(f"✓ PyAutoGUI {pyautogui.__version__} loaded successfully", file=sys.stderr)
    except ImportError as e:
        print(f"✗ Error importing PyAutoGUI: {e}", file=sys.stderr)
        sys.exit(1)

    # Check for optional dependencies
    try:
        import cv2
        print("✓ OpenCV (cv2) found. Image recognition with 'confidence' will be available.", file=sys.stderr)
    except ImportError:
        print("⚠️  Warning: OpenCV (cv2) not found. The 'confidence' parameter for image location will not work.", file=sys.stderr)
        print("   To install it, run: pip install opencv-python", file=sys.stderr)


    # Run the server
    print("Starting PyAutoGUI MCP Server...", file=sys.stderr)
    server.run()
