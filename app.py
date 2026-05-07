import streamlit as st
import plotly.graph_objects as go
import data

st.set_page_config(layout="wide")
states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]
job_roles = [
    "Data Analyst",
    "Software Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Machine Learning Engineer",
    "DevOps Engineer",
    "Other"
]
st.sidebar.title("CareerRadar")
st.sidebar.header("Tabs:")
tab=st.sidebar.radio(label="Tabs:",options=['Job Search','Skill Extractor','Role HeatMap','Trending Categories'],label_visibility="collapsed",)

if tab=="Job Search":
    st.title("💼 Job Finder")
    st.write("Search any job that fits you requirments")
    st.sidebar.divider()
    st.sidebar.header('🔍 Search')
    # st.sidebar.subheader("JOB Title / KEYWORDS")
    KeyWord=st.sidebar.text_input("JOB TITLE",placeholder="e.g. Python Developer")
    CompName=st.sidebar.text_input("COMPANY NAME",placeholder="e.g. Google")
    Location=st.sidebar.selectbox("LOCATION",states,placeholder="Select a State",index=None)
    st.sidebar.divider()
    st.sidebar.subheader('💰Salary')
    salary_range=st.sidebar.slider("ANNUAL SALARY RANGE ($)",min_value=0,max_value=500000,value=(50000,150000))
    st.sidebar.write(f"Selected range: {salary_range[0]} - {salary_range[1]}")
    st.sidebar.divider()
    st.sidebar.subheader('🎯Filter')
    contract_type=st.sidebar.selectbox("CONTRACT TYPE ",["Full Time","Part Time","Contract"],index=None,placeholder="Select Type")
    categories=st.sidebar.selectbox("CATEGORIES ",["Accounting & Finance Jobs","IT Jobs","Sales Jobs","Customer Services Jobs","Engineering Jobs","HR & Recruitment Jobs","Healthcare & Nursing Jobs","Hospitality & Catering Jobs","PR, Advertising & Marketing Jobs","Logistics & Warehouse Jobs","Teaching Jobs","Trade & Construction Jobs","Admin Jobs","Legal Jobs","Creative & Design Jobs","Graduate Jobs","Retail Jobs","Consultancy Jobs","Manufacturing Jobs","Scientific & QA Jobs","Social work Jobs","Travel Jobs","Energy, Oil & Gas Jobs","Property Jobs","Charity & Voluntary Jobs","Domestic help & Cleaning Jobs","Maintenance Jobs","Part time Jobs","Other/General Jobs","Unknown"],index=None,placeholder="Select Category")
    date_posted=st.sidebar.selectbox("ENTER DATE",["Any","3 Days","Last Week","Last Month","Last 3 Months","Last Year"],index=None,placeholder="Enter Date")
    st.sidebar.divider()
    search=st.sidebar.button("🔎 Search Jobs",help="Click to fetch jobs",use_container_width=True)
    if search:
        with st.spinner("Running..."):
            request,count=data.job_search(category=categories,KeyWord=KeyWord,CompName=CompName,Location=Location,salary_range=salary_range,contract_type=contract_type,date_posted=date_posted)
        if count!=0:
            if count<=100:
                st.success(f"Showing top {count} Results")
            elif count>100:
                st.success(f"Showing top 100 of {count} Results")
            for i in request:
                with st.expander(f"🏢 {i['company']['display_name']} | {i['title']} | 💵 {i['salary_min']}"):
                    st.write(f"{i['description']}")
        if count==0:
            st.error("No jobs found for these conditions")

elif tab=="Skill Extractor":
    st.title("🧠 Skill Extractor")
    st.write("Search any job role and see which skills employers actually ask for.")
    st.sidebar.divider()
    st.sidebar.header("Skill Extractor")
    job_role=st.sidebar.selectbox("JOB ROLE",job_roles,placeholder="Enter a Role",accept_new_options=True,index=None)
    location=st.sidebar.selectbox("LOCATION",states,placeholder="Select a State",index=None)
    Category=st.sidebar.selectbox("CATEGORIES ",["Accounting & Finance Jobs","IT Jobs","Sales Jobs","Customer Services Jobs","Engineering Jobs","HR & Recruitment Jobs","Healthcare & Nursing Jobs","Hospitality & Catering Jobs","PR, Advertising & Marketing Jobs","Logistics & Warehouse Jobs","Teaching Jobs","Trade & Construction Jobs","Admin Jobs","Legal Jobs","Creative & Design Jobs","Graduate Jobs","Retail Jobs","Consultancy Jobs","Manufacturing Jobs","Scientific & QA Jobs","Social work Jobs","Travel Jobs","Energy, Oil & Gas Jobs","Property Jobs","Charity & Voluntary Jobs","Domestic help & Cleaning Jobs","Maintenance Jobs","Part time Jobs","Other/General Jobs","Unknown"],index=None,placeholder="Select Category")
    st.sidebar.divider()
    run=st.sidebar.button("🔎 SEARCH",use_container_width=True)
    try:
        if run:
            if not job_role.strip():
                st.error("Job Role not entered")
            else: 
                with st.spinner(f"Scaning for job description {job_role}"):
                    jobs=data.skill_extractor(job_role,location=location,category=Category) 
                    if not jobs:
                        st.error("No jobs with these specific Filters")
                    else:
                        # st.write(jobs)
                        skills = list(jobs.keys())
                        mentions = list(jobs.values())
                        fig = go.Figure(data=go.Bar(
                        x=mentions,
                        y=skills,
                        orientation='h'
                        ))
                        fig.update_layout(
                            title=f"Highest Demand Skills for {job_role}",
                            xaxis_title="Mentions",
                            yaxis_title="Skills"
                        )
                        st.plotly_chart(fig,use_container_width=True)
    except:
        st.error("No skills found")    
                
elif tab=="Role HeatMap":
    st.title("🗺️ Role Demand Heatmap")
    st.write("See where in the US a skill is most in demand. Darker = more job listings.")
    st.sidebar.divider()
    st.sidebar.header("Skill Heatmap")
    job_role=st.sidebar.selectbox("JOB ROLE",job_roles,placeholder="Enter a Role",accept_new_options=True,index=None)
    selected_states = st.sidebar.multiselect("STATES TO CHECK", states, default=None,)
    st.sidebar.divider()
    run=st.sidebar.button("🔍 Search",use_container_width=True)
 
    if run:
        with st.spinner("Running..."):
            mentions=data.heat_map(job_role,selected_states)
        locations = [data.state_abr[s] for s in selected_states]
        counts = [mentions[data.state_abr[s]] for s in selected_states]
        fig = go.Figure(go.Choropleth(
                locations=locations,
                z=counts,
                locationmode="USA-states",
                colorscale="Blues",
                text=selected_states,
                colorbar_title="Job Listings",
            ))
        fig.update_layout(
                title=f'Job listings mentioning "{job_role}" by State',
                geo=dict(scope="usa", bgcolor="rgba(0,0,0,0)"),
            )        
        st.plotly_chart(fig, use_container_width=True)
elif tab=="Trending Categories":
    st.sidebar.divider()
    st.sidebar.header("Trending Categories")
    st.title("📈Trending Categories")
    st.write("See how job volume has changed over time across different industries.")
    role=st.sidebar.multiselect("CATEGORIES TO COMAPRE",data.category_map.keys(),placeholder="Select Catogies")
    search_time =int(st.sidebar.slider("Months to Search",3,24,12))
    st.sidebar.divider()
    run=st.sidebar.button("🔍 Fetch Trends",use_container_width=True)
    if run:
        with st.spinner("Fetching Historical data via Adzuna api..."):
            trends=data.trending_categories(role,search_time)
        fig = go.Figure()
        data_dict={}
        for i in range(len(role)):
            data_dict = trends[i]
            months = sorted(list(data_dict.keys()))
            values = sorted([data_dict[m] for m in months])
            fig.add_trace(go.Scatter(
                x=months,
                y=values,
                name=role[i],
                mode="lines+markers",
            ))
        fig.update_layout(
            title="Job Volume Over Time by Category",
            xaxis_title="Month",
            yaxis_title="Job Listings",
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)
