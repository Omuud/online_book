package com.example.notes

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.os.bundleOf
import androidx.core.widget.doAfterTextChanged
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import com.example.notes.databinding.FragmentEditNoteBinding

class EditNoteFragment : Fragment() {
    private var _binding: FragmentEditNoteBinding? = null
    private val binding get() = _binding!!

    private val viewModel: NotesViewModel by activityViewModels()

    private var noteId: Long? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        noteId = arguments?.getLong(ARG_NOTE_ID)
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentEditNoteBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        noteId?.let { id ->
            viewModel.getNoteById(id)?.let { note ->
                binding.titleEdit.setText(note.title)
                binding.contentEdit.setText(note.content)
            }
        }

        binding.saveButton.setOnClickListener {
            val title = binding.titleEdit.text?.toString()?.trim().orEmpty()
            val content = binding.contentEdit.text?.toString()?.trim().orEmpty()
            val id = noteId
            if (id == null) {
                viewModel.addNote(title, content)
            } else {
                viewModel.updateNote(id, title, content)
            }
            parentFragmentManager.popBackStack()
        }

        binding.cancelButton.setOnClickListener {
            parentFragmentManager.popBackStack()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        private const val ARG_NOTE_ID = "note_id"
        fun newInstance(noteId: Long?): EditNoteFragment {
            val fragment = EditNoteFragment()
            if (noteId != null) {
                fragment.arguments = bundleOf(ARG_NOTE_ID to noteId)
            }
            return fragment
        }
    }
}

