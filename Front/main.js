// Get the token and role from localStorage
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");


// determine the role
let isLoggedIn = false;
let isAnalystLoggedIn = false;
let isOrganizationLoggedIn = false;
let isAdminLoggedIn = false;

if (token != null && role != null) {

    if (role == "Admin") {
        isAdminLoggedIn = true;
    } else if (role == "Organization") {
        isOrganizationLoggedIn = true;
    } else if (role == "Analyst") {
        isAnalystLoggedIn = true;
    } else {
        isAdminLoggedIn = false;
        isAnalystLoggedIn = false;
        isOrganizationLoggedIn = false;
    }
    isLoggedIn = isAdminLoggedIn || isAnalystLoggedIn || isOrganizationLoggedIn;
}

async function verifyToken(role) {
    const response = await fetch(`http://localhost:8000/Authorization/verify?role=${role}`, {
        method: "GET",
        headers: {
            "authorization": `Bearer ${token}`
        },
    });
    const result = await response.json();
    return result;
}

async function protectedPage(role) {
    if (isLoggedIn) {
        let decoded = await verifyToken(role);
        if (decoded.detail == "Invalid token" || decoded.detail == "Token has expired") {
            location.replace("/Front/pages/Login.html");
            localStorage.clear();
        }
    } else {
        location.replace("/Front/pages/Login.html");
        localStorage.clear();
    }
}

function visitorPage() {
    if(isLoggedIn) {
        if(isAdminLoggedIn) {
            location.replace("/Front/pages/Admin/index.html");
        } else if(isOrganizationLoggedIn) {
            location.replace("/Front/pages/Organization/index.html");
        } else if(isAnalystLoggedIn) {
            location.replace("/Front/pages/Analyst/index.html");
        }
    }
}

function logout() {
    location.replace("/Front/pages/Login.html");
    localStorage.clear();
}

function disable(cond, el) {
    if (cond) {
        $(el).remove();
    }
}

