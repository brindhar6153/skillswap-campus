package com.example.skillswapcampus.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation3.runtime.NavKey
import com.example.skillswapcampus.*
import com.example.skillswapcampus.models.*
import com.example.skillswapcampus.ui.auth.*
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

/**
 * Standard Scaffolding structure for internal dashboard application pages
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppScreenScaffold(
    title: String,
    onBack: (() -> Unit)?,
    onNavigate: (NavKey) -> Unit,
    modifier: Modifier = Modifier,
    content: @Composable (PaddingValues) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(title, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    if (onBack != null) {
                        IconButton(onClick = onBack) {
                            Icon(imageVector = Icons.Default.ArrowBack, contentDescription = "Back")
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        },
        bottomBar = {
            if (onBack != null && title != "Splash" && title != "Log In" && title != "Register") {
                NavigationBar {
                    NavigationBarItem(
                        selected = title == "Dashboard Home",
                        onClick = { onNavigate(Home) },
                        icon = { Icon(Icons.Default.Home, "Home") },
                        label = { Text("Home") }
                    )
                    NavigationBarItem(
                        selected = title == "My Skills Mapping",
                        onClick = { onNavigate(Skills) },
                        icon = { Icon(Icons.Default.List, "Skills") },
                        label = { Text("Skills") }
                    )
                    NavigationBarItem(
                        selected = title == "Teachable Matches",
                        onClick = { onNavigate(Matches) },
                        icon = { Icon(Icons.Default.Search, "Matches") },
                        label = { Text("Matches") }
                    )
                    NavigationBarItem(
                        selected = title == "Swap Requests",
                        onClick = { onNavigate(SwapRequests) },
                        icon = { Icon(Icons.Default.Send, "Requests") },
                        label = { Text("Requests") }
                    )
                    NavigationBarItem(
                        selected = title == "Student Profile",
                        onClick = { onNavigate(Profile) },
                        icon = { Icon(Icons.Default.Person, "Profile") },
                        label = { Text("Profile") }
                    )
                }
            }
        },
        modifier = modifier,
        content = content
    )
}

@Composable
fun SplashScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit
) {
    val authState by authViewModel.authState.collectAsStateWithLifecycle()

    // Automatic route check
    LaunchedEffect(authState) {
        if (authState is AuthState.Authenticated) {
            onNavigate(Home)
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.primary),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.padding(24.dp)
        ) {
            Text(
                text = "SkillSwap Campus",
                fontSize = 32.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color.White,
                modifier = Modifier.padding(bottom = 8.dp)
            )
            Text(
                text = "Zero-Cost Knowledge Sharing Network",
                fontSize = 16.sp,
                color = Color.White.copy(alpha = 0.8f),
                modifier = Modifier.padding(bottom = 48.dp)
            )
            
            if (authState is AuthState.Loading) {
                CircularProgressIndicator(color = Color.White)
            } else {
                Button(
                    onClick = { onNavigate(Login) },
                    colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = MaterialTheme.colorScheme.primary),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Get Started", fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
fun LoginScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit,
    onBack: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val loginState by authViewModel.loginState.collectAsStateWithLifecycle()
    val authState by authViewModel.authState.collectAsStateWithLifecycle()

    var passwordVisible by remember { mutableStateOf(false) }

    LaunchedEffect(authState) {
        if (authState is AuthState.Authenticated) {
            authViewModel.clearStates()
            onNavigate(Home)
        }
    }

    AppScreenScaffold(title = "Log In", onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Welcome Back", fontSize = 24.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 24.dp))
            
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email Address") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                singleLine = true
            )
            
            val icon = if (passwordVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
                visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    IconButton(onClick = { passwordVisible = !passwordVisible }) {
                        Icon(imageVector = icon, contentDescription = "Toggle password visibility")
                    }
                },
                singleLine = true
            )

            if (loginState is OperationState.Error) {
                Card(
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                    modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
                ) {
                    Text(
                        text = (loginState as OperationState.Error).message,
                        color = MaterialTheme.colorScheme.onErrorContainer,
                        modifier = Modifier.padding(12.dp),
                        textAlign = TextAlign.Center
                    )
                }
            }
            
            if (loginState is OperationState.Loading) {
                CircularProgressIndicator()
            } else {
                Button(
                    onClick = { authViewModel.login(email, password) },
                    modifier = Modifier.fillMaxWidth().height(48.dp),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Log In", fontWeight = FontWeight.Bold)
                }
            }
            
            TextButton(
                onClick = { 
                    authViewModel.clearStates()
                    onNavigate(Register) 
                },
                modifier = Modifier.padding(top = 12.dp)
            ) {
                Text("Don't have an account? Register here")
            }
        }
    }
}

@Composable
fun RegisterScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit,
    onBack: () -> Unit
) {
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var major by remember { mutableStateOf("") }
    var gradYearString by remember { mutableStateOf("") }
    var bio by remember { mutableStateOf("") }

    var passwordVisible by remember { mutableStateOf(false) }
    var confirmPasswordVisible by remember { mutableStateOf(false) }

    val registerState by authViewModel.registerState.collectAsStateWithLifecycle()

    AppScreenScaffold(title = "Register", onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(24.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Create Account & Profile", fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 24.dp))
            
            OutlinedTextField(
                value = name,
                onValueChange = { name = it },
                label = { Text("Full Name") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                singleLine = true
            )
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email Address") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                singleLine = true
            )

            val pIcon = if (passwordVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    IconButton(onClick = { passwordVisible = !passwordVisible }) {
                        Icon(imageVector = pIcon, contentDescription = "Toggle password visibility")
                    }
                },
                singleLine = true
            )

            val cpIcon = if (confirmPasswordVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff
            OutlinedTextField(
                value = confirmPassword,
                onValueChange = { confirmPassword = it },
                label = { Text("Confirm Password") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                visualTransformation = if (confirmPasswordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    IconButton(onClick = { confirmPasswordVisible = !confirmPasswordVisible }) {
                        Icon(imageVector = cpIcon, contentDescription = "Toggle password visibility")
                    }
                },
                singleLine = true
            )

            OutlinedTextField(
                value = major,
                onValueChange = { major = it },
                label = { Text("Major / Course of Study") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                singleLine = true
            )

            OutlinedTextField(
                value = gradYearString,
                onValueChange = { gradYearString = it },
                label = { Text("Graduation Year") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                singleLine = true
            )

            OutlinedTextField(
                value = bio,
                onValueChange = { bio = it },
                label = { Text("Bio / Description") },
                modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
                minLines = 3
            )

            when (registerState) {
                is OperationState.Success -> {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color(0xFFD4EDDA)),
                        modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
                    ) {
                        Text(
                            text = (registerState as OperationState.Success).message,
                            color = Color(0xFF155724),
                            modifier = Modifier.padding(12.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                }
                is OperationState.Error -> {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                        modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
                    ) {
                        Text(
                            text = (registerState as OperationState.Error).message,
                            color = MaterialTheme.colorScheme.onErrorContainer,
                            modifier = Modifier.padding(12.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                }
                else -> {}
            }
            
            if (registerState is OperationState.Loading) {
                CircularProgressIndicator()
            } else if (registerState !is OperationState.Success) {
                Button(
                    onClick = { 
                        authViewModel.register(
                            name = name, 
                            email = email, 
                            word = password, 
                            confirm = confirmPassword,
                            major = major,
                            gradYear = gradYearString.toIntOrNull(),
                            bio = bio
                        ) 
                    },
                    modifier = Modifier.fillMaxWidth().height(48.dp),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Register & Onboard", fontWeight = FontWeight.Bold)
                }
            }
            
            TextButton(
                onClick = { 
                    authViewModel.clearStates()
                    onNavigate(Login) 
                },
                modifier = Modifier.padding(top = 12.dp)
            ) {
                Text("Already have an account? Login here")
            }
        }
    }
}

@Composable
fun HomeScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit,
    onBack: () -> Unit
) {
    val authState by authViewModel.authState.collectAsStateWithLifecycle()
    val userSkills by authViewModel.userSkills.collectAsStateWithLifecycle()
    val user = (authState as? AuthState.Authenticated)?.user

    // Fetch latest user details and skills on screen launch
    LaunchedEffect(Unit) {
        authViewModel.refreshProfile()
    }

    AppScreenScaffold(title = "Dashboard Home", onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Text(
                    text = "Welcome back, ${user?.name ?: "Student"}!",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Time Bank Balance", fontSize = 14.sp, color = MaterialTheme.colorScheme.onPrimaryContainer)
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.padding(top = 4.dp)
                        ) {
                            Icon(Icons.Default.Star, "Credits", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(28.dp))
                            val balance = user?.credits ?: 2.00
                            Text(" ${String.format("%.2f", balance)} Credits", fontSize = 28.sp, fontWeight = FontWeight.Black)
                        }
                        Text(
                            text = "College: ${user?.college ?: "State College"}",
                            fontSize = 13.sp,
                            modifier = Modifier.padding(top = 8.dp),
                            color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
                        )
                        Text(
                            text = "Major: ${user?.major ?: "Not specified"}",
                            fontSize = 13.sp,
                            color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
                        )
                    }
                }
            }

            item {
                Text("Skills Portfolio Summary", fontWeight = FontWeight.Bold, fontSize = 18.sp)
            }

            item {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Skills I Teach", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                        val teachList = userSkills?.teach ?: emptyList()
                        if (teachList.isEmpty()) {
                            Text(
                                "No teaching skills configured yet.",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.secondary,
                                modifier = Modifier.padding(top = 4.dp)
                            )
                        } else {
                            teachList.forEach { skill ->
                                Text(
                                    "• ${skill.name} (${skill.proficiency.replaceFirstChar { it.uppercase() }})",
                                    modifier = Modifier.padding(top = 4.dp)
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(12.dp))

                        Text("Skills I Want to Learn", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                        val learnList = userSkills?.learn ?: emptyList()
                        if (learnList.isEmpty()) {
                            Text(
                                "No learning skills configured yet.",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.secondary,
                                modifier = Modifier.padding(top = 4.dp)
                            )
                        } else {
                            learnList.forEach { skill ->
                                Text(
                                    "• ${skill.name} (${skill.proficiency.replaceFirstChar { it.uppercase() }})",
                                    modifier = Modifier.padding(top = 4.dp)
                                )
                            }
                        }
                    }
                }
            }

            item {
                Text("Quick Navigation Actions", fontWeight = FontWeight.Bold, fontSize = 18.sp)
            }

            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Button(
                        onClick = { onNavigate(Matches) },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(Icons.Default.Search, "Matches")
                            Text("Matches", fontSize = 11.sp, maxLines = 1)
                        }
                    }
                    Button(
                        onClick = { onNavigate(SwapRequests) },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(Icons.Default.Send, "Requests")
                            Text("Requests", fontSize = 11.sp, maxLines = 1)
                        }
                    }
                    Button(
                        onClick = { onNavigate(Sessions) },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(Icons.Default.DateRange, "Sessions")
                            Text("Sessions", fontSize = 11.sp, maxLines = 1)
                        }
                    }
                }
            }

            item {
                Spacer(modifier = Modifier.height(12.dp))
            }
        }
    }
}

@Composable
fun ProfileScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit,
    onBack: () -> Unit
) {
    var profileData by remember { mutableStateOf<ProfileResponse?>(null) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        try {
            isLoading = true
            profileData = authViewModel.repository.getProfile()
            errorMessage = null
        } catch (e: Exception) {
            errorMessage = e.message ?: "Failed to fetch profile details"
        } finally {
            isLoading = false
        }
    }

    AppScreenScaffold(title = "Student Profile", onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(24.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(modifier = Modifier.padding(top = 48.dp))
                }
            } else if (errorMessage != null) {
                Card(
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                    modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
                ) {
                    Text(
                        text = errorMessage!!,
                        color = MaterialTheme.colorScheme.onErrorContainer,
                        modifier = Modifier.padding(12.dp),
                        textAlign = TextAlign.Center
                    )
                }
            } else if (profileData != null) {
                val data = profileData!!
                val coroutineScope = rememberCoroutineScope()

                var showEditDialog by remember { mutableStateOf(false) }
                var editCollege by remember { mutableStateOf("") }
                var editMajor by remember { mutableStateOf("") }
                var editBio by remember { mutableStateOf("") }
                var editGradYear by remember { mutableStateOf("") }
                var isSavingProfile by remember { mutableStateOf(false) }
                var editError by remember { mutableStateOf<String?>(null) }

                Box(
                    modifier = Modifier
                        .size(100.dp)
                        .background(MaterialTheme.colorScheme.secondaryContainer, RoundedCornerShape(50.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.Person, "Avatar", modifier = Modifier.size(50.dp), tint = MaterialTheme.colorScheme.onSecondaryContainer)
                }
                Text(data.name, fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 16.dp))
                Text(data.email, fontSize = 14.sp, color = MaterialTheme.colorScheme.secondary, modifier = Modifier.padding(bottom = 8.dp))
                Text("${data.college ?: "State College"} | ${data.major ?: "Major Not Specified"}", fontSize = 14.sp, modifier = Modifier.padding(bottom = 4.dp))
                Text("Graduation Year: ${data.gradYear ?: "N/A"}", fontSize = 14.sp, color = MaterialTheme.colorScheme.secondary, modifier = Modifier.padding(bottom = 12.dp))
                
                Card(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Bio & Tutoring Focus", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        Text(data.bio ?: "No bio provided.", modifier = Modifier.padding(top = 4.dp))
                    }
                }

                Card(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("Current Balance:", fontWeight = FontWeight.Bold)
                        Text("${String.format("%.2f", data.creditBalance)} Credits", fontWeight = FontWeight.Black)
                    }
                }

                Button(
                    onClick = {
                        editCollege = data.college ?: ""
                        editMajor = data.major ?: ""
                        editBio = data.bio ?: ""
                        editGradYear = data.gradYear?.toString() ?: ""
                        editError = null
                        showEditDialog = true
                    },
                    modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp).height(48.dp),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
                        Icon(Icons.Default.Edit, "Edit")
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Edit Profile Details", fontWeight = FontWeight.Bold)
                    }
                }

                Button(
                    onClick = { 
                        authViewModel.logout()
                        onNavigate(Login)
                    },
                    modifier = Modifier.fillMaxWidth().height(48.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
                        Icon(Icons.Default.ExitToApp, "Logout")
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Log Out", fontWeight = FontWeight.Bold)
                    }
                }

                if (showEditDialog) {
                    AlertDialog(
                        onDismissRequest = { showEditDialog = false },
                        title = { Text("Edit Student Profile") },
                        text = {
                            Column(modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState())) {
                                if (editError != null) {
                                    Text(editError!!, color = MaterialTheme.colorScheme.error, modifier = Modifier.padding(bottom = 8.dp))
                                }
                                OutlinedTextField(
                                    value = editCollege,
                                    onValueChange = { editCollege = it },
                                    label = { Text("College") },
                                    modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                                )
                                OutlinedTextField(
                                    value = editMajor,
                                    onValueChange = { editMajor = it },
                                    label = { Text("Major / Course") },
                                    modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                                )
                                OutlinedTextField(
                                    value = editGradYear,
                                    onValueChange = { editGradYear = it },
                                    label = { Text("Graduation Year") },
                                    modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                                )
                                OutlinedTextField(
                                    value = editBio,
                                    onValueChange = { editBio = it },
                                    label = { Text("Bio / Focus") },
                                    modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                                    minLines = 3
                                )
                            }
                        },
                        confirmButton = {
                            Button(
                                enabled = !isSavingProfile,
                                onClick = {
                                    val gradYearInt = editGradYear.toIntOrNull()
                                    if (editGradYear.isNotBlank() && (gradYearInt == null || gradYearInt < 2026)) {
                                        editError = "Graduation year must be 2026 or later."
                                        return@Button
                                    }
                                    coroutineScope.launch {
                                        try {
                                            isSavingProfile = true
                                            editError = null
                                            val res = authViewModel.repository.updateProfile(
                                                ProfileUpdateRequest(
                                                    college = editCollege.trim().ifBlank { null },
                                                    major = editMajor.trim().ifBlank { null },
                                                    bio = editBio.trim().ifBlank { null },
                                                    gradYear = gradYearInt
                                                )
                                            )
                                            profileData = res
                                            showEditDialog = false
                                        } catch (e: Exception) {
                                            editError = e.message ?: "Failed to save profile changes"
                                        } finally {
                                            isSavingProfile = false
                                        }
                                    }
                                }
                            ) {
                                if (isSavingProfile) {
                                    CircularProgressIndicator(modifier = Modifier.size(20.dp), color = Color.White)
                                } else {
                                    Text("Save Changes")
                                }
                            }
                        },
                        dismissButton = {
                            TextButton(onClick = { showEditDialog = false }) {
                                Text("Cancel")
                            }
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun SkillsScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit,
    onBack: () -> Unit
) {
    val userSkillsState by authViewModel.userSkills.collectAsStateWithLifecycle()
    
    var localTeach by remember { mutableStateOf<List<UserSkillInfo>>(emptyList()) }
    var localLearn by remember { mutableStateOf<List<UserSkillInfo>>(emptyList()) }
    
    var globalSkills by remember { mutableStateOf<List<Skill>>(emptyList()) }
    var isLoadingGlobal by remember { mutableStateOf(true) }
    val saveSkillsState by authViewModel.saveSkillsState.collectAsStateWithLifecycle()

    var searchQuery by remember { mutableStateOf("") }
    val allCategoriesLabel = "All Categories"
    var selectedCategoryFilter by remember { mutableStateOf(allCategoriesLabel) }
    var activePortfolioTab by remember { mutableStateOf(0) } // 0 = Teach, 1 = Learn

    // Dialog state for adding/editing a skill
    var skillToConfigure by remember { mutableStateOf<Skill?>(null) }
    var configRoleTeach by remember { mutableStateOf(true) }
    var configProficiency by remember { mutableStateOf("beginner") }

    val coroutineScope = rememberCoroutineScope()

    LaunchedEffect(userSkillsState) {
        userSkillsState?.let {
            localTeach = it.teach
            localLearn = it.learn
        }
    }

    LaunchedEffect(Unit) {
        try {
            isLoadingGlobal = true
            globalSkills = authViewModel.repository.getSkills()
        } catch (e: Exception) {
            // Ignore catalog fetch errors
        } finally {
            isLoadingGlobal = false
        }
    }

    val proficiencyOptions = listOf("beginner", "intermediate", "advanced")

    // Extract categories
    val categories = remember(globalSkills) {
        listOf(allCategoriesLabel) + globalSkills.map { it.category }.distinct().sorted()
    }

    // Filter skills by search query and category
    val filteredSkills = remember(globalSkills, searchQuery, selectedCategoryFilter) {
        val query = searchQuery.trim()
        globalSkills.filter { skill ->
            val matchesCategory = (selectedCategoryFilter == allCategoriesLabel || skill.category.equals(selectedCategoryFilter, ignoreCase = true))
            if (query.isNotEmpty()) {
                val matchesSearch = skill.name.contains(query, ignoreCase = true) || skill.category.contains(query, ignoreCase = true)
                matchesSearch && matchesCategory
            } else {
                matchesCategory
            }
        }
    }

    val groupedSkills = remember(filteredSkills) {
        filteredSkills.groupBy { it.category }
    }

    AppScreenScaffold(title = "Skills & Expertise", onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp)
                .verticalScroll(rememberScrollState())
        ) {
            Text(
                text = "Skill Portfolio Management",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 4.dp)
            )
            Text(
                text = "Select technologies you can teach and skills you want to learn to get matched with peers.",
                fontSize = 13.sp,
                color = MaterialTheme.colorScheme.secondary,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            // Current Portfolio Active Tabs
            TabRow(
                selectedTabIndex = activePortfolioTab,
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                containerColor = MaterialTheme.colorScheme.surfaceVariant
            ) {
                Tab(
                    selected = activePortfolioTab == 0,
                    onClick = { activePortfolioTab = 0 },
                    text = { Text("Can Teach (${localTeach.size})", fontWeight = FontWeight.Bold) }
                )
                Tab(
                    selected = activePortfolioTab == 1,
                    onClick = { activePortfolioTab = 1 },
                    text = { Text("Want to Learn (${localLearn.size})", fontWeight = FontWeight.Bold) }
                )
            }

            // Active Portfolio Card
            Card(
                modifier = Modifier.fillMaxWidth().padding(bottom = 20.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    val currentList = if (activePortfolioTab == 0) localTeach else localLearn
                    val emptyMessage = if (activePortfolioTab == 0) {
                        "No teaching skills selected yet. Browse below to add skills you can teach!"
                    } else {
                        "No learning goals selected yet. Browse below to add skills you want to learn!"
                    }

                    if (currentList.isEmpty()) {
                        Text(
                            text = emptyMessage,
                            color = MaterialTheme.colorScheme.secondary,
                            fontSize = 13.sp,
                            modifier = Modifier.padding(8.dp)
                        )
                    } else {
                        currentList.forEach { skill ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 4.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(
                                        text = skill.name,
                                        fontWeight = FontWeight.SemiBold,
                                        fontSize = 15.sp
                                    )
                                    Row(
                                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Surface(
                                            color = MaterialTheme.colorScheme.primaryContainer,
                                            shape = RoundedCornerShape(4.dp)
                                        ) {
                                            Text(
                                                text = skill.category,
                                                fontSize = 11.sp,
                                                color = MaterialTheme.colorScheme.onPrimaryContainer,
                                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                            )
                                        }
                                        Surface(
                                            color = MaterialTheme.colorScheme.secondaryContainer,
                                            shape = RoundedCornerShape(4.dp)
                                        ) {
                                            Text(
                                                text = skill.proficiency.replaceFirstChar { it.uppercase() },
                                                fontSize = 11.sp,
                                                color = MaterialTheme.colorScheme.onSecondaryContainer,
                                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                            )
                                        }
                                    }
                                }
                                IconButton(
                                    onClick = {
                                        if (activePortfolioTab == 0) {
                                            localTeach = localTeach.filter { it.skillId != skill.skillId }
                                        } else {
                                            localLearn = localLearn.filter { it.skillId != skill.skillId }
                                        }
                                    }
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Delete,
                                        contentDescription = "Remove skill",
                                        tint = MaterialTheme.colorScheme.error
                                    )
                                }
                            }
                            HorizontalDivider(modifier = Modifier.padding(vertical = 2.dp), color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
                        }
                    }
                }
            }

            // Save status card
            when (saveSkillsState) {
                is OperationState.Success -> {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color(0xFFD4EDDA)),
                        modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
                    ) {
                        Text(
                            text = (saveSkillsState as OperationState.Success).message,
                            color = Color(0xFF155724),
                            modifier = Modifier.padding(12.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                }
                is OperationState.Error -> {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                        modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
                    ) {
                        Text(
                            text = (saveSkillsState as OperationState.Error).message,
                            color = MaterialTheme.colorScheme.onErrorContainer,
                            modifier = Modifier.padding(12.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                }
                else -> {}
            }

            // Save Portfolio Button
            if (saveSkillsState is OperationState.Loading) {
                Box(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else {
                Button(
                    onClick = {
                        val teachList = localTeach.map { UserSkill(it.skillId, "teach", it.proficiency) }
                        val learnList = localLearn.map { UserSkill(it.skillId, "learn", it.proficiency) }
                        authViewModel.saveSkills(teachList, learnList)
                    },
                    modifier = Modifier.fillMaxWidth().height(48.dp).padding(bottom = 8.dp),
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Save Skills Portfolio", fontWeight = FontWeight.Bold)
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Browse & Search Catalog Section
            Text(
                text = "Browse Technology Skills Catalog",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 8.dp)
            )

            // Search Bar
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { newQuery ->
                    // If the user starts typing a search query while a category filter is active, automatically reset to All Categories
                    if (newQuery.isNotBlank() && searchQuery.isBlank() && selectedCategoryFilter != allCategoriesLabel) {
                        selectedCategoryFilter = allCategoriesLabel
                    }
                    searchQuery = newQuery
                },
                label = { Text("Search skills by name or category...") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search") },
                trailingIcon = {
                    if (searchQuery.isNotBlank()) {
                        IconButton(onClick = { searchQuery = "" }) {
                            Icon(Icons.Default.Close, contentDescription = "Clear search")
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                shape = RoundedCornerShape(10.dp),
                singleLine = true
            )

            // Category Filter Chips
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(bottom = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                categories.forEach { cat ->
                    val isSelected = (selectedCategoryFilter == cat)
                    FilterChip(
                        selected = isSelected,
                        onClick = { selectedCategoryFilter = cat },
                        label = {
                            Text(
                                text = if (cat == allCategoriesLabel) "All" else cat,
                                fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                            )
                        },
                        leadingIcon = if (isSelected) {
                            { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        } else null,
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                            selectedLabelColor = MaterialTheme.colorScheme.onPrimaryContainer,
                            selectedLeadingIconColor = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    )
                }
            }

            if (isLoadingGlobal) {
                Box(modifier = Modifier.fillMaxWidth().padding(24.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (filteredSkills.isEmpty()) {
                Card(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Text(
                        text = "No skills match your search query.",
                        color = MaterialTheme.colorScheme.secondary,
                        modifier = Modifier.padding(16.dp),
                        textAlign = TextAlign.Center
                    )
                }
            } else {
                // Grouped Categorized Skills Display
                groupedSkills.forEach { (categoryName, skillsInCategory) ->
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                    ) {
                        Column(modifier = Modifier.padding(14.dp)) {
                            // Category Header
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = categoryName,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 16.sp,
                                    color = MaterialTheme.colorScheme.primary
                                )
                                Surface(
                                    color = MaterialTheme.colorScheme.primaryContainer,
                                    shape = RoundedCornerShape(12.dp)
                                ) {
                                    Text(
                                        text = "${skillsInCategory.size} skills",
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.Medium,
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                                    )
                                }
                            }

                            // Skills list in this category
                            skillsInCategory.forEach { skill ->
                                val isTeaching = localTeach.any { it.skillId == skill.id }
                                val isLearning = localLearn.any { it.skillId == skill.id }

                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 6.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(text = skill.name, fontWeight = FontWeight.Medium, fontSize = 14.sp)
                                        if (isTeaching || isLearning) {
                                            Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                                if (isTeaching) {
                                                    val teachInfo = localTeach.firstOrNull { it.skillId == skill.id }
                                                    Text(
                                                        text = "Teaching (${teachInfo?.proficiency?.replaceFirstChar { it.uppercase() }})",
                                                        fontSize = 11.sp,
                                                        color = MaterialTheme.colorScheme.primary
                                                    )
                                                }
                                                if (isLearning) {
                                                    val learnInfo = localLearn.firstOrNull { it.skillId == skill.id }
                                                    Text(
                                                        text = "Learning (${learnInfo?.proficiency?.replaceFirstChar { it.uppercase() }})",
                                                        fontSize = 11.sp,
                                                        color = MaterialTheme.colorScheme.tertiary
                                                    )
                                                }
                                            }
                                        }
                                    }

                                    // Add/Configure Button
                                    OutlinedButton(
                                        onClick = {
                                            skillToConfigure = skill
                                            configRoleTeach = (activePortfolioTab == 0)
                                            configProficiency = "beginner"
                                        },
                                        shape = RoundedCornerShape(8.dp),
                                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                                        modifier = Modifier.height(34.dp)
                                    ) {
                                        Icon(Icons.Default.Add, contentDescription = "Add", modifier = Modifier.size(16.dp))
                                        Spacer(modifier = Modifier.width(4.dp))
                                        Text("Add", fontSize = 12.sp)
                                    }
                                }
                                HorizontalDivider(modifier = Modifier.padding(vertical = 2.dp), color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))
                            }
                        }
                    }
                }
            }
        }
    }

    // Configure and Add Skill Dialog
    if (skillToConfigure != null) {
        val skill = skillToConfigure!!
        AlertDialog(
            onDismissRequest = { skillToConfigure = null },
            title = {
                Column {
                    Text(text = "Add to Portfolio", fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Text(text = skill.name, fontSize = 15.sp, color = MaterialTheme.colorScheme.primary)
                    Text(text = "Category: ${skill.category}", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
                }
            },
            text = {
                Column(modifier = Modifier.fillMaxWidth()) {
                    Text("Select Role:", fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(top = 8.dp, bottom = 4.dp))
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        RadioButton(
                            selected = configRoleTeach,
                            onClick = { configRoleTeach = true }
                        )
                        Text("I Can Teach", fontSize = 14.sp)
                        Spacer(modifier = Modifier.width(16.dp))
                        RadioButton(
                            selected = !configRoleTeach,
                            onClick = { configRoleTeach = false }
                        )
                        Text("I Want to Learn", fontSize = 14.sp)
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    Text("Proficiency Level:", fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(bottom = 4.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        proficiencyOptions.forEach { opt ->
                            FilterChip(
                                selected = configProficiency == opt,
                                onClick = { configProficiency = opt },
                                label = { Text(opt.replaceFirstChar { it.uppercase() }, fontSize = 12.sp) }
                            )
                        }
                    }
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        val newInfo = UserSkillInfo(
                            skillId = skill.id,
                            name = skill.name,
                            category = skill.category,
                            proficiency = configProficiency
                        )
                        if (configRoleTeach) {
                            localTeach = localTeach.filter { it.skillId != skill.id } + newInfo
                        } else {
                            localLearn = localLearn.filter { it.skillId != skill.id } + newInfo
                        }
                        skillToConfigure = null
                    }
                ) {
                    Text("Add to Portfolio")
                }
            },
            dismissButton = {
                TextButton(onClick = { skillToConfigure = null }) {
                    Text("Cancel")
                }
            }
        )
    }
}

@Composable
fun PlaceholderPage(
    title: String,
    description: String,
    icon: ImageVector,
    onBack: () -> Unit,
    onNavigate: (NavKey) -> Unit
) {
    AppScreenScaffold(title = title, onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(24.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = title,
                    modifier = Modifier.size(72.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
                Text(
                    text = title,
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(top = 16.dp, bottom = 8.dp)
                )
                Text(
                    text = description,
                    fontSize = 14.sp,
                    textAlign = TextAlign.Center,
                    color = MaterialTheme.colorScheme.secondary
                )
            }
        }
    }
}

@Composable
fun MatchesScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit,
    onBack: () -> Unit
) {
    var matches by remember { mutableStateOf<List<MatchResponse>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    var showRequestDialog by remember { mutableStateOf(false) }
    var selectedMatch by remember { mutableStateOf<MatchResponse?>(null) }
    var messageText by remember { mutableStateOf("") }
    var selectedTeachSkillId by remember { mutableStateOf<Int?>(null) }
    var selectedLearnSkillId by remember { mutableStateOf<Int?>(null) }
    var isSendingRequest by remember { mutableStateOf(false) }
    var requestError by remember { mutableStateOf<String?>(null) }
    var requestSuccess by remember { mutableStateOf<String?>(null) }

    val coroutineScope = rememberCoroutineScope()

    val fetchMatches = {
        coroutineScope.launch {
            try {
                isLoading = true
                matches = authViewModel.repository.getMatches()
                errorMessage = null
            } catch (e: Exception) {
                errorMessage = e.message ?: "Failed to fetch compatible matches."
            } finally {
                isLoading = false
            }
        }
    }

    LaunchedEffect(Unit) {
        fetchMatches()
    }

    AppScreenScaffold(title = "Teachable Matches", onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (errorMessage != null) {
                Column(
                    modifier = Modifier.fillMaxSize().padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Text(errorMessage!!, color = MaterialTheme.colorScheme.error, textAlign = TextAlign.Center)
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { fetchMatches() }) {
                        Text("Retry")
                    }
                }
            } else if (matches.isEmpty()) {
                Column(
                    modifier = Modifier.fillMaxSize().padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Icon(Icons.Default.Search, "No Matches", modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.secondary)
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("No matches found yet.", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    Text("Try adding more teaching or learning skills to get recommended compatible peers!", color = MaterialTheme.colorScheme.secondary, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 8.dp))
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize().padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(matches.size) { index ->
                        val match = matches[index]
                        Card(modifier = Modifier.fillMaxWidth()) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(match.user.name, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                                    val chipColor = if (match.reciprocal) Color(0xFFD4EDDA) else MaterialTheme.colorScheme.primaryContainer
                                    val textColor = if (match.reciprocal) Color(0xFF155724) else MaterialTheme.colorScheme.onPrimaryContainer
                                    val labelText = if (match.reciprocal) "Reciprocal (100%)" else "One-way (50%)"
                                    Card(
                                        colors = CardDefaults.cardColors(containerColor = chipColor)
                                    ) {
                                        Text(
                                            labelText,
                                            color = textColor,
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.Bold,
                                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                        )
                                    }
                                }
                                Text("Major: ${match.user.major ?: "N/A"} | College: ${match.user.college ?: "N/A"}", fontSize = 13.sp, color = MaterialTheme.colorScheme.secondary, modifier = Modifier.padding(vertical = 4.dp))
                                Text(match.user.bio ?: "No bio provided.", fontSize = 13.sp, modifier = Modifier.padding(bottom = 12.dp))

                                HorizontalDivider(modifier = Modifier.padding(bottom = 8.dp))

                                Row(modifier = Modifier.fillMaxWidth()) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text("Skills They Teach", fontWeight = FontWeight.Bold, fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                                        if (match.teachSkills.isEmpty()) {
                                            Text("None", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
                                        } else {
                                            match.teachSkills.forEach { s ->
                                                Text("• ${s.name} (${s.proficiency})", fontSize = 12.sp)
                                            }
                                        }
                                    }
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text("Skills They Learn", fontWeight = FontWeight.Bold, fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                                        if (match.learnSkills.isEmpty()) {
                                            Text("None", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
                                        } else {
                                            match.learnSkills.forEach { s ->
                                                Text("• ${s.name} (${s.proficiency})", fontSize = 12.sp)
                                            }
                                        }
                                    }
                                }

                                Spacer(modifier = Modifier.height(16.dp))

                                Button(
                                    onClick = {
                                        selectedMatch = match
                                        selectedTeachSkillId = match.learnSkills.firstOrNull()?.id ?: match.teachSkills.firstOrNull()?.id
                                        selectedLearnSkillId = match.teachSkills.firstOrNull()?.id ?: match.learnSkills.firstOrNull()?.id
                                        messageText = "Hi, let's swap skills!"
                                        requestError = null
                                        requestSuccess = null
                                        showRequestDialog = true
                                    },
                                    modifier = Modifier.fillMaxWidth().height(40.dp),
                                    shape = RoundedCornerShape(8.dp)
                                ) {
                                    Text("Send Swap Proposal", fontSize = 13.sp)
                                }
                            }
                        }
                    }
                }
            }

            if (showRequestDialog && selectedMatch != null) {
                val match = selectedMatch!!
                AlertDialog(
                    onDismissRequest = { showRequestDialog = false },
                    title = { Text("Send Swap Proposal") },
                    text = {
                        Column(modifier = Modifier.fillMaxWidth()) {
                            if (requestError != null) {
                                Text(requestError!!, color = MaterialTheme.colorScheme.error, modifier = Modifier.padding(bottom = 8.dp))
                            }
                            if (requestSuccess != null) {
                                Text(requestSuccess!!, color = Color(0xFF155724), modifier = Modifier.padding(bottom = 8.dp))
                            }
                            Text("Proposing exchange with ${match.user.name}", fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))

                            OutlinedTextField(
                                value = messageText,
                                onValueChange = { messageText = it },
                                label = { Text("Message proposal") },
                                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp)
                            )
                        }
                    },
                    confirmButton = {
                        Button(
                            enabled = !isSendingRequest && requestSuccess == null,
                            onClick = {
                                coroutineScope.launch {
                                    try {
                                        isSendingRequest = true
                                        requestError = null
                                        val res = authViewModel.repository.sendSwapRequest(
                                            SendSwapRequest(
                                                receiverId = match.user.id,
                                                teachSkillId = selectedTeachSkillId,
                                                learnSkillId = selectedLearnSkillId,
                                                message = messageText
                                            )
                                        )
                                        requestSuccess = res.message
                                        delay(1500)
                                        showRequestDialog = false
                                    } catch (e: Exception) {
                                        requestError = e.message ?: "Failed to send proposal"
                                    } finally {
                                        isSendingRequest = false
                                    }
                                }
                            }
                        ) {
                            if (isSendingRequest) {
                                CircularProgressIndicator(modifier = Modifier.size(20.dp), color = Color.White)
                            } else {
                                Text("Send Proposal")
                            }
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { showRequestDialog = false }) {
                            Text("Cancel")
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun SwapRequestsScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit,
    onBack: () -> Unit
) {
    var swapRequests by remember { mutableStateOf<SwapRequestsResponse?>(null) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var selectedTabIncoming by remember { mutableStateOf(true) }

    // Session scheduling dialog state
    var showScheduleDialog by remember { mutableStateOf(false) }
    var selectedRequestForScheduling by remember { mutableStateOf<SwapRequestItem?>(null) }
    var scheduledDateText by remember { mutableStateOf("") } // e.g. 2026-09-01
    var scheduledTimeText by remember { mutableStateOf("10:00:00") } // e.g. 10:00:00
    var durationText by remember { mutableStateOf("1.0") }
    var venueText by remember { mutableStateOf("Campus Library") }
    var schedulingError by remember { mutableStateOf<String?>(null) }
    var schedulingSuccess by remember { mutableStateOf<String?>(null) }
    var isSavingSession by remember { mutableStateOf(false) }

    val coroutineScope = rememberCoroutineScope()

    val fetchRequests = {
        coroutineScope.launch {
            try {
                isLoading = true
                swapRequests = authViewModel.repository.getSwapRequests()
                errorMessage = null
            } catch (e: Exception) {
                errorMessage = e.message ?: "Failed to fetch swap requests."
            } finally {
                isLoading = false
            }
        }
    }

    LaunchedEffect(Unit) {
        fetchRequests()
    }

    AppScreenScaffold(title = "Swap Requests", onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            TabRow(selectedTabIndex = if (selectedTabIncoming) 0 else 1) {
                Tab(
                    selected = selectedTabIncoming,
                    onClick = { selectedTabIncoming = true },
                    text = { Text("Incoming") }
                )
                Tab(
                    selected = !selectedTabIncoming,
                    onClick = { selectedTabIncoming = false },
                    text = { Text("Outgoing") }
                )
            }

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
            ) {
                if (isLoading) {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                } else if (errorMessage != null) {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Text(errorMessage!!, color = MaterialTheme.colorScheme.error, textAlign = TextAlign.Center)
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = { fetchRequests() }) {
                            Text("Retry")
                        }
                    }
                } else {
                    val requestsList = if (selectedTabIncoming) {
                        swapRequests?.incoming ?: emptyList()
                    } else {
                        swapRequests?.outgoing ?: emptyList()
                    }

                    if (requestsList.isEmpty()) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Text(
                                text = if (selectedTabIncoming) "No incoming swap requests." else "No outgoing swap requests.",
                                style = MaterialTheme.typography.bodyLarge,
                                color = MaterialTheme.colorScheme.secondary
                            )
                        }
                    } else {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(requestsList.size) { index ->
                                val request = requestsList[index]
                                Card(modifier = Modifier.fillMaxWidth()) {
                                    Column(modifier = Modifier.padding(16.dp)) {
                                        Row(
                                            modifier = Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.SpaceBetween,
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            val peerName = if (selectedTabIncoming) request.sender.name else request.receiver.name
                                            Text(peerName, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                                            Card(
                                                colors = CardDefaults.cardColors(
                                                    containerColor = when (request.status) {
                                                        "accepted" -> Color(0xFFD4EDDA)
                                                        "rejected" -> MaterialTheme.colorScheme.errorContainer
                                                        "pending" -> MaterialTheme.colorScheme.primaryContainer
                                                        else -> MaterialTheme.colorScheme.surfaceVariant
                                                    }
                                                )
                                            ) {
                                                Text(
                                                    request.status.replaceFirstChar { it.uppercase() },
                                                    fontSize = 11.sp,
                                                    fontWeight = FontWeight.Bold,
                                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                                                    color = when (request.status) {
                                                        "accepted" -> Color(0xFF155724)
                                                        "rejected" -> MaterialTheme.colorScheme.onErrorContainer
                                                        else -> MaterialTheme.colorScheme.onPrimaryContainer
                                                    }
                                                )
                                            }
                                        }

                                        Spacer(modifier = Modifier.height(4.dp))
                                        Text("Exchange Summary:", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                                        Text("• Teach: ${request.teachSkill?.name ?: "None"}", fontSize = 12.sp)
                                        Text("• Learn: ${request.learnSkill?.name ?: "None"}", fontSize = 12.sp)

                                        if (!request.message.isNullOrBlank()) {
                                            Text("Message: \"${request.message}\"", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary, modifier = Modifier.padding(top = 4.dp))
                                        }

                                        Text("Sent: ${request.createdAt}", fontSize = 10.sp, color = Color.Gray, modifier = Modifier.padding(top = 8.dp))

                                        if (request.status == "pending") {
                                            Spacer(modifier = Modifier.height(12.dp))
                                            if (selectedTabIncoming) {
                                                Row(
                                                    modifier = Modifier.fillMaxWidth(),
                                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                                ) {
                                                    Button(
                                                        onClick = {
                                                            coroutineScope.launch {
                                                                try {
                                                                    authViewModel.repository.respondSwapRequest(request.id, "accept")
                                                                    fetchRequests()
                                                                } catch (e: Exception) {}
                                                            }
                                                        },
                                                        modifier = Modifier.weight(1f),
                                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF28A745))
                                                    ) {
                                                        Text("Accept", color = Color.White)
                                                    }
                                                    Button(
                                                        onClick = {
                                                            coroutineScope.launch {
                                                                try {
                                                                    authViewModel.repository.respondSwapRequest(request.id, "reject")
                                                                    fetchRequests()
                                                                } catch (e: Exception) {}
                                                            }
                                                        },
                                                        modifier = Modifier.weight(1f),
                                                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                                                    ) {
                                                        Text("Reject")
                                                    }
                                                }
                                            } else {
                                                Button(
                                                    onClick = {
                                                        coroutineScope.launch {
                                                            try {
                                                                authViewModel.repository.respondSwapRequest(request.id, "cancel")
                                                                fetchRequests()
                                                            } catch (e: Exception) {}
                                                        }
                                                    },
                                                    modifier = Modifier.fillMaxWidth(),
                                                    colors = ButtonDefaults.buttonColors(containerColor = Color.Gray)
                                                ) {
                                                    Text("Cancel Proposal", color = Color.White)
                                                }
                                            }
                                        }

                                        if (request.status == "accepted") {
                                            Spacer(modifier = Modifier.height(12.dp))
                                            Button(
                                                onClick = {
                                                    selectedRequestForScheduling = request
                                                    scheduledDateText = "2026-09-01"
                                                    scheduledTimeText = "10:00:00"
                                                    durationText = "1.0"
                                                    venueText = "Campus Library"
                                                    schedulingError = null
                                                    schedulingSuccess = null
                                                    showScheduleDialog = true
                                                },
                                                modifier = Modifier.fillMaxWidth()
                                            ) {
                                                Text("Schedule Exchange Session")
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            if (showScheduleDialog && selectedRequestForScheduling != null) {
                val req = selectedRequestForScheduling!!
                AlertDialog(
                    onDismissRequest = { showScheduleDialog = false },
                    title = { Text("Schedule Swap Session") },
                    text = {
                        Column(modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState())) {
                            if (schedulingError != null) {
                                Text(schedulingError!!, color = MaterialTheme.colorScheme.error, modifier = Modifier.padding(bottom = 8.dp))
                            }
                            if (schedulingSuccess != null) {
                                Text(schedulingSuccess!!, color = Color(0xFF155724), modifier = Modifier.padding(bottom = 8.dp))
                            }
                            Text("Scheduling with: ${if (selectedTabIncoming) req.sender.name else req.receiver.name}", fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 8.dp))
                            Text("Skill to exchange: ${req.teachSkill?.name ?: req.learnSkill?.name ?: "Tutoring Skill"}", modifier = Modifier.padding(bottom = 12.dp))

                            OutlinedTextField(
                                value = scheduledDateText,
                                onValueChange = { scheduledDateText = it },
                                label = { Text("Date (YYYY-MM-DD)") },
                                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                            )
                            OutlinedTextField(
                                value = scheduledTimeText,
                                onValueChange = { scheduledTimeText = it },
                                label = { Text("Time (HH:MM:SS)") },
                                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                            )
                            OutlinedTextField(
                                value = durationText,
                                onValueChange = { durationText = it },
                                label = { Text("Duration (Hours)") },
                                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                            )
                            OutlinedTextField(
                                value = venueText,
                                onValueChange = { venueText = it },
                                label = { Text("Venue / Location") },
                                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                            )
                        }
                    },
                    confirmButton = {
                        Button(
                            enabled = !isSavingSession && schedulingSuccess == null,
                            onClick = {
                                val dur = durationText.toDoubleOrNull()
                                if (dur == null || dur <= 0) {
                                    schedulingError = "Duration must be a positive decimal."
                                    return@Button
                                }
                                val scheduledAt = "$scheduledDateText $scheduledTimeText"
                                coroutineScope.launch {
                                    try {
                                        isSavingSession = true
                                        schedulingError = null
                                        
                                        // Determine teacher/learner logic from the request:
                                        // Whichever skill exists decides roles.
                                        val (tId, lId, sId) = if (selectedTabIncoming) {
                                            if (req.teachSkill != null) {
                                                Triple(req.sender.id, req.receiver.id, req.teachSkill.id)
                                            } else {
                                                Triple(req.receiver.id, req.sender.id, req.learnSkill!!.id)
                                            }
                                        } else {
                                            if (req.teachSkill != null) {
                                                Triple(req.sender.id, req.receiver.id, req.teachSkill.id)
                                            } else {
                                                Triple(req.receiver.id, req.sender.id, req.learnSkill!!.id)
                                            }
                                        }

                                        val res = authViewModel.repository.createSession(
                                            ScheduleSessionRequest(
                                                requestId = req.id,
                                                teacherId = tId,
                                                learnerId = lId,
                                                skillId = sId,
                                                scheduledAt = scheduledAt,
                                                durationHours = dur,
                                                venue = venueText
                                            )
                                        )
                                        schedulingSuccess = res.message
                                        delay(1500)
                                        showScheduleDialog = false
                                        fetchRequests()
                                    } catch (e: Exception) {
                                        schedulingError = e.message ?: "Failed to schedule session."
                                    } finally {
                                        isSavingSession = false
                                    }
                                }
                            }
                        ) {
                            if (isSavingSession) {
                                CircularProgressIndicator(modifier = Modifier.size(20.dp), color = Color.White)
                            } else {
                                Text("Schedule")
                            }
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { showScheduleDialog = false }) {
                            Text("Cancel")
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun SessionsScreen(
    authViewModel: AuthViewModel,
    onNavigate: (NavKey) -> Unit,
    onBack: () -> Unit
) {
    var sessions by remember { mutableStateOf<List<SessionItem>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    var showDetailsDialog by remember { mutableStateOf(false) }
    var selectedSessionId by remember { mutableStateOf<Int?>(null) }
    var sessionDetails by remember { mutableStateOf<SessionDetailResponse?>(null) }
    var isLoadingDetails by remember { mutableStateOf(false) }
    var detailsError by remember { mutableStateOf<String?>(null) }

    var isExecutingAction by remember { mutableStateOf(false) }
    var actionError by remember { mutableStateOf<String?>(null) }
    var actionSuccess by remember { mutableStateOf<String?>(null) }

    val coroutineScope = rememberCoroutineScope()

    val fetchSessions = {
        coroutineScope.launch {
            try {
                isLoading = true
                sessions = authViewModel.repository.getSessions()
                errorMessage = null
            } catch (e: Exception) {
                errorMessage = e.message ?: "Failed to fetch swap sessions."
            } finally {
                isLoading = false
            }
        }
    }

    LaunchedEffect(Unit) {
        fetchSessions()
    }

    val fetchSessionDetails = { sessionId: Int ->
        coroutineScope.launch {
            try {
                isLoadingDetails = true
                detailsError = null
                sessionDetails = authViewModel.repository.getSessionDetails(sessionId)
            } catch (e: Exception) {
                detailsError = e.message ?: "Failed to fetch session details."
            } finally {
                isLoadingDetails = false
            }
        }
    }

    AppScreenScaffold(title = "Sessions Manager", onBack = onBack, onNavigate = onNavigate) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (errorMessage != null) {
                Column(
                    modifier = Modifier.fillMaxSize().padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Text(errorMessage!!, color = MaterialTheme.colorScheme.error, textAlign = TextAlign.Center)
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { fetchSessions() }) {
                        Text("Retry")
                    }
                }
            } else if (sessions.isEmpty()) {
                Column(
                    modifier = Modifier.fillMaxSize().padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Icon(Icons.Default.DateRange, "No Sessions", modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.secondary)
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("No exchange sessions scheduled.", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    Text("Coordinate with accepted swap proposals to schedule dynamic tutoring hours!", color = MaterialTheme.colorScheme.secondary, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 8.dp))
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize().padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(sessions.size) { index ->
                        val session = sessions[index]
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    selectedSessionId = session.id
                                    actionError = null
                                    actionSuccess = null
                                    fetchSessionDetails(session.id)
                                    showDetailsDialog = true
                                }
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(session.partnerName, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                                    Card(
                                        colors = CardDefaults.cardColors(
                                            containerColor = when (session.status) {
                                                "completed" -> Color(0xFFD4EDDA)
                                                "cancelled" -> MaterialTheme.colorScheme.errorContainer
                                                "scheduled" -> MaterialTheme.colorScheme.primaryContainer
                                                else -> MaterialTheme.colorScheme.surfaceVariant
                                            }
                                        )
                                    ) {
                                        Text(
                                            session.status.replaceFirstChar { it.uppercase() },
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.Bold,
                                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                                            color = when (session.status) {
                                                "completed" -> Color(0xFF155724)
                                                "cancelled" -> MaterialTheme.colorScheme.onErrorContainer
                                                else -> MaterialTheme.colorScheme.onPrimaryContainer
                                            }
                                        )
                                    }
                                }
                                Text("Exchange Skill: ${session.skillName}", fontSize = 13.sp, modifier = Modifier.padding(top = 4.dp))
                                Text("Role: ${session.role.replaceFirstChar { it.uppercase() }}", fontSize = 13.sp, color = MaterialTheme.colorScheme.secondary)
                                Text("Scheduled: ${session.scheduledAt} (${session.durationHours} hrs)", fontSize = 13.sp, color = Color.Gray, modifier = Modifier.padding(top = 8.dp))
                            }
                        }
                    }
                }
            }

            if (showDetailsDialog && selectedSessionId != null) {
                AlertDialog(
                    onDismissRequest = { showDetailsDialog = false },
                    title = { Text("Session Exchange Details") },
                    text = {
                        Column(modifier = Modifier.fillMaxWidth()) {
                            if (isLoadingDetails) {
                                Box(modifier = Modifier.fillMaxWidth().padding(24.dp), contentAlignment = Alignment.Center) {
                                    CircularProgressIndicator()
                                }
                            } else if (detailsError != null) {
                                Text(detailsError!!, color = MaterialTheme.colorScheme.error)
                            } else if (sessionDetails != null) {
                                val s = sessionDetails!!
                                if (actionError != null) {
                                    Text(actionError!!, color = MaterialTheme.colorScheme.error, modifier = Modifier.padding(bottom = 8.dp))
                                }
                                if (actionSuccess != null) {
                                    Text(actionSuccess!!, color = Color(0xFF155724), modifier = Modifier.padding(bottom = 8.dp))
                                }

                                Text("Teacher: ${s.teacherName}", fontSize = 14.sp, modifier = Modifier.padding(bottom = 4.dp))
                                Text("Learner: ${s.learnerName}", fontSize = 14.sp, modifier = Modifier.padding(bottom = 4.dp))
                                Text("Exchange Skill: ${s.skillName}", fontSize = 14.sp, modifier = Modifier.padding(bottom = 4.dp))
                                Text("Scheduled Date/Time: ${s.scheduledAt}", fontSize = 14.sp, modifier = Modifier.padding(bottom = 4.dp))
                                Text("Duration: ${s.durationHours} hours", fontSize = 14.sp, modifier = Modifier.padding(bottom = 4.dp))
                                Text("Venue: ${s.venue}", fontSize = 14.sp, modifier = Modifier.padding(bottom = 4.dp))
                                Text("Current Status: ${s.status.replaceFirstChar { it.uppercase() }}", fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.padding(bottom = 12.dp))

                                if (s.status == "cancelled" && !s.cancelledReason.isNullOrBlank()) {
                                    Text("Reason Cancelled: \"${s.cancelledReason}\"", color = MaterialTheme.colorScheme.error, fontSize = 13.sp)
                                }
                            }
                        }
                    },
                    confirmButton = {
                        if (sessionDetails != null && sessionDetails!!.status == "scheduled" && !isExecutingAction && actionSuccess == null) {
                            val s = sessionDetails!!
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                Button(
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF28A745)),
                                    onClick = {
                                        coroutineScope.launch {
                                            try {
                                                isExecutingAction = true
                                                actionError = null
                                                val res = authViewModel.repository.respondSession(s.id, "complete", null)
                                                actionSuccess = res.message
                                                authViewModel.refreshProfile()
                                                delay(1500)
                                                showDetailsDialog = false
                                                fetchSessions()
                                            } catch (e: Exception) {
                                                actionError = e.message ?: "Failed to complete session."
                                            } finally {
                                                isExecutingAction = false
                                            }
                                        }
                                    }
                                ) {
                                    Text("Complete", color = Color.White)
                                }
                                Button(
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
                                    onClick = {
                                        coroutineScope.launch {
                                            try {
                                                isExecutingAction = true
                                                actionError = null
                                                val res = authViewModel.repository.respondSession(s.id, "cancel", "Cancelled by student request")
                                                actionSuccess = res.message
                                                authViewModel.refreshProfile()
                                                delay(1500)
                                                showDetailsDialog = false
                                                fetchSessions()
                                            } catch (e: Exception) {
                                                actionError = e.message ?: "Failed to cancel session."
                                            } finally {
                                                isExecutingAction = false
                                            }
                                        }
                                    }
                                ) {
                                    Text("Cancel")
                                }
                            }
                        } else {
                            TextButton(onClick = { showDetailsDialog = false }) {
                                Text("Close")
                            }
                        }
                    }
                )
            }
        }
    }
}

