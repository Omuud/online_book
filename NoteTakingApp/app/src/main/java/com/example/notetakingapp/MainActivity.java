package com.example.notetakingapp;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

public class MainActivity extends AppCompatActivity implements 
        NoteListFragment.OnNoteActionListener, 
        NoteEditFragment.OnNoteSaveListener {
    
    private NoteListFragment noteListFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        if (savedInstanceState == null) {
            noteListFragment = new NoteListFragment();
            noteListFragment.setOnNoteActionListener(this);
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.fragment_container, noteListFragment)
                    .commit();
        }
    }

    @Override
    public void onAddNote() {
        NoteEditFragment editFragment = NoteEditFragment.newInstance();
        editFragment.setOnNoteSaveListener(this);
        
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.fragment_container, editFragment)
                .addToBackStack(null)
                .commit();
    }

    @Override
    public void onEditNote(Note note) {
        NoteEditFragment editFragment = NoteEditFragment.newInstance(note);
        editFragment.setOnNoteSaveListener(this);
        
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.fragment_container, editFragment)
                .addToBackStack(null)
                .commit();
    }

    @Override
    public void onNoteSaved(Note note, boolean isNewNote) {
        if (isNewNote) {
            noteListFragment.addNote(note);
        } else {
            noteListFragment.updateNote(note);
        }
        
        getSupportFragmentManager().popBackStack();
    }

    @Override
    public void onBackPressed() {
        FragmentManager fragmentManager = getSupportFragmentManager();
        if (fragmentManager.getBackStackEntryCount() > 0) {
            fragmentManager.popBackStack();
        } else {
            super.onBackPressed();
        }
    }
}