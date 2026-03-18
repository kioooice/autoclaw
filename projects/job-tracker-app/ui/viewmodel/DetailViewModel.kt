package com.example.jobtracker.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.jobtracker.data.model.JobApplication
import com.example.jobtracker.data.repository.JobApplicationRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class DetailUiState(
    val application: JobApplication? = null,
    val isLoading: Boolean = false,
    val isDeleted: Boolean = false,
    val errorMessage: String? = null
)

@HiltViewModel
class DetailViewModel @Inject constructor(
    private val repository: JobApplicationRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(DetailUiState())
    val uiState: StateFlow<DetailUiState> = _uiState.asStateFlow()

    fun loadApplication(id: Long) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            try {
                val application = repository.getApplicationById(id)
                _uiState.update {
                    it.copy(
                        application = application,
                        isLoading = false
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

    fun deleteApplication() {
        val application = _uiState.value.application ?: return
        
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            try {
                repository.delete(application)
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        isDeleted = true
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