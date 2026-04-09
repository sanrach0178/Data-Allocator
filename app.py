import streamlit as st
import streamlit.components.v1 as components
import random
import time
import os

# Configure the page
st.set_page_config(
    page_title="ByteWise Kids",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- TTS HELPER ---
def speak(text):
    js = f"""
    <script>
    setTimeout(function() {{
        var SpeechSynthesisUtterance = window.SpeechSynthesisUtterance;
        if(SpeechSynthesisUtterance) {{
            var msg = new SpeechSynthesisUtterance("{text.replace('"', '')}");
            msg.rate = 0.95;
            window.speechSynthesis.speak(msg);
        }}
    }}, 100);
    </script>
    """
    components.html(js, height=0)


# --- STT COMPONENT INJECTION ---
_STT_DIR = os.path.join(os.path.dirname(__file__), "stt_component_v2")
if not os.path.exists(_STT_DIR):
    os.makedirs(_STT_DIR)

_HTML_CONTENT = """<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/streamlit-component-lib@1.3.0/dist/streamlit.js"></script>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800&display=swap');
      body { margin: 0; padding: 0; overflow: hidden; background: transparent; }
      button {
        width: 100%; height: 140px; font-size: 2.5rem; background-color: #ffffff;
        border: 4px solid #e2e8f0; border-radius: 24px; font-weight: 800; cursor: pointer; color: #1e293b;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06); transition: all 0.2s; font-family: 'Nunito', sans-serif;
      }
      button:hover { background-color: #f1f8ff; box-shadow: 0 12px 30px rgba(59,130,246,0.15); transform: translateY(-3px); border-color: #3b82f6; }
    </style>
  </head>
  <body>
    <button id="stt-btn">🎤 Tap to Speak</button>
    <script>
      function onRender(event) { Streamlit.setFrameHeight(160); }
      Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
      Streamlit.setComponentReady();
      
      const btn = document.getElementById("stt-btn");
      btn.onclick = async function() {
          try {
              let targetSpeech = window.SpeechRecognition || window.webkitSpeechRecognition;
              
              // Streamlit iframes natively block microphone permissions. 
              // We explicitly bypass the iframe sandbox by grabbing the parent window's Speech API!
              try {
                  if (window.parent && (window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition)) {
                       targetSpeech = window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition;
                  }
              } catch(e) {} // Ignore cross-origin sandboxing just in case
              
              if (!targetSpeech) {
                  Streamlit.setComponentValue("ERROR_NOT_SUPPORTED");
                  return;
              }
              const recognition = new targetSpeech();
              recognition.onresult = function(event) {
                  const text = event.results[0][0].transcript;
                  btn.innerText = "⭐ Captured!";
                  Streamlit.setComponentValue(text);
              };
              recognition.onerror = function(event) {
                  btn.innerText = "❌ Mic Error! Check Permissions";
              };
              recognition.onspeechend = function() { recognition.stop(); };
              recognition.start(); // This triggers the top-level Browser popup securely!
              btn.innerText = "🎧 Listening... (Speak Now)";
              setTimeout(() => { btn.innerText = "🎤 Tap to Speak"; }, 6000);
          } catch(err) {
              btn.innerText = "❌ " + err.message;
          }
      };
    </script>
  </body>
</html>
"""

_FILE_PATH = os.path.join(_STT_DIR, "index.html")
with open(_FILE_PATH, "w", encoding="utf-8") as f:
    f.write(_HTML_CONTENT)

speech_to_text = components.declare_component("speech_to_text_v2", path=_STT_DIR)


# Playful Kids CSS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800;900&display=swap');
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp { background-color: #f2f7f9; }
    
    h1, h2, h3, h4, p, span, div { font-family: 'Nunito', sans-serif !important; }
    h1 { font-weight: 900; color: #1e293b; margin-top: 0 !important; padding-top: 0 !important; font-size: 2.8rem;}
    h2, h3 { font-weight: 800; color: #334155; }
    
    /* Playful Custom Containers / Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: none !important;
        border-radius: 28px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.06) !important;
        padding: 1.5rem !important;
    }
    
    div[data-testid="stVerticalBlock"] > div > div[style*="border-color"] {
        border: none !important;
        border-radius: 28px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.04) !important;
        padding: 1.5rem !important;
    }
    
    [data-testid="stForm"] { 
        border: none !important; border-radius: 28px !important; padding: 2rem !important; 
        background-color: #ffffff; box-shadow: 0px 10px 30px rgba(0,0,0,0.04) !important;
    }
    
    .kids-header {
        font-size: 1.6rem; font-weight: 900; color: #0f172a; margin-top: 1rem; margin-bottom: 1rem;
    }

    .stButton button { 
        border-radius: 30px; font-weight: 800; font-size: 1.1rem; border: none;
        background-color: #3b82f6; color: white; transition: all 0.3s ease;
        padding: 0.5rem 1.2rem; box-shadow: 0 6px 15px rgba(59, 130, 246, 0.25);
    }
    .stButton button:hover { background-color: #2563eb; transform: translateY(-3px); box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4); }
    
    div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 900; color: #3b82f6; }
    div[data-testid="stMetricLabel"] { font-weight: 700; color: #64748b; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;}
    
    /* Pastel Badges */
    .content-tag {
        display: inline-block; padding: 8px 18px; border-radius: 24px; margin-right: 8px; margin-bottom: 8px;
        font-size: 0.95rem; background: #f1f5f9; border: none; color: #475569; font-weight: 800;
    }
    .tag-Video { color: #e11d48; background: #ffe4e6; } /* Rose */
    .tag-Audio { color: #d97706; background: #fef3c7; } /* Amber */
    .tag-Quiz { color: #0284c7; background: #e0f2fe; }  /* Light Blue */
    .tag-Text { color: #059669; background: #d1fae5; }  /* Emerald */
    
    /* Layout Overrides */
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 95% !important;}
</style>
""", unsafe_allow_html=True)

CONTENT_COSTS = {"Text": 5, "Quiz": 15, "Audio": 40, "Video": 150}
CONTENT_LABELS = {"Text": "Text Lesson", "Quiz": "Mini Quiz", "Audio": "Audio Story", "Video": "Full Video"}

def calculate_unrestricted_demand(students):
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
        if s["goal"] == "Basic Literacy":
            q = ["Text", "Text", "Quiz", "Text", "Audio", "Text", "Quiz", "Text", "Quiz", "Text", "Text"]
        elif s["goal"] == "Concept Building":
            q = ["Text", "Audio", "Text", "Quiz", "Video", "Text", "Audio", "Quiz", "Text", "Audio"]
        else:
            q = ["Quiz", "Video", "Text", "Quiz", "Audio", "Quiz", "Video", "Text", "Quiz", "Video", "Quiz"]
            
        if low_data_mode:
            q = ["Quiz" if item == "Video" else item for item in q]

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
        results.append({"plan": student_plan, "allocated_mb": student_mb})
        
    return results, global_used_mb

def generate_ai_insights(results, global_used_mb, total_mb, low_data_mode):
    score = (global_used_mb / total_mb * 100) if total_mb > 0 else 0
    recs = []
    if low_data_mode:
        recs.append("Turned off videos to squeeze everyone in! 🚀")
    elif score > 90:
        recs.append("Careful, you're using almost all the data! 🚨")
    elif score > 0:
        recs.append("Great job managing data fairly! ⭐")
    return score, recs
# --- STATE ---
if 'students' not in st.session_state: st.session_state.students = []
if 'a11y_mode' not in st.session_state: st.session_state.a11y_mode = False
if 'a11y_step' not in st.session_state: st.session_state.a11y_step = 0
if 'a11y_budget' not in st.session_state: st.session_state.a11y_budget = 1024
if 'speak_queue' not in st.session_state: st.session_state.speak_queue = None

if st.session_state.speak_queue:
    speak(st.session_state.speak_queue)
    st.session_state.speak_queue = None


# --------------------------
# STANDARD (KIDS) MODE
# --------------------------
def render_standard_mode():
    c_head1, c_head2, c_head3 = st.columns([7, 2, 2])
    with c_head1:
        st.markdown("<h1 style='margin-bottom: -5px;'>🎨 ByteWise</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: #64748b; font-weight: 700; margin-bottom: 5px;'>Super Fun Learning Dashboard!</p>", unsafe_allow_html=True)
    with c_head2:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        if st.button("♿ Accessibility", use_container_width=True):
            st.session_state.a11y_mode = True
            st.session_state.a11y_step = 0
            if 'spoken_welcome' in st.session_state: del st.session_state.spoken_welcome
            if 'spoken_results' in st.session_state: del st.session_state.spoken_results
            st.rerun()
            
    with c_head3:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        if st.button("🔮 Load Test Data", use_container_width=True):
            st.session_state.students = [
                {"name": "Aarav", "age": 8, "level": "Beginner", "goal": "Basic Literacy"},
                {"name": "Diya", "age": 14, "level": "Intermediate", "goal": "Concept Building"},
                {"name": "Rohan", "age": 17, "level": "Advanced", "goal": "Exam Preparation"}
            ]
            st.rerun()

    # --- ROW 1 ---
    row1, row2 = st.columns([1, 1.8])
    with row1:
        st.markdown("<div class='kids-header'>🎯 Set the Rules!</div>", unsafe_allow_html=True)
        with st.container(border=True):
            col_b1, col_b2 = st.columns([2, 1])
            with col_b1:
                data_budget = st.number_input("Limit", min_value=0.0, step=0.1, value=1.5, format="%.2f", key="budget")
            with col_b2:
                unit = st.selectbox("Unit", ["GB", "MB"])
            
            total_mb = data_budget * 1024 if unit == "GB" else data_budget
            st.markdown(f"<p style='margin-top: 5px; margin-bottom: 10px; font-weight: 800; font-size: 1.1rem; color: #3b82f6;'>Total Data: {total_mb:.0f} MB</p>", unsafe_allow_html=True)
            user_toggled_low_data = st.toggle("🚀 Turbo Saving Mode", value=False)
            
    with row2:
        st.markdown("<div class='kids-header'>👦 Add Friends</div>", unsafe_allow_html=True)
        with st.form("add_student_form", clear_on_submit=True):
            c0, c1, c2, c3 = st.columns([2, 1, 1.5, 1.5])
            with c0:
                name = st.text_input("Name", placeholder="e.g. Rahul")
            with c1:
                age = st.number_input("Age", min_value=3, max_value=100, step=1, value=12)
            with c2:
                level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
            with c3:
                goal = st.selectbox("Goal", ["Basic Literacy", "Concept Building", "Exam Preparation"])
            
            submitted = st.form_submit_button("✨ Add to Dashboard!", use_container_width=True)
            if submitted:
                s_name = name if name.strip() != "" else f"Friend {len(st.session_state.students) + 1}"
                st.session_state.students.append({"name": s_name, "age": age, "level": level, "goal": goal})
                st.rerun()

    # --- ROW 2 ---
    st.markdown("<div class='kids-header'>📊 Mission Progress</div>", unsafe_allow_html=True)
    
    if not st.session_state.students:
        st.info("No friends added yet. Let's add some to start the fun!")
        return
    if total_mb <= 0: return

    raw_demand_mb = calculate_unrestricted_demand(st.session_state.students)
    demand_pct = (raw_demand_mb / total_mb) * 100 if total_mb > 0 else 100
    auto_restrict_engaged = False
    
    c_tel1, c_tel2 = st.columns([1.5, 1])
    with c_tel1:
        st.markdown(f"<p style='font-weight: 800; color: #1e293b;'>Base Demand ({min(demand_pct, 100):.1f}%)</p>", unsafe_allow_html=True)
        st.progress(min(demand_pct / 100.0, 1.0))
        
    with c_tel2:
        if demand_pct >= 100:
            st.error("Too much data! We activated Turbo Saving Mode! 🚀")
            auto_restrict_engaged = True
        elif demand_pct >= 90:
            st.warning("Almost out of data! Careful! 🚨")
        elif demand_pct >= 70:
            st.info("Using a lot of data! 📉")
        else:
            st.success("Perfectly safe! 🌈")

    combined_low_data_mode = user_toggled_low_data or auto_restrict_engaged

    # --- RESULTS ---
    results, global_used_mb = optimize_allocations(st.session_state.students, total_mb, combined_low_data_mode)
    
    # Custom 3-card layout mimicking the screenshot
    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        with st.container(border=True):
            st.markdown("<h3 style='margin:0; font-size:1.1rem; color:#64748b;'>👩‍🎓 Total Friends</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color:#3b82f6;'>{len(st.session_state.students)}</h1>", unsafe_allow_html=True)
    with dcol2:
        with st.container(border=True):
            st.markdown("<h3 style='margin:0; font-size:1.1rem; color:#64748b;'>📦 Used Payload</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color:#ec4899;'>{global_used_mb:.0f} MB</h1>", unsafe_allow_html=True)
    with dcol3:
        eff = (global_used_mb / total_mb * 100) if total_mb > 0 else 0
        with st.container(border=True):
            st.markdown("<h3 style='margin:0; font-size:1.1rem; color:#64748b;'>⚡ System Load</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color:#10b981;'>{eff:.1f}%</h1>", unsafe_allow_html=True)

    st.markdown("<div class='kids-header'>🏆 Learning Quests</div>", unsafe_allow_html=True)
    
    # Evaluate insights before tracking tips
    eff_score, recommendations = generate_ai_insights(results, global_used_mb, total_mb, combined_low_data_mode)
    
    # 💡 Move Smart Tips ABOVE the grid to save lateral space
    if recommendations:
        tip_text = recommendations[0] if global_used_mb > 0 else "No tips needed currently! 🎉"
    else:
        tip_text = "No tips needed currently! 🎉"
        
    with st.container(border=True):
        st.markdown(f"<div style='margin:0; padding: 10px; font-size: 1.3rem; font-weight: 800; display: flex; align-items: center; color: #334155;'>💡 Smart Tip: <span style='margin-left: 8px; font-weight: 600; color:#475569;'>{tip_text}</span></div>", unsafe_allow_html=True)

    # 👩‍🎓 Full-Width 3-Column Student Grid
    st.markdown("<br>", unsafe_allow_html=True)
    st_cols = st.columns(3)
    
    for i, s in enumerate(st.session_state.students):
        res = results[i]
        with st_cols[i % 3]:
            with st.container(border=True):
                # Pre-build tags for inline horizontal flow
                html_tags = []
                for key, count in res['plan'].items():
                    if count > 0:
                        html_tags.append(f"<span class='content-tag tag-{key}' style='padding: 4px 10px; font-size: 0.8rem; margin: 0;'>{count}x {CONTENT_LABELS[key]}</span>")
                
                tags_str = "<div style='display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px;'>" + "".join(html_tags) + "</div>" if html_tags else "<span style='color:#e03131; font-weight: 800;'>Oh no! Not enough data to play!</span>"
                
                # Single unified block to avoid heavy Streamlit vertical padding
                ui_block = f"""
                <div style="line-height: 1.3; padding: 6px; padding-bottom: 12px;">
                    <h2 style='margin-bottom: 2px; margin-top: 0; color: #1e293b; font-size: 1.4rem;'>🌟 {s['name']}</h2>
                    <span style='color: #64748b; font-size: 0.9rem; font-weight: 700;'>Lvl {s['level']} | {s['goal']}</span>
                    <p style='margin-top: 8px; margin-bottom: 8px; font-weight: 800; color: #8b5cf6; font-size: 1.1rem;'>🎁 Magic Data Box: {res['allocated_mb']:.0f} MB</p>
                    <hr style='margin: 8px 0px; border-top: 2px dashed #e2e8f0;'>
                    {tags_str}
                </div>
                """
                st.markdown(ui_block, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🧹 Clear the Board", type="secondary"):
        st.session_state.students = []
        st.rerun()

# --------------------------
# ACCESSIBILITY MODE
# --------------------------
def render_a11y_mode():
    st.markdown("""
        <style>
        /* Giant Interactive Buttons */
        button[data-testid="baseButton-primary"] {
            height: 140px !important; font-size: 2.2rem !important; margin-bottom: 25px !important;
            background-color: #ffffff !important; border: 4px solid #e2e8f0 !important; border-radius: 32px !important;
            box-shadow: 0 15px 35px rgba(0,0,0,0.06) !important; font-family: 'Nunito', sans-serif !important;
            color: #1e293b !important; font-weight: 900 !important; transition: all 0.3s ease !important;
        }
        button[data-testid="baseButton-primary"]:hover { 
            background-color: #eff6ff !important; border-color: #3b82f6 !important; 
            transform: translateY(-5px) !important; box-shadow: 0 20px 40px rgba(59, 130, 246, 0.25) !important;
        }
        
        /* Compact Red Exit Button */
        button[data-testid="baseButton-secondary"] {
            height: 60px !important; font-size: 1.2rem !important; background-color: #ef4444 !important;
            color: #ffffff !important; border-radius: 20px !important; border: none !important;
            box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3) !important; font-weight: 800 !important;
            width: auto !important; padding: 0 30px !important;
        }
        button[data-testid="baseButton-secondary"]:hover { background-color: #dc2626 !important; }
        
        h1, h2, h3 { text-align: center; margin-bottom: 1.5rem; font-family: 'Nunito', sans-serif;}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>♿ Voice Setup Wizard</h1>", unsafe_allow_html=True)
    
    col_left, _, col_right = st.columns([1, 4, 1])
    with col_left:
        if st.button("❌ Exit Wizard", key="exit_btn", type="secondary"):
            st.session_state.a11y_mode = False
            st.rerun()
            
    st.divider()
    step = st.session_state.a11y_step
    
    if step == 0:
        if 'spoken_welcome' not in st.session_state:
            st.session_state.speak_queue = "Welcome to the Voice Wizard. Tap the giant button below to begin."
            st.session_state.spoken_welcome = True
            st.rerun()
            
        if st.button("🚀 Begin Setup", type="primary", use_container_width=True):
            st.session_state.a11y_step = 1
            st.session_state.speak_queue = "Step one. Tap a preset limit, or speak your absolute data budget aloud by clicking the microphone button."
            st.rerun()
            
    elif step == 1:
        st.markdown("<h2>Choose your Data Internet Rule:</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("500 MB", type="primary", use_container_width=True):
                st.session_state.a11y_budget = 500
                st.session_state.a11y_step = 2
                st.session_state.speak_queue = "Limit set. Step two. Use the microphone to dictate your student's profile."
                st.rerun()
        with col2:
            if st.button("1 GB", type="primary", use_container_width=True):
                st.session_state.a11y_budget = 1024
                st.session_state.a11y_step = 2
                st.session_state.speak_queue = "Limit set. Step two. Use the microphone to dictate your student's profile."
                st.rerun()
        with col3:
            if st.button("2 GB", type="primary", use_container_width=True):
                st.session_state.a11y_budget = 2048
                st.session_state.a11y_step = 2
                st.session_state.speak_queue = "Limit set. Step two. Use the microphone to dictate your student's profile."
                st.rerun()
                
        st.markdown("<p style='text-align: center; color: gray;'>Say things like: '1500 mb' or '2 gb'</p>", unsafe_allow_html=True)
        
        voice_budget_id = st.session_state.get('stt_b_key', 0)
        transcript = speech_to_text(key=f"voice_budget_{voice_budget_id}")
        
        if transcript:
            if transcript == "ERROR_NOT_SUPPORTED": st.error("Browser unsupported.")
            else:
                t = transcript.lower()
                nums = ''.join(filter(str.isdigit, t))
                if nums:
                    val = int(nums)
                    budget = val * 1024 if "gb" in t else val
                    st.session_state.a11y_budget = budget
                    st.session_state.a11y_step = 2
                    st.session_state.speak_queue = f"Understood. Budget set to {budget} megabytes. Step two. Tell me about the student."
                    st.session_state.stt_b_key = voice_budget_id + 1
                    st.rerun()
                else:
                    st.session_state.speak_queue = "I didn't capture a numeric budget limit. Tap microphone to attempt again."
                    st.session_state.stt_b_key = voice_budget_id + 1
                    st.rerun()

    elif step == 2:
        st.markdown("<h2>Add Friends via Voice</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3>Currently Enrolled: {len(st.session_state.students)}</h3>", unsafe_allow_html=True)
        
        voice_student_id = st.session_state.get('stt_s_key', 0)
        transcript = speech_to_text(key=f"voice_student_{voice_student_id}")
        
        if transcript:
            if transcript == "ERROR_NOT_SUPPORTED": st.error("Browser unsupported.")
            else:
                t = transcript.lower()
                words = t.split()
                name = "Unknown"
                if "name is" in t:
                    try:
                        idx = words.index("is")
                        if idx + 1 < len(words): name = words[idx + 1].replace(',', '').replace('.', '').capitalize()
                    except ValueError: pass
                elif len(words) > 0:
                    name = words[0].replace(',', '').replace('.', '').capitalize()
                    
                age = 12
                for w in words:
                    cand = ''.join(filter(str.isdigit, w))
                    if cand:
                        age = int(cand)
                        break
                        
                level = "Beginner"
                goal = "Basic Literacy"
                if "concept" in t: goal = "Concept Building"
                if "exam" in t: goal = "Exam Preparation"
                
                new_st = {"name": name, "age": age, "level": level, "goal": goal}
                st.session_state.students.append(new_st)
                
                st.session_state.speak_queue = f"Transcribed successfully. Added {name}, age {age}."
                st.session_state.stt_s_key = voice_student_id + 1
                st.rerun()
                
        st.divider()
        if st.button("✅ Calculate Result", type="primary", use_container_width=True):
            st.session_state.a11y_step = 3
            st.rerun()
            
    elif step == 3:
        budget = st.session_state.a11y_budget
        results, global_used_mb = optimize_allocations(st.session_state.students, budget, low_data_mode=False)
        eff_score, recommendations = generate_ai_insights(results, global_used_mb, budget, False)
        
        if 'spoken_results' not in st.session_state:
            rec_text = recommendations[0] if recommendations else "No alerts."
            st.session_state.speak_queue = f"Finished. Final payload of {global_used_mb} megabytes out of {budget}."
            st.session_state.spoken_results = True
            st.rerun()
            
        st.markdown(f"<h2>Payload Processed: {global_used_mb} MB / {budget} MB</h2>", unsafe_allow_html=True)
        st.divider()
        st.markdown("<h2>Student Plans Generated</h2>", unsafe_allow_html=True)
        # Compact Voice Output mode
        grid_cols = st.columns(2)
        for i, s in enumerate(st.session_state.students):
            res = results[i]
            with grid_cols[i % 2]:
                with st.container(border=True):
                    st.markdown(f"<h2 style='margin: 0;'>{s['name']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #8b5cf6; font-weight: 800;'>{res['allocated_mb']} MB</p>", unsafe_allow_html=True)
                    for key, count in res['plan'].items():
                        if count > 0:
                            st.markdown(f"<h4>{count}x {CONTENT_LABELS[key]}</h4>", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.students = []
            st.session_state.a11y_step = 0
            if 'spoken_welcome' in st.session_state: del st.session_state.spoken_welcome
            if 'spoken_results' in st.session_state: del st.session_state.spoken_results
            st.rerun()


def main():
    if st.session_state.a11y_mode:
        render_a11y_mode()
    else:
        render_standard_mode()

if __name__ == "__main__":
    main()
