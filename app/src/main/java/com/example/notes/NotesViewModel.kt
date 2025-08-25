package com.example.notes

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.notes.model.Note

class NotesViewModel : ViewModel() {
    private val _notes = MutableLiveData<List<Note>>(emptyList())
    val notes: LiveData<List<Note>> = _notes

    private var nextId: Long = 1L

    fun addNote(title: String, content: String) {
        val note = Note(id = nextId++, title = title, content = content)
        _notes.value = _notes.value?.plus(note)
    }

    fun updateNote(id: Long, title: String, content: String) {
        _notes.value = _notes.value?.map { existing ->
            if (existing.id == id) existing.copy(title = title, content = content) else existing
        }
    }

    fun deleteNote(id: Long) {
        _notes.value = _notes.value?.filterNot { it.id == id }
    }

    fun getNoteById(id: Long): Note? {
        return _notes.value?.firstOrNull { it.id == id }
    }
}

