/* ==========================================
   SkillSwap Campus - REST API Fetch Wrapper Helper
   ========================================== */

const API_BASE_URL = "http://127.0.0.1:5000/api";

const Api = {
  /**
   * Send HTTP requests using fetch
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Setup standard headers
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    // Integrate authentication credentials if stored
    const loggedInUser = localStorage.getItem("skillswap_user");
    if (loggedInUser) {
      const user = JSON.parse(loggedInUser);
      // We can attach a mock authorization header for later phase API calls
      headers["Authorization"] = `Bearer mock-token-for-${user.email}`;
    }

    const config = {
      ...options,
      headers,
      credentials: "include",
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || `Request failed with status ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`API Error on ${url}:`, error.message);
      throw error;
    }
  },

  /**
   * HTTP GET Request Wrapper
   */
  async get(endpoint) {
    return this.request(endpoint, { method: "GET" });
  },

  /**
   * HTTP POST Request Wrapper
   */
  async post(endpoint, body) {
    return this.request(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  /**
   * HTTP PUT Request Wrapper
   */
  async put(endpoint, body) {
    return this.request(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
    });
  },

  /**
   * HTTP DELETE Request Wrapper
   */
  async delete(endpoint) {
    return this.request(endpoint, { method: "DELETE" });
  },
};
