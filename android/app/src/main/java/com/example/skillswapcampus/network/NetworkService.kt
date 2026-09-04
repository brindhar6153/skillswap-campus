package com.example.skillswapcampus.network

import com.example.skillswapcampus.models.*
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.Response
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path

/**
 * Global App Configuration for Base URL and properties
 */
object AppConfig {
    // Production public HTTPS API base URL
    var baseUrl: String = "https://skillswap-campus-890k.onrender.com/"
}

/**
 * Lightweight interceptor to persist and transmit Flask session cookies
 */
class SessionCookieInterceptor : Interceptor {
    @Volatile
    private var sessionCookies: List<String> = emptyList()

    fun clearSession() {
        sessionCookies = emptyList()
    }

    override fun intercept(chain: Interceptor.Chain): Response {
        val requestBuilder = chain.request().newBuilder()
        
        // Append stored cookies to headers
        for (cookie in sessionCookies) {
            requestBuilder.addHeader("Cookie", cookie)
        }
        
        val response = chain.proceed(requestBuilder.build())
        
        // Intercept and store any cookies set by response headers
        val setCookieHeaders = response.headers("Set-Cookie")
        if (setCookieHeaders.isNotEmpty()) {
            sessionCookies = setCookieHeaders
        }
        
        return response
    }
}

/**
 * Retrofit Interface defining Flask Backend endpoints
 */
interface SkillSwapApi {
    @POST("/api/auth/register")
    suspend fun register(@Body request: RegisterRequest): AuthResponse

    @POST("/api/auth/login")
    suspend fun login(@Body request: LoginRequest): AuthResponse

    @POST("/api/auth/logout")
    suspend fun logout(): AuthResponse

    @GET("/api/auth/me")
    suspend fun getCurrentUser(): User

    @GET("/api/onboarding/profile")
    suspend fun getProfile(): ProfileResponse

    @POST("/api/onboarding/profile")
    suspend fun updateProfile(@Body request: ProfileUpdateRequest): ProfileResponse

    @GET("/api/skills")
    suspend fun getSkills(): List<Skill>

    @POST("/api/onboarding/skills")
    suspend fun updateSkills(@Body request: SkillsUpdateRequest): MessageResponse

    @GET("/api/onboarding/skills")
    suspend fun getUserSkills(): UserSkillsResponse

    @GET("/api/onboarding/availability")
    suspend fun getAvailability(): List<AvailabilitySlot>

    @POST("/api/onboarding/availability")
    suspend fun updateAvailability(@Body request: List<AvailabilitySlot>): MessageResponse

    @GET("/api/matches")
    suspend fun getMatches(): List<MatchResponse>

    @POST("/api/swap-requests")
    suspend fun sendSwapRequest(@Body request: SendSwapRequest): MessageResponse

    @GET("/api/swap-requests")
    suspend fun getSwapRequests(): SwapRequestsResponse

    @POST("/api/swap-requests/{id}/respond")
    suspend fun respondSwapRequest(@Path("id") requestId: Int, @Body request: RespondSwapRequest): MessageResponse

    @POST("/api/sessions")
    suspend fun createSession(@Body request: ScheduleSessionRequest): MessageResponse

    @GET("/api/sessions")
    suspend fun getSessions(): List<SessionItem>

    @GET("/api/sessions/{id}")
    suspend fun getSessionDetails(@Path("id") sessionId: Int): SessionDetailResponse

    @POST("/api/sessions/{id}/respond")
    suspend fun respondSession(@Path("id") sessionId: Int, @Body request: RespondSessionRequest): MessageResponse
}

/**
 * Network builder configuring OkHttpClient and Retrofit
 */
object NetworkService {
    val cookieInterceptor = SessionCookieInterceptor()

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(cookieInterceptor)
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        })
        .build()

    val api: SkillSwapApi by lazy {
        Retrofit.Builder()
            .baseUrl(AppConfig.baseUrl)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(SkillSwapApi::class.java)
    }
}
