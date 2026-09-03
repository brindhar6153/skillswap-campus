package com.example.skillswapcampus.repository

import com.example.skillswapcampus.models.*
import com.example.skillswapcampus.network.NetworkService
import com.example.skillswapcampus.network.SkillSwapApi

interface SkillSwapRepository {
    suspend fun register(request: RegisterRequest): AuthResponse
    suspend fun login(request: LoginRequest): AuthResponse
    suspend fun logout(): AuthResponse
    suspend fun getCurrentUser(): User
    suspend fun getProfile(): ProfileResponse
    suspend fun updateProfile(request: ProfileUpdateRequest): ProfileResponse
    suspend fun getSkills(): List<Skill>
    suspend fun updateSkills(request: SkillsUpdateRequest): MessageResponse
    suspend fun getUserSkills(): UserSkillsResponse
    suspend fun getAvailability(): List<AvailabilitySlot>
    suspend fun updateAvailability(request: List<AvailabilitySlot>): MessageResponse
    suspend fun getMatches(): List<MatchResponse>
    suspend fun sendSwapRequest(request: SendSwapRequest): MessageResponse
    suspend fun getSwapRequests(): SwapRequestsResponse
    suspend fun respondSwapRequest(requestId: Int, action: String): MessageResponse
    suspend fun createSession(request: ScheduleSessionRequest): MessageResponse
    suspend fun getSessions(): List<SessionItem>
    suspend fun getSessionDetails(sessionId: Int): SessionDetailResponse
    suspend fun respondSession(sessionId: Int, action: String, reason: String?): MessageResponse
}

class DefaultSkillSwapRepository(
    private val api: SkillSwapApi = NetworkService.api
) : SkillSwapRepository {
    
    override suspend fun register(request: RegisterRequest): AuthResponse {
        return api.register(request)
    }

    override suspend fun login(request: LoginRequest): AuthResponse {
        return api.login(request)
    }

    override suspend fun logout(): AuthResponse {
        val res = api.logout()
        NetworkService.cookieInterceptor.clearSession()
        return res
    }

    override suspend fun getCurrentUser(): User {
        return api.getCurrentUser()
    }

    override suspend fun getProfile(): ProfileResponse {
        return api.getProfile()
    }

    override suspend fun updateProfile(request: ProfileUpdateRequest): ProfileResponse {
        return api.updateProfile(request)
    }

    override suspend fun getSkills(): List<Skill> {
        return api.getSkills()
    }

    override suspend fun updateSkills(request: SkillsUpdateRequest): MessageResponse {
        return api.updateSkills(request)
    }

    override suspend fun getUserSkills(): UserSkillsResponse {
        return api.getUserSkills()
    }

    override suspend fun getAvailability(): List<AvailabilitySlot> {
        return api.getAvailability()
    }

    override suspend fun updateAvailability(request: List<AvailabilitySlot>): MessageResponse {
        return api.updateAvailability(request)
    }

    override suspend fun getMatches(): List<MatchResponse> {
        return api.getMatches()
    }

    override suspend fun sendSwapRequest(request: SendSwapRequest): MessageResponse {
        return api.sendSwapRequest(request)
    }

    override suspend fun getSwapRequests(): SwapRequestsResponse {
        return api.getSwapRequests()
    }

    override suspend fun respondSwapRequest(requestId: Int, action: String): MessageResponse {
        return api.respondSwapRequest(requestId, RespondSwapRequest(action))
    }

    override suspend fun createSession(request: ScheduleSessionRequest): MessageResponse {
        return api.createSession(request)
    }

    override suspend fun getSessions(): List<SessionItem> {
        return api.getSessions()
    }

    override suspend fun getSessionDetails(sessionId: Int): SessionDetailResponse {
        return api.getSessionDetails(sessionId)
    }

    override suspend fun respondSession(sessionId: Int, action: String, reason: String?): MessageResponse {
        return api.respondSession(sessionId, RespondSessionRequest(action, reason))
    }
}
