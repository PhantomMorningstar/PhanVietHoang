import tkinter as tk  # Import tkinter for GUI development
import video_library as lib  # Import the video library module
import font_manager as fonts  # Import the font manager module
from tkinter import messagebox  # Import messagebox for displaying dialog boxes

def set_text_area_content(text_area, content):  # Function to update text in a text area
    text_area.delete("1.0", tk.END)  # Remove existing text from the text area
    text_area.insert("1.0", content)  # Insert new text into the text area

class Tooltip:  # Class to create tooltips for widgets
    def __init__(self, widget, text):  # Constructor
        self.widget = widget  # The widget to attach the tooltip to
        self.text = text  # The text to display in the tooltip
        self.tooltip = None  # Tooltip window placeholder
        self.widget.bind("<Enter>", self.display_tooltip)  # Show tooltip on mouse enter
        self.widget.bind("<Leave>", self.remove_tooltip)  # Hide tooltip on mouse leave

    def display_tooltip(self, event=None):  # Show tooltip when mouse enters widget
        x, y, _, _ = self.widget.bbox("insert")  # Get position of the widget
        x += self.widget.winfo_rootx() + 25  # Adjust x position
        y += self.widget.winfo_rooty() + 25  # Adjust y position

        self.tooltip = tk.Toplevel(self.widget)  # Create a new top-level window for the tooltip
        self.tooltip.wm_overrideredirect(True)  # Remove window decorations
        self.tooltip.wm_geometry(f"+{x}+{y}")  # Set tooltip position
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)  # Label for the tooltip
        label.pack(ipadx=2)  # Add label to the tooltip window

    def remove_tooltip(self, event=None):  # Hide tooltip when mouse leaves widget
        if self.tooltip:  # Check if the tooltip exists
            self.tooltip.destroy()  # Destroy the tooltip window
            
class UpdateVideo:  # Class for handling video rating updates
    def __init__(self, window):  # Constructor
        window.geometry("600x300")  # Set the dimensions of the window
        window.title("Update Videos")  # Set the title of the window

        self.video_list = []  # Initialize an empty list for video information

        tk.Label(window, text="Enter Video Number").grid(row=0, column=1, padx=10, pady=10)  # Label for video number input
        self.input_txt = tk.Entry(window, width=3)  # Entry widget for video number
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)  # Place entry widget in the window

        tk.Label(window, text="Enter New Rating Number").grid(row=0, column=3, padx=10, pady=10)  # Label for new rating input
        self.input_rating = tk.Entry(window, width=3)  # Entry widget for new rating
        self.input_rating.grid(row=0, column=4, padx=10, pady=10)  # Place entry widget in the window
        Tooltip(self.input_rating, "Rating should be between 1 and 5")  # Tooltip for the rating input field

        tk.Button(window, text="Update Video", command=self.handle_update_button_click).grid(row=1, column=1, padx=10, pady=10)  # Button to trigger video update

        self.video_txt = tk.Text(window, width=24, height=4, wrap="none")  # Text widget for displaying video details
        self.video_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)  # Place text widget in the window

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))  # Status label for messages
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)  # Place status label in the window

        self.status_lbl1 = tk.Label(window, text="Enter a valid video number like 01, 02,...", font=("Helvetica", 10))  # Additional status message
        self.status_lbl1.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)  # Place additional status label in the window

    def validate_video_number(self, video_number):  # Method to check the format of the video number
        if video_number.isdigit() and len(video_number) == 2:  # Ensure it is a 2-digit number
            return True  # Valid format
        else:
            return False  # Invalid format

    def handle_update_button_click(self):  # Method to handle the "Update Video" button click
        video_id = self.input_txt.get()  # Retrieve video number from input
        name = lib.get_name(video_id)  # Fetch video name from the library
        director = lib.get_director(video_id)  # Fetch video director from the library
        new_rating = self.input_rating.get()  # Retrieve new rating from input

        if not self.validate_video_number(video_id):  # Validate video number format
            messagebox.showinfo("Prompt", "Please enter a video number like 01, 02,...")  # Show error message
        else:
            if new_rating:  # Check if new rating is provided
                try:
                    rating_value = int(new_rating)  # Convert new rating to integer

                    if 1 <= rating_value <= 5:  # Ensure the rating is within the valid range
                        play_count = lib.get_play_count(video_id)  # Get play count from the library
                        lib.set_rating(video_id, rating_value)  # Update the rating in the library

                        video_details = f"Movie: {name}\nDirector: {director}\nNew Rating: {rating_value}\nPlays: {play_count}"  # Prepare video details
                        set_text_area_content(self.video_txt, video_details)  # Display video details
                    else:
                        messagebox.showinfo("Prompt", "Rating must be between 1 and 5")  # Show error message for invalid rating
                except ValueError:
                    messagebox.showinfo("Prompt", "Please enter a valid numerical rating")  # Show error message for non-numeric input
            else:
                messagebox.showinfo("Prompt", "Please provide a new rating")  # Prompt user to enter a rating

if __name__ == "__main__":  # Check if this script is run as the main program
    main_window = tk.Tk()  # Create a main tkinter window
    fonts.configure()  # Set up fonts using the font manager
    UpdateVideo(main_window)  # Create an instance of the UpdateVideo class with the main window
    main_window.mainloop()  # Start the tkinter event loop
