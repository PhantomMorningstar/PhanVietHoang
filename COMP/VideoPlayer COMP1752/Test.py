import tkinter as tk
import font_manager as fonts
from create_video_list import CreateVideoList
from check_videos import CheckVideos
from update_video import UpdateVideo
import os

def on_check_videos():  # Action handler for the "Check Videos" button
    status_lbl.config(text="Check Videos button was pressed!")
    CheckVideos(tk.Toplevel(window))  # Open the CheckVideos window

def on_create_video_list():  # Action handler for the "Create Video List" button
    status_lbl.config(text="Create Video List button was pressed!")
    CreateVideoList(tk.Toplevel(window))  # Open the CreateVideoList window

def on_update_videos():  # Action handler for the "Update Videos" button
    status_lbl.config(text="Update Videos button was pressed!")
    UpdateVideo(tk.Toplevel(window))  # Open the UpdateVideo window

# Initialize the main application window
window = tk.Tk()
window.geometry("520x150")  # Set the dimensions of the window
window.title("Video Player")  # Set the title of the window

# Apply font settings
fonts.configure()

# Create and place the header label
header_lbl = tk.Label(window, text="Select an option by clicking one of the buttons below")
header_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Create and place the "Check Videos" button
check_videos_btn = tk.Button(window, text="Check Videos", command=on_check_videos)
check_videos_btn.grid(row=1, column=0, padx=10, pady=10)

# Create and place the "Create Video List" button
create_video_list_btn = tk.Button(window, text="Create Video List", command=on_create_video_list)
create_video_list_btn.grid(row=1, column=1, padx=10, pady=10)

# Create and place the "Update Videos" button
update_videos_btn = tk.Button(window, text="Update Videos", command=on_update_videos)
update_videos_btn.grid(row=1, column=2, padx=10, pady=10)

# Create and place the status label
status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Start the Tkinter event loop
window.mainloop()

