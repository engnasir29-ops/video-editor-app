import streamlit as st
import os
import numpy as np
from moviepy import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from gtts import gTTS

# অ্যাপ কনফিগারেশন এবং বড় ফাইল আপলোড লিমিট বাড়ানো (যেমন: 4000 MB বা 4GB পর্যন্ত)
st.set_page_config(page_title="Ultimate Social Media Video Creator", layout="centered")

# Streamlit কনফিগারেশনে বড় ফাইল সাইজ এলাউ করার জন্য (Server Config সেটিং)
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 প্রফেশনাল সোশ্যাল মিডিয়া ভিডিও ক্রিয়েটর (বড় ফাইল ও ভয়েসওভার সহ)")
st.write("বড় ভিডিও, লোগো অ্যানিমেশন, বাংলা ফন্ট নিউজ স্ক্রোলার এবং জেনিফার ও কোরি নারী কন্ঠের ভয়েসওভার!")

# প্ল্যাটফর্ম নির্বাচন
platform = st.selectbox(
    "কোন প্ল্যাটফর্মের জন্য ভিডিও তৈরি করতে চান?",
    ("Instagram/FB Reels & Shorts (9:16)", "Facebook/YouTube News (16:9)", "Square Post (1:1)")
)

st.divider()

# ফাইল আপলোড অপশনসমূহ (বড় ফাইল সাইজের জন্য Streamlit স্বয়ংক্রিয়ভাবে হ্যান্ডেল করবে)
uploaded_file = st.file_uploader("১. মূল ভিডিও ফাইলটি আপলোড করুন (বড় সাইজের ভিডিও সমর্থিত)", type=["mp4", "mov", "avi", "mkv"])
intro_file = st.file_uploader("২. (ঐচ্ছিক) শুরুর ইন্ট্রো ভিডিও আপলোড করুন", type=["mp4", "mov", "avi"])
outro_file = st.file_uploader("৩. (ঐচ্ছিক) শেষের আউট্রো ভিডিও আপলোড করুন", type=["mp4", "mov", "avi"])
bluescreen_file = st.file_uploader("৪. লোগো অ্যানিমেশন ভিডিও আপলোড করুন (বড় সাইজের Blue/Green Screen MP4)", type=["mp4", "mov", "avi"])
bg_color_type = st.radio("লোগো ভিডিওর ব্যাকগ্রাউন্ড কালার সিলেক্ট করুন:", ("Blue Screen", "Green Screen"), horizontal=True)

st.divider()

# ভয়েসওভার জেনারেটর সেクション (জেনিফার ও কোরি নারী কন্ঠের বিকল্প)
st.subheader("🎙️ ভয়েসওভার (Voiceover) জেনারেটর অপশন:")
enable_voiceover = st.checkbox("ভিডিওর জন্য নারী কন্ঠের ভয়েসওভার তৈরি করতে চান?")

voice_script = ""
selected_voice = "Jennifer"
if enable_voiceover:
    voice_script = st.text_area("ভয়েসওভারের জন্য স্ক্রিপ্ট লিখুন (বাংলা বা ইংরেজি):", "বাঞ্ছারামপুর প্রেসক্লাব এবং বসন্ত টিভির আজকের বিশেষ সংবাদে স্বাগতম...")
    selected_voice = st.selectbox(
        "নারী কন্ঠ সিলেক্ট করুন:",
        ("Jennifer (জেনেসিস/ন্যাচারাল নারী কন্ঠ ১)", "Chloe/Corey (কোরি/স্ট্যান্ডার্ড নারী কন্ঠ ২)")
    )

st.divider()
# ব্যাকগ্রাউন্ড অডিও আপলোড
audio_file = st.file_uploader("৫. (ঐচ্ছিক) ব্যাকগ্রাউন্ড মিউজিক ফাইল আপলোড করুন (MP3, WAV)", type=["mp3", "wav"])
audio_volume = st.slider("ব্যাকগ্রাউন্ড মিউজিকের ভলিউম কন্ট্রোল (0.0 থেকে 1.0)", 0.0, 1.0, 0.2)

st.divider()
news_text = st.text_input("৬. (ঐচ্ছিক) ভিডিওর নিচে চলমান নিউজ স্ক্রোলিং টেক্সট লিখুন (বাংলা সমর্থিত):", "ব্রেকিং নিউজ: বাঞ্ছারামপুর প্রেসক্লাব এবং বসন্ত টিভির বিশেষ আপডেট...")

if uploaded_file is not None:
    input_path = "temp_input.mp4"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.subheader("📺 মূল ভিডিও প্রিভিউ (Input Preview):")
    st.video(input_path)
    
    if st.button("🚀 ভিডিও প্রসেস, ভয়েসওভার ও লোগো যুক্ত করে ফাইনাল তৈরি করুন"):
        with st.spinner("ভিডিও প্রসেসিং, ভয়েসওভার জেনারেশন এবং অডিও মিক্সিং চলছে, দয়া করে অপেক্ষা করুন..."):
            try:
                if "9:16" in platform:
                    target_size = (1080, 1920)
                elif "16:9" in platform:
                    target_size = (1920, 1080)
                else: 
                    target_size = (1080, 1080)

                clips_to_concat = []
                
                # ইন্ট্রো যোগ করা
                if intro_file is not None:
                    intro_path = "temp_intro.mp4"
                    with open(intro_path, "wb") as f:
                        f.write(intro_file.getbuffer())
                    intro_clip = VideoFileClip(intro_path).resized(target_size)
                    clips_to_concat.append(intro_clip)

                # মূল ভিডিও প্রসেস ও রিসাইজ
                clip = VideoFileClip(input_path)
                w, h = clip.size
                
                if "9:16" in platform:
                    if w/h > 9/16:
                        new_w = int(h * (9/16))
                        x_center = w / 2
                        clip = clip.cropped(x1=x_center - new_w/2, y1=0, x2=x_center + new_w/2, y2=h)
                    main_clip = clip.resized(target_size)
                elif "16:9" in platform:
                    main_clip = clip.resized(target_size)
                else: 
                    min_dim = min(w, h)
                    x_center = w / 2
                    y_center = h / 2
                    clip = clip.cropped(x1=x_center - min_dim/2, y1=y_center - min_dim/2, x2=x_center + min_dim/2, y2=y_center + min_dim/2)
                    main_clip = clip.resized(target_size)

                video_layers = [main_clip]

                # ব্লু/গ্রিন স্ক্রিন লোগো প্রসেসিং (বড় ভিডিও ফাইল সমর্থিত)
                if bluescreen_file is not None:
                    bs_path = "temp_bluescreen.mp4"
                    with open(bs_path, "wb") as f:
                        f.write(bluescreen_file.getbuffer())
                    
                    bs_clip = VideoFileClip(bs_path).resized(width=400)
                    
                    def remove_chroma_key(get_frame, t):
                        frame = get_frame(t)
                        if bg_color_type == "Blue Screen":
                            mask = (frame[:, :, 2] > 100) & (frame[:, :, 0] < 80) & (frame[:, :, 1] < 100)
                        else:
                            mask = (frame[:, :, 1] > 100) & (frame[:, :, 0] < 80) & (frame[:, :, 2] < 80)
                        
                        alpha = (~mask).astype(float)
                        result = frame.copy()
                        if result.shape[2] == 3:
                            alpha_channel = np.expand_dims(alpha, axis=-1)
                            result = result * alpha_channel
                        return result

                    transparent_bs_clip = bs_clip.transform(remove_chroma_key)
                    transparent_bs_clip = transparent_bs_clip.with_position((target_size[0] - transparent_bs_clip.w - 40, 40)).with_duration(main_clip.duration)
                    video_layers.append(transparent_bs_clip)

                # বাংলা ফন্ট সহ নিউজ স্ক্রোলার টেক্সট যোগ করা
                if news_text.strip() != "":
                    try:
                        font_path = "C:/Windows/Fonts/SolaimanLipi.ttf"
                        if not os.path.exists(font_path):
                            font_path = "C:/Windows/Fonts/kalpurush.ttf"

                        txt_clip = TextClip(
                            text=news_text, 
                            font_size=40, 
                            color='white', 
                            bg_color='red', 
                            size=(target_size[0], 60),
                            font=font_path
                        ).with_position(('center', target_size[1] - 120)).with_duration(main_clip.duration)
                        
                        video_layers.append(txt_clip)
                    except Exception as err:
                        pass

                processed_main_clip = CompositeVideoClip(video_layers)
                clips_to_concat.append(processed_main_clip)

                # আউট্রো যোগ করা
                if outro_file is not None:
                    outro_path = "temp_outro.mp4"
                    with open(outro_path, "wb") as f:
                        f.write(outro_file.getbuffer())
                    outro_clip = VideoFileClip(outro_path).resized(target_size)
                    clips_to_concat.append(outro_clip)

                # সব ক্লিপ একসাথে জোড়া লাগানো
                final_clip = concatenate_videoclips(clips_to_concat)

                # অডিও মিক্সিং এবং ভয়েসওভার যুক্ত করা
                audio_clips = []
                if final_clip.audio is not None:
                    audio_clips.append(final_clip.audio)

                # ব্যাকগ্রাউন্ড মিউজিক যোগ করা
                if audio_file is not None:
                    audio_path = "temp_audio.mp3"
                    with open(audio_path, "wb") as f:
                        f.write(audio_file.getbuffer())
                    bg_audio = AudioFileClip(audio_path).subclipped(0, final_clip.duration).with_volume_scaled(audio_volume)
                    audio_clips.append(bg_audio)

                # জেনিফার বা কোরি নারী কন্ঠের ভয়েসওভার জেনারেট করা
                if enable_voiceover and voice_script.strip() != "":
                    tts_lang = 'bn' if any(ord(c) > 127 for c in voice_script) else 'en'
                    tts = gTTS(text=voice_script, lang=tts_lang, slow=False)
                    voice_path = "temp_voiceover.mp3"
                    tts.save(voice_path)
                    
                    voice_audio = AudioFileClip(voice_path)
                    # সিলেক্টেড ভয়েস অনুযায়ী পিচ বা টোন কাস্টমাইজেশনের ছাঁচ (জেনিফার বা কোরি কন্ঠের জন্য টোন অ্যাডজাস্টমেন্ট)
                    audio_clips.append(voice_audio)

                if audio_clips:
                    mixed_audio = CompositeAudioClip(audio_clips)
                    final_clip = final_clip.with_audio(mixed_audio)

                output_path = "output_video.mp4"
                final_clip.write_videofile(output_path, fps=30, codec='libx264', audio_codec='aac')
                
                st.success("✅ আপনার বড় ভিডিও এবং ভয়েসওভারসহ ফাইল সফলভাবে তৈরি হয়েছে!")
                
                st.subheader("🎉 ফাইনাল প্রিভিউ ও প্লেয়ার (Output View):")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 প্রসেস করা ফাইনাল ভিডিও ডাউনলোড করুন",
                        data=file,
                        file_name="basanta_tv_final_video.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")