package com.example.notetakingapp;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class NoteEditFragment extends Fragment {
    
    private EditText titleEditText;
    private EditText contentEditText;
    private Button saveButton;
    private Button cancelButton;
    private Note note;
    private boolean isEditMode;
    private OnNoteSaveListener saveListener;

    public interface OnNoteSaveListener {
        void onNoteSaved(Note note, boolean isNewNote);
    }

    public static NoteEditFragment newInstance() {
        return new NoteEditFragment();
    }

    public static NoteEditFragment newInstance(Note note) {
        NoteEditFragment fragment = new NoteEditFragment();
        fragment.note = note;
        fragment.isEditMode = true;
        return fragment;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_note_edit, container, false);
        
        titleEditText = view.findViewById(R.id.title_edit_text);
        contentEditText = view.findViewById(R.id.content_edit_text);
        saveButton = view.findViewById(R.id.save_button);
        cancelButton = view.findViewById(R.id.cancel_button);
        
        if (isEditMode && note != null) {
            titleEditText.setText(note.getTitle());
            contentEditText.setText(note.getContent());
        }
        
        saveButton.setOnClickListener(v -> saveNote());
        cancelButton.setOnClickListener(v -> {
            if (getActivity() != null) {
                getActivity().onBackPressed();
            }
        });
        
        return view;
    }

    private void saveNote() {
        String title = titleEditText.getText().toString().trim();
        String content = contentEditText.getText().toString().trim();
        
        if (title.isEmpty()) {
            titleEditText.setError("Title is required");
            return;
        }
        
        if (content.isEmpty()) {
            contentEditText.setError("Content is required");
            return;
        }
        
        if (isEditMode && note != null) {
            note.setTitle(title);
            note.setContent(content);
            note.setTimestamp(new java.util.Date());
        } else {
            note = new Note(title, content);
        }
        
        if (saveListener != null) {
            saveListener.onNoteSaved(note, !isEditMode);
        }
    }

    public void setOnNoteSaveListener(OnNoteSaveListener listener) {
        this.saveListener = listener;
    }
}