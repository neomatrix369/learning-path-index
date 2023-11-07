import streamlit as st

# Define your Streamlit app and return the input variable   
def app():
    # Add a title to your app
    st.title("KaggleX Learning Path Index Search")

    # Add some text to your app
    st.write("Embark your Learning Path Journey with right search !!")

    # Add a text input to your app
    user_input = st.text_input("Enter your course query here")

    # Store the input in a variable
    my_variable = user_input
    # Display the stored variable
    # st.write(f"The stored variable is: {my_variable}")
    
    return my_variable

# Run your Streamlit app
# if __name__ == "__main__":
#     var = app()
#     print(var)