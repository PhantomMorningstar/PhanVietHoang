import tkinter as tk  # Import tkinter module and alias it as tk
import tkinter.scrolledtext as tkst  # Import the ScrolledText widget from tkinter, aliasing as tkst
import video_library as lib  # Import video_library module with alias lib
import font_manager as fonts  # Import font_manager module with alias fonts
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL (Python Imaging Library)
import difflib  # Import difflib module for comparing strings
from tkinter import messagebox  # Import messagebox from tkinter for displaying messages

def update_text_widget(text_area, content):  # Function to update content in a text widget
    text_area.delete("1.0", tk.END)  # Remove existing content
    text_area.insert("1.0", content)  # Insert new content

class Tooltip:  # Class to manage tooltips for widgets
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):  # Method to display the tooltip
        x, y, _, _ = self.widget.bbox("insert")  # Obtain widget coordinates
        x += self.widget.winfo_rootx() + 25  # Adjust x-coordinate for tooltip position
        y += self.widget.winfo_rooty() + 25  # Adjust y-coordinate for tooltip position

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)  # Make tooltip window borderless
        self.tooltip.wm_geometry(f"+{x}+{y}")  # Set tooltip window position
        # Create label for displaying tooltip text
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=2)

    def hide_tooltip(self, event=None):  # Method to hide the tooltip
        if self.tooltip:
            self.tooltip.destroy()  # Remove the tooltip window

class CheckVideos:  # Class for the CheckVideos window
    def __init__(self, window):
        window.geometry("1100x400")  # Set dimensions for the window
        window.title("Check Videos")  # Set window title

        # Button to list all videos
        list_videos_btn = tk.Button(window, text="List All Videos", command=self.on_list_videos_click)
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10)  # Place button in the window

        # Button to check a video
        check_video_btn = tk.Button(window, text="Check Video", command=self.on_check_video_click)
        check_video_btn.grid(row=0, column=3, padx=10, pady=10)  # Place button in the window
        Tooltip(check_video_btn, "Search and check a video after entering the keyword")

        # Scrolled text widget for listing videos
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        # Text widget for displaying details of a selected video
        self.video_txt = tk.Text(window, width=24, height=4, wrap="none")
        self.video_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        # Status label for messages
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        # Label for displaying video images
        self.picture_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.picture_lbl.grid(row=1, column=5, columnspan=3, sticky="NW", padx=10, pady=10)

        # Populate the video list initially
        self.on_list_videos_click()

        # Search functionality
        self.search_input = tk.Entry(window, width=30)  # Entry field for search term
        self.search_input.grid(row=1, column=3, padx=10, pady=10)
        Tooltip(self.search_input, "Enter characters to search for videos")

        search_btn = tk.Button(window, text="Search", command=self.search_video)
        search_btn.grid(row=1, column=4, padx=10, pady=10)

        # Dictionary for video images
        self.video_images = {
            "01": "image1.jpg",
            "02": "image2.jpg",
            "03": "image3.jpg",
            "04": "image4.jpg",
            "05": "image5.jpg",
            "06": "image6.jpg",
        }

    def search_video(self):  # Search for videos based on input
        search_term = self.search_input.get()  # Retrieve search term
        results = []

        # Search video names and directors
        for key in self.video_images:
            name = lib.get_name(key)
            director = lib.get_director(key)
            # Check similarity of search term with video name or director
            if difflib.SequenceMatcher(None, search_term, name).ratio() >= 0.5 or \
                    difflib.SequenceMatcher(None, search_term, director).ratio() >= 0.5 or \
                    difflib.SequenceMatcher(None, search_term, key).ratio() >= 0.8:
                results.append(f"{key}: {name} (Directed by {director})")

        # Display search results
        if results:
            update_text_widget(self.list_txt, "\n".join(results))
            self.status_lbl.config(text=f"Search results for '{search_term}'")
        else:
            self.status_lbl.config(text=f"No results for '{search_term}'")
            messagebox.showinfo("Prompt", "Enter more keywords to refine the search")
            update_text_widget(self.list_txt, "")
            update_text_widget(self.video_txt, "")

    def on_check_video_click(self):  # Handle checking video details
        search_term = self.search_input.get()  # Get search term

        if not search_term:
            messagebox.showinfo("Error", "Enter a keyword to search for a video.")
            return

        search_results = self.list_txt.get("1.0", tk.END).strip().split("\n")  # Retrieve search results
        valid_keys = self.video_images.keys()
        image_path = None

        for result in search_results:
            key = result[:2]
            if key in valid_keys:
                # Retrieve video details
                name = lib.get_name(key)
                director = lib.get_director(key)
                rating = lib.get_rating(key)
                play_count = lib.get_play_count(key)
                details = f"Movie: {name}\nDirector: {director}\nRating: {rating}\nPlays: {play_count}"
                update_text_widget(self.video_txt, details)

                # Load and display video image
                image_path = self.video_images[key]
                image = Image.open(image_path)
                image = image.resize((200, 200))
                tk_image = ImageTk.PhotoImage(image)
                self.picture_lbl.config(image=tk_image)
                self.picture_lbl.image = tk_image
                return

        if not image_path:
            self.picture_lbl.config(image="")
            messagebox.showinfo("Error", "No valid video found.")
            update_text_widget(self.video_txt, "")
        else:
            messagebox.showinfo("Error", "No valid video found.")
            update_text_widget(self.video_txt, "")
            update_text_widget(self.search_input, "")

    def on_list_videos_click(self):  # Handle listing all videos
        video_list = lib.list_all()  # Retrieve all videos
        update_text_widget(self.list_txt, video_list)
        self.status_lbl.config(text="Video list updated.")

if __name__ == "__main__":  # Execute script if run as the main module
    window = tk.Tk()  # Create the main window
    fonts.configure()  # Apply font settings
    CheckVideos(window)  # Initialize CheckVideos class with the main window
    window.mainloop()  # Start the Tkinter event loop

