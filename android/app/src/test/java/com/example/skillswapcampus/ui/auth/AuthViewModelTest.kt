package com.example.skillswapcampus.ui.auth

import android.app.Application
import org.junit.Assert.assertNotNull
import org.junit.Test

class AuthViewModelTest {

    @Test
    fun testReflectionConstructor() {
        val constructor = AuthViewModel::class.java.getConstructor(Application::class.java)
        assertNotNull(constructor)
    }
}
