import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Study Data Allocator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom minimal CSS for styling & highlighting
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif; }
    .stButton button { border-radius: 8px; font-weight: 500; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; color: #1f2937; }
    
    /* Content Tag Base Styling */
    .content-tag {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        margin-right: 6px;
        margin-bottom: 6px;
        font-size: 0.85rem;
        background: #f3f4f6;
        border: 1px solid #d1d5db;
        color: #374151;
        font-weight: 600;
    }
    
    /* Highlight High Data Consuming Items */
    .tag-Video {
        background: #fee2e2 !important;
        border: 1px solid #fca5a5 !important;
        color: #b91c1c !important;
    }
    .tag-Audio {
        background: #fef3c7 !important;
        border: 1px solid #fde68a !important;
        color: #b45309 !important;
    }
    .tag-Quiz {
        background: #e0e7ff !important;
        border: 1px solid #c7d2fe !important;
        color: #4338ca !important;
    }
    .tag-Text {
        background: #dcfce7 !important;
        border: 1px solid #bbf7d0 !important;
        color: #15803d !important;
    }
</style>
""", unsafe_allow_html=True)

CONTENT_COSTS = {
    "Text": 5,      
    "Quiz": 15,     
    "Audio": 40,    
    "Video": 150    
}

CONTENT_LABELS = {
    "Text": "Text-based learning",
    "Quiz": "Quizzes/practice",
    "Audio": "Audio explanations",
    "Video": "Video lectures"
}

def calculate_unrestricted_demand(students):
    """Calculates exactly how much data the ideal curriculum requests without any budget cuts."""
    demand_mb = 0
    for s in students:
        if s["goal"] == "Basic Literacy":
            q = ["Text", "Text", "Quiz", "Text", "Audio", "Text", "Quiz", "Text", "Quiz", "Text", "Text"]
        elif s["goal"] == "Concept Building":
            q = ["Text", "Audio", "Text", "Quiz", "Video", "Text", "Audio", "Quiz", "Text", "Audio"]
        else:
            q = ["Quiz", "Video", "Text", "Quiz", "Audio", "Quiz", "Video", "Text", "Quiz", "Video", "Quiz"]
        
        demand_mb += sum([CONTENT_COSTS[item] for item in q])
    return demand_mb

def optimize_allocations(students, total_budget_mb, low_data_mode):
    g_score = {"Basic Literacy": 1.0, "Concept Building": 2.0, "Exam Preparation": 3.0}
    l_score = {"Beginner": 1.0, "Intermediate": 1.2, "Advanced": 1.5}
    
    plans = [{"Text": 0, "Quiz": 0, "Audio": 0, "Video": 0} for _ in students]
    queues = []
    
    for idx, s in enumerate(students):
        # Configure optimum baseline matrix
        if s["goal"] == "Basic Literacy":
            q = ["Text", "Text", "Quiz", "Text", "Audio", "Text", "Quiz", "Text", "Quiz", "Text", "Text"]
        elif s["goal"] == "Concept Building":
            q = ["Text", "Audio", "Text", "Quiz", "Video", "Text", "Audio", "Quiz", "Text", "Audio"]
        else:
            q = ["Quiz", "Video", "Text", "Quiz", "Audio", "Quiz", "Video", "Text", "Quiz", "Video", "Quiz"]
            
        # Apply Low Data Mode Filtering
        if low_data_mode:
            filtered_q = []
            for item in q:
                if item == "Video":
                    filtered_q.append("Quiz") # Substitute heavy video directly with lightweight practice
                else:
                    filtered_q.append(item)
            q = filtered_q

        base_priority = g_score[s["goal"]] * l_score[s["level"]] * (1.0 + s["age"]/100.0)
        queues.append({"items": q, "base_priority": base_priority, "idx": idx})
        
    global_used_mb = 0
    engine_active = True
    
    while engine_active and global_used_mb < total_budget_mb:
        engine_active = False
        
        def current_priority(q_obj):
            idx = q_obj["idx"]
            my_used_mb = sum([plans[idx][k] * CONTENT_COSTS[k] for k in CONTENT_COSTS])
            return q_obj["base_priority"] / (1.0 + (my_used_mb / 40.0))
            
        queues.sort(key=current_priority, reverse=True)
        
        for q_obj in queues:
            idx = q_obj["idx"]
            items_list = q_obj["items"]
            
            item_granted = False
            for i, item_req in enumerate(items_list):
                if global_used_mb + CONTENT_COSTS[item_req] <= total_budget_mb:
                    plans[idx][item_req] += 1
                    global_used_mb += CONTENT_COSTS[item_req]
                    items_list.pop(i)
                    item_granted = True
                    engine_active = True
                    break
                    
            if item_granted:
                break 
                
    results = []
    for idx, s in enumerate(students):
        student_plan = plans[idx]
        student_mb = sum([student_plan[k] * CONTENT_COSTS[k] for k in CONTENT_COSTS])
        results.append({
            "plan": student_plan,
            "allocated_mb": student_mb
        })
        
    return results, global_used_mb

def generate_ai_insights(results, global_used_mb, total_budget_mb, combined_low_data_mode):
    total_items = sum(sum(res['plan'].values()) for res in results)
    total_video = sum(res['plan'].get("Video", 0) for res in results)
    total_audio = sum(res['plan'].get("Audio", 0) for res in results)
    
    if global_used_mb == 0 or total_items == 0:
        eff_score = "N/A"
    else:
        avg_cost = global_used_mb / total_items
        if avg_cost <= 25:
            eff_score = "High"
        elif avg_cost <= 60:
            eff_score = "Medium"
        else:
            eff_score = "Low"
            
    recommendations = []
    
    if combined_low_data_mode:
         recommendations.append("🛡️ **Low Data Protection Active:** The engine has forcibly disabled generic Video lectures, substituting them for bandwidth-friendly Text & Quizzes.")
         
    if total_video > 0:
        recommendations.append("📉 **Eliminate Rich Media:** High-data Video lectures emerged. Enable 'Low Data Mode' above to block them, saving ~150 MB per unit.")
        
    if total_audio > 0 and eff_score != "High":
        recommendations.append("📖 **Increase Text Baseline:** Consider shifting generalized learning from audio to text-based summaries. Text uses just 12% of the bandwidth.")
        
    if eff_score == "Low" and not combined_low_data_mode:
        recommendations.append("⚠️ **Heavy Network Dependency:** Curriculum relies heavily on media. We suggest engaging the 'Low Data Mode' flag!")
    
    if eff_score == "High":
        recommendations.append("🌟 **Astonishing Efficiency Scale:** Absolute optimal deployment. You are transferring massive knowledge payloads across all users with trivial bandwidth.")
        
    if len(recommendations) < 2:
        recommendations.append("🧠 **Peer Engagement Dynamics:** Combine Concept Builders dynamically so one device caches queries, minimizing data pull per query.")
        
    return eff_score, recommendations[:3]

def main():
    st.title("⚡ AI Study Data Allocator")
    st.markdown("Intelligently balances daily internet quotas across multiple students utilizing learning optimization logic.")
    
    # Pre-load demo state button for presentation edge
    c_demo1, c_demo2 = st.columns([10, 2.5])
    with c_demo2:
        if st.button("🧪 Auto-Load Demo", use_container_width=True, help="Populates 3 varied students for a quick demo"):
            st.session_state.students = [
                {"name": "Aarav", "age": 8, "level": "Beginner", "goal": "Basic Literacy"},
                {"name": "Diya", "age": 14, "level": "Intermediate", "goal": "Concept Building"},
                {"name": "Rohan", "age": 17, "level": "Advanced", "goal": "Exam Preparation"}
            ]
            st.rerun()
            
    st.divider()

    if 'students' not in st.session_state:
        st.session_state.students = []

    # --- SECTION 1: SETTINGS & ENROLLMENT ---
    row1, row2 = st.columns([1, 1.8])
    
    with row1:
        st.subheader("⚙️ 1. Constraints")
        with st.container(border=True):
            col_b1, col_b2 = st.columns([2, 1])
            with col_b1:
                data_budget = st.number_input("Limit", min_value=0.0, step=0.1, value=1.5, format="%.2f", key="budget")
            with col_b2:
                unit = st.selectbox("Unit", ["GB", "MB"])
            
            total_mb = data_budget * 1024 if unit == "GB" else data_budget
            st.info(f"Bandwidth Restraint: **{total_mb:.0f} MB**")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Optimization Layer**")
            user_toggled_low_data = st.toggle("🌍 Strict Low Data Mode\n\n*(Forces blocking heavy Video constraints)*", value=False)
            
    with row2:
        st.subheader("👥 2. Roster Injection")
        with st.container(border=True):
            with st.form("add_student_form", clear_on_submit=True):
                c0, c1, c2, c3 = st.columns([2, 1, 1.5, 1.5])
                with c0:
                    name = st.text_input("Name", placeholder="e.g. Rahul")
                with c1:
                    age = st.number_input("Age", min_value=3, max_value=100, step=1, value=12)
                with c2:
                    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
                with c3:
                    goal = st.selectbox("Priority Goal", ["Basic Literacy", "Concept Building", "Exam Preparation"])
                
                submitted = st.form_submit_button("Add to Engine Database", use_container_width=True)
                if submitted:
                    s_name = name if name.strip() != "" else f"Student {len(st.session_state.students) + 1}"
                    st.session_state.students.append({
                        "name": s_name,
                        "age": age,
                        "level": level,
                        "goal": goal
                    })
                    st.success(f"Deployed profile sequence for {s_name}!")
                    
    st.divider()

    # --- SECTION 2: REAL-TIME USAGE TRACKING ---
    st.subheader("🛰️ 3. Real-Time Telemetry & Monitoring")
    
    if not st.session_state.students:
        st.info("Awaiting structural parameters. Please build initial models using Roster Injection or trigger 'Auto-Load Demo'.")
        return
        
    if total_mb <= 0:
        st.error("⚠️ Compute Error: Your strict structural parameter (Global Data Budget) equals Zero or below. Provide bandwidth limits minimum.")
        return
        
    if total_mb < 5:
        st.warning("⚠️ Bandwidth Warning: System detected a budget severely deprived (< 5 MB). Cannot deploy any standard baseline blocks.")
        return

    # 1) Calculate RAW Unrestricted Demand
    raw_demand_mb = calculate_unrestricted_demand(st.session_state.students)
    demand_pct = (raw_demand_mb / total_mb) * 100 if total_mb > 0 else 100
    
    # 2) Process Dynamic Auto-Restriction Flags & Warnings
    auto_restrict_engaged = False
    
    c_tel1, c_tel2 = st.columns([1.5, 1])
    with c_tel1:
        st.markdown(f"**Curriculum Demand vs System Target ({min(demand_pct, 100):.1f}% Load)**")
        # Ensure progress bar takes max 1.0 (100%) but safely captures overflow context visually
        st.progress(min(demand_pct / 100.0, 1.0))
        st.caption(f"Initial raw data request: {raw_demand_mb:.0f} MB / Capacity Limit: {total_mb:.0f} MB")
        
    with c_tel2:
        # Threshold Logic & Alerts
        if demand_pct >= 100:
            st.error("🛑 **Critical Overload:** 100%+ Usage detected. The system has automatically activated high-data content restrictions (Videos removed) to enforce the budget.")
            auto_restrict_engaged = True
        elif demand_pct >= 90:
            st.warning("⚠️ **90% Usage Alert:** Demand is extremely close to the limit. **Avoid high-data content to stay within budget.**")
        elif demand_pct >= 70:
            st.info("ℹ️ **70% Usage Alert:** Network demand is rising significantly. **Switch to audio or text to save data** moving forward.")
        else:
            st.success("✅ **Stable Capacity:** Optimal operating runway detected.")

    # Apply Auto Restrictions merging with User Toggle
    combined_low_data_mode = user_toggled_low_data or auto_restrict_engaged

    st.divider()

    # --- SECTION 3: RESULTS DASHBOARD ---
    st.subheader("🧠 4. Optimization Matrix")

    # Execute Engine Execution with final resolved parameters
    results, global_used_mb = optimize_allocations(st.session_state.students, total_mb, combined_low_data_mode)
    
    # Dashboard Metrics Interface
    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        st.metric("Total Students Enrolled", len(st.session_state.students))
    with dcol2:
        st.metric("Total Executed Content Load", f"{global_used_mb:.0f} MB")
    with dcol3:
        eff = (global_used_mb / total_mb * 100) if total_mb > 0 else 0
        st.metric("Post-Optimization Usage", f"{eff:.1f}% System Load")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Output Results Map
    cols = st.columns(3)
    for i, s in enumerate(st.session_state.students):
        res = results[i]
        col = cols[i % 3] 
        
        with col:
            with st.container(border=True):
                st.markdown(f"<h3 style='margin-bottom: 0;'>{s['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: gray; font-size: 0.9rem;'>{s['age']} yrs • {s['level']} • {s['goal']}</span>", unsafe_allow_html=True)
                st.divider()
                st.markdown(f"**Data Profile Share**: `{res['allocated_mb']:.0f} MB`")
                st.markdown("<p style='margin-bottom: 5px; font-weight: 600;'>Module Curriculum Pattern:</p>", unsafe_allow_html=True)
                
                has_modules = False
                for key, count in res['plan'].items():
                    if count > 0:
                        has_modules = True
                        st.markdown(f"<span class='content-tag tag-{key}'><b>{count}x</b> {CONTENT_LABELS[key]}</span>", unsafe_allow_html=True)
                
                if not has_modules:
                    st.markdown("<span style='color:#e03131; font-style:italic;'>Insufficient student budget parameter for single module assignment.</span>", unsafe_allow_html=True)

    # --- SECTION 4: AI INSIGHTS ---
    st.divider()
    st.subheader("💡 5. Diagnostics & Insights")
    
    eff_score, recommendations = generate_ai_insights(results, global_used_mb, total_mb, combined_low_data_mode)
    
    in_col1, in_col2 = st.columns([1, 2.5])
    with in_col1:
        with st.container(border=True):
            st.markdown("**Efficiency Diagnostic Matrix**")
            if eff_score == "High":
                st.markdown("<h1 style='color:#15803d; margin:0;'>High</h1>", unsafe_allow_html=True)
            elif eff_score == "Medium":
                st.markdown("<h1 style='color:#b45309; margin:0;'>Medium</h1>", unsafe_allow_html=True)
            elif eff_score == "Low":
                st.markdown("<h1 style='color:#b91c1c; margin:0;'>Low</h1>", unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='color:gray; margin:0;'>N/A</h1>", unsafe_allow_html=True)
            st.caption("Ratio analysis computed automatically from bandwidth density footprints.")
            
    with in_col2:
        with st.container(border=True):
            st.markdown("**Strategic Advisories Output**")
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"{rec}")
            else:
                st.markdown("Waiting for diagnostic triggers.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Purge System State Matrix", type="primary"):
        st.session_state.students = []
        st.rerun()

if __name__ == "__main__":
    main()
