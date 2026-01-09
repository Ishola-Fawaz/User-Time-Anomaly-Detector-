# Login Anomaly Detector

**Group Project: Time-Based Anomaly Detection System**

## Project Overview
This system monitors user logins in real-time and detects anomalies based on **Role-Based Time Windows**. It distinguishes between normal behavior (e.g., a student logging in during the day) and suspicious behavior (e.g., a student logging in at midnight).

## Key Features
- **Real-Time Detection**: Instantly flags logins as "Normal", "Abnormal", or "Blocked".
- **Role-Based Logic**:
    - **Student**: Allowed 08:00 - 17:00.
    - **Guard**: Allowed 18:00 - 06:00.
    - **Admin**: Allowed 24/7.
- **Visual Dashboard**: Interactive charts and live tables.
- **Historic Data**: Database seeded with realistic login history.

---

## 🚀 How to Run the Project

1.  **Open Terminal** and navigate to the project folder.
2.  **Start the Application**:
    ```bash
    python app.py
    ```
3.  **Open in Browser**:
    Go to **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---
