// --- DASHBOARD LOGIC ---

// Check if we are currently on the dashboard page
if (window.location.pathname.includes("dashboard.html")) {
    
    // 1. Security Check: Block users who don't have a token
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Security Alert: You must be logged in to access the dashboard.");
        window.location.href = "index.html"; // Kick them back to login
    }

    // 2. Personalize the Dashboard
    const userName = localStorage.getItem("name");
    document.getElementById("welcomeMessage").innerText = "Welcome, " + userName + "!";

    // 3. Logout Functionality
    document.getElementById("logoutBtn").addEventListener("click", () => {
        localStorage.clear(); // Destroy the token
        window.location.href = "index.html"; // Send back to login
    });

    // 4. Fetch Students from MySQL via FastAPI
    async function loadStudents() {
        try {
            const response = await fetch(`${API_BASE_URL}/students/`);
            const data = await response.json();
            
            const list = document.getElementById("studentsList");
            list.innerHTML = ""; // Clear the "Loading..." text
            
            // Loop through the database records and create HTML list items
            data.students.forEach(student => {
                let li = document.createElement("li");
                li.innerHTML = `<strong>${student.name}</strong> (${student.roll_no}) - ${student.class}`;
                list.appendChild(li);
            });
        } catch (error) {
            document.getElementById("studentsList").innerText = "Error loading database records.";
        }
    }

    // 5. Fetch Subjects from MySQL via FastAPI
    async function loadSubjects() {
        try {
            const response = await fetch(`${API_BASE_URL}/subjects/`);
            const data = await response.json();
            
            const list = document.getElementById("subjectsList");
            list.innerHTML = ""; // Clear the "Loading..." text
            
            // Loop through subjects and create HTML list items
            data.subjects.forEach(subject => {
                let li = document.createElement("li");
                li.innerText = subject.name;
                list.appendChild(li);
            });
        } catch (error) {
            document.getElementById("subjectsList").innerText = "Error loading database records.";
        }
    }

    // Fire the engines when the page loads!
    loadStudents();
    loadSubjects();
}