package com.example.jobtracker.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.jobtracker.data.model.ApplicationStatus
import com.example.jobtracker.data.model.JobApplication
import com.example.jobtracker.data.repository.JobApplicationRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class HomeUiState(
    val applications: List<JobApplication> = emptyList(),
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
    val totalCount: Int = 0,
    val offerCount: Int = 0,
    val interviewCount: Int = 0,
    val rejectedCount: Int = 0
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val repository: JobApplicationRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadApplications()
        loadStatistics()
    }

    private fun loadApplications() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            repository.getAllApplications()
                .catch { exception ->
                    _uiState.update { 
                        it.copy(
                            isLoading = false,
                            errorMessage = exception.message
                        )
                    }
                }
                .collect { applications ->
                    _uiState.update { 
                        it.copy(
                            applications = applications,
                            isLoading = false
                        )
                    }
                }
        }
    }

    private fun loadStatistics() {
        viewModelScope.launch {
            combine(
                repository.getTotalCount(),
                repository.getCountByStatus(ApplicationStatus.OFFER),
                repository.getCountByStatus(ApplicationStatus.INTERVIEW),
                repository.getCountByStatus(ApplicationStatus.REJECTED)
            ) { total, offer, interview, rejected ->
                HomeUiState(
                    totalCount = total,
                    offerCount = offer,
                    interviewCount = interview,
                    rejectedCount = rejected
                )
            }.collect { stats ->
                _uiState.update { currentState ->
                    currentState.copy(
                        totalCount = stats.totalCount,
                        offerCount = stats.offerCount,
                        interviewCount = stats.interviewCount,
                        rejectedCount = stats.rejectedCount
                    )
                }
            }
        }
    }

    fun deleteApplication(id: Long) {
        viewModelScope.launch {
            try {
                repository.deleteById(id)
            } catch (e: Exception) {
                _uiState.update { 
                    it.copy(errorMessage = e.message)
                }
            }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(errorMessage = null) }
    }
}
