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

## 🎤 Demo Script (For Supervisors)

**Step 1: Introduction**
> "We built a system that prevents unauthorized access based on time. Instead of complex black-box AI, we used deterministic logic that ensures specific roles can only login during their assigned shifts."

**Step 2: Show the Logic**
- Open `detector/core.py`.
- Point to the `USER_WINDOWS` dictionary at the top.
> "Here are the strict rules. As you can see, Students are restricted to daytime, while Guards are restricted to nighttime."

**Step 3: Show the Dashboard**
- Show the **"Summary Cards"** at the top.
> "The dashboard gives an immediate overview of system health, showing total logins and detected anomalies."

**Step 4: Live Demonstration**
1.  **Select "Student"** from the dropdown.
2.  **If Daytime**: Click "Log In".
    - *Result*: **Green "Normal Login"**.
    - *Explanation*: "Since it's day, the student works."
3.  **If Nighttime**: Click "Log In".
    - *Result*: **Red "Anomaly Detected"**.
    - *Explanation*: "The system correctly flagged this as suspicious."
4.  **Select "Guard"** and repeat to show the inverse behavior.

**Step 5: Conclusion**
- Scroll through the "Live Login Monitor" table.
> "We also maintain a full audit trail of all attempts, clearly labeled with the reason for approval or rejection."
