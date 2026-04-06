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
            "issue": "Vision Agent: Detected alcohol as the Hero Image (violates pg 4 of Checklist).", 
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
            "name": "Ghost Kitchen 99", 
            "status": "Requires Review", 
            "risk": "High", 
            "issue": "Integrity Service: SQL Match found in Blacklist DB (Known Fraudulent Entity).", 
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
            "issue": "OCR Agent: Menu text illegible. Digitization failed (Score: 0.35).", 
            "image": "blurry.png",
            "agent_a_flag": False,
            "agent_b_flag": False,
            "agent_c_flag": True
        }
    ]
    st.session_state.merchant_submission_status = None

# Mock Data (Pre-processed by AI Fast Track)
if 'restaurants' not in st.session_state:
    init_mock_data()

# --- TAB 1: MERCHANT ONBOARDING ---
def show_merchant_tab():
    st.title("🏪 สมัครเปิดร้านบน LINE MAN Wongnai")
    st.markdown("ยินดีต้อนรับ! กรุณาส่งข้อมูลร้านค้าและรูปถ่ายเมนูเพื่อเข้าร่วม LINE MAN Wongnai")
    
    st.subheader("เลือกลองใช้งาน (Simulate User Journey):")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🟢 ผ่านการอนุมัติ (Success Path)")
            st.caption("ข้อมูลครบถ้วน รูปภาพชัดเจน ไม่มีข้อผิดพลาดตามนโยบาย")
            if st.button("จำลองการอนุมัติสำเร็จ", key="btn_sim_success", use_container_width=True):
                st.session_state.merchant_submission_status = "Processing"
                st.session_state.simulation_type = "Success"
                st.rerun()
                
    with col2:
        with st.container(border=True):
            st.markdown("### 🟡 ถูกปฏิเสธ (Auto-Reprocessing & Dispute)")
            st.caption("ทำผิดนโยบาย (เช่น มีเครื่องดื่มแอลกอฮอล์) ระบบปฏิเสธทันทีและแจ้งให้แก้ไข ร้านค้าสามารถกดยื่นอุทธรณ์ได้")
            if st.button("จำลองการถูกปฏิเสธ", key="btn_sim_reject", use_container_width=True):
                st.session_state.merchant_submission_status = "Processing"
                st.session_state.simulation_type = "Auto-Reprocessing"
                st.rerun()

    # Simulate AI Processing feedback to the Merchant
    if st.session_state.merchant_submission_status in ["Processing", "Disputed"]:
        st.divider()
        st.subheader("⚙️ AI Fast Track กำลังตรวจสอบข้อมูล...")
        
        # Only show the progress bar if it's the initial processing
        if st.session_state.merchant_submission_status == "Processing":
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.markdown("🔄 **Parallel Ingestion:** กำลังดึงข้อมูลจาก Salesforce & G-Drive...")
            time.sleep(1)
            progress_bar.progress(33)
            
            status_text.markdown("🧠 **Parallel AI Services:** กำลังรัน Integrity, Vision, และ OCR Agents...")
            time.sleep(1.5)
            progress_bar.progress(66)
            
            status_text.markdown("⚖️ **Triage & Decision Gate:** กำลังประเมินผลตาม Checklist 15 หน้า...")
            time.sleep(1.5)
            progress_bar.progress(100)
            st.session_state.merchant_submission_status = "Finished_Processing"
            st.rerun()

    if st.session_state.merchant_submission_status in ["Finished_Processing", "Disputed"]:
        st.divider()
        sim_type = st.session_state.get("simulation_type", "")
        
        if sim_type == "Success":
            st.success("✅ **อนุมัติสำเร็จ!**")
            st.info("ร้านค้าของคุณผ่านการตรวจสอบทั้งหมดและพร้อมเปิดให้บริการบนแอปพลิเคชันแล้ว (Live on Wongnai Prod DB)")
            
        elif sim_type == "Auto-Reprocessing":
            st.error("❌ **โปรดดำเนินการ: ต้องแก้ไขข้อมูลที่ส่งมา**")
            st.markdown("""
            **ข้อความจาก LINE MAN Wongnai:**
            
            สวัสดีครับ! ระบบตรวจสอบพบว่าหนึ่งในรูปถ่ายที่คุณอัปโหลดมีเครื่องดื่มแอลกอฮอล์เป็นภาพหลัก ตามนโยบายของเรา ไม่อนุญาตให้ใช้ภาพเครื่องดื่มแอลกอฮอล์เป็นภาพหน้าปกร้านครับ
            
            รบกวนช่วยอัปโหลดรูปภาพใหม่ลงในโฟลเดอร์ G-Drive ของคุณ โดยเน้นที่รูปอาหารแทน เมื่อคุณอัปโหลดเสร็จ ระบบของเราจะทำการตรวจสอบอีกครั้งโดยอัตโนมัติครับ!
            """)
            if os.path.exists("beer.png"):
                st.image("beer.png", caption="รูปภาพที่มีปัญหา (มีแอลกอฮอล์)", width=300)
                
            st.divider()
            st.markdown("### คุณเห็นด้วยกับคำตัดสินนี้หรือไม่?")
            col_agree, col_disagree = st.columns(2)
            with col_agree:
                if st.button("✅ เข้าใจแล้ว ฉันจะไปอัปโหลดรูปภาพใหม่", use_container_width=True):
                    st.success("ขอบคุณครับ! ระบบกำลังรอรูปภาพใหม่จาก G-Drive...")
            with col_disagree:
                if st.button("⚖️ ฉันไม่เห็นด้วย นี่ไม่ใช่แอลกอฮอล์ / ขอส่งให้พนักงานตรวจ", use_container_width=True):
                    st.session_state.simulation_type = "Fallback"
                    st.session_state.merchant_submission_status = "Disputed"
                    st.rerun()
            
        elif sim_type == "Fallback":
            st.success("✅ **ส่งคำร้องขออุทธรณ์สำเร็จแล้ว!**")
            st.warning("⏳ **อยู่ระหว่างการรอตรวจสอบโดยพนักงาน**")
            st.markdown("""
            **ข้อความจาก LINE MAN Wongnai:**
            
            ขอบคุณที่แจ้งให้เราทราบครับ คำร้องของคุณถูกส่งไปยังทีม Quality ของเราเพื่อทำการตรวจสอบด้วยพนักงาน (Human Review) แล้ว
            
            **ระยะเวลาดำเนินการโดยประมาณ:** ทีมงานของเราจะตรวจสอบเคสของคุณและแจ้งกลับภายใน **8 ชั่วโมง** ครับ
            """)
            
        # Only mark as Done if it's Success so it doesn't clear the dispute screen
        if sim_type == "Success":
            st.session_state.merchant_submission_status = "Done"

# --- TAB 2: HUMAN VALIDATOR DASHBOARD ---
def show_validator_dashboard():
    # Only show dashboard if we aren't investigating a specific case
    if 'selected_res_id' in st.session_state and st.session_state.selected_res_id is not None:
        show_case_detail(st.session_state.selected_res_id)
        return

    st.markdown("""
    **แดชบอร์ดภายใน: ระบบตรวจสอบเนื้อหาร้านอาหาร (Restaurant Content Validation)**
    """)
    
    st.subheader("📋 คิวงานที่มีปัญหา: รอพนักงานตรวจสอบ (Human Fallback Required)")
    
    # Filter only those requiring review
    review_queue = [res for res in st.session_state.restaurants if res["status"] == "Requires Review"]
    
    if not review_queue:
        st.success("🎉 ตรวจสอบเสร็จสิ้น! ไม่มีร้านอาหารที่รอคิวตรวจสอบโดยพนักงานในขณะนี้ (เคลียร์คิวงาน 3-5 วันเรียบร้อย)")
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
                        st.error(f"ความเสี่ยง: สูง (High)")
                    else:
                        st.warning(f"ความเสี่ยง: ปานกลาง (Medium)")
                with col4:
                    if st.button("ตรวจสอบ 🔍", key=f"btn_{res['id']}"):
                        st.session_state.selected_res_id = res["id"]
                        st.rerun()
                        
    st.divider()
    st.subheader("✅ ร้านที่ผ่านการอนุมัติอัตโนมัติ (Live in Wongnai Prod DB)")
    approved_queue = [res for res in st.session_state.restaurants if res["status"] == "Auto-Approved"]
    for res in approved_queue:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 3])
            with col1:
                st.markdown(f"**{res['id']}**")
            with col2:
                st.markdown(f"{res['name']}")
            with col3:
                st.success("อนุมัติอัตโนมัติ (ผ่าน Decision Gates ทั้งหมด)")

def show_case_detail(res_id):
    res = next((r for r in st.session_state.restaurants if r["id"] == res_id), None)
    
    if not res:
        st.error("ไม่พบข้อมูลร้านอาหาร")
        if st.button("กลับไปหน้าแดชบอร์ด"):
            st.session_state.selected_res_id = None
            st.rerun()
        return

    st.button("⬅️ กลับไปหน้าแดชบอร์ด", on_click=lambda: st.session_state.pop('selected_res_id', None))
    
    st.title(f"กำลังตรวจสอบ: {res['name']} ({res['id']})")
    
    # Context
    st.markdown("**1. Parallel Ingestion:** Salesforce (ข้อมูลตัวอักษร) & G-Drive (รูปภาพ)")
    
    # Display AI Audit Results
    st.subheader("🧠 2. ผลลัพธ์จาก Parallel AI Services")
    
    colA, colB, colC = st.columns(3)
    
    with colA:
        with st.container(border=True):
            st.markdown("##### 🛡️ Integrity Service")
            st.caption("SQL Match ตรวจสอบ Blacklist DB")
            if res["agent_a_flag"]:
                st.error("❌ พบปัญหา: ข้อมูลตรงกับบัญชีดำ (Blacklist)!")
            else:
                st.success("✅ ผ่าน: ไม่พบประวัติการทุจริต")
            
    with colB:
        with st.container(border=True):
            st.markdown("##### 👁️ Vision Agent")
            st.caption("CV Scan ตรวจหา แอลกอฮอล์ / ภาพเบลอ / ลายน้ำ")
            if res["agent_b_flag"]:
                st.warning("⚠️ พบปัญหา: ตรวจพบแอลกอฮอล์ในภาพหน้าปกร้าน")
            else:
                st.success("✅ ผ่าน: รูปภาพเป็นไปตามนโยบาย")

    with colC:
        with st.container(border=True):
            st.markdown("##### 📝 OCR Agent")
            st.caption("Digitization เพื่อแปลงเมนูเป็น Structured JSON")
            if res["agent_c_flag"]:
                st.error("❌ พบปัญหา: Digitization ล้มเหลว (อ่านตัวหนังสือไม่ออก)")
            else:
                st.success("✅ ผ่าน: แปลงเป็น JSON สำเร็จ")

    st.divider()
    
    st.subheader("📊 3. Triage & Decision Gate: สรุปผลจาก AI (AI Reasoning Report)")
    
    summary_text = res["issue"]
    st.info(f"**🤖 ผลจาก Decision Gate:** {summary_text} -> ถูกส่งมายังพนักงานตรวจสอบ (Human Fallback)")
    
    # Show image if available for the flagged case
    if res.get("image") and os.path.exists(res["image"]):
        st.markdown(f"**🔍 หลักฐานรูปภาพจาก G-Drive:** `{res['image']}`")
        st.image(res["image"], caption=f"ภาพที่มีปัญหาของร้าน {res['name']}", width=400)

    st.divider()
    
    # Human Review Dashboard Actions
    st.subheader("4️⃣ Action & Feedback (การตัดสินใจโดยพนักงาน)")
    
    # Extract the rational for rejection
    rational = res['issue'].split(': ', 1)[1] if ': ' in res['issue'] else res['issue']
    
    st.markdown("### เหตุผลที่ระบบปฏิเสธ")
    st.error(f"**เหตุผล:** {rational}")
    
    st.markdown("### Communicator Agent: ข้อความแจ้งเตือนร่างอัตโนมัติ")
    draft_email = f"เรียน เจ้าของร้าน {res['name']},\n\nขอบคุณที่เลือกเป็นพาร์ทเนอร์กับ LINE MAN Wongnai ครับ\n\nระบบของเราพบปัญหาในข้อมูลที่คุณส่งมา: {rational}\n\nรบกวนช่วยแก้ไขข้อมูลและรูปภาพใน G-Drive เพื่อดำเนินการต่อครับ"
    
    # Display draft email in a text area for editing
    edited_email = st.text_area("ตรวจสอบและแก้ไขข้อความแจ้งเตือน ก่อนส่งผ่าน Communicator Agent:", value=draft_email, height=180)
    
    col_yes, col_no = st.columns(2)
    with col_no:
        if st.button("❌ ยืนยันการปฏิเสธ & ส่งข้อความแจ้งเตือน", type="primary", use_container_width=True):
            st.success("Communicator Agent ทำงานแล้ว ส่งการแจ้งเตือนไปยังเจ้าของร้านผ่าน G-Drive ทันที")
            # Update state to simulate it being handled
            res["status"] = "Rejected"
            time.sleep(1.5)
            st.session_state.selected_res_id = None
            st.rerun()
            
    with col_yes:
        if st.button("✅ อนุมัติทันที (Human Override)", use_container_width=True):
            st.warning("พนักงานยืนยันการอนุมัติ (Override) กำลังนำร้านขึ้นสู่ระบบ Wongnai Prod DB...")
            # Update state to simulate it being handled
            res["status"] = "Auto-Approved"
            time.sleep(1.5)
            st.session_state.selected_res_id = None
            st.rerun()


# --- MAIN APP LAYOUT ---
col_title, col_reset = st.columns([5, 1.5])
with col_title:
    st.title("🛵 LINE MAN Wongnai: AI Fast Track")
with col_reset:
    st.write("") # Spacing
    st.markdown("<p style='text-align: right; font-size: 12px; margin-bottom: 0px;'>กรุณากดปุ่ม Reset ทุกครั้งที่เข้าใช้ Demo</p>", unsafe_allow_html=True)
    if st.button("🔄 Reset Demo", use_container_width=True):
        init_mock_data()
        st.rerun()

tab1, tab2 = st.tabs(["Merchant Journey", "Validator Journey"])

with tab1:
    show_merchant_tab()

with tab2:
    show_validator_dashboard()

