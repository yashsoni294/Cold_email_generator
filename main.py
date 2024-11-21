import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader


def create_streamlit_app(llm, portfolio, clean_text):
    
    st.title("Cold Mail Generator")
    url_input = st.text_input("Enter a  URL:", value=r"https://jobs.lever.co/paytm/43e1a748-88e0-4068-a934-8e519a72982b")
    submit_button = st.button("Submit")
    
    if submit_button:
        
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            # st.write(data)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            for job in jobs:
                # st.write(job)
                # skills = job.get(("skills", []))
                # st.write(job)
                skills = job["skills"]
                links = portfolio.query_links(skills)
                email = llm.write_email(job, links)
                st.code(email, language="markdown")
        except Exception as e:
            st.error(f"An Error Occurred : {e}")
        
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon=" ")
    create_streamlit_app(chain, portfolio, clean_text)
