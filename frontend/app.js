// Point this to your FastAPI backend address
const API_BASE_URL = "http://127.0.0.1:8000";

// ==========================================
// 1. LOGIN PAGE LOGIC (index.html)
// ==========================================
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // Stops the '?' page refresh!

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const errorMsg = document.getElementById("errorMessage");

        try {
            const response = await fetch(`${API_BASE_URL}/users/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email, password: password })
            });

            const data = await response.json();

            if (response.ok) {
                // Success! Save tokens and redirect
                localStorage.setItem("token", data.access_token);
                localStorage.setItem("role", data.role);
                localStorage.setItem("name", data.name);
                
                alert("Login Successful! Welcome " + data.name);
                window.location.href = "dashboard.html"; 
            } else {
                errorMsg.style.display = "block";
                errorMsg.innerText = data.detail || "Invalid credentials";
            }
        } catch (error) {
            errorMsg.style.display = "block";
            errorMsg.innerText = "Cannot connect to the server. Is FastAPI running?";
        }
    });
}

// ==========================================
// 2. DASHBOARD PAGE LOGIC (dashboard.html)
// ==========================================
if (window.location.pathname.includes("dashboard.html")) {
    
    // Security Check
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Security Alert: You must be logged in to access the dashboard.");
        window.location.href = "index.html"; 
    }

    // Personalize the Dashboard
    const userName = localStorage.getItem("name");
    document.getElementById("welcomeMessage").innerText = "Welcome, " + userName + "!";

    // Logout Functionality
    document.getElementById("logoutBtn").addEventListener("click", () => {
        localStorage.clear(); 
        window.location.href = "index.html"; 
    });

    // Fetch Students
    async function loadStudents() {
        try {
            const response = await fetch(`${API_BASE_URL}/students/`);
            const data = await response.json();
            const list = document.getElementById("studentsList");
            list.innerHTML = ""; 
            
            data.students.forEach(student => {
                let li = document.createElement("li");
                li.innerHTML = `<strong>${student.name}</strong> (${student.roll_no}) - ${student.class}`;
                list.appendChild(li);
            });
        } catch (error) {
            document.getElementById("studentsList").innerText = "Error loading students.";
        }
    }

    // Fetch Subjects
    async function loadSubjects() {
        try {
            const response = await fetch(`${API_BASE_URL}/subjects/`);
            const data = await response.json();
            const list = document.getElementById("subjectsList");
            list.innerHTML = ""; 
            
            data.subjects.forEach(subject => {
                let li = document.createElement("li");
                li.innerText = subject.name;
                list.appendChild(li);
            });
        } catch (error) {
            document.getElementById("subjectsList").innerText = "Error loading subjects.";
        }
    }

    // Fire the table loaders
    loadStudents();
    loadSubjects();

    // --- ADMIN CONTROL PANEL LOGIC ---

    // Submit New Subject
    document.getElementById("subjectForm").addEventListener("submit", async (e) => {
        e.preventDefault(); 
        const name = document.getElementById("subjName").value;
        try {
            const res = await fetch(`${API_BASE_URL}/subjects/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: name })
            });
            const data = await res.json();
            if(res.ok) { 
                alert("Success: " + data.message); 
                document.getElementById("subjectForm").reset(); 
                loadSubjects(); 
            } else { alert("Error: " + data.detail); }
        } catch (error) { alert("Server error"); }
    });

    // Submit New Student
    document.getElementById("studentForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            name: document.getElementById("stuName").value,
            roll_no: document.getElementById("stuRoll").value,
            student_class: document.getElementById("stuClass").value
        };
        try {
            const res = await fetch(`${API_BASE_URL}/students/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if(res.ok) { 
                alert("Success: " + data.message); 
                document.getElementById("studentForm").reset(); 
                loadStudents(); 
            } else { alert("Error: " + data.detail); }
        } catch (error) { alert("Server error"); }
    });

    // Assign New Result
    document.getElementById("resultForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            student_id: parseInt(document.getElementById("resStudentId").value),
            subject_id: parseInt(document.getElementById("resSubjectId").value),
            marks: parseInt(document.getElementById("resMarks").value)
        };
        try {
            const res = await fetch(`${API_BASE_URL}/results/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if(res.ok) { 
                alert(`Success! Final Grade Calculated: ${data.grade}`); 
                document.getElementById("resultForm").reset(); 
            } else { alert("Error: " + data.detail); }
        } catch (error) { alert("Server error"); }
    });
}