import tkinter as tk
import font_manager as fonts
from create_video_list import CreateVideoList
from check_videos import CheckVideos
from update_video import UpdateVideo

# Function to handle the Check Videos button click
def check_videos_clicked():
    status_lbl.configure(text="Check Videos button was clicked!")
    CheckVideos(tk.Toplevel(window))  # Open a new window for CheckVideos

# Function to handle the Create Video List button click
def create_videos_clicked():
    status_lbl.configure(text="Create Videos List button was clicked!")
    CreateVideoList(tk.Toplevel(window))  # Open a new window for CreateVideoList

# Function to handle the Update Videos button click
def update_video_clicked():
    status_lbl.configure(text="Update Videos button was clicked!")
    UpdateVideo(tk.Toplevel(window))  # Open a new window for UpdateVideo

# Create the main window
window = tk.Tk()
window.geometry("520x150")  # Set the window size
window.title("Video Player")  # Set the window title

# Apply custom font settings
fonts.configure()

# Add a label to guide the user
header_lbl = tk.Label(window, text="Select an option by clicking one of the buttons below")
header_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)  # Position and size the label

# Button to check videos
check_videos_btn = tk.Button(window, text="Check Videos", command=check_videos_clicked)
check_videos_btn.grid(row=1, column=0, padx=10, pady=10)  # Position and size the button

# Button to create a video list
create_video_list_btn = tk.Button(window, text="Create Video List", command=create_videos_clicked)
create_video_list_btn.grid(row=1, column=1, padx=10, pady=10)  # Position and size the button

# Button to update videos
update_videos_btn = tk.Button(window, text="Update Videos", command=update_video_clicked)
update_videos_btn.grid(row=1, column=2, padx=10, pady=10)  # Position and size the button

# Status label to display messages
status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)  # Position and size the label

# Start the Tkinter event loop
window.mainloop()
