from screeninfo import get_monitors

def center_window(win_width, win_height, window):
    

    try:
        monitors = get_monitors()
        if monitors:
            # Wir suchen den Monitor mit der größten Breite (dein 4K-Schirm)
            # Das ist robuster als 'is_primary', da dieses Attribut oft fehlt
            target = max(monitors, key=lambda m: m.width)
            
            # Berechnung mit den Werten des breitesten Monitors
            WIN_X = target.x + (target.width // 2) - (win_width // 2)
            WIN_Y = target.y + (target.height // 2) - (win_height // 2)

    except Exception as e:
        # Standard-Fallback auf Gesamtdesktop
        WIN_X = (window.winfo_screenwidth() - win_width) // 2
        WIN_Y = (window.winfo_screenheight() - win_height) // 2
        
    geometry = f"{win_width}x{win_height}+{WIN_X}+{WIN_Y}"
    return geometry