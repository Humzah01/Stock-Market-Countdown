import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import math

def marketCountdown():
    now = datetime.now()
    marketOpen = now.replace(hour=9, minute=30, second=0, microsecond=0)
    marketClose = now.replace(hour=16, minute=0, second=0, microsecond=0)



    if now.weekday() < 5:
        if now < marketOpen:
            countdown = marketOpen - now
            status = "Market CLOSED - Opens in: "
        elif now >= marketOpen and now < marketClose:
            countdown = marketClose - now
            status = "Market OPEN - Closes in: "
        else:
            nextOpen = marketOpen + timedelta(days=1)
            while nextOpen.weekday() >= 5:
                nextOpen += timedelta(days=1)
            countdown = nextOpen - now
            status = "Market CLOSED - Opens in: "
    else:
        daysUntilMonday = (7 - now.weekday()) % 7
        if daysUntilMonday == 0:
            daysUntilMonday = 1
        nextOpen = marketOpen + timedelta(days=daysUntilMonday)
        countdown = nextOpen - now
        status = "Market CLOSED - Opens in: "
    return status + str(countdown).split('.')[0]



def create_clock_face(canvas):
    # Create clock circle
    canvas.create_oval(10, 10, 190, 190, width=2, outline="#FFD700")
    
    # Create hour markers and numbers
    for i in range(12):
        angle = i * math.pi/6 - math.pi/2
        
        # Hour markers (lines)
        start_x = 100 + 80 * math.cos(angle)
        start_y = 100 + 80 * math.sin(angle)
        end_x = 100 + 90 * math.cos(angle)
        end_y = 100 + 90 * math.sin(angle)
        canvas.create_line(start_x, start_y, end_x, end_y, width=2)
        
        # Hour numbers
        # Move numbers slightly inside the markers
        num_x = 100 + 65 * math.cos(angle)
        num_y = 100 + 65 * math.sin(angle)
        # Convert 0 to 12, else use the hour number
        hour_num = 12 if i == 0 else i
        canvas.create_text(num_x, num_y, text=str(hour_num), 
                         font=('Arial', 12, 'bold' ), fill='#Ffd700')
def update_clock():
    now = datetime.now()
    
    # Clear previous hands
    canvas.delete("hand")
    
    # Hour hand
    hour_angle = (now.hour % 12 + now.minute / 60) * math.pi/6 - math.pi/2
    hour_x = 100 + 50 * math.cos(hour_angle)
    hour_y = 100 + 50 * math.sin(hour_angle)
    canvas.create_line(100, 100, hour_x, hour_y, width=4, fill='yellow', tags="hand")
    
    # Minute hand
    minute_angle = now.minute * math.pi/30 - math.pi/2
    minute_x = 100 + 70 * math.cos(minute_angle)
    minute_y = 100 + 70 * math.sin(minute_angle)
    canvas.create_line(100, 100, minute_x, minute_y, width=3, fill='red', tags="hand")
    
    # Second hand
    second_angle = now.second * math.pi/30 - math.pi/2
    second_x = 100 + 80 * math.cos(second_angle)
    second_y = 100 + 80 * math.sin(second_angle)
    canvas.create_line(100, 100, second_x, second_y, width=1, fill='orange', tags="hand")
    
    # Center dot
    canvas.create_oval(97, 97, 103, 103, fill='#Ffd700', tags="hand")
    
    # Update market status
    status = marketCountdown()

    market_label.config(text=status)
	
    
    # Schedule next update
    root.after(1000, update_clock)

# Initialize the main window
root = tk.Tk()
root.title("Stock Market Countdown")
root.geometry("600x300")  # Set window size

# Create main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create and pack the clock canvas
canvas = tk.Canvas(main_frame, width=200, height=200, bg='black')
canvas.pack(pady=10)

# Create and pack the market status label
market_label = tk.Label(main_frame, text="", font=("Monospace", 24))
market_label.pack(pady=10)

# Initialize clock face and start updates
create_clock_face(canvas)
update_clock()

root.mainloop()