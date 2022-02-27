import streamlit as st 
from pytube import YouTube
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi


nav = st.sidebar.radio("Navigation ", ["Home", "About us"], index=1)

if nav == "Home":
    v2 = st.sidebar.selectbox("Select one feature", [
                              "Youtube_Video_Downloader", "Youtube_Text_summarziation", "Text_Summarization"], index=0)
    if v2 == "Youtube_Video_Downloader":

        st.title("Youtube Video Downloader")
        st.subheader("Enter the URL:")
        url = st.text_input(label='URL')
        yt = YouTube(url)
        print(yt.streams)

        if url != '':
            yt = YouTube(url)
            st.image(yt.thumbnail_url, width=300)
            st.subheader('''
            {}
            ## Length: {} seconds
            ## Rating: {} 
            '''.format(yt.title, yt.length, yt.rating))
            video = yt.streams
            if len(video) > 0:
                downloaded, download_audio = False, False
                download_video = st.button("Download Video")
                if yt.streams.filter(only_audio=True):
                    download_audio = st.button("Download Audio Only")
                if download_video:
                    video.get_lowest_resolution().download()
                    downloaded = True
                if download_audio:
                    video.filter(only_audio=True).first().download()
                    downloaded = True
                if downloaded:
                    st.subheader("Download Complete")
            else:
                st.subheader("Sorry, this video can not be downloaded")
    if v2 == "Youtube_Text_summarziation":

        st.title("YouTube text summarizer")
        youtube_video = st.text_input("Enter the Youtube video URL:")
        # Embed a youtube video
        st.video(youtube_video)

        video_id = youtube_video.split("=")[1]

        YouTubeTranscriptApi.get_transcript(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # converting to txt file and adding 'text' whenever we encounter text.
        result = ""
        for i in transcript:
            result += ' ' + i['text']
        # print(result)
        st.write(''' # Total no. of characters = {}'''.format(
            len(result)))  # 14521 characters
        # transcript part is finished now.
        summarizer = pipeline('summarization')
        # summarizing using transformer's summary pipeline by default it is using bart model with pytorch model. We can use T5 with tensor flow.

        if (len(result) > 1000):
            # 1000 characters of batch size in this case of 14521 we will iterate 14 or 15 times
            num_iters = int(len(result)/1000)
            summarized_text = []            # empty list to have the summarized text
            for i in range(0, num_iters + 1):
                start = 0
                start = i * 1000
                end = (i + 1) * 1000
                print("input text : \n" + result[start:end])
                out = summarizer(result[start:end])
                out = out[0]
                out = out['summary_text']
                print("Summarized text :\n"+out)
                summarized_text.append(out)
        else:
            out = summarizer(result[0:-1])
            out = out[0]
            out = out['summary_text']
            print("Summarized text :\n"+out)
            summarized_text = out

            # print(summarized_text)

        st.subheader(''' Length of summarized text(no. of characters) : {} '''.format(
            len(str(summarized_text))))
        st.subheader(''' Summarized text : {} '''.format(str(summarized_text)))
    if v2 == "Text_Summarization":

        st.title(" Text summarizer")
        txt = st.text_area("Enter the text here:", height=50)

        result = ""
        result = txt

        st.write(''' ## Total no. of Characters = {}'''.format(
            len(result)))  # 14521 words

        summarizer = pipeline('summarization')
        # summarizing using transformer's summary pipeline by default it is using bart model with pytorch model. We can use T5 with tensor flow.

        if (len(result) > 1000):
            # 1000 characters of batch size in this case of 14521 we will iterate 14 or 15 times
            num_iters = int(len(result)/1000)
            summarized_text = []            # empty list to have the summarized text
            for i in range(0, num_iters + 1):
                start = 0
                start = i * 1000
                end = (i + 1) * 1000
                print("input text : \n" + result[start:end])
                out = summarizer(result[start:end])
                out = out[0]
                out = out['summary_text']
                print("Summarized text :\n"+out)
                summarized_text.append(out)
        else:
            out = summarizer(result[0:-1])
            out = out[0]
            out = out['summary_text']
            print("Summarized text :\n"+out)
            summarized_text = out

            # print(summarized_text)

        st.subheader(''' Length of summarized text(No. of characters) : {} '''.format(
            len(str(summarized_text))))
        st.subheader(''' Summarized text : {} '''.format(str(summarized_text)))


if nav == "About us":
    st.markdown(' **It is a multi featured app.  \n It has various options like Text summarization, YouTube Transcript summarization and YouTube video Downloader. Through this project we have implemented the text summarization methodology by which we can obtain the summaries of any long article or any YouTube video having transcript** ')
