import tkinter as tk
import requests
import time
import threading

def send_message():
    channel_id = channel_entry.get()
    user_header = header_entry.get()
    cooldown_time = int(cooldown_entry.get())

    payload = {
        'content': "s"
    }

    header = {
        'Authorization': user_header
    }

    while not stop_flag.is_set():
        try:
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header)

            if r.status_code == 200:
                print("Message sent successfully.")
            else:
                print(f"Failed to send the message. Status code: {r.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")

        time.sleep(cooldown_time)

def start_sending():
    global stop_flag
    stop_flag.clear()
    send_thread = threading.Thread(target=send_message)
    send_thread.start()

def stop_sending():
    global stop_flag
    stop_flag.set()

# Create the main window
window = tk.Tk()
window.title("Discord Message Sender by n1katio")

# Create and position the widgets
tk.Label(window, text="Channel ID:").grid(row=0, column=0, padx=5, pady=5)
channel_entry = tk.Entry(window)
channel_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(window, text="Token:").grid(row=1, column=0, padx=5, pady=5)
header_entry = tk.Entry(window)
header_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(window, text="Cooldown (seconds):").grid(row=2, column=0, padx=5, pady=5)
cooldown_entry = tk.Entry(window)
cooldown_entry.grid(row=2, column=1, padx=5, pady=5)

start_button = tk.Button(window, text="Start", command=start_sending)
start_button.grid(row=3, column=0, padx=5, pady=5)

stop_button = tk.Button(window, text="Stop", command=stop_sending)
stop_button.grid(row=3, column=1, padx=5, pady=5)

# Create a flag to stop the sending process
stop_flag = threading.Event()

# Start the GUI event loop
window.mainloop()
