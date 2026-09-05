package com.example.skillswapcampus.ui.auth

import android.app.Application
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test

class AuthViewModelTest {

    @Test
    fun testReflectionConstructor() {
        val constructor = AuthViewModel::class.java.getConstructor(Application::class.java)
        assertNotNull(constructor)
    }

    @Test
    fun testEmailRegex_collegeAndPersonalEmails() {
        val emailPattern = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$".toRegex()
        val validEmails = listOf(
            "student@university.edu",
            "researcher@college.edu.in",
            "john.doe@gmail.com",
            "jane_doe@outlook.com",
            "user.name123@yahoo.com",
            "contact@company.org"
        )
        for (email in validEmails) {
            assertTrue("Expected valid: $email", email.matches(emailPattern))
        }
    }

    @Test
    fun testEmailRegex_invalidEmails() {
        val emailPattern = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$".toRegex()
        val invalidEmails = listOf(
            "",
            "plainaddress",
            "missing@domain",
            "@missingusername.com",
            "username@.com",
            "user space@domain.com"
        )
        for (email in invalidEmails) {
            assertFalse("Expected invalid: $email", email.matches(emailPattern))
        }
    }
}
