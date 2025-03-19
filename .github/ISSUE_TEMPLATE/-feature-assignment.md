---
name: " Feature Assignment"
about: 'about: Assign a new feature development task to a collaborator'
title: ''
labels: ''
assignees: ''

---

When assigning a feature development task to a collaborator, you should provide clear details to ensure they understand what needs to be done. Below is a structured **task content template** you can use when assigning a feature in GitHub Issues, Slack, or any project management tool.  

---

### **🚀 Feature Assignment Template**  

#### **📌 Feature Title:**  
`[Feature Name]` (e.g., "Implement User Login System")  

#### **📝 Description:**  
Provide a brief overview of what this feature should do.  
> Example:  
> "Develop a user authentication system where users can register, log in, and log out. The login system should use a username and password-based authentication, storing passwords securely using hashing."

#### **✅ Requirements / Acceptance Criteria:**  
List the key functionalities the feature must include.  

✔ User can **register** with a unique username and password  
✔ User can **log in** with valid credentials  
✔ User gets an error message for incorrect credentials  
✔ Passwords should be securely hashed (e.g., using `bcrypt`)  
✔ Implement a **logout feature** that destroys the session  
✔ Redirect users to the correct pages after login/logout  

#### **📂 File & Code Structure:**  
Mention where the code should be implemented and any specific files to modify.  
> Example:  
> - Create a new Django app: `auth_system`  
> - Define models in `models.py`  
> - Implement views in `views.py`  
> - Use HTML forms in `templates/auth/`  
> - Routes in `urls.py`  

#### **🔧 Tech Stack & Guidelines:**  
Specify any libraries, frameworks, or coding guidelines.  
> Example:  
> - Backend: Django, Python  
> - Frontend: HTML, Bootstrap  
> - Authentication: Custom (not Django’s built-in auth system)  
> - Hashing: `bcrypt` for password security  

#### **⏳ Deadline:**  
Specify when you expect the feature to be completed.  
> Example: `March 22, 2025`  

#### **📌 Branching & PR Process:**  
Explain how the collaborator should work on this feature.  
1. Create a new branch from `main`:  
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature-user-auth
   ```  
2. Work on the feature and commit changes.  
3. Push the branch and create a **Pull Request (PR)**.  
4. Assign the PR to **[Your Name]** for review.  

---

### **🔄 Additional Notes:**  
- If you face any issues, tag me in the GitHub issue or Slack.  
- Follow the existing project structure for consistency.  
- Ensure code is properly documented and formatted.  

---

### **💡 Next Steps**  
Would you like me to help you draft this as a **GitHub Issue template** so you can use it repeatedly? 🚀
