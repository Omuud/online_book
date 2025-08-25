package com.example.notes

import android.app.AlertDialog
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.fragment.app.commit
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.notes.databinding.FragmentNoteListBinding
import com.example.notes.model.Note

class NoteListFragment : Fragment() {
    private var _binding: FragmentNoteListBinding? = null
    private val binding get() = _binding!!

    private val viewModel: NotesViewModel by activityViewModels()
    private lateinit var adapter: NotesAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentNoteListBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupRecyclerView()
        setupFab()
        observeNotes()
    }

    private fun setupRecyclerView() {
        adapter = NotesAdapter(
            onClick = { note -> openEditor(note) },
            onDelete = { note -> confirmDelete(note) }
        )
        binding.recyclerView.layoutManager = LinearLayoutManager(requireContext())
        binding.recyclerView.adapter = adapter
    }

    private fun setupFab() {
        binding.fab.setOnClickListener {
            openEditor(null)
        }
    }

    private fun observeNotes() {
        viewModel.notes.observe(viewLifecycleOwner) { notes ->
            adapter.submitList(notes)
        }
    }

    private fun openEditor(note: Note?) {
        parentFragmentManager.commit {
            replace(R.id.fragment_container, EditNoteFragment.newInstance(note?.id))
            addToBackStack(null)
        }
    }

    private fun confirmDelete(note: Note) {
        AlertDialog.Builder(requireContext())
            .setTitle(R.string.delete_note_title)
            .setMessage(R.string.delete_note_message)
            .setPositiveButton(R.string.delete_note_confirm) { _, _ ->
                viewModel.deleteNote(note.id)
            }
            .setNegativeButton(R.string.delete_note_cancel, null)
            .show()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        fun newInstance() = NoteListFragment()
    }
}

