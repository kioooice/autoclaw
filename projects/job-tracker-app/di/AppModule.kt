package com.example.jobtracker.di

import android.content.Context
import com.example.jobtracker.data.local.JobApplicationDao
import com.example.jobtracker.data.local.JobApplicationDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): JobApplicationDatabase {
        return JobApplicationDatabase.getDatabase(context)
    }
    
    @Provides
    @Singleton
    fun provideJobApplicationDao(database: JobApplicationDatabase): JobApplicationDao {
        return database.jobApplicationDao()
    }
}
