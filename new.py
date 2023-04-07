import os
import streamlit as st
import main
from streamlit_player import st_player
from streamlit_option_menu import option_menu
from PIL import Image 

st.set_page_config(page_title="Summerizer" , page_icon=":mask:" , layout="centered")
st.title(":blue[Video Transcript Summarizer]")
selected=option_menu(
    menu_title="",
    options=["Home","Translate"],
    default_index=0,
    orientation="horizontal",
)

if 'output' not in st.session_state:
    st.session_state['output']=""
link=""
if(selected=="Home"):
    with st.container():
        st.write("---")
        #a=st.radio("Choose method:",("Have a URL","Have the Audio File"))
        a=st.radio("Choose method:",["Have a URL","Have the Audio File"])
        #text_input=st.text_input("Enter URL:")
        if a=="Have a URL":
            link=""
            link=st.text_input("Enter URL:")
            if link:
                st_player(link)
                with st.spinner("Generating transcript..."):
                    st.session_state.output=main.get_transcript(link)
                expander = st.expander("See full Transcript")
                expander.write(st.session_state.output)
                # print(st.session_state.output)
        elif(a=="Have the Audio File"):
            #upload=st.file_uploader('upload your file here')
            upload=st.file_uploader('upload your file here',type=["mp3"])
            if upload is not None:
                with open(os.path.join(os.getcwd(), 'audio_file.mp3'), 'wb') as f:
                    f.write(upload.getbuffer())
                st.success(f"File uploaded successfully.")    
                with st.spinner("Processing audio file..."):
                    audio_text = main.audio_to_text(upload, True)
                
                st.write(audio_text)
                st.session_state.output=audio_text
if(selected=="Translate"):
    #st.write(res)
    st.header("select any of the languages")
    options = ['Telugu', 'Hindi', 'Tamil' , 'English']
    selected_option = st.selectbox('', options)
    if st.session_state.output:
        translated_text = main.translate_transcript(st.session_state.output, selected_option)
        st.session_state.output = translated_text
        expand=st.expander("See Translated text")
        expand.write(translated_text)
        st.download_button('Download', translated_text)
        with st.spinner("Generating audio file..."):    
            main.text_to_speech(translated_text, selected_option) 
        st.audio("savedaudiofile.mp3")

