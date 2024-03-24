import clipboard
import subprocess
from pathlib import Path
from tkinter import (Tk, ttk, Button, Label, Entry, END, W, messagebox)
from yt_streamgrabber import (StreamType, download_yt_stream, download_yt_streams_from_playlist)


class YTMainWindow:
    def set_text(self, entry, text):
        entry.delete(0,END)
        entry.insert(0,text)
        return
    
    
    def set_label(self, label, text):
        label['text'] = text
        return


    def __init__(self, window):
        self.bg_color = "#ece7f2"
        self.window = window
        self.setup_window()

        # 1st grid row
        #----------------------------------------------------------------
        self.lbl_url = Label(self.window, text="YT-URL:", bg=self.bg_color)
        self.lbl_url.grid(row=0, column=0, padx=10, pady=20)

        self.txt_url = Entry(width=60)
        self.txt_url.grid(row=0, column=1, padx=0, pady=20, sticky=W)

        self.cmd_paste_from_clipboard = Button(self.window, text="From clipboard...", command=self.paste_from_clipboard)
        self.cmd_paste_from_clipboard.grid(row=0, column=2, padx=15, pady=20, sticky=W)
        #----------------------------------------------------------------

        # 2nd grid row
        #----------------------------------------------------------------
        self.lbl_type = Label(self.window, text="Type:", bg=self.bg_color)
        self.lbl_type.grid(row=1, column=0, padx=0, pady=0)

        self.combobox = ttk.Combobox(self.window, state="readonly")
        self.combobox["values"] = ("Audio", "Video")
        self.combobox.current(0)
        self.combobox.grid(row=1, column=1, padx=0, pady=0, sticky=W)  

        style = ttk.Style()
        style.configure("TCheckbutton", indicatorbackground="black", indicatorforeground="white", background=self.bg_color, foreground="black")

        self.chk_playlist = ttk.Checkbutton(self.window, text="Playlist url", onvalue=1, offvalue=0)
        self.chk_playlist.grid(row=1, column=2, padx=15, pady=0, sticky=W)
        self.chk_playlist.state(['!alternate'])
        self.chk_playlist.state(['!selected'])
        #----------------------------------------------------------------

        # 3rd grid row
        #----------------------------------------------------------------
        self.lbl_folder = Label(self.window, text="Folder:", bg=self.bg_color)
        self.lbl_folder.grid(row=2, column=0, padx=0, pady=20)

        self.txt_folder = Entry(width=60)
        self.txt_folder.grid(row=2, column=1, padx=0, pady=0, sticky=W)
        self.txt_folder.bind('<Double-Button-1>', self.open_folder)

        self.cmd_download = Button(self.window, text="Download stream!", command=self.download)
        self.cmd_download.grid(row=2, column=2, padx=10, pady=0, sticky=W)     
        #----------------------------------------------------------------


    def setup_window(self):
        window_height = 150
        window_width = 573
        self.window.resizable(False, False) 

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))

        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))
        self.window.title(f"YT-Stream Downloader")
        self.window['background'] = self.bg_color
        #self.window.wm_attributes('-transparentcolor', window['bg']) <-- sets entire form transparent
        self.window.attributes('-topmost',True)


    def open_folder(self, event):
        folder = self.txt_folder.get()

        if folder == "" or not Path(folder).exists():
            subprocess.Popen(fr'explorer "{Path().resolve()}"')
        else:
            subprocess.Popen(fr'explorer "{folder}"')


    def paste_from_clipboard(self):
        self.set_text(self.txt_url, clipboard.paste())


    def download(self):
        stream_type = StreamType.Audio if self.combobox.current() == 0 else StreamType.Video
        url = self.txt_url.get()
        dest_folder = self.txt_folder.get()
        is_playlist_url = self.chk_playlist.instate(['selected'])

        # Perform multiple downloads (for each url in the playlist)
        if is_playlist_url:
            download_yt_streams_from_playlist(url, dest_folder=None, stream_type=stream_type)
            self.set_text(self.txt_result, "Downloads completed!")
        
        # Perform single download
        else:
            download_successful, msg = download_yt_stream(url=url, stream_type=stream_type, dest_folder=dest_folder)
            messagebox.showinfo("Download successful !", msg) if download_successful else messagebox.showerror("Download failed !", msg)


if __name__ == "__main__":
    app = Tk()
    YTMainWindow(app)
    app.mainloop()