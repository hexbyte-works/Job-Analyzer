import os
from dotenv import load_dotenv
import requests 
import re
import streamlit as st


load_dotenv()

YOUR_APP_ID = os.getenv("YOUR_APP_ID") or st.secrets["YOUR_APP_ID"]
YOUR_APP_KEY = os.getenv("YOUR_APP_KEY") or st.secrets("YOUR_APP_KEY")

skills = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go",
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB",
    ],
    "Web / Frameworks": [
        "React", "Angular", "Vue", "Django", "Flask", "FastAPI", "Node.js",
        "Express", "Spring", "Laravel", "Next.js", "REST", "GraphQL",
    ],
    "Data & Analytics": [
        "SQL", "Excel", "Tableau", "Power BI", "Pandas", "NumPy", "Spark",
        "Hadoop", "Kafka", "dbt", "Looker", "SAS", "SPSS",
    ],
    "Machine Learning / AI": [
        "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch",
        "Scikit-learn", "Keras", "LLM", "Computer Vision", "MLOps",
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
        "CI/CD", "Jenkins", "Git", "Linux", "Ansible", "Helm",
    ],
    "Databases": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Cassandra", "Oracle", "DynamoDB", "Snowflake", "BigQuery",
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Agile", "Scrum", "Project Management", "Presentation",
    ],
}

all_skills = [skill for group in skills.values() for skill in group]

state_abr = {
    "Alabama": "AL",        "Alaska": "AK",         "Arizona": "AZ",
    "Arkansas": "AR",       "California": "CA",      "Colorado": "CO",
    "Connecticut": "CT",    "Delaware": "DE",        "Florida": "FL",
    "Georgia": "GA",        "Hawaii": "HI",          "Idaho": "ID",
    "Illinois": "IL",       "Indiana": "IN",         "Iowa": "IA",
    "Kansas": "KS",         "Kentucky": "KY",        "Louisiana": "LA",
    "Maine": "ME",          "Maryland": "MD",        "Massachusetts": "MA",
    "Michigan": "MI",       "Minnesota": "MN",       "Mississippi": "MS",
    "Missouri": "MO",       "Montana": "MT",         "Nebraska": "NE",
    "Nevada": "NV",         "New Hampshire": "NH",   "New Jersey": "NJ",
    "New Mexico": "NM",     "New York": "NY",        "North Carolina": "NC",
    "North Dakota": "ND",   "Ohio": "OH",            "Oklahoma": "OK",
    "Oregon": "OR",         "Pennsylvania": "PA",    "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD",    "Tennessee": "TN",
    "Texas": "TX",          "Utah": "UT",            "Vermont": "VT",
    "Virginia": "VA",       "Washington": "WA",      "West Virginia": "WV",
    "Wisconsin": "WI",      "Wyoming": "WY",
}

category_map = {
    "Accounting & Finance Jobs": "accounting-finance-jobs",
    "Admin Jobs": "admin-jobs",
    "Charity & Voluntary Jobs": "charity-voluntary-jobs",
    "Consultancy Jobs": "consultancy-jobs",
    "Creative & Design Jobs": "creative-design-jobs",
    "Customer Services Jobs": "customer-services-jobs",
    "Domestic help & Cleaning Jobs": "domestic-help-cleaning-jobs",
    "Energy, Oil & Gas Jobs": "energy-oil-gas-jobs",
    "Engineering Jobs": "engineering-jobs",
    "Graduate Jobs": "graduate-jobs",
    "Healthcare & Nursing Jobs": "healthcare-nursing-jobs",
    "Hospitality & Catering Jobs": "hospitality-catering-jobs",
    "HR & Recruitment Jobs": "hr-recruitment-jobs",
    "IT Jobs": "it-jobs",
    "Legal Jobs": "legal-jobs",
    "Logistics & Warehouse Jobs": "logistics-warehouse-jobs",
    "Maintenance Jobs": "maintenance-jobs",
    "Manufacturing Jobs": "manufacturing-jobs",
    "Other/General Jobs": "other-general-jobs",
    "Part time Jobs": "part-time-jobs",
    "PR, Advertising & Marketing Jobs": "pr-advertising-marketing-jobs",
    "Property Jobs": "property-jobs",
    "Retail Jobs": "retail-jobs",
    "Sales Jobs": "sales-jobs",
    "Scientific & QA Jobs": "scientific-qa-jobs",
    "Social work Jobs": "social-work-jobs",
    "Teaching Jobs": "teaching-jobs",
    "Trade & Construction Jobs": "trade-construction-jobs",
    "Travel Jobs": "travel-jobs",
    "Unknown": "unknown"
}


def job_search(category=None,KeyWord=None,CompName=None,Location=None,salary_range=None,contract_type=None,date_posted=None):
    output=[]
    add=""
    if category:
        mapped = category_map.get(category)
        if mapped:
            add += f"&category={mapped}" 
    if KeyWord:
        add +=f"&title_only={KeyWord}" 
    if CompName:
        add+=f"&company={CompName}"
    if Location:
        add+=f"&where={Location}"
    if salary_range:
        add+=f"&salary_min={salary_range[0]}&salary_max={salary_range[1]}"
    if contract_type:
        if contract_type=="Full Time":
            add += "&full_time=1"
        elif contract_type=="Part Time":
            add += "&part_time=1"
        elif contract_type=="Contract":
            add += "&contract=1"
    if date_posted and date_posted!="Any":
        if date_posted == "3 Days":
            add += "&max_days_old=3"
        elif date_posted == "Last Week":
            add += "&max_days_old=7"
        elif date_posted == "Last Month":
            add += "&max_days_old=30"
        elif date_posted == "Last 3 Months":
            add += "&max_days_old=90"
        elif date_posted == "Last Year":
            add += "&max_days_old=365"
    count=max_runs=no_of_runs=0
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}&results_per_page=2"
    url = url + add
    request=requests.get(url)
    result = request.json()
    count=int(result["count"])
    if count==0:
        return [],0
    elif count>=100:
        no_of_runs=10
    elif count<100 and count>=10:
        no_of_runs=count//10
    elif count<10:
        no_of_runs=1
        max_runs=count
    if max_runs==0:        
        for i in range(1,no_of_runs+1):
            url = f"https://api.adzuna.com/v1/api/jobs/us/search/{i}?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
            url = url + add
            request=requests.get(url)
            result = request.json()
            for j in range(0,10):
                output.append(result["results"][j])
    elif max_runs!=0:
        url = url + add
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
        url = url + add
        request=requests.get(url)
        result = request.json()
        for j in range(0,max_runs):
            output.append(result["results"][j])      
    return output,count

def skill_extractor(job_role,location=None,category=None):
    jobs={}
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
        add=""
        add +=f"&title_only={job_role}" 
        if category:
            mapped = category_map.get(category)
            if mapped:
                add += f"&category={mapped}" 
        if location:
            add+=f"&where={location}"
        request=requests.get(f'{url}&results_per_page=2{add}')
        result = request.json()
        count=int(result["count"])
        no_of_runs=1 if count//10==0 else min(5, count//10)
        for j in range(no_of_runs):
            url = f"https://api.adzuna.com/v1/api/jobs/us/search/{j+1}?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
            url+=add
            request=requests.get(url)
            result = request.json()
            for i in result['results']:
                text= str(i["title"]) + str(i['description'])
                text= text.lower()
                for skill in all_skills:
                    pattern=r'\b' + re.escape(skill.lower()) + r'\b'
                    match= re.findall(pattern,text)
                    if match:
                        if skill in jobs:
                            jobs[skill] += len(match)
                        else:
                            jobs[skill] = len(match)
        return jobs
    except:
        return {}

def heat_map(job_role,location):
    mentions={}
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}"
    url+=f"&title_only={job_role}"
    for state in location:
        try:
            request=requests.get(f'{url}&where={state}&results_per_page=2')
            result = request.json()
            count=int(result["count"])
            mentions[state_abr[state]]=count
        except:
            mentions[state_abr[state]]=0
    return mentions

def trending_categories(roles,search_time):
    history=[]
    for role in roles:
        url = f"https://api.adzuna.com/v1/api/jobs/gb/history?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}&category={category_map.get(role)}&months={search_time}"
        request=requests.get(url)
        result=request.json()
        history.append(result['month']) 
    return history