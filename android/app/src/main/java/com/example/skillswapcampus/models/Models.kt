package com.example.skillswapcampus.models

import com.google.gson.annotations.SerializedName

data class User(
    val id: Int,
    val name: String,
    val email: String,
    val college: String?,
    @SerializedName("course") val major: String?,
    val credits: Double
)

data class Skill(
    val id: Int,
    val name: String,
    val category: String
)

data class UserSkill(
    @SerializedName("skill_id") val skillId: Int,
    val role: String, // "teach" or "learn"
    val proficiency: String // "beginner", "intermediate", "advanced"
)

data class AvailabilitySlot(
    @SerializedName("day_of_week") val dayOfWeek: Int, // 0 = Sunday, 6 = Saturday
    @SerializedName("start_time") val startTime: String, // "HH:MM"
    @SerializedName("end_time") val endTime: String // "HH:MM"
)

// Network API Payload Objects
data class RegisterRequest(
    val name: String,
    val email: String,
    val password: String,
    @SerializedName("confirm_password") val confirmPassword: String
)

data class LoginRequest(
    val email: String,
    val password: String
)

data class AuthResponse(
    val success: Boolean,
    val message: String?,
    val user: User?
)

data class ProfileResponse(
    val name: String,
    val email: String,
    val college: String?,
    val major: String?,
    val bio: String?,
    @SerializedName("grad_year") val gradYear: Int?,
    @SerializedName("credit_balance") val creditBalance: Double
)

data class ProfileUpdateRequest(
    val college: String?,
    val major: String?,
    val bio: String?,
    @SerializedName("grad_year") val gradYear: Int?
)

data class SkillsUpdateRequest(
    val teach: List<UserSkill>,
    val learn: List<UserSkill>
)

data class MessageResponse(
    val message: String
)

data class ErrorResponse(
    val error: String,
    val message: String
)

data class UserSkillInfo(
    @SerializedName("skill_id") val skillId: Int,
    val name: String,
    val category: String,
    val proficiency: String
)

data class UserSkillsResponse(
    val teach: List<UserSkillInfo>,
    val learn: List<UserSkillInfo>
)

data class MatchUser(
    val id: Int,
    val name: String,
    val email: String,
    val major: String?,
    val bio: String?,
    val college: String?
)

data class MatchSkillInfo(
    val id: Int,
    val name: String,
    val category: String,
    val proficiency: String
)

data class MatchResponse(
    val user: MatchUser,
    @SerializedName("teach_skills") val teachSkills: List<MatchSkillInfo>,
    @SerializedName("learn_skills") val learnSkills: List<MatchSkillInfo>,
    val reciprocal: Boolean,
    @SerializedName("match_score") val matchScore: Int
)

data class SendSwapRequest(
    @SerializedName("receiver_id") val receiverId: Int,
    @SerializedName("teach_skill_id") val teachSkillId: Int?,
    @SerializedName("learn_skill_id") val learnSkillId: Int?,
    val message: String
)

data class SwapRequestUser(
    val id: Int,
    val name: String,
    val major: String?
)

data class SwapRequestSkill(
    val id: Int,
    val name: String
)

data class SwapRequestItem(
    val id: Int,
    val sender: SwapRequestUser,
    val receiver: SwapRequestUser,
    @SerializedName("teach_skill") val teachSkill: SwapRequestSkill?,
    @SerializedName("learn_skill") val learnSkill: SwapRequestSkill?,
    val status: String,
    val message: String?,
    @SerializedName("created_at") val createdAt: String
)

data class SwapRequestsResponse(
    val incoming: List<SwapRequestItem>,
    val outgoing: List<SwapRequestItem>
)

data class RespondSwapRequest(
    val action: String
)

data class ScheduleSessionRequest(
    @SerializedName("request_id") val requestId: Int,
    @SerializedName("teacher_id") val teacherId: Int,
    @SerializedName("learner_id") val learnerId: Int,
    @SerializedName("skill_id") val skillId: Int,
    @SerializedName("scheduled_at") val scheduledAt: String,
    @SerializedName("duration_hours") val durationHours: Double,
    val venue: String
)

data class SessionItem(
    val id: Int,
    @SerializedName("partner_name") val partnerName: String,
    @SerializedName("skill_name") val skillName: String,
    @SerializedName("scheduled_at") val scheduledAt: String,
    @SerializedName("duration_hours") val durationHours: Double,
    val venue: String,
    val status: String,
    val role: String
)

data class SessionDetailResponse(
    val id: Int,
    @SerializedName("teacher_name") val teacherName: String,
    @SerializedName("learner_name") val learnerName: String,
    @SerializedName("skill_name") val skillName: String,
    @SerializedName("scheduled_at") val scheduledAt: String,
    @SerializedName("duration_hours") val durationHours: Double,
    val venue: String,
    val status: String,
    @SerializedName("completed_at") val completedAt: String?,
    @SerializedName("cancelled_by") val cancelledBy: Int?,
    @SerializedName("cancelled_reason") val cancelledReason: String?
)

data class RespondSessionRequest(
    val action: String,
    val reason: String?
)
