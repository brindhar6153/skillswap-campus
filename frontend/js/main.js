/* ==========================================
   SkillSwap Campus - Common JS Foundation & Auth Protection
   ========================================== */

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  checkAuthSession();
});

/**
 * Handle mobile navigation toggle drawer
 */
function initNavigation() {
  const toggleBtn = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener("click", () => {
      navLinks.classList.toggle("open");
      const spans = toggleBtn.querySelectorAll("span");
      if (navLinks.classList.contains("open")) {
        spans[0].style.transform = "rotate(45deg) translate(5px, 5px)";
        spans[1].style.opacity = "0";
        spans[2].style.transform = "rotate(-45deg) translate(6px, -6px)";
      } else {
        spans[0].style.transform = "none";
        spans[1].style.opacity = "1";
        spans[2].style.transform = "none";
      }
    });
  }
}

/**
 * Check authentication session with Flask backend (/auth/me)
 */
function checkAuthSession() {
  const isAuthPage = window.location.pathname.includes("login.html") || window.location.pathname.includes("register.html");
  const isLandingPage = window.location.pathname.endsWith("index.html") || window.location.pathname.endsWith("/");

  if (isAuthPage || isLandingPage) {
    const loggedInUser = localStorage.getItem("skillswap_user");
    if (loggedInUser) {
      updateNavLinks(JSON.parse(loggedInUser));
    }
    return;
  }

  // Protected pages validation check via API call
  Api.get("/auth/me")
    .then(data => {
      // Sync local storage with latest verified profile details
      localStorage.setItem("skillswap_user", JSON.stringify(data.user));
      updateNavLinks(data.user);
      
      // Dispatch custom event to notify page templates that user data is loaded and ready
      document.dispatchEvent(new CustomEvent("userDataLoaded", { detail: data.user }));
    })
    .catch(err => {
      console.warn("Session invalid, redirecting to login:", err.message);
      localStorage.removeItem("skillswap_user");
      
      const basePath = window.location.pathname.includes("/pages/") ? "login.html" : "pages/login.html";
      window.location.href = basePath;
    });
}

/**
 * Update Navbar links according to authentication status
 */
function updateNavLinks(user) {
  const navLinksUl = document.querySelector(".nav-links");
  if (!navLinksUl) return;

  const pathPrefix = window.location.pathname.includes("/pages/") ? "" : "pages/";

  navLinksUl.innerHTML = `
    <li><a href="${pathPrefix}dashboard.html" class="${isActive('dashboard.html')}">Dashboard</a></li>
    <li><a href="${pathPrefix}skills.html" class="${isActive('skills.html')}">Skills</a></li>
    <li><a href="${pathPrefix}requests.html" class="${isActive('requests.html')}">Requests</a></li>
    <li><a href="${pathPrefix}sessions.html" class="${isActive('sessions.html')}">Sessions</a></li>
    <li><a href="${pathPrefix}profile.html" class="${isActive('profile.html')}">Profile</a></li>
    <li><a href="#" id="global-logout" class="nav-btn">Logout</a></li>
  `;
  
  initLogout();
}

/**
 * Utility: Checks if target link represents current page
 */
function isActive(pageName) {
  return window.location.pathname.includes(pageName) ? "active" : "";
}

/**
 * Initialize Logout API call
 */
function initLogout() {
  const logoutBtn = document.getElementById("global-logout") || document.querySelector(".logout-link");
  if (logoutBtn) {
    if (logoutBtn.dataset.listenerBound) return;
    logoutBtn.dataset.listenerBound = "true";

    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      
      Api.post("/auth/logout", {})
        .then(() => {
          localStorage.removeItem("skillswap_user");
          const exitPath = window.location.pathname.includes("/pages/") ? "../index.html" : "index.html";
          window.location.href = exitPath;
        })
        .catch(err => {
          console.error("Logout error on server:", err);
          // Force local clearance and redirect anyway
          localStorage.removeItem("skillswap_user");
          const exitPath = window.location.pathname.includes("/pages/") ? "../index.html" : "index.html";
          window.location.href = exitPath;
        });
    });
  }
}
