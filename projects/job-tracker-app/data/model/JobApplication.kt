package com.example.jobtracker.data.model

data class JobApplication(
    val id: Long = 0,
    val companyName: String,
    val position: String,
    val status: ApplicationStatus,
    val applyDate: Long,
    val salary: String = "",
    val location: String = "",
    val notes: String = "",
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
)
