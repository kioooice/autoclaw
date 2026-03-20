package com.example.jobtracker.data.model

enum class ApplicationStatus(val displayName: String, val colorHex: String) {
    APPLIED("已投递", "#9E9E9E"),
    SCREENING("简历筛选", "#FFC107"),
    WRITTEN_TEST("笔试", "#FF9800"),
    INTERVIEW("面试", "#2196F3"),
    OFFER("Offer", "#4CAF50"),
    REJECTED("已拒绝", "#F44336");

    companion object {
        fun fromString(value: String): ApplicationStatus {
            return entries.find { it.name == value } ?: APPLIED
        }
    }
}
