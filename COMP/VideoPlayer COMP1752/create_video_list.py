import tkinter as tk  # Import tkinter for GUI elements
import tkinter.scrolledtext as tkst  # Import ScrolledText widget from tkinter
from tkinter import messagebox  # Import messagebox for pop-up messages
import video_library as lib  # Import video_library for accessing video data
import font_manager as fonts  # Import font_manager for font settings

def update_text_widget(text_widget, content):
    text_widget.delete("1.0", tk.END)  # Clear current text
    text_widget.insert("1.0", content)  # Insert new text

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")  # Get widget coordinates
        x += self.widget.winfo_rootx() + 25  # Adjust x-coordinate
        y += self.widget.winfo_rooty() + 25  # Adjust y-coordinate

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)  # Create a borderless window
        self.tooltip.wm_geometry(f"+{x}+{y}")  # Set window position
        # Create and display the tooltip label
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=2)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()  # Close the tooltip window

class CreateVideoList:
    def __init__(self, window):
        self.window = window
        self.play_count = 0
        window.geometry("700x350")
        window.title("Manage Video Playlist")
        self.video_list = []  # Initialize an empty playlist

        # Widgets for adding videos
        enter_label = tk.Label(window, text="Enter Video Number")
        enter_label.grid(row=0, column=1, padx=10, pady=10)

        self.input_entry = tk.Entry(window, width=3)
        self.input_entry.grid(row=0, column=2, padx=10, pady=10)
        Tooltip(self.input_entry, "Enter a valid number like 01, 02...")

        add_video_button = tk.Button(window, text="Add Video", command=self.add_video)
        add_video_button.grid(row=0, column=0, padx=10, pady=10)
        Tooltip(add_video_button, "Add video to the playlist")

        # Widgets for playing videos
        self.play_entry = tk.Entry(window, width=3)
        self.play_entry.grid(row=0, column=3, padx=10, pady=10)

        play_playlist_button = tk.Button(window, text="Play Playlist", command=self.play_playlist)
        play_playlist_button.grid(row=0, column=3, padx=10, pady=10)
        Tooltip(play_playlist_button, "Increase play count for all videos")

        # Reset button and status label
        reset_button = tk.Button(window, text="Reset Playlist", command=self.reset_playlist)
        reset_button.grid(row=1, column=3, padx=10, pady=10)
        Tooltip(reset_button, "Clear the playlist")

        # ScrolledText widget to display playlist
        self.playlist_display = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.playlist_display.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.status_label = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_label.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

    def add_video(self):
        video_key = self.input_entry.get()  # Retrieve video number from entry
        if video_key.isdigit() and len(video_key) == 2:  # Validate video number
            if video_key not in self.video_list:  # Check if video is already in playlist
                video_name = lib.get_name(video_key)  # Fetch video name from library
                if video_name:  # Ensure video name is valid
                    video_details = f" {video_name}\n"  # Prepare video details
                    update_text_widget(self.playlist_display, video_details)  # Display video name
                    self.video_list.append(video_key)  # Add video to playlist
                else:
                    messagebox.showinfo("Prompt", "Invalid video number")
            else:
                self.status_label.config(text="Video already in playlist")
        else:
            messagebox.showinfo("Prompt", "Enter a valid number like 01, 02...")
        self.display_playlist()  # Update playlist display

    def play_playlist(self):
        if not self.video_list:  # Check if playlist is empty
            messagebox.showinfo("Prompt", "No videos in the playlist. Add videos first.")
        else:
            for key in self.video_list:  # Increment play count for each video
                lib.increment_play_count(key)
            self.status_label.config(text="Playlist updated")

    def reset_playlist(self):
        self.video_list = []  # Clear the playlist
        self.playlist_display.delete("1.0", tk.END)  # Clear the playlist display
        self.status_label.config(text="Playlist has been reset")

    def display_playlist(self):
        output = ""  # Prepare to display video names
        for key in self.video_list:
            name = lib.get_name(key)  # Fetch video name
            output += f"{name}\n"  # Append video name to output
        update_text_widget(self.playlist_display, output)  # Update the display

if __name__ == "__main__":
    main_window = tk.Tk()  # Create main window
    fonts.configure()  # Set up fonts
    CreateVideoList(main_window)  # Initialize the CreateVideoList GUI
    main_window.mainloop()  # Start the Tkinter event loop
