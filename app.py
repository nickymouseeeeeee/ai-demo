import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(
    page_title="LM WN AI Fast Track", 
    layout="wide", 
    page_icon="🛵",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit header, menu, and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="stHeader"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Function to initialize or reset mock data
def init_mock_data():
    st.session_state.restaurants = [
        {
            "id": "RES-8803",
            "name": "Chill Bar & Bistro", 
            "status": "Requires Review", 
            "risk": "Medium", 
            "issue": "Agent B: Vision AI detected alcohol as the Hero Image (violates pg 4 of Checklist).", 
            "image": "beer.png",
            "agent_a_flag": False,
            "agent_b_flag": True,
            "agent_c_flag": False
        },
        {
            "id": "RES-8801",
            "name": "Krapao Station", 
            "status": "Auto-Approved", 
            "risk": "Low", 
            "issue": None, 
            "image": None,
            "agent_a_flag": False,
            "agent_b_flag": False,
            "agent_c_flag": False
        },
        {
            "id": "RES-8802",
            "name": "Ghost Kitchen 99 (Duplicate)", 
            "status": "Requires Review", 
            "risk": "High", 
            "issue": "Agent A: Exact match found in Wongnai Blacklist DB (Known Fraudulent Entity).", 
            "image": None,
            "agent_a_flag": True,
            "agent_b_flag": False,
            "agent_c_flag": False
        },
        {
            "id": "RES-8804",
            "name": "Noodle Express", 
            "status": "Requires Review", 
            "risk": "High", 
            "issue": "Agent C: OCR Engine scored menu legibility at 0.35 (Unreadable - violates pg 12 of Checklist).", 
            "image": "blurry.png",
            "agent_a_flag": False,
            "agent_b_flag": False,
            "agent_c_flag": True
        }
    ]

# Mock Data (Pre-processed by AI Fast Track)
if 'restaurants' not in st.session_state:
    init_mock_data()

def show_main_dashboard():
    col_title, col_reset = st.columns([5, 1.5])
    with col_title:
        st.title("🛵 LINE MAN Wongnai: AI Fast Track Dashboard")
    with col_reset:
        st.write("") # Spacing
        st.markdown("<p style='text-align: right; font-size: 12px; margin-bottom: 0px;'>กรุณากดปุ่ม Reset ทุกครั้งที่เข้าใช้ Demo</p>", unsafe_allow_html=True)
        if st.button("🔄 Reset Demo", use_container_width=True):
            init_mock_data()
            st.rerun()

    st.markdown("""
    **Restaurant Content Validation**
    
    This AI-driven workflow reduces the manual validation bottleneck from **3-5 days to under 5 minutes**. 
    It ingests data from Salesforce and Google Drive, processes it through specialized AI agents against the 15-page brand checklist, and routes only exceptions to human agents.
    """)
    
    st.subheader("📋 Exception Queue: Awaiting Human Validation")
    
    # Filter only those requiring review
    review_queue = [res for res in st.session_state.restaurants if res["status"] == "Requires Review"]
    
    if not review_queue:
        st.success("🎉 All caught up! No restaurants currently require human review. The 3-5 day backlog is clear.")
    else:
        # Display as a table/list
        for res in review_queue:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                with col1:
                    st.markdown(f"**{res['id']}**")
                with col2:
                    st.markdown(f"{res['name']}")
                with col3:
                    if res["risk"] == "High":
                        st.error(f"Risk: {res['risk']}")
                    else:
                        st.warning(f"Risk: {res['risk']}")
                with col4:
                    if st.button("Investigate 🔍", key=f"btn_{res['id']}"):
                        st.session_state.selected_res_id = res["id"]
                        st.rerun()
                        
    st.divider()
    st.subheader("✅ Fast Tracked (Auto-Approved)")
    approved_queue = [res for res in st.session_state.restaurants if res["status"] == "Auto-Approved"]
    for res in approved_queue:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 3])
            with col1:
                st.markdown(f"**{res['id']}**")
            with col2:
                st.markdown(f"{res['name']}")
            with col3:
                st.success("Auto-Approved (Passed all 15-page PDF Checklist rules)")

def show_case_detail(res_id):
    res = next((r for r in st.session_state.restaurants if r["id"] == res_id), None)
    
    if not res:
        st.error("Restaurant not found.")
        if st.button("Back to Dashboard"):
            st.session_state.selected_res_id = None
            st.rerun()
        return

    st.button("⬅️ Back to Dashboard", on_click=lambda: st.session_state.pop('selected_res_id', None))
    
    st.title(f"Investigating: {res['name']} ({res['id']})")
    
    # Context
    st.markdown("**Data Sources Ingested:** Salesforce CRM Data & Google Drive Images")
    
    # Display AI Audit Results
    st.subheader("🧠 Parallel AI Audit Results")
    
    colA, colB, colC = st.columns(3)
    
    with colA:
        with st.container(border=True):
            st.markdown("##### 🕵️ Agent A: Database Search")
            st.caption("Checks Wongnai Database for Blacklist/Duplicates")
            if res["agent_a_flag"]:
                st.error("❌ Flag: Match found in Wongnai Blacklist DB!")
            else:
                st.success("✅ Clear: No fraudulent entities found")
            
    with colB:
        with st.container(border=True):
            st.markdown("##### 👁️ Agent B: Vision AI")
            st.caption("Scans Google Drive photos for Checklists (Watermarks/Alcohol)")
            if res["agent_b_flag"]:
                st.warning("⚠️ Flag: Alcohol detected as Hero Image")
            else:
                st.success("✅ Clear: Brand guidelines met")

    with colC:
        with st.container(border=True):
            st.markdown("##### 📝 Agent C: OCR Engine")
            st.caption("Parses menu text legibility")
            if res["agent_c_flag"]:
                st.error("❌ Flag: Menu text unreadable")
            else:
                st.success("✅ Clear: Menu legible")

    st.divider()
    
    st.subheader("📊 The Translator: GenAI Summary")
    
    summary_text = res["issue"]
    st.info(f"**🤖 AI Conclusion against 15-page Checklist:** {summary_text}")
    
    # Show image if available for the flagged case
    if res.get("image") and os.path.exists(res["image"]):
        st.markdown(f"**🔍 Google Drive Evidence:** `{res['image']}`")
        st.image(res["image"], caption=f"Flagged evidence for {res['name']}", width=400)

    st.divider()
    
    # Human Review Dashboard Actions
    st.subheader("4️⃣ Human Review Decision")
    
    # Extract the rational for rejection
    rational = res['issue'].split(': ', 1)[1] if ': ' in res['issue'] else res['issue']
    
    st.markdown("### Failure Rationale")
    st.error(f"**Reason:** {rational}")
    
    st.markdown("### Draft Communication to Merchant")
    draft_email = f"Dear {res['name']} Owner,\n\nThank you for choosing to partner with LINE MAN Wongnai.\n\nUnfortunately, we cannot proceed with your storefront onboarding at this time because: {rational}\n\nPlease update your submission materials on Google Drive and try again."
    
    # Display draft email in a text area for editing
    edited_email = st.text_area("Review and Edit Draft Email before sending:", value=draft_email, height=180)
    
    col_yes, col_no = st.columns(2)
    with col_no:
        if st.button("❌ Confirm Rejection & Send Email", type="primary", use_container_width=True):
            st.success("Restaurant Rejected. Email sent to the owner.")
            # Update state to simulate it being handled
            res["status"] = "Rejected"
            time.sleep(1.5)
            st.session_state.selected_res_id = None
            st.rerun()
            
    with col_yes:
        if st.button("✅ Force Approve (Override AI)", use_container_width=True):
            st.warning("Restaurant Approved by Human Override. Updating Salesforce CRM...")
            # Update state to simulate it being handled
            res["status"] = "Auto-Approved"
            time.sleep(1.5)
            st.session_state.selected_res_id = None
            st.rerun()


# Routing Logic
if 'selected_res_id' in st.session_state and st.session_state.selected_res_id is not None:
    show_case_detail(st.session_state.selected_res_id)
else:
    show_main_dashboard()
