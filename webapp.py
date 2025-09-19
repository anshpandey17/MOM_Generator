

import google.generativeai as genai
import os
import streamlit as st
from pdfextractor import text_extractor_pdf
from docxexctractor import text_extracor_docx
from imageextractor import extract_text_image

# Configure the Model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key='AIzaSyAd0ryPa58oDWVJOOlyck11oOPMHnJn2_A')

model = genai.GenerativeModel('gemini-2.5-flash-lite')



# upload a file in sidebar
user_text = None
st.sidebar.title(':orange[Upload your MoM Notes here:]')
st.sidebar.subheader('Only Upload Images, PDFs and DOCX')
user_file = st.sidebar.file_uploader('Upload your file', type=['pdf','docx','jpg','jpeg'])
if user_file:

  if user_file.type == 'application/pdf':
    user_text = text_extractor_pdf(user_file)
  elif user_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    user_text = text_extractor_docx(user_file)
  elif user_file.type in ['image/jpg','image/jpeg','image/png']:
    user_text = extract_text_image(user_file)

  else:
        st.write("Upload Correct File Format")

   


# Main Page
st.title(':blue[Minutes of Meeting]: :green[AI Assisted MoM generator in standardized form]')
tips = ''' Tips to use this app 
* Upload your Notes in sidebar (Image, PDF or DOCX)
* Click on generate MoM and get the standardized Mom's '''

st.write(tips)
if st.button('Generate MoM'):
  if user_text is None:
    st.error('Text is not generated')

  else:
    with st.spinner('Processing your dara...'):
       prompt = f'''Assume you are expert in creating Minutes of meeting, user has privided notes of a meeting in text format.
        using this data you need to create a standardized minutes of meeting for the user. 
        output must follow word/docx format, strictly in the following mannere.
        title : Title of Meeting
        Heading : Meeting Agenda
        Subheading : Name of Attendees (if attendees name is not there keep it NA)
        subheading : date of meeting and place of meeting(pplace means name of conference room if not provided keep t online )
        Body : the body must follow the following sequence of points.
        * Key points discussed
        * highlight any decision that has finalized
        * mention actionable items
        * any additional notes.
        * any deadline that has been discussed
        * any next meeting date that has been discussed.
        * 2-3 lines of summary
        * use bullet points and highlight or bold the keywords such that context is clear.
        * Generate the output in such a way that it can be copied and paste in word


        the data provided by user is as follows
        {user_text}  '''
       response = model.generate_content(prompt)
       st.write(response.text)

       st.download_button(label='Click to Download',
                          data = response.text,
                          file_name = 'MoM.text',
                          mime= 'text/plain')
       
        
       











