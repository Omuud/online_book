NotesApp (Simple Note-Taking Android App)

A minimal example app demonstrating Fragments, RecyclerView, and a shared ViewModel.

Features:
- Add a note with title and content (via FAB)
- List shows title and content snippet
- Tap a note to edit
- Delete with confirmation dialog

Requirements:
- Android Studio (AGP 8.5+, Kotlin 1.9)
- Android SDK 34

Getting Started:
1. Open Android Studio.
2. File > Open > select this folder.
3. Let Gradle sync finish.
4. Run the app configuration on an emulator or device (API 24+).

Project Structure:
- app/src/main/java/com/example/notes/
  - MainActivity.kt
  - NoteListFragment.kt
  - EditNoteFragment.kt
  - NotesViewModel.kt
  - model/Note.kt
- app/src/main/res/layout/
  - activity_main.xml, fragment_note_list.xml, fragment_edit_note.xml, item_note.xml

Notes:
- Data is in-memory only. Closing the app clears notes.
- Icons use Android system drawables for simplicity.

