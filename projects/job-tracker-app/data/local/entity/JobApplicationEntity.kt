package com.example.jobtracker.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "job_applications")
data class JobApplicationEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val companyName: String,
    val position: String,
    val status: String,
    val applyDate: Long,
    val salary: String = "",
    val location: String = "",
    val notes: String = "",
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
)
