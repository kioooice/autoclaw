package com.example.jobtracker.data.local

import androidx.room.*
import com.example.jobtracker.data.local.entity.JobApplicationEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface JobApplicationDao {
    
    @Query("SELECT * FROM job_applications ORDER BY applyDate DESC")
    fun getAllApplications(): Flow<List<JobApplicationEntity>>
    
    @Query("SELECT * FROM job_applications WHERE id = :id")
    suspend fun getApplicationById(id: Long): JobApplicationEntity?
    
    @Query("SELECT * FROM job_applications WHERE status = :status ORDER BY applyDate DESC")
    fun getApplicationsByStatus(status: String): Flow<List<JobApplicationEntity>>
    
    @Query("SELECT COUNT(*) FROM job_applications")
    fun getTotalCount(): Flow<Int>
    
    @Query("SELECT COUNT(*) FROM job_applications WHERE status = :status")
    fun getCountByStatus(status: String): Flow<Int>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(application: JobApplicationEntity): Long
    
    @Update
    suspend fun update(application: JobApplicationEntity)
    
    @Delete
    suspend fun delete(application: JobApplicationEntity)
    
    @Query("DELETE FROM job_applications WHERE id = :id")
    suspend fun deleteById(id: Long)
}
