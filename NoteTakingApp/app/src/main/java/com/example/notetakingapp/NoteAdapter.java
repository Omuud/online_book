package com.example.notetakingapp;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.List;

public class NoteAdapter extends RecyclerView.Adapter<NoteAdapter.NoteViewHolder> {
    
    private List<Note> notes;
    private OnNoteClickListener listener;
    private OnNoteDeleteListener deleteListener;

    public interface OnNoteClickListener {
        void onNoteClick(Note note);
    }

    public interface OnNoteDeleteListener {
        void onNoteDelete(Note note);
    }

    public NoteAdapter(List<Note> notes, OnNoteClickListener listener, OnNoteDeleteListener deleteListener) {
        this.notes = notes;
        this.listener = listener;
        this.deleteListener = deleteListener;
    }

    @NonNull
    @Override
    public NoteViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.note_item, parent, false);
        return new NoteViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull NoteViewHolder holder, int position) {
        Note note = notes.get(position);
        holder.bind(note);
    }

    @Override
    public int getItemCount() {
        return notes.size();
    }

    public void updateNotes(List<Note> newNotes) {
        this.notes = newNotes;
        notifyDataSetChanged();
    }

    class NoteViewHolder extends RecyclerView.ViewHolder {
        private TextView titleTextView;
        private TextView contentPreviewTextView;
        private ImageButton deleteButton;

        public NoteViewHolder(@NonNull View itemView) {
            super(itemView);
            titleTextView = itemView.findViewById(R.id.note_title);
            contentPreviewTextView = itemView.findViewById(R.id.note_content_preview);
            deleteButton = itemView.findViewById(R.id.delete_button);

            itemView.setOnClickListener(v -> {
                int position = getAdapterPosition();
                if (position != RecyclerView.NO_POSITION && listener != null) {
                    listener.onNoteClick(notes.get(position));
                }
            });

            deleteButton.setOnClickListener(v -> {
                int position = getAdapterPosition();
                if (position != RecyclerView.NO_POSITION && deleteListener != null) {
                    deleteListener.onNoteDelete(notes.get(position));
                }
            });
        }

        public void bind(Note note) {
            titleTextView.setText(note.getTitle());
            String content = note.getContent();
            if (content.length() > 50) {
                content = content.substring(0, 50) + "...";
            }
            contentPreviewTextView.setText(content);
        }
    }
}