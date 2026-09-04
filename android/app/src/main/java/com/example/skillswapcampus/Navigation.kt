package com.example.skillswapcampus

import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.runtime.rememberNavBackStack
import androidx.navigation3.ui.NavDisplay
import com.example.skillswapcampus.ui.*
import com.example.skillswapcampus.ui.auth.AuthViewModel
import com.example.skillswapcampus.ui.auth.AuthState

@Composable
fun MainNavigation() {
    // Initial route starts at Splash
    val backStack = rememberNavBackStack(Splash)
    
    // Shared ViewModel initialized at the navigation root
    val authViewModel: AuthViewModel = viewModel()
    val authState by authViewModel.authState.collectAsStateWithLifecycle()

    val handleBack: () -> Unit = {
        if (backStack.size > 1) {
            backStack.removeLastOrNull()
        }
    }

    // Automatically manage backstack based on AuthState
    LaunchedEffect(authState) {
        when (authState) {
            is AuthState.Authenticated -> {
                if (backStack.lastOrNull() != Home) {
                    backStack.add(Home)
                    while (backStack.size > 1) {
                        backStack.removeAt(0)
                    }
                }
            }
            is AuthState.Unauthenticated -> {
                // Redirect to Login if currently on a dashboard page
                val lastKey = backStack.lastOrNull()
                if (lastKey != Splash && lastKey != Login && lastKey != Register) {
                    backStack.add(Login)
                    while (backStack.size > 1) {
                        backStack.removeAt(0)
                    }
                }
            }
            else -> {}
        }
    }

    NavDisplay(
        backStack = backStack,
        onBack = handleBack,
        entryProvider = entryProvider {
            entry<Splash> {
                SplashScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) }
                )
            }
            entry<Login> {
                LoginScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) },
                    onBack = handleBack
                )
            }
            entry<Register> {
                RegisterScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) },
                    onBack = handleBack
                )
            }
            entry<Home> {
                HomeScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) },
                    onBack = handleBack
                )
            }
            entry<Profile> {
                ProfileScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) },
                    onBack = handleBack
                )
            }
            entry<Skills> {
                SkillsScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) },
                    onBack = handleBack
                )
            }
            entry<Matches> {
                MatchesScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) },
                    onBack = handleBack
                )
            }
            entry<SwapRequests> {
                SwapRequestsScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) },
                    onBack = handleBack
                )
            }
            entry<Sessions> {
                SessionsScreen(
                    authViewModel = authViewModel,
                    onNavigate = { key -> backStack.add(key) },
                    onBack = handleBack
                )
            }
            entry<TimeCredits> {
                PlaceholderPage(
                    title = "Time Bank Transactions",
                    description = "Audit ledger transfers, starting credit grants, pending locks, and completed tutor credit balances.",
                    icon = Icons.Default.Info,
                    onBack = handleBack,
                    onNavigate = { key -> backStack.add(key) }
                )
            }
            entry<Reviews> {
                PlaceholderPage(
                    title = "Double-Blind Reviews",
                    description = "Post feedback for tutoring sessions. Reviews remain completely hidden until both partners submit feedback, protecting ratings objectivity.",
                    icon = Icons.Default.Star,
                    onBack = handleBack,
                    onNavigate = { key -> backStack.add(key) }
                )
            }
            entry<Notifications> {
                PlaceholderPage(
                    title = "Alerts & Notifications",
                    description = "Stay updated on newly matched profiles, booking confirmations, session completions, and ledger balance alerts.",
                    icon = Icons.Default.Notifications,
                    onBack = handleBack,
                    onNavigate = { key -> backStack.add(key) }
                )
            }
        }
    )
}
