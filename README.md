# Virtual Instrumentation & Learning Analytics Platform for Semiconductor Physics

An interactive, web-based virtual laboratory application designed for Higher National Diploma (HND) Physics and Electronics programs. This platform serves as a software-defined laboratory instrument (simulating a digital curve tracer/oscilloscope) to model solid-state semiconductor components under varying conditions while actively tracking student pedagogical metrics.

## 🚀 Live Demo
[Insert your live Streamlit Community Cloud URL here once deployed]

---

## 📌 Project Overview
In tertiary institutions, access to high-precision physical lab instruments (such as source measurement units, variable DC power supplies, and thermal chambers) is frequently limited by high cost or hardware shortages. 

This project bridges that gap by implementing a **Virtual Instrumentation Layer** using Python and Streamlit. The application models the underlying solid-state physics equations dynamically based on user interface inputs. Concurrently, an embedded **Learning Analytics Engine** logs student interaction telemetry data, mapping procedural troubleshooting efficiency for academic coordinators.

---

## 🛠️ Features

* **Scientific Physics Simulation Engine:** Iteratively models the forward and reverse bias states of Silicon (Si) and Germanium (Ge) junctions using the Shockley Ideal Diode Equation.
* **Thermal Chamber Simulator:** Simulates temperature-dependent variations (from -50°C to 150°C), altering thermal voltages ($V_t$) and calculating exponential saturation current ($I_s$) scales on the fly.
* **Avalanche Breakdown Controls:** Simulates high-field electron multiplier collisions and reverse breakdown profiles.
* **Interactive UI/UX Canvas:** Leverages Plotly graphics to enable precise coordinate querying and visualization.
* **Persistent Student Telemetry Log:** Captures and serializes parameter adjustments, timestamps, and quiz metrics asynchronously into a structured format.
* **Instructor Oversight Portal:** Provides live visualization dashboards displaying global cohort actions and learning activity metrics.

---

## 📐 System Architecture

The application is structured into three unified tiers to maintain absolute separation of concerns:

```text
[Student Frontend UI] <─── Session State ───> [Learning Analytics Engine]
         │                                              │
         ▼                                              ▼
[Mathematical Physics Engine]                [Persistent SQLite/CSV Storage]


├── app.py                      # Main Streamlit application source code
├── requirements.txt            # Python third-party dependency file
├── student_analytics_log.csv   # Aggregated telemetry log file (Auto-generated)
└── README.md                   # Project documentation manual
