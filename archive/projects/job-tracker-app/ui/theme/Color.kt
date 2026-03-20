package com.example.jobtracker.ui.theme

import androidx.compose.ui.graphics.Color

// Primary colors
val PrimaryBlue = Color(0xFF1976D2)
val PrimaryBlueDark = Color(0xFF1565C0)
val PrimaryBlueLight = Color(0xFF64B5F6)

// Status colors
val StatusApplied = Color(0xFF9E9E9E)
val StatusScreening = Color(0xFFFFC107)
val StatusWrittenTest = Color(0xFFFF9800)
val StatusInterview = Color(0xFF2196F3)
val StatusOffer = Color(0xFF4CAF50)
val StatusRejected = Color(0xFFF44336)

// Background colors
val BackgroundLight = Color(0xFFF5F5F5)
val SurfaceLight = Color(0xFFFFFFFF)
val BackgroundDark = Color(0xFF121212)
val SurfaceDark = Color(0xFF1E1E1E)

// Text colors
val TextPrimary = Color(0xFF212121)
val TextSecondary = Color(0xFF757575)
val TextHint = Color(0xFFBDBDBD)

// Error color
val ErrorRed = Color(0xFFB00020)

fun getStatusColor(status: String): Color {
    return when (status) {
        "APPLIED" -> StatusApplied
        "SCREENING" -> StatusScreening
        "WRITTEN_TEST" -> StatusWrittenTest
        "INTERVIEW" -> StatusInterview
        "OFFER" -> StatusOffer
        "REJECTED" -> StatusRejected
        else -> StatusApplied
    }
}
