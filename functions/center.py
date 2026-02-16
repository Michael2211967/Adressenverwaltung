def center_window(win_width, win_height, window):
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    WIN_X = (screenWidth - win_width) // 2
    WIN_Y = (screenHeight - win_height) // 2
    geometry = f"{win_width}x{win_height}+{WIN_X}+{WIN_Y}"
    return geometry