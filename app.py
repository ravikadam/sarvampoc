import streamlit as st
import os
from models import Profile
from api_utils import speech_to_text, text_to_speech
from extractor import ProfileExtractor
import json
from audiorecorder import audiorecorder
import random

def get_missing_field_question(profile: Profile) -> str:
    """Generate a question about missing profile information"""
    missing_fields = []
    
    if not profile.name:
        missing_fields.append(("name", "What is your name?"))
    if not profile.gender:
        missing_fields.append(("gender", "What is your gender?"))
    if not profile.age:
        missing_fields.append(("age", "How old are you?"))
    if not profile.mobile_number:
        missing_fields.append(("mobile", "What is your mobile number?"))
    if not profile.email:
        missing_fields.append(("email", "What is your email address?"))
    if not profile.address.state:
        missing_fields.append(("state", "Which state do you live in?"))
    if not profile.address.city:
        missing_fields.append(("city", "Which city do you live in?"))
    if not profile.address.zipcode:
        missing_fields.append(("zipcode", "What is your zipcode?"))
    if not profile.address.location:
        missing_fields.append(("location", "What is your area or locality name?"))
    if not profile.address.building_name:
        missing_fields.append(("building", "What is your building or apartment name?"))
    if not profile.address.house_number:
        missing_fields.append(("house", "What is your house or flat number?"))
    
    if not missing_fields:
        return "Thank you! I have all the information I need. Is there anything else you'd like to tell me?"
    
    # Select a random missing field and its question
    field, question = random.choice(missing_fields)
    
    # Add context to make the conversation more natural
    context_phrases = [
        f"I notice I don't have your {field} yet. {question}",
        f"Could you please tell me {question.lower()}",
        f"I'd like to know {question.lower()}",
        f"Let's fill in some more details. {question}"
    ]
    
    return random.choice(context_phrases)

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = Profile()
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Initialize the profile extractor
extractor = ProfileExtractor(os.getenv('OPENAI_API_KEY'))

st.title("Voice Chat Profile Builder")

# Create two columns for layout
col1, col2 = st.columns([7, 3])

with col1:
    st.subheader("Conversation")
    
    # Audio input using audiorecorder
    audio_input = audiorecorder("Click to record", "Recording...")
    
    if len(audio_input) > 0:
        # Convert audio data to bytes
        audio_bytes = audio_input.export(format="wav").read()
        
        # Convert speech to text
        text = speech_to_text(audio_bytes)
        if text:
            st.session_state.conversation.append({"role": "user", "content": text})
            
            # Extract profile information
            st.session_state.profile = extractor.extract_profile_info(
                text, 
                st.session_state.profile
            )
            
            # Generate bot response based on missing information
            bot_response = get_missing_field_question(st.session_state.profile)
            st.session_state.conversation.append({"role": "assistant", "content": bot_response})
            
            # Convert bot response to speech
            audio_response = text_to_speech(bot_response)
            if audio_response:
                st.audio(audio_response, format="audio/wav")
    
    # Display conversation history
    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.write(message["content"])

with col2:
    st.subheader("Profile Information")
    profile_data = st.session_state.profile.model_dump()
    
    # Display profile information in a more readable format
    st.write("Basic Information:")
    st.write(f"Name: {profile_data['name'] or 'Not provided'}")
    st.write(f"Gender: {profile_data['gender'] or 'Not provided'}")
    st.write(f"Age: {profile_data['age'] or 'Not provided'}")
    st.write(f"Mobile: {profile_data['mobile_number'] or 'Not provided'}")
    st.write(f"Email: {profile_data['email'] or 'Not provided'}")
    
    st.write("Address Information:")
    address = profile_data['address']
    st.write(f"State: {address['state'] or 'Not provided'}")
    st.write(f"City: {address['city'] or 'Not provided'}")
    st.write(f"Zipcode: {address['zipcode'] or 'Not provided'}")
    st.write(f"Location: {address['location'] or 'Not provided'}")
    st.write(f"Building: {address['building_name'] or 'Not provided'}")
    st.write(f"House No: {address['house_number'] or 'Not provided'}")
    
    # Progress indicator
    st.write("Profile Completion:")
    completion_percentage = sum(1 for v in st.session_state.profile.model_dump(exclude_none=True).values() if v) / 11 * 100
    st.progress(completion_percentage / 100) 