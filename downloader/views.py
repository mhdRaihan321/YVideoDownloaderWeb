# views.py
import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DownloadForm
from pytube import YouTube

def home(requset):
    return render(requset, 'index.html')

def download_view(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            quality = form.cleaned_data['quality']

            try:
                # Create a YouTube object
                yt = YouTube(video_url)

                # Get the video title
                video_title = yt.title

                # Remove invalid characters from the video title
                valid_chars = '-_() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                video_title_cleaned = ''.join(c for c in video_title if c in valid_chars)

                if quality == "highest":
                    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                elif quality == "lowest":
                    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()
                else:
                    return HttpResponse("Invalid quality selection")
                if video_stream is None:
                    return HttpResponse("No video stream found")

                # Ask user for download location (optional)
                # download_dir = filedialog.askdirectory(initialdir="D:/Downloader", title="Select Download Directory")
                # You may choose to use a default directory or prompt the user for one
                download_directory = os.path.join("D:\YoutubeVideoDownloader" )
                if not os.path.exists(download_directory):
                    os.makedirs(download_directory)

                # Download the video
                video_stream.download(output_path=download_directory, filename=f"{video_title_cleaned}.mp4")

                # Optionally, you can provide a link for the user to download the file
                download_link = f'<a href="YoutubeVideoDownloader/{video_title_cleaned}.mp4" download>Download Video</a>'
                return render(request, 'download_success.html', {'video_title_cleaned': video_title_cleaned})

            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
    else:
        form = DownloadForm()
    return render(request, 'download_form.html', {'form': form},)
