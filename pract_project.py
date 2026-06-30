import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Semiconductor Virtual Lab & Analytics",
    page_icon="🔬",
    layout="wide"
)

# --- DIRECTORY & FILE SETUP FOR LEARNING ANALYTICS ---
LOG_FILE = "student_analytics_log.csv"

def log_user_action(student_id, action_type, details):
    """Logs student telemetry data to a CSV file for learning analytics."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = pd.DataFrame([{
        "Timestamp": timestamp,
        "Student_ID": student_id,
        "Action_Type": action_type,
        "Details": str(details)
    }])
    
    if not os.path.isfile(LOG_FILE):
        log_data.to_csv(LOG_FILE, index=False)
    else:
        log_data.to_csv(LOG_FILE, mode='a', header=False, index=False)

# --- INITIALIZE SESSION STATE VARIABLES ---
if 'student_id' not in st.session_state:
    st.session_state['student_id'] = "Guest_Student"
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'quiz_submitted' not in st.session_state:
    st.session_state['quiz_submitted'] = False

# --- APPLICATION HEADER ---
st.title("🔬 Virtual Instrumentation & Learning Analytics Platform")
st.subheader("Department of Physics/Electronics — Solid State Semiconductor Physics Lab")
st.markdown("---")

# --- USER AUTHENTICATION / LOGIN ---
if not st.session_state['authenticated']:
    st.info("👋 Welcome! Please enter your Student Matriculation Number to initialize the instrumentation bench and tracking metrics.")
    matric_no = st.text_input("Enter Student Matriculation Number (e.g., HND/PHY/2024/001):")
    if st.button("Initialize Lab Bench"):
        if matric_no.strip() != "":
            st.session_state['student_id'] = matric_no.strip()
            st.session_state['authenticated'] = True
            log_user_action(st.session_state['student_id'], "Session_Start", "Initialized laboratory bench simulator.")
            st.rerun()
        else:
            st.warning("Please enter a valid identification number.")
    st.stop()

# --- SIDEBAR: VIRTUAL INSTRUMENTATION CONTROLS (THE HARDWARE BENCH) ---
st.sidebar.header("🎛️ Virtual Instrument Bench Controls")
st.sidebar.markdown("*Simulating DC Power Supply & Thermal Chamber controls*")

# Student configuration controls
material = st.sidebar.selectbox("1. Select Semiconductor Material", ["Silicon (Si)", "Germanium (Ge)"])
temp_celsius = st.sidebar.slider("2. Thermal Chamber Temperature (°C)", min_value=-50, max_value=150, value=25, step=5)
doping_concentration = st.sidebar.select_slider("3. Acceptor/Donor Doping Level (cm⁻³)", 
                                                options=[1e15, 1e16, 1e17, 1e18], value=1e16)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Logged in as:** `{st.session_state['student_id']}`")
if st.sidebar.button("Log Out / Reset Bench"):
    log_user_action(st.session_state['student_id'], "Session_End", "Logged out of bench.")
    st.session_state['authenticated'] = False
    st.session_state['quiz_submitted'] = False
    st.rerun()

# Log variable modifications natively for analytics tracking
if st.sidebar.button("Log Current Parameter Calibration"):
    details = f"Material: {material}, Temp: {temp_celsius}°C, Doping: {doping_concentration}"
    log_user_action(st.session_state['student_id'], "Parameter_Calibration", details)
    st.sidebar.success("Telemetry telemetry stored!")

# --- CORE MATHEMATICAL PHYSICS SIMULATION ENGINE ---
def simulate_pn_junction(material, temp_c, doping):
    # Fundamental Constants
    q = 1.602e-19       # Charge of electron (C)
    k = 1.381e-23       # Boltzmann constant (J/K)
    T = temp_c + 273.15 # Convert to Absolute Kelvin
    
    # Material specific properties
    Eg = 1.12 if "Silicon" in material else 0.67  # Bandgap Energy in eV
    eta = 1.0  # Ideality factor
    
    # Calculate thermal voltage Vt
    V_thermal = (k * T) / q
    
    # Model scale factor for reverse saturation current Is tracking over temperature
    Is0 = 1e-12 if "Silicon" in material else 1e-6
    # Is scales exponentially with temperature variations
    Is = Is0 * ((T / 300.15) ** 3) * np.exp(-Eg / (2 * V_thermal))
    
    # Adjust Is slightly based on doping level (higher doping equals lower leakage)
    Is = Is * (1e16 / doping)
    
    # Generate Applied Voltage Array spanning from Reverse Breakdown to Forward Bias
    v_forward = np.linspace(0, 0.85, 100)
    v_reverse = np.linspace(-5, 0, 50)
    v_array = np.concatenate((v_reverse, v_forward))
    
    # Apply the Shockley Ideal Diode Equation
    i_array = Is * (np.exp(v_array / (eta * V_thermal)) - 1)
    
    # Simulate simple Zener/Avalanche breakdown behavior in extreme reverse bias
    breakdown_voltage = -4.0 if "Silicon" in material else -3.0
    i_array = np.where(v_array < breakdown_voltage, i_array - 0.05 * (breakdown_voltage - v_array)**2, i_array)
    
    return v_array, i_array, V_thermal, Is

# Execute simulation based on sidebar state inputs
v_data, i_data, vt, leakage_current = simulate_pn_junction(material, temp_celsius, doping_concentration)

# --- MAIN DASHBOARD GRAPHICS LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Live Telemetry: P-N Junction I-V Characteristics Curve")
    st.markdown("Interact with the plot to read coordinate variables precisely. Note how altering parameters changes the knee voltage and reverse leakage currents.")
    
    # Plotly Visual Layout Rendering
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=v_data, y=i_data, mode='lines', name=material, line=dict(color='#FF4B4B', width=3)))
    
    fig.update_layout(
        xaxis_title="Applied Bias Voltage (V)",
        yaxis_title="Diode Current (A)",
        xaxis=dict(range=[-5.5, 1.0], zeroline=True, zeroimagename="black"),
        yaxis=dict(range=[-0.01, 0.05], zeroline=True, zeroimagename="black"),
        template="plotly_dark",
        margin=dict(l=20, r=20, t=20, b=20),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Virtual Instrument Readout")
    st.markdown("Calculated theoretical properties computed by the Physics engine logic:")
    
    st.metric(label="Thermal Voltage (V_thermal)", value=f"{vt:.4f} V")
    st.metric(label="Reverse Saturation Leakage Current (I_s)", value=f"{leakage_current:.4e} A")
    
    knee_v = 0.7 if "Silicon" in material else 0.3
    st.markdown(f"**Expected Turn-on (Knee) Voltage:** ~`{knee_v}V` at room temperature.")
    
    # Helpful pedagogical hints
    st.info("💡 **Physics Hint:** As temperature increases, notice how the thermal voltage increases and the entire forward curve shifts to the left, reflecting a reduction in barrier resistance.")

st.markdown("---")

# --- INTERACTIVE PEDAGOGICAL ASSESSMENT LAYER ---
st.header("📝 Diagnostic Evaluation Module")
st.markdown("Answer the dynamic analytical questions below based on your instrumentation testing trends above.")

with st.form("quiz_form"):
    q1 = st.radio(
        "1. Based on your adjustments, what happens to the reverse saturation current (leakage) when the chamber temperature increases?",
        ["It decreases exponentially.", "It increases exponentially.", "It remains perfectly constant since it depends entirely on voltage."]
    )
    
    q2 = st.radio(
        "2. Which material exhibits a lower forward barrier turn-on (knee) potential during active forward biasing?",
        ["Silicon (Si)", "Germanium (Ge)", "Both trigger conductivity profiles symmetrically at 0.7V."]
    )
    
    submitted = st.form_submit_form("Submit Practical Evaluation Answers")
    
    if submitted:
        st.session_state['quiz_submitted'] = True
        score = 0
        details_summary = ""
        
        # Grade evaluation logic
        if q1 == "It increases exponentially.":
            score += 50
        if q2 == "Germanium (Ge)":
            score += 50
            
        st.subheader("🎯 Test Performance Results")
        st.write(f"Your calculated comprehension score: **{score}/100**")
        
        if score == 100:
            st.success("Excellent! You've accurately calibrated your variables and recorded real semiconductor physical metrics.")
        else:
            st.error("Some answers are incorrect. Adjust the parameters on the sidebar bench to review the physical curves again.")
            
        # Log results to the Instructor's Analytics Registry
        log_user_action(st.session_state['student_id'], "Quiz_Submission", f"Score: {score}%. Q1: {q1}, Q2: {q2}")

st.markdown("---")

# --- ADMINISTRATIVE INSTRUCTOR ANALYTICS AREA ---
st.header("📊 Instructor Portal & Learning Analytics Summary")
st.markdown("*This tracking interface provides real-time oversight of student interactions to map learning workflows transparently.*")

if os.path.exists(LOG_FILE):
    try:
        df_logs = pd.read_csv(LOG_FILE)
        # Filter for current user to show immediate interaction tracking trail
        user_logs = df_logs[df_logs["Student_ID"] == st.session_state['student_id']]
        
        col_summary1, col_summary2 = st.columns(2)
        with col_summary1:
            st.subheader("Your Live Telemetry Log Profile")
            st.dataframe(user_logs, use_container_width=True)
            
        with col_summary2:
            st.subheader("Global Action Breakdown Metric")
            action_counts = df_logs["Action_Type"].value_value_counts().reset_index()
            action_counts.columns = ["Action", "Frequency"]
            
            fig_pie = go.Figure(data=[go.Pie(labels=action_counts["Action"], values=action_counts["Frequency"], hole=.3)])
            fig_pie.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=30, b=10), height=250)
            st.plotly_chart(fig_pie, use_container_width=True)
    except Exception as e:
        st.warning("Data repository tracking stream initializing...")
else:
    st.info("No learning analytics records have been aggregated yet. Interact with control structures above to initialize tracking pipelines.")