package com.example.jobtracker.ui.viewmodel

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.jobtracker.data.model.ApplicationStatus
import com.example.jobtracker.data.model.JobApplication
import com.example.jobtracker.data.repository.JobApplicationRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class AddEditUiState(
    val companyName: String = "",
    val position: String = "",
    val status: ApplicationStatus = ApplicationStatus.APPLIED,
    val applyDate: Long = System.currentTimeMillis(),
    val salary: String = "",
    val location: String = "",
    val notes: String = "",
    val isLoading: Boolean = false,
    val isSaved: Boolean = false,
    val errorMessage: String? = null
)

@HiltViewModel
class AddEditViewModel @Inject constructor(
    private val repository: JobApplicationRepository,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _uiState = MutableStateFlow(AddEditUiState())
    val uiState: StateFlow<AddEditUiState> = _uiState.asStateFlow()

    private var applicationId: Long = 0
    private var isEditMode = false

    init {
        savedStateHandle.get<Long>("applicationId")?.let { id ->
            if (id > 0) {
                applicationId = id
                isEditMode = true
                loadApplication(id)
            }
        }
    }

    private fun loadApplication(id: Long) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            try {
                repository.getApplicationById(id)?.let { application ->
                    _uiState.update {
                        it.copy(
                            companyName = application.companyName,
                            position = application.position,
                            status = application.status,
                            applyDate = application.applyDate,
                            salary = application.salary,
                            location = application.location,
                            notes = application.notes,
                            isLoading = false
                        )
                    }
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        errorMessage = e.message
                    )
                }
            }
        }
    }

    fun updateCompanyName(name: String) {
        _uiState.update { it.copy(companyName = name) }
    }

    fun updatePosition(position: String) {
        _uiState.update { it.copy(position = position) }
    }

    fun updateStatus(status: ApplicationStatus) {
        _uiState.update { it.copy(status = status) }
    }

    fun updateApplyDate(date: Long) {
        _uiState.update { it.copy(applyDate = date) }
    }

    fun updateSalary(salary: String) {
        _uiState.update { it.copy(salary = salary) }
    }

    fun updateLocation(location: String) {
        _uiState.update { it.copy(location = location) }
    }

    fun updateNotes(notes: String) {
        _uiState.update { it.copy(notes = notes) }
    }

    fun saveApplication() {
        val currentState = _uiState.value
        
        // 验证
        if (currentState.companyName.isBlank()) {
            _uiState.update { it.copy(errorMessage = "请输入公司名称") }
            return
        }
        if (currentState.position.isBlank()) {
            _uiState.update { it.copy(errorMessage = "请输入职位名称") }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            try {
                val application = JobApplication(
                    id = applicationId,
                    companyName = currentState.companyName.trim(),
                    position = currentState.position.trim(),
                    status = currentState.status,
                    applyDate = currentState.applyDate,
                    salary = currentState.salary.trim(),
                    location = currentState.location.trim(),
                    notes = currentState.notes.trim()
                )

                if (isEditMode) {
                    repository.update(application)
                } else {
                    repository.insert(application)
                }

                _uiState.update { 
                    it.copy(
                        isLoading = false,
                        isSaved = true
                    )
                }
            } catch (e: Exception) {
                _uiState.update { 
                    it.copy(
                        isLoading = false,
                        errorMessage = e.message
                    )
                }
            }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(errorMessage = null) }
    }
}
