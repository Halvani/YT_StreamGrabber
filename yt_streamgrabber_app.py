
from pathlib import Path
from tkinter import filedialog, messagebox
from ttkbootstrap.constants import LEFT, END
from yt_streamgrabber import (StreamType, download_yt_stream, download_yt_streams_from_playlist)

import subprocess
import tkinter as tk
import ttkbootstrap as ttk
import clipboard

class Window(ttk.Frame):
    def set_text(self, entry, text):
        entry.delete(0, END)
        entry.insert(0, text)
        return


    def set_label(self, label, text):
        label['text'] = text
        return


    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))

        self.master_window = master_window
        self.master_window.attributes('-topmost',True)
        self.master_window.place_window_center()


        #------------------------------------------------------------------------------
        self.frame_one = ttk.Frame(self.master_window)
        self.frame_one.pack()

        self.lbl_url = ttk.Label(self.frame_one, text="YT-URL:")
        self.lbl_url.pack(side=LEFT, padx=5, pady=10)

        self.txt_url = ttk.Entry(self.frame_one, width=60)
        self.txt_url.pack(side=LEFT, padx=5, pady=10)

        cmd_paste_from_clipboard = ttk.Button(self.frame_one,
                                              text="Paste from Clipboard...",
                                              command=self.paste_from_clipboard) #, bootstyle=SUCCESS)
        cmd_paste_from_clipboard.pack(side=LEFT, padx=5, pady=10)
        #------------------------------------------------------------------------------



        #------------------------------------------------------------------------------
        self.frame_two = ttk.Frame(self.master_window)
        self.frame_two.pack()

        self.lbl_stream_type = ttk.Label(self.frame_two, text="Stream type:")
        self.lbl_stream_type.pack(side=LEFT, padx=5, pady=10)

        self.combo_stream_type = ttk.Combobox(self.frame_two, state="readonly")
        self.combo_stream_type["values"] = ("Audio", "Video")
        self.combo_stream_type.current(0)
        self.combo_stream_type.pack(side=LEFT, padx=5, pady=10)

        style = ttk.Style()
        style.configure("TCheckbutton", indicatorbackground="black", indicatorforeground="white", foreground="black")

        self.chk_playlist = ttk.Checkbutton(self.frame_two, text="Playlist url", onvalue=1, offvalue=0)
        self.chk_playlist.state(['!alternate'])
        self.chk_playlist.state(['!selected'])
        self.chk_playlist.pack(side=LEFT, padx=5, pady=10)
        #------------------------------------------------------------------------------


        #------------------------------------------------------------------------------
        self.frame_three = ttk.Frame(self.master_window)
        self.frame_three.pack()

        self.lbl_folder = ttk.Label(self.frame_three, text="Destination folder:")
        self.lbl_folder.pack(side=LEFT, padx=5, pady=10)

        self.txt_folder = ttk.Entry(self.frame_three, width=60)
        self.txt_folder.bind('<Double-Button-1>', self.open_folder)
        self.txt_folder.pack(side=LEFT, padx=5, pady=10)

        self.cmd_folderpath = ttk.Button(self.frame_three, text="Select folder...", command=self.select_foldername)
        self.cmd_folderpath.pack(side=LEFT, padx=5, pady=10)
        self.set_text(self.txt_folder, Path(__file__).parent.resolve())
        #------------------------------------------------------------------------------

        #------------------------------------------------------------------------------
        self.frame_four = ttk.Frame(self.master_window)
        self.frame_four.pack()

        self.cmd_download = ttk.Button(self.frame_four, text="Download stream!", command=self.download)
        self.cmd_download.pack(side=LEFT, padx=5, pady=10)
        #------------------------------------------------------------------------------



    def select_foldername(self):
        folder_path = filedialog.askdirectory()
        self.set_text(self.txt_folder, folder_path)
        
    def paste_from_clipboard(self):
        self.set_text(self.txt_url, clipboard.paste())


    def open_folder(self, event):
        folder = self.txt_folder.get()

        if folder == "" or not Path(folder).exists():
            subprocess.Popen(fr'explorer "{Path().resolve()}"')
        else:
            subprocess.Popen(fr'explorer "{folder}"')

    def download(self):
        stream_type = StreamType.Audio if self.combo_stream_type.current() == 0 else StreamType.Video
        url = self.txt_url.get()
        dest_folder = self.txt_folder.get()
        is_playlist_url = self.chk_playlist.instate(['selected'])

        # Perform multiple downloads (for each url in the playlist)
        if is_playlist_url:
            download_yt_streams_from_playlist(url, dest_folder=None, stream_type=stream_type)
            #self.set_text(self.txt_result, "Downloads completed!")

        # Perform single download
        else:
            download_successful, msg = download_yt_stream(url=url, stream_type=stream_type, dest_folder=dest_folder)
            messagebox.showinfo("Download successful !", msg) if download_successful else messagebox.showerror("Download failed !", msg)




if __name__ == '__main__':
    app = ttk.Window(title="YT_StreamGrabber", size=(600, 200), resizable=(False, False))
    Window(app)
    app.mainloop()
