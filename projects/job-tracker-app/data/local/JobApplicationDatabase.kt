package com.example.jobtracker.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.example.jobtracker.data.local.entity.JobApplicationEntity

@Database(
    entities = [JobApplicationEntity::class],
    version = 1,
    exportSchema = false
)
abstract class JobApplicationDatabase : RoomDatabase() {
    
    abstract fun jobApplicationDao(): JobApplicationDao
    
    companion object {
        @Volatile
        private var INSTANCE: JobApplicationDatabase? = null
        
        fun getDatabase(context: Context): JobApplicationDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    JobApplicationDatabase::class.java,
                    "job_tracker_database"
                )
                    .fallbackToDestructiveMigration()
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
