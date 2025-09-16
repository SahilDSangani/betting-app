import streamlit as st

st.title("My First Streamlit App 🎲")
st.write("Welcome to my betting app prototype!")

bet_amount = st.number_input("Enter your bet amount:", min_value=0, value=10)
team_choice = st.selectbox("Pick a team:", ["Team A", "Team B"])

if st.button("Place Bet"):
    st.success(f"You bet ${bet_amount} on {team_choice}")

