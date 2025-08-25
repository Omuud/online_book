package com.example.notetakingapp;

import android.app.AlertDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import java.util.ArrayList;
import java.util.List;

public class NoteListFragment extends Fragment implements NoteAdapter.OnNoteClickListener, NoteAdapter.OnNoteDeleteListener {
    
    private RecyclerView recyclerView;
    private NoteAdapter adapter;
    private List<Note> notes;
    private OnNoteActionListener actionListener;

    public interface OnNoteActionListener {
        void onAddNote();
        void onEditNote(Note note);
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        notes = new ArrayList<>();
        // Add some sample notes
        notes.add(new Note("Welcome", "Welcome to your Note Taking App! Click the + button to add your first note."));
        notes.add(new Note("Sample Note", "This is a sample note to get you started. Tap on any note to edit it."));
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_note_list, container, false);
        
        recyclerView = view.findViewById(R.id.notes_recycler_view);
        FloatingActionButton addButton = view.findViewById(R.id.add_note_button);
        
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        adapter = new NoteAdapter(notes, this, this);
        recyclerView.setAdapter(adapter);
        
        addButton.setOnClickListener(v -> {
            if (actionListener != null) {
                actionListener.onAddNote();
            }
        });
        
        return view;
    }

    @Override
    public void onNoteClick(Note note) {
        if (actionListener != null) {
            actionListener.onEditNote(note);
        }
    }

    @Override
    public void onNoteDelete(Note note) {
        new AlertDialog.Builder(requireContext())
                .setTitle("Delete Note")
                .setMessage("Are you sure you want to delete this note?")
                .setPositiveButton("Delete", (dialog, which) -> {
                    notes.remove(note);
                    adapter.notifyDataSetChanged();
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    public void addNote(Note note) {
        notes.add(0, note);
        adapter.notifyItemInserted(0);
        recyclerView.scrollToPosition(0);
    }

    public void updateNote(Note updatedNote) {
        for (int i = 0; i < notes.size(); i++) {
            if (notes.get(i).getId() == updatedNote.getId()) {
                notes.set(i, updatedNote);
                adapter.notifyItemChanged(i);
                break;
            }
        }
    }

    public void setOnNoteActionListener(OnNoteActionListener listener) {
        this.actionListener = listener;
    }
}