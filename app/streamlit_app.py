import streamlit as st
import requests
import time
from calculator import Calculator

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Jenkins AutoTesting 🚀", page_icon="⚙️", layout="centered")
st.title("🛠️ Jenkins AutoTesting Calculator")

# --- Background image via HTML ---
st.markdown("""
    <style>
        body {
            background-image: url("https://cdn.wallpapersafari.com/97/31/nsDGar.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            height: 100vh;
        }
        .main {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2rem;
            border-radius: 10px;
            max-width: 900px;
            margin: 0 auto;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Input fields ---
num1 = st.number_input("🔢 Enter Number 1", value=0, step=1, format="%d")
num2 = st.number_input("🔢 Enter Number 2", value=0, step=1, format="%d")

operation = st.selectbox("🔧 Choose Operation", ["Add", "Subtract", "Multiply", "Divide"])

# --- Submit Button ---
if st.button("🚀 Submit and Run Tests"):
    calc = Calculator()

    try:
        # Perform calculation
        if operation == "Add":
            result = calc.add(num1, num2)
        elif operation == "Subtract":
            result = calc.subtract(num1, num2)
        elif operation == "Multiply":
            result = calc.multiply(num1, num2)
        elif operation == "Divide":
            # Explicitly check for division by zero
            if num2 == 0:
                raise ValueError("🚨 Division by Zero Error!")
            result = calc.divide(num1, num2)

        st.success(f"🎯 Result: **{result}**")
        
        # --- GitHub Info from Streamlit Secrets ---
        GITHUB_TOKEN = st.secrets["github"]["token"]
        REPO_OWNER = st.secrets["github"]["repo_owner"]
        REPO_NAME = st.secrets["github"]["repo_name"]
        WORKFLOW_FILE = st.secrets["github"]["workflow_file"]

        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        # --- Trigger GitHub Action ---
        dispatch_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches"
        dispatch_payload = {"ref": "main"}
        dispatch_response = requests.post(dispatch_url, headers=headers, json=dispatch_payload)

        if dispatch_response.status_code == 204:
            st.success("✅ GitHub Action triggered successfully!")
        else:
            st.error(f"❌ Failed to trigger GitHub Action. Status: {dispatch_response.status_code}")
            st.stop()

        # --- Poll for Workflow Status ---
        st.info("⏳ Waiting for GitHub Action to complete...")
        time.sleep(5)  # Small delay to let the workflow start

        runs_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"
        build_status_placeholder = st.empty()
        build_time_placeholder = st.empty()
        progress_bar = st.progress(0)

        build_completed = False
        progress = 0
        start_time = time.time()

        while not build_completed:
            runs_response = requests.get(runs_url, headers=headers)
            if runs_response.status_code == 200:
                runs_data = runs_response.json()
                latest_run = runs_data["workflow_runs"][0]

                status = latest_run["status"]  # queued, in_progress, completed
                conclusion = latest_run["conclusion"]  # success, failure, cancelled

                elapsed_time = int(time.time() - start_time)
                build_time_placeholder.info(f"⏱️ Build Time: {elapsed_time} seconds")

                if status == "completed":
                    build_completed = True
                    if conclusion == "success":
                        build_status_placeholder.success("✅ Build Passed! 🎉")
                    else:
                        build_status_placeholder.error("❌ Build Failed! ❗")
                    progress_bar.empty()
                else:
                    build_status_placeholder.info(f"🔄 Build {status.capitalize()}... Please wait")
                    progress = (progress + 8) % 100
                    progress_bar.progress(progress)

                time.sleep(5)
            else:
                build_status_placeholder.error("❌ Failed to fetch workflow runs.")
                st.stop()

    except ValueError as e:
        st.error(f"🚨 Error: {e}")
        st.markdown("### 🔴 Build Failed! ❌", unsafe_allow_html=True)
        
        # Triggering a test for the failed operation
        try:
            # Triggering division by zero test
            calc.divide(1, 0)
        except Exception as e:
            st.error(f"❌ Error occurred while performing the test: {e}")
            st.stop()

    except Exception as e:
        st.error(f"🚨 Unexpected Error: {e}")
        st.markdown("### 🔴 Build Failed! ❌", unsafe_allow_html=True)
