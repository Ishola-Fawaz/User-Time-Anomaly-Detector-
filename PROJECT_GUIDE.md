# Project Guide: Login Anomaly Detector

This document serves as the master guide for **Users**, **Developers**, and **Supervisors**.

---

## 📘 Part 1: User Guide (For You & Colleagues)

### **Getting Started**
1.  Open the **Dashboard** at `http://127.0.0.1:5000`.
2.  You will see:
    *   **Summary Cards**: Quick stats (Total Logins, Anomalies).
    *   **Login Simulator**: A panel to try logging in as different users.
    *   **Live Monitor**: A real-time table showing all activity.

### **How to Use**
*   **Normal Login**: Select a user (e.g., `Student`) during their allowed hours (Daytime). You will see a **Green Success** message.
*   **Simulate Attack**: Select a user outside their allowed hours (e.g., `Student` at Midnight). You will see a **Red Alert** and a popup warning.
*   **Download Report**: Click the blue **"DOWNLOAD REPORT"** button to get a CSV file of all logs.

---

## 🛠️ Part 2: Developer Guide (Technical Details)

### **System Architecture**
*   **Backend**: Python (Flask).
*   **Database**: SQLite (`database.db`).
*   **Frontend**: HTML + Tailwind CSS + JavaScript.

### **Key Files**
*   `app.py`: The web server and API endpoints.
*   `detector/core.py`: **The Brain**. This file contains the logic for `USER_WINDOWS` (Time-based rules).
*   `seed_data.py`: A script used to generate dummy data for the presentation.

### **Logic Explanation**
The system uses **Role-Based Time Windows**:
```python
USER_WINDOWS = {
    'student': (8, 17),    # 8 AM - 5 PM
    'guard': (18, 6),      # 6 PM - 6 AM
    'admin': (0, 24)       # All Day
}
```
If a user logs in outside these hours, it is flagged as an `anomaly`.

---

## 🎓 Part 3: Supervisor Guide (Presentation)

### **Project Pitch**
"We developed a proactive security system that detects insider threats based on behavioral patterns. Instead of waiting for a hack, we stop unauthorized access attempts by enforcing strict time-based policies for valid credentials."

### **Features Delivered**
1.  ✅ **Real-Time Detection**: Immediate flagging of anomalies.
2.  ✅ **Role-Based Security**: Custom rules for Students vs Guards.
3.  ✅ **Visual Dashboard**: Live monitoring with charts.
4.  ✅ **Reporting**: CSV Export for compliance.
5.  ✅ **Alert System**: Instant visual feedback on threats.

### **Demo Script**
1.  **Show Logic**: Open `core.py` to prove the rules exist.
2.  **Show Dashboard**: Point out the "Live Monitor" and "Summary Cards".
3.  **Action - Normal**: Log in as `Student` (Day) -> **Green**.
4.  **Action - Anomalous**: Log in as `Student` (Night) -> **Red Alert Popup**.
5.  **Action - Report**: Download the CSV to show audit capability.
