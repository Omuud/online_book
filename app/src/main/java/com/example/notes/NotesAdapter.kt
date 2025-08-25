package com.example.notes

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.notes.databinding.ItemNoteBinding
import com.example.notes.model.Note

class NotesAdapter(
    private val onClick: (Note) -> Unit,
    private val onDelete: (Note) -> Unit
) : ListAdapter<Note, NotesAdapter.NoteViewHolder>(Diff) {

    object Diff : DiffUtil.ItemCallback<Note>() {
        override fun areItemsTheSame(oldItem: Note, newItem: Note): Boolean = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: Note, newItem: Note): Boolean = oldItem == newItem
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): NoteViewHolder {
        val binding = ItemNoteBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return NoteViewHolder(binding)
    }

    override fun onBindViewHolder(holder: NoteViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class NoteViewHolder(private val binding: ItemNoteBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(note: Note) {
            binding.title.text = note.title.ifBlank { "(No title)" }
            val snippet = note.content.take(80)
            binding.content.text = snippet

            binding.root.setOnClickListener { onClick(note) }
            binding.deleteButton.setOnClickListener { onDelete(note) }
        }
    }
}

