# 🎨 ByteWise Kids Dashboard: Study Time & Data Allocator 🚀

ByteWise is a highly interactive, accessible, and dynamic learning data allocation platform built with Streamlit. It solves a crucial problem in modern digital education: **How do we fairly distribute a limited internet data allowance safely across multiple students learning at different grades and speeds?**

The dashboard employs a strict constraint-optimization engine that distributes granular "Learning Quests" (Text, Audio, Quizzes, Video) natively, evaluating age, learning maturity, and baseline goals recursively until the global internet data threshold is perfectly consumed at `100.0%` efficiency.

## ✨ System Features

### 1. 🎙️ One-Shot Intelligent Voice Command 
Say goodbye to complex input forms! Emphasizing absolute accessibility for disabled, motor-impaired, or young users, ByteWise implements a **Voice Sandbox Escape**.
- **Omni-Directional NLP Parser:** Users can tap the microphone and speak freely: *"Rahul, 12 years, intermediate, exam preparation, 1 GB data"*.
- **Regex-Driven Subparser:** The backend isolates critical schema fields intelligently without relying on paid black-box LLMs, deploying it natively to the manual entry forms for instant visual validation.

### 2. ⚡ Turbo Saving Mode Auto-Engagement
ByteWise continuously evaluates the `Base Demand` vs the `Global Quota`.
- If a user demands more resources than physically possible, the internal load-balancer fires **Turbo Saving Mode**, physically ripping out high-cost payloads (Full HD Video Lessons -> 150 MB) and seamlessly shifting them to lightweight conceptual equivalents (Mini Quizzes -> 15 MB) dynamically.

### 3. ♿ Blind-Interface Accessibility Mode
The dashboard ships with a hidden accessibility fallback for physically damaged screens:
- Converting the complex masonry parameter arrays into a monolithic logic sequence navigated purely via audio.
- A unified microphone captures intent cleanly with Voice Command overrides (`"begin"`, `"calculate"`, `"clear"`).

### 4. 🧠 Autonomous Metric Insights
The framework acts as a real-time monitor, validating global usage heuristics after the constraint algorithm successfully bounds variables. It automatically fires heuristic alerts on overload thresholds.

## 🧱 Technical Architecture 
*   **Python 3.x & Streamlit**: The core framework driving state mutation (`st.session_state`) and frontend reactivity.
*   **HTML5/Javascript Hooks**: Built a custom bi-directional Streamlit component wrapping the `window.SpeechRecognition` API. A critical iframe-sandbox breakout was achieved to securely harvest the user's microphone streams utilizing top-level browser roots to bypass block constraints!
*   **Custom Styling**: Pure CSS injected rapidly (`st.markdown`) to purge default Streamlit margins and force pastel-based floating soft-shadow arrays.

## 🚀 Installation & Deployment

1. **Clone the Repository:**
   ```bash
   git clone <your-repository-url>
   cd Study_Time_Allocator
   ```
2. **Install Depenecies:**
   You must have `streamlit` installed locally.
   ```bash
   pip install streamlit
   ```
3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```
   *The system binds gracefully to port `8501`. Navigate to `http://localhost:8501` to test the module!*
