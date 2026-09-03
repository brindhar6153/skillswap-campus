/* ==========================================
   SkillSwap Campus - Authentication Validations & API Integration
   ========================================== */

document.addEventListener("DOMContentLoaded", () => {
  initLoginForm();
  initRegisterForm();
});

/**
 * Handle Login Form API Submission and Client-Side Validations
 */
function initLoginForm() {
  const loginForm = document.getElementById("login-form");
  if (!loginForm) return;

  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    let isValid = true;

    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const errorAlert = document.getElementById("login-error-alert");

    // Hide any previous global login error
    if (errorAlert) {
      errorAlert.style.display = "none";
      errorAlert.textContent = "";
    }

    // Email Check
    if (!validateEmail(email.value)) {
      showError(email, "Please enter a valid email address.");
      isValid = false;
    } else {
      clearError(email);
    }

    // Password Check
    if (password.value.trim().length < 6) {
      showError(password, "Password must be at least 6 characters.");
      isValid = false;
    } else {
      clearError(password);
    }

    if (isValid) {
      const submitBtn = loginForm.querySelector("button[type='submit']");
      const originalBtnText = submitBtn.textContent;
      
      // Prevent duplicate submissions and show loading state
      submitBtn.disabled = true;
      submitBtn.textContent = "Logging in...";

      Api.post("/auth/login", {
        email: email.value.trim(),
        password: password.value
      })
      .then(data => {
        // Save safe profile information returned by backend
        localStorage.setItem("skillswap_user", JSON.stringify(data.user));
        // Redirect to protected dashboard
        window.location.href = "dashboard.html";
      })
      .catch(err => {
        console.error("Login failed:", err);
        if (errorAlert) {
          errorAlert.textContent = err.message || "Invalid email or password. Please try again.";
          errorAlert.style.display = "block";
        }
        // Restore button state
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
      });
    }
  });
}

/**
 * Handle Registration Form API Submission and Client-Side Validations
 */
function initRegisterForm() {
  const registerForm = document.getElementById("register-form");
  if (!registerForm) return;

  registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    let isValid = true;

    const fullName = document.getElementById("full-name");
    const email = document.getElementById("email");
    const college = document.getElementById("college");
    const course = document.getElementById("course");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm-password");
    const domainErrorAlert = document.getElementById("domain-error-alert");

    // Hide any previous domain error alerts
    if (domainErrorAlert) {
      domainErrorAlert.style.display = "none";
      domainErrorAlert.textContent = "";
    }

    // Name Check
    if (fullName.value.trim().length < 2) {
      showError(fullName, "Full name must be at least 2 characters.");
      isValid = false;
    } else {
      clearError(fullName);
    }

    // Email Check
    const emailVal = email.value.trim();
    if (!validateEmail(emailVal)) {
      showError(email, "Please enter a valid email address.");
      isValid = false;
    } else if (!emailVal.endsWith(".edu")) {
      showError(email, "Email must be a valid institutional domain (.edu).");
      isValid = false;
    } else {
      clearError(email);
    }

    // College Check
    if (college.value.trim().length < 2) {
      showError(college, "Please enter your college/university name.");
      isValid = false;
    } else {
      clearError(college);
    }

    // Course Check (Major)
    if (course.value.trim().length < 2) {
      showError(course, "Please specify your course major.");
      isValid = false;
    } else {
      clearError(course);
    }

    // Password checks
    if (password.value.length < 6) {
      showError(password, "Password must be at least 6 characters.");
      isValid = false;
    } else {
      clearError(password);
    }

    // Match Password Checks
    if (confirmPassword.value !== password.value) {
      showError(confirmPassword, "Passwords do not match.");
      isValid = false;
    } else {
      clearError(confirmPassword);
    }

    if (isValid) {
      const submitBtn = registerForm.querySelector("button[type='submit']");
      const originalBtnText = submitBtn.textContent;

      // Prevent duplicate submissions and show loading state
      submitBtn.disabled = true;
      submitBtn.textContent = "Creating Account...";

      Api.post("/auth/register", {
        name: fullName.value.trim(),
        email: emailVal,
        password: password.value,
        confirm_password: confirmPassword.value,
        college: college.value.trim(),
        course: course.value.trim()
      })
      .then(data => {
        alert(data.message || "Registration successful! Redirecting you to login.");
        window.location.href = "login.html";
      })
      .catch(err => {
        console.error("Registration failed:", err);
        if (domainErrorAlert) {
          domainErrorAlert.textContent = err.message || "Registration failed. Please check inputs.";
          domainErrorAlert.style.display = "block";
        }
        // Restore button state
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
      });
    }
  });
}

/**
 * Email regex evaluator helper
 */
function validateEmail(email) {
  const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return re.test(String(email).toLowerCase());
}

/**
 * Display Validation error fields helper
 */
function showError(inputElement, errorMessage) {
  const formGroup = inputElement.closest(".form-group");
  if (!formGroup) return;

  inputElement.classList.add("is-invalid");
  let errorDisplay = formGroup.querySelector(".form-error");
  if (!errorDisplay) {
    errorDisplay = document.createElement("div");
    errorDisplay.className = "form-error";
    formGroup.appendChild(errorDisplay);
  }
  errorDisplay.textContent = errorMessage;
  errorDisplay.style.display = "block";
}

/**
 * Clear Validation error fields helper
 */
function clearError(inputElement) {
  const formGroup = inputElement.closest(".form-group");
  if (!formGroup) return;

  inputElement.classList.remove("is-invalid");
  const errorDisplay = formGroup.querySelector(".form-error");
  if (errorDisplay) {
    errorDisplay.style.display = "none";
  }
}
