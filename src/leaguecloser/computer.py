"""
Abstracts Windows-specific tasks into a simple external API.

By Giantpizzahead
"""
import re
import signal
import time
import psutil
import pyautogui
import win32com.client
import win32con
import win32gui


# ======================
# Configurable constants
# ======================


WPM = 120
"""float: The words per minute to try and simulate when typing."""

MOUSE_DURATION = 0.1
"""float: The amount of time to spend moving the mouse cursor to new positions."""

WAIT_AFTER = 0.05
"""float: The default amount of time to wait after performing an action."""

# Disable PyAutoGUI's built-in delay
pyautogui.PAUSE = 0


# ================
# Helper functions
# ================


def wait(seconds):
    """Waits for a specified amount of time.

    Args:
        seconds (float): The amount of time to wait, in seconds.
    """
    time.sleep(seconds)


def sequenced_action(func):
    """A decorator function that adds a small delay after each function call.

    The wait time can be customized by passing a "wait_after" float keyword argument to the function.

    Args:
        func (function): The function to decorate.
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        wait(kwargs.get("wait_after", WAIT_AFTER))
        return result

    return wrapper


# ==========================
# Mouse and keyboard control
# ==========================


@sequenced_action
def click():
    """Clicks the left mouse button."""
    pyautogui.click()


@sequenced_action
def right_click():
    """Clicks the right mouse button."""
    pyautogui.click(button="right")


@sequenced_action
def double_click(interval=0.15):
    """Double clicks the left mouse button.

    Args:
        interval (float): The time between clicks, in seconds.
    """
    pyautogui.click(clicks=2, interval=0.15)


@sequenced_action
def move_mouse(x, y, duration=MOUSE_DURATION):
    """Moves the mouse cursor to the specified coordinates in the specified time.

    Args:
        x (int): The x coordinate to move the mouse to.
        y (int): The y coordinate to move the mouse to.
        duration (float): The duration of the mouse movement, in seconds.
    """
    pyautogui.moveTo(x, y, duration=duration)


@sequenced_action
def drag_mouse(x, y, duration=MOUSE_DURATION):
    """Drags the mouse cursor to the specified coordinates in the specified time.

    Args:
        x (int): The x coordinate to drag the mouse to.
        y (int): The y coordinate to drag the mouse to.
        duration (float): The duration of the mouse movement, in seconds.
    """
    pyautogui.dragTo(x, y, duration=duration)


@sequenced_action
def press(key):
    """Presses a single key on the keyboard.

    In addition to the standard keys, you can also press keys like "win" (Windows key), "enter", "esc", etc.

    Args:
        key (str): The key to press.
    """
    pyautogui.press(key)


@sequenced_action
def typewrite(text, wpm=WPM):
    """Types a string of text using the keyboard.

    You can specify a custom WPM to type at. Random delays will be added to simulate human typing.

    Args:
        text (str): The text to type.
        wpm (float): The words per minute to type at, on average.
    """
    # Type with the given WPM
    delay = 60 / (wpm * 5)
    pyautogui.typewrite(text, interval=delay)


# ==========================
# Windows process management
# ==========================


def _find_process(process_name):
    """Finds a process by its name.

    Args:
        process_name (str): The exact name of the process to find.

    Returns:
        psutil.Process: The process object if it was found, None if it wasn't.
    """
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc
    return None


def is_process_running(process_name):
    """Check if a process is currently running.

    Args:
        process_name (str): The exact name of the process to check.

    Returns:
        bool: True if the process is running, False otherwise.
    """
    return _find_process(process_name) is not None


def open_app(app_name, wait_after=2):
    """Opens a program by its application name (not process name!).

    You don't need to specify the exact name of the application, just use what you'd type in the start menu!

    Args:
        app_name (str): The name of the application to open.
        wait_after (float): The time to wait after opening the process.
    """
    # Launch the application
    press("win")
    wait(0.1)
    typewrite(app_name)
    wait(0.1)
    press("enter")
    wait(wait_after)


def close_process(process_name, timeout=3):
    """Terminates a program by its process name.

    Will send a SIGTERM signal first for a graceful shutdown, then a SIGKILL signal if the process keeps running.

    Args:
        process_name (str): The exact name of the process to terminate.
        timeout (float): The time to wait for the process to gracefully terminate, in seconds.

    Returns:
        bool: True if the process was terminated, False if it wasn't running.
    """
    proc = _find_process(process_name)
    if proc is None:
        return False
    # Send a SIGTERM signal first
    proc.send_signal(signal.SIGTERM)
    # Wait for the process to terminate
    for _ in range(int(timeout * 10)):
        if proc.status() == psutil.STATUS_ZOMBIE:
            return True
        wait(0.1)
    # Send a SIGKILL signal if the process is still running
    proc.send_signal(signal.SIGKILL)
    return True


# =========================
# Windows window management
# =========================


def find_window(window_name, allow_regex=True):
    """Finds a window by its title.

    Args:
        window_name (str): The exact name of the window title to find.
        allow_regex (bool): Whether to allow regular expressions in the window name.

    Returns:
        int: The window handle, or 0 if the window couldn't be found.
    """

    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if allow_regex and re.search(window_name, window_title):
                extra.append(hwnd)
            elif window_title == window_name:
                extra.append(hwnd)

    hwnds = []
    win32gui.EnumWindows(enum_callback, hwnds)
    return hwnds[0] if hwnds else 0


def focus_window(window_name, wait_after=0.3):
    """Focuses a window by unminimizing it and bringing it to the foreground.

    Args:
        window_name (str): The exact name of the window title to focus.
        wait_after (float): The time to wait after focusing the window.

    Returns:
        bool: True if the window was focused, False if it couldn't be focused or wasn't found.
    """
    # Get the window handle
    hwnd = find_window(window_name)
    if hwnd == 0:
        return False
    # Focus the window
    win32com.client.Dispatch("WScript.Shell").SendKeys('%')
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    wait(wait_after)
    # Check if the window is visible and focused
    return win32gui.IsWindowVisible(hwnd) and win32gui.GetForegroundWindow() == hwnd


def get_window_rect(window_name):
    """Gets the window rectangle (x, y, width, height) of a window.

    Args:
        window_name (str): The exact name of the window title to get the rectangle of.

    Returns:
        tuple: The window rectangle (x, y, width, height), or (0, 0, 0, 0) if the window couldn't be found.
    """
    # Get the window handle
    hwnd = find_window(window_name)
    if hwnd == 0:
        return 0, 0, 0, 0
    # Get the window rectangle
    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
    return x1, y1, x2 - x1, y2 - y1


# =================
# Development tools
# =================


def dev_find_process_name(app_name, wait_after=2):
    """Helper function to find the process name for an application.

    You don't need to specify the exact name of the application, just use what you'd type in the start menu!
    Prints a list of all processes that appeared after launching the application.

    Args:
        app_name (str): The name of the application to search for.
        wait_after (float): The time to wait after opening the application.

    Examples:
        Finding the process name for Notepad:
        >>> dev_find_process_name("Notepad")

        Finding League of Legends (with a longer loading time):
        >>> dev_find_process_name("league", wait_after=20)
    """
    # Get all processes before launching the application
    processes_before = set(psutil.process_iter())

    # Launch the application
    open_app(app_name, wait_after=wait_after)

    # Get all processes after launching the application
    processes_after = set(psutil.process_iter())

    # Print a list of all processes that appeared after launching the application
    processes = processes_after - processes_before
    print(f"Processes that appeared after launching {app_name}:")
    for proc in processes:
        print(f" - {proc.name()}")


def dev_print_all_processes():
    """Prints a list of all processes currently running on the computer.

    Handy for finding the exact name of a process during development.
    """
    from prettytable import PrettyTable

    # Create a table with all running processes
    table = PrettyTable()
    table.field_names = ["Process ID", "Raw Name"]
    for proc in psutil.process_iter():
        try:
            # Record the process ID and name
            table.add_row([proc.pid, proc.name()])
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            # Skip processes that we cannot access
            pass
    # Print the table
    print("All running processes:")
    print(table)


def dev_print_all_windows():
    """Prints a list of all windows currently open on the computer.

    Handy for finding the exact title of a window during development.
    """
    from prettytable import PrettyTable

    # Create a table with all open windows
    table = PrettyTable()
    table.field_names = ["Window ID", "Raw Name"]

    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            table.add_row([hwnd, window_title])

    win32gui.EnumWindows(enum_callback, None)
    # Print the table
    print("All open windows:")
    print(table)
