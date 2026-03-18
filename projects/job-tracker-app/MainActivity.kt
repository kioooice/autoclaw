package com.example.jobtracker

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.example.jobtracker.ui.screens.AddEditScreen
import com.example.jobtracker.ui.screens.DetailScreen
import com.example.jobtracker.ui.screens.HomeScreen
import com.example.jobtracker.ui.theme.JobTrackerTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            JobTrackerTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()
                    
                    NavHost(
                        navController = navController,
                        startDestination = "home"
                    ) {
                        composable("home") {
                            HomeScreen(
                                onNavigateToAdd = {
                                    navController.navigate("add")
                                },
                                onNavigateToDetail = { id ->
                                    navController.navigate("detail/$id")
                                }
                            )
                        }
                        
                        composable("add") {
                            AddEditScreen(
                                onNavigateBack = {
                                    navController.popBackStack()
                                }
                            )
                        }
                        
                        composable(
                            route = "edit/{applicationId}",
                            arguments = listOf(
                                navArgument("applicationId") { type = NavType.LongType }
                            )
                        ) {
                            AddEditScreen(
                                onNavigateBack = {
                                    navController.popBackStack()
                                }
                            )
                        }
                        
                        composable(
                            route = "detail/{applicationId}",
                            arguments = listOf(
                                navArgument("applicationId") { type = NavType.LongType }
                            )
                        ) { backStackEntry ->
                            val applicationId = backStackEntry.arguments?.getLong("applicationId") ?: 0
                            DetailScreen(
                                applicationId = applicationId,
                                onNavigateBack = {
                                    navController.popBackStack()
                                },
                                onNavigateToEdit = { id ->
                                    navController.navigate("edit/$id")
                                }
                            )
                        }
                    }
                }
            }
        }
    }
}