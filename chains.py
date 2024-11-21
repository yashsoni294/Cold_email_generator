import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.1,
        groq_api_key = os.getenv("GROQ_API_KEY"),
        model_name = "llama-3.1-70b-versatile"
        )
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """### SCRAPED TEXT FROM WEBSITE:
            ### INSTRUCTION:
            The scraped text is from the career's page of a website. Below is the job description text extracted from the page:
            {page_data}
            Your task is to extract the job posting information and return a JSON object containing the following keys: 
            - 'role'
            - 'experience'
            - 'skills'
            - 'description'

            Only return a valid JSON object, without any additional text or comments.

            ### VALID JSON (NO PREAMBLE):
            """
            )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Content is too big. Unable to parse jobs.")
        
        return res if isinstance(res, list) else [res]
        # return res
    
    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
                ### JOB DESCRIPTION:
                {job_description}
        
                ### INSTRUCTION:
                You are Suresh Sharma, a business development executive at Samta Infotech Pvt Ltd. Samta Infotech Pvt Ltd. is an AI & Software 
                Consulting company dedicated to 
                facilitating
                the seamless integration of business processes through automated tools. 
                Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
                process optimization, cost reduction, and heightened overall efficiency. 
                Your job is to write a cold email to the client regarding the job mentioned above describing the capability of 
                Samta Infotech Pvt Ltd 
                in fulfilling their needs.
                Also add the most relevant ones from the following links to showcase Samta Infotech Pvt Ltd's portfolio: {link_list}
                Remember you are Mohan, BDE at Samta Infotech Pvt Ltd. 
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):
        
            """)

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description" : str(job), "link_list" : links})
        return res.content
        

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))