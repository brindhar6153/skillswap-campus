package com.example.skillswapcampus.data

import android.content.Context
import android.content.SharedPreferences
import com.example.skillswapcampus.models.User
import com.google.gson.Gson

class SessionManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("skillswap_prefs", Context.MODE_PRIVATE)
    private val gson = Gson()

    fun saveUser(user: User) {
        val json = gson.toJson(user)
        prefs.edit().putString("auth_user", json).apply()
    }

    fun getUser(): User? {
        val json = prefs.getString("auth_user", null) ?: return null
        return try {
            gson.fromJson(json, User::class.java)
        } catch (e: Exception) {
            null
        }
    }

    fun clearSession() {
        prefs.edit().remove("auth_user").apply()
    }

    fun isLoggedIn(): Boolean {
        return prefs.contains("auth_user")
    }
}
