# 🔐 Secure SDLC Demonstration Web Application

A secure web application built using **Python Flask** to demonstrate the implementation of **Secure Software Development Lifecycle (SSDLC)** practices.

The project integrates multiple security controls such as password hashing, HTTPS encryption, input validation, brute-force protection, and security logging while following **Privacy by Design** principles.

---

# 📌 Project Overview

This project demonstrates how security can be integrated into the development process from the design stage through implementation. The application allows users to register and log in securely while protecting sensitive data through modern security practices.

Key focus areas include:

* Secure authentication implementation
* Protection against common web attacks
* Security monitoring through logging
* Threat modeling and risk analysis
* Privacy-aware application design

---

# 🛡 Security Features Implemented

The application implements the following security controls:

* **Password Hashing**
  User passwords are hashed using **PBKDF2** before storage to prevent plaintext credential exposure.

* **HTTPS Encryption**
  Communication between client and server is encrypted using HTTPS to protect data in transit.

* **Input Validation**
  User inputs are validated to prevent malicious payloads and injection attacks.

* **SQL Injection Prevention**
  Parameterized database queries are used to ensure safe database operations.

* **Brute Force Protection**
  Login attempts are tracked by IP address and temporarily blocked after multiple failed attempts.

* **Security Logging**
  Security-related events such as failed login attempts and user registrations are logged for monitoring and auditing.

* **Secure HTTP Headers**
  Security headers are added to mitigate attacks such as clickjacking and MIME-type sniffing.

---

# 🔐 Privacy by Design

This application follows **Privacy by Design principles** by:

* Minimizing personal data collection (only email and password)
* Hashing credentials before storage
* Avoiding logging of sensitive information
* Encrypting communication via HTTPS
* Implementing secure authentication mechanisms

These practices help ensure **data confidentiality, integrity, and protection of user privacy**.

---

# 🏗 Architecture Overview

System Flow:

User
↓
HTTPS Request
↓
Flask Web Application
↓
Input Validation
↓
Password Hashing
↓
SQLite Database
↓
Security Logging

---

# 📂 Project Structure

```
sdlc_website
│
├── app.py
├── README.md
├── docs
│   ├── threat_model.md
│   ├── risk_analysis.md
│   └── data_flow_diagram.png
│
├── .gitignore
```

Ignored files (not stored in repository):

```
cert.pem
key.pem
users.db
app.log
```

---

# ⚙️ Local Setup Instructions

## 1️⃣ Clone the Repository

```
git clone https://github.com/sujankc67/sdlc_website.git
cd sdlc_website
```

---

## 2️⃣ Install Dependencies

```
pip install flask
```

---

## 3️⃣ Generate SSL Certificates (for HTTPS)

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

---

## 4️⃣ Run the Application

```
python app.py
```

---

## 5️⃣ Open the Application

Open your browser and visit:

```
https://localhost:5000
```

Because a self-signed certificate is used, the browser may show a security warning. This is expected for local development.

---

# 📊 Threat Modeling (STRIDE)

| Threat                 | Example                     | Mitigation             |
| ---------------------- | --------------------------- | ---------------------- |
| Spoofing               | Unauthorized login attempts | Password hashing       |
| Tampering              | Manipulated requests        | HTTPS encryption       |
| Repudiation            | User denying actions        | Security logging       |
| Information Disclosure | Data leakage                | Encrypted credentials  |
| Denial of Service      | Brute force login attacks   | Login attempt limiting |
| Privilege Escalation   | Unauthorized access         | Input validation       |

---

# 📈 Risk Analysis

| Risk                | Likelihood | Impact | Mitigation                 |
| ------------------- | ---------- | ------ | -------------------------- |
| Credential theft    | Medium     | High   | Password hashing           |
| SQL injection       | Medium     | High   | Parameterized queries      |
| Data exposure       | Low        | High   | HTTPS encryption           |
| Brute force attacks | Medium     | Medium | Login attempt restrictions |

---

# 📷 Screenshots

Example screenshots that can be added:

* User Registration Page
* Login Page
* Security Log Output
* Successful Login Dashboard

---

# 🚀 Future Improvements

Possible enhancements for further security improvements:

* Multi-Factor Authentication (MFA)
* Rate limiting
* JWT-based authentication
* Containerization using Docker
* Automated security testing using OWASP ZAP
* Deployment using cloud platforms

---

# 📚 Technologies Used

* Python
* Flask
* SQLite
* OpenSSL
* Git & GitHub

---

# 🎯 Learning Outcome

This project demonstrates practical implementation of:

* Secure Software Development Lifecycle (SSDLC)
* Secure authentication mechanisms
* Basic threat modeling and risk analysis
* Privacy by Design principles
* Secure coding practices in web development

---

# 📜 License

This project is created for educational and demonstration purposes.
