import tkinter as tk
from tkinter import filedialog
import requests
import time
import threading
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import datetime
import json

TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'  # Replace with your chat ID

def send_message():
    channel_id = channel_entry.get()
    user_header = header_entry.get()
    payload_text = payload_entry.get()
    cooldown_time = int(cooldown_entry.get())

    payload = {
        'content': payload_text
    }

    header = {
        'Authorization': user_header
    }

    gif_path = gif_entry.get()

    while not stop_flag.is_set():
        try:
            files = {}
            if gif_path:
                files = {'file': open(gif_path, 'rb')}
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header, files=files)

            if r.status_code == 200:
                log_message(channel_id)
                send_log_to_telegram(f"MSG sent to {channel_id}")
            else:
                log_message(f"Failed to send to {channel_id}. Status code: {r.status_code}")
                send_log_to_telegram(f"Failed to send to {channel_id}. Status code: {r.status_code}")

        except requests.exceptions.RequestException as e:
            log_message(f"Error occurred: {e}")
            send_log_to_telegram(f"Error occurred: {e}")

        time.sleep(cooldown_time)

def check_empty_fields():
    fields = {
        'Channel ID': channel_entry.get(),
        'Token': header_entry.get(),
        'Cooldown': cooldown_entry.get(),
        'Text': payload_entry.get()
    }

    for field_name, field_value in fields.items():
        if not field_value.strip():
            messagebox.showerror("Error", f"{field_name} field cannot be empty.")
            return False
    return True

# Save data to a JSON file when the application is closed
def on_close():
    if check_empty_fields():
        data = {
            'channel_id': channel_entry.get(),
            'header': header_entry.get(),
            'cooldown': cooldown_entry.get(),
            'payload': payload_entry.get(),
            'gif_path': gif_entry.get(),
            'debugging_enabled': debug_checkbox_var.get(),
            'telegram_bot_token': telegram_bot_token_entry.get(),
            'telegram_chat_id': telegram_chat_id_entry.get()
        }
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    window.destroy()

def load_data():
    try:
        with open('data.json', 'r') as infile:
            data = json.load(infile)
            channel_entry.insert(0, data.get('channel_id', ''))
            header_entry.insert(0, data.get('header', ''))
            cooldown_entry.insert(0, data.get('cooldown', ''))
            payload_entry.insert(0, data.get('payload', ''))
            gif_entry.insert(0, data.get('gif_path', ''))
            debug_checkbox_var.set(data.get('debugging_enabled', False))
            telegram_bot_token_entry.insert(0, data.get('telegram_bot_token', ''))
            telegram_chat_id_entry.insert(0, data.get('telegram_chat_id', ''))
    except FileNotFoundError:
        messagebox.showwarning("File Not Found", "Data file not found.")

def log_message(message):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    log_text = f"{current_time}  |  {message}\n"

    log_text_widget.configure(state=tk.NORMAL)
    log_text_widget.insert(tk.END, log_text)
    log_text_widget.configure(state=tk.DISABLED)
    log_text_widget.see(tk.END)

def send_log_to_telegram(message):
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage', data=payload)

def start_sending():
    global stop_flag
    stop_flag.clear()

    telegram_bot_token = telegram_bot_token_entry.get()
    telegram_chat_id = telegram_chat_id_entry.get()
    use_telegram_debugging = debug_checkbox_var.get()

    if use_telegram_debugging and telegram_bot_token and telegram_chat_id:
        # Use provided Telegram Bot Token and Chat ID for debugging
        global TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
        TELEGRAM_BOT_TOKEN = telegram_bot_token
        TELEGRAM_CHAT_ID = telegram_chat_id

    send_thread = threading.Thread(target=send_message)
    send_thread.start()

def stop_sending():
    global stop_flag
    stop_flag.set()

def paste_channel_id():
    clipboard_text = window.clipboard_get()
    channel_entry.delete(0, tk.END)
    channel_entry.insert(0, clipboard_text)

def paste_header():
    clipboard_text = window.clipboard_get()
    header_entry.delete(0, tk.END)
    header_entry.insert(0, clipboard_text)

def paste_cooldown():
    clipboard_text = window.clipboard_get()
    cooldown_entry.delete(0, tk.END)
    cooldown_entry.insert(0, clipboard_text)

def paste_payload():
    clipboard_text = window.clipboard_get()
    payload_entry.delete(0, tk.END)
    payload_entry.insert(0, clipboard_text)

def choose_gif():
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    gif_entry.delete(0, tk.END)
    gif_entry.insert(0, file_path)

# Create the main window
window = tk.Tk()
window.title("Discord Message Sender by n1katio")

# Create and position the widgets
tk.Label(window, text="Channel ID:").grid(row=0, column=0, padx=5, pady=5)
channel_entry = tk.Entry(window)
channel_entry.grid(row=0, column=1, padx=5, pady=5)
paste_channel_button = tk.Button(window, text="Paste", command=paste_channel_id)
paste_channel_button.grid(row=0, column=2, padx=5, pady=5)

tk.Label(window, text="Token:").grid(row=1, column=0, padx=5, pady=5)
header_entry = tk.Entry(window)
header_entry.grid(row=1, column=1, padx=5, pady=5)
paste_header_button = tk.Button(window, text="Paste", command=paste_header)
paste_header_button.grid(row=1, column=2, padx=5, pady=5)

tk.Label(window, text="Cooldown (seconds):").grid(row=2, column=0, padx=5, pady=5)
cooldown_entry = tk.Entry(window)
cooldown_entry.grid(row=2, column=1, padx=5, pady=5)
paste_cooldown_button = tk.Button(window, text="Paste", command=paste_cooldown)
paste_cooldown_button.grid(row=2, column=2, padx=5, pady=5)

tk.Label(window, text="Text:").grid(row=3, column=0, padx=5, pady=5)
payload_entry = tk.Entry(window)
payload_entry.grid(row=3, column=1, padx=5, pady=5)
paste_payload_button = tk.Button(window, text="Paste", command=paste_payload)
paste_payload_button.grid(row=3, column=2, padx=5, pady=5)

tk.Label(window, text="GIF Path:").grid(row=4, column=0, padx=5, pady=5)
gif_entry = tk.Entry(window)
gif_entry.grid(row=4, column=1, padx=5, pady=5)
choose_gif_button = tk.Button(window, text="Choose GIF", command=choose_gif)
choose_gif_button.grid(row=4, column=2, padx=5, pady=5)

start_button = tk.Button(window, text="Start", command=start_sending)
start_button.grid(row=5, column=0, padx=5, pady=5)

stop_button = tk.Button(window, text="Stop", command=stop_sending)
stop_button.grid(row=5, column=1, padx=5, pady=5)

log_text_widget = tk.Text(window, height=10, width=50, state=tk.DISABLED)
log_text_widget.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

debug_frame = tk.Frame(window)
debug_frame.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

debug_checkbox_var = tk.BooleanVar()
debug_checkbox = tk.Checkbutton(debug_frame, text="Enable Telegram Debugging", variable=debug_checkbox_var)
debug_checkbox.pack()

tk.Label(debug_frame, text="TELEGRAM BOT TOKEN:").pack()
telegram_bot_token_entry = tk.Entry(debug_frame)
telegram_bot_token_entry.pack()

tk.Label(debug_frame, text="TELEGRAM CHAT ID:").pack()
telegram_chat_id_entry = tk.Entry(debug_frame)
telegram_chat_id_entry.pack()

load_data()

window.protocol("WM_DELETE_WINDOW", on_close)

# Create a flag to stop the sending process
stop_flag = threading.Event()

# Start the GUI event loop
window.mainloop()
