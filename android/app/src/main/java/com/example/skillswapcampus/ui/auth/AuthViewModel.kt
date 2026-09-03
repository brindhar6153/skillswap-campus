package com.example.skillswapcampus.ui.auth

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.skillswapcampus.data.SessionManager
import com.example.skillswapcampus.models.*
import com.example.skillswapcampus.repository.DefaultSkillSwapRepository
import com.example.skillswapcampus.repository.SkillSwapRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed interface AuthState {
    object Idle : AuthState
    object Loading : AuthState
    data class Authenticated(val user: User) : AuthState
    object Unauthenticated : AuthState
    data class Error(val message: String) : AuthState
}

sealed interface OperationState {
    object Idle : OperationState
    object Loading : OperationState
    data class Success(val message: String) : OperationState
    data class Error(val message: String) : OperationState
}

class AuthViewModel(
    application: Application,
    val repository: SkillSwapRepository = DefaultSkillSwapRepository()
) : AndroidViewModel(application) {

    private val sessionManager = SessionManager(application)

    private val _authState = MutableStateFlow<AuthState>(AuthState.Idle)
    val authState: StateFlow<AuthState> = _authState.asStateFlow()

    private val _loginState = MutableStateFlow<OperationState>(OperationState.Idle)
    val loginState: StateFlow<OperationState> = _loginState.asStateFlow()

    private val _registerState = MutableStateFlow<OperationState>(OperationState.Idle)
    val registerState: StateFlow<OperationState> = _registerState.asStateFlow()

    private val _userSkills = MutableStateFlow<UserSkillsResponse?>(null)
    val userSkills: StateFlow<UserSkillsResponse?> = _userSkills.asStateFlow()

    private val _saveSkillsState = MutableStateFlow<OperationState>(OperationState.Idle)
    val saveSkillsState: StateFlow<OperationState> = _saveSkillsState.asStateFlow()

    init {
        checkSession()
    }

    fun fetchUserSkills() {
        viewModelScope.launch {
            try {
                val response = repository.getUserSkills()
                _userSkills.value = response
            } catch (e: Exception) {
                // Ignore silent errors
            }
        }
    }

    fun refreshProfile() {
        viewModelScope.launch {
            try {
                val user = repository.getCurrentUser()
                sessionManager.saveUser(user)
                _authState.value = AuthState.Authenticated(user)
                fetchUserSkills()
            } catch (e: Exception) {
                // Ignore silent errors
            }
        }
    }

    fun checkSession() {
        viewModelScope.launch {
            _authState.value = AuthState.Loading
            val cachedUser = sessionManager.getUser()
            if (cachedUser != null) {
                try {
                    val user = repository.getCurrentUser()
                    sessionManager.saveUser(user)
                    _authState.value = AuthState.Authenticated(user)
                    fetchUserSkills()
                } catch (e: Exception) {
                    // Fall back to cached session if network check fails
                    _authState.value = AuthState.Authenticated(cachedUser)
                    fetchUserSkills()
                }
            } else {
                _authState.value = AuthState.Unauthenticated
            }
        }
    }

    fun login(email: String, word: String) {
        viewModelScope.launch {
            _loginState.value = OperationState.Loading
            try {
                val res = repository.login(LoginRequest(email, word))
                if (res.success && res.user != null) {
                    sessionManager.saveUser(res.user)
                    _authState.value = AuthState.Authenticated(res.user)
                    fetchUserSkills()
                    _loginState.value = OperationState.Success(res.message ?: "Login successful")
                } else {
                    _loginState.value = OperationState.Error(res.message ?: "Authentication failed")
                }
            } catch (e: Exception) {
                _loginState.value = OperationState.Error(e.message ?: "Connection failure. Please check your backend.")
            }
        }
    }

    fun register(
        name: String,
        email: String,
        word: String,
        confirm: String,
        major: String,
        gradYear: Int?,
        bio: String
    ) {
        viewModelScope.launch {
            _registerState.value = OperationState.Loading
            
            // Client-side validations
            if (name.isBlank()) {
                _registerState.value = OperationState.Error("Full name is required.")
                return@launch
            }
            if (email.isBlank() || !email.endsWith(".edu")) {
                _registerState.value = OperationState.Error("Institutional email ending in .edu is required.")
                return@launch
            }
            if (word.length < 6) {
                _registerState.value = OperationState.Error("Password must be at least 6 characters.")
                return@launch
            }
            if (word != confirm) {
                _registerState.value = OperationState.Error("Passwords do not match.")
                return@launch
            }
            if (gradYear != null && gradYear < 2026) {
                _registerState.value = OperationState.Error("Graduation year must be 2026 or later.")
                return@launch
            }

            try {
                // Step 1: Register
                val regRes = repository.register(RegisterRequest(name, email.trim(), word, confirm))
                if (regRes.success) {
                    // Step 2: Login to obtain session cookie
                    val loginRes = repository.login(LoginRequest(email.trim(), word))
                    if (loginRes.success && loginRes.user != null) {
                        // Step 3: Onboard profile details
                        val profileReq = ProfileUpdateRequest(
                            college = "State College", // default college
                            major = major.trim().ifBlank { null },
                            bio = bio.trim().ifBlank { null },
                            gradYear = gradYear
                        )
                        repository.updateProfile(profileReq)
                        
                        // Save session & update state to trigger home redirection
                        sessionManager.saveUser(loginRes.user)
                        _authState.value = AuthState.Authenticated(loginRes.user)
                        _registerState.value = OperationState.Success("Registration and Onboarding completed successfully!")
                    } else {
                        _registerState.value = OperationState.Error(loginRes.message ?: "Login failed after registration.")
                    }
                } else {
                    _registerState.value = OperationState.Error(regRes.message ?: "Registration failed.")
                }
            } catch (e: Exception) {
                _registerState.value = OperationState.Error(e.message ?: "Connection failure. Please check your backend.")
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            try {
                repository.logout()
            } catch (e: Exception) {
                // Ignore API failures on logout, force clear local session anyway
            }
            sessionManager.clearSession()
            _authState.value = AuthState.Unauthenticated
            _loginState.value = OperationState.Idle
            _registerState.value = OperationState.Idle
        }
    }

    fun clearStates() {
        _loginState.value = OperationState.Idle
        _registerState.value = OperationState.Idle
        _saveSkillsState.value = OperationState.Idle
    }

    fun saveSkills(teach: List<UserSkill>, learn: List<UserSkill>) {
        viewModelScope.launch {
            _saveSkillsState.value = OperationState.Loading
            try {
                val req = SkillsUpdateRequest(teach, learn)
                val res = repository.updateSkills(req)
                _saveSkillsState.value = OperationState.Success(res.message ?: "Skills updated successfully")
                fetchUserSkills() // sync userSkills flow locally
            } catch (e: Exception) {
                _saveSkillsState.value = OperationState.Error(e.message ?: "Failed to save skills portfolio")
            }
        }
    }
}
