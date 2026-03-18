package com.example.jobtracker.data.repository

import com.example.jobtracker.data.local.JobApplicationDao
import com.example.jobtracker.data.local.entity.JobApplicationEntity
import com.example.jobtracker.data.model.ApplicationStatus
import com.example.jobtracker.data.model.JobApplication
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class JobApplicationRepository @Inject constructor(
    private val dao: JobApplicationDao
) {
    
    fun getAllApplications(): Flow<List<JobApplication>> {
        return dao.getAllApplications().map { entities ->
            entities.map { it.toDomainModel() }
        }
    }
    
    suspend fun getApplicationById(id: Long): JobApplication? {
        return dao.getApplicationById(id)?.toDomainModel()
    }
    
    fun getApplicationsByStatus(status: ApplicationStatus): Flow<List<JobApplication>> {
        return dao.getApplicationsByStatus(status.name).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }
    
    fun getTotalCount(): Flow<Int> = dao.getTotalCount()
    
    fun getCountByStatus(status: ApplicationStatus): Flow<Int> {
        return dao.getCountByStatus(status.name)
    }
    
    suspend fun insert(application: JobApplication): Long {
        return dao.insert(application.toEntity())
    }
    
    suspend fun update(application: JobApplication) {
        dao.update(application.toEntity())
    }
    
    suspend fun delete(application: JobApplication) {
        dao.delete(application.toEntity())
    }
    
    suspend fun deleteById(id: Long) {
        dao.deleteById(id)
    }
    
    private fun JobApplicationEntity.toDomainModel(): JobApplication {
        return JobApplication(
            id = id,
            companyName = companyName,
            position = position,
            status = ApplicationStatus.fromString(status),
            applyDate = applyDate,
            salary = salary,
            location = location,
            notes = notes,
            createdAt = createdAt,
            updatedAt = updatedAt
        )
    }
    
    private fun JobApplication.toEntity(): JobApplicationEntity {
        return JobApplicationEntity(
            id = id,
            companyName = companyName,
            position = position,
            status = status.name,
            applyDate = applyDate,
            salary = salary,
            location = location,
            notes = notes,
            createdAt = createdAt,
            updatedAt = System.currentTimeMillis()
        )
    }
}
