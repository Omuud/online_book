# Note Taking App

A simple Android note-taking application that demonstrates the use of Fragments for UI modularity and RecyclerView for displaying lists of data.

## Features

### 1. Note Creation
- Users can add new notes by clicking the "+" floating action button
- Each note has a title and content/body
- After creating a note, it appears at the top of the list

### 2. Note List
- Main screen displays all created notes using RecyclerView
- Each note item shows the title and a preview of the content (first 50 characters)
- Notes are displayed in Material Design cards with elevation

### 3. Note Editing
- Tap on any note from the list to edit it
- Editing is done in a separate fragment
- Changes are immediately reflected in the note list
- Form validation ensures title and content are not empty

### 4. Note Deletion
- Each note has a delete button (trash icon)
- Clicking delete shows a confirmation dialog
- Notes are permanently removed after confirmation

## Technical Implementation

### Architecture
- **MainActivity**: Manages fragment transactions and navigation
- **NoteListFragment**: Displays the list of notes using RecyclerView
- **NoteEditFragment**: Handles note creation and editing
- **NoteAdapter**: Manages the RecyclerView data binding
- **Note**: Data model class for notes

### Key Components
- **Fragments**: Used for UI modularity and better user experience
- **RecyclerView**: Efficiently displays the list of notes
- **Material Design**: Modern UI components and styling
- **Fragment Transactions**: Smooth navigation between screens

### Dependencies
- AndroidX AppCompat
- Material Design Components
- RecyclerView
- Fragment support

## Building and Running

### Prerequisites
- Android Studio (latest version recommended)
- Android SDK (API level 24 or higher)
- Java 8 or higher

### Steps to Build
1. Open the project in Android Studio
2. Sync Gradle files
3. Build the project (Build > Make Project)
4. Run on an emulator or physical device

### Alternative: Command Line
```bash
cd NoteTakingApp
./gradlew assembleDebug
```

## Project Structure

```
NoteTakingApp/
├── app/
│   └── src/
│       └── main/
│           ├── java/
│           │   └── com/example/notetakingapp/
│           │       ├── MainActivity.java
│           │       ├── Note.java
│           │       ├── NoteAdapter.java
│           │       ├── NoteListFragment.java
│           │       └── NoteEditFragment.java
│           ├── res/
│           │   ├── layout/
│           │   │   ├── activity_main.xml
│           │   │   ├── fragment_note_list.xml
│           │   │   ├── fragment_note_edit.xml
│           │   │   └── note_item.xml
│           │   └── values/
│           │       ├── strings.xml
│           │       ├── colors.xml
│           │       └── themes.xml
│           └── AndroidManifest.xml
├── build.gradle
├── app/build.gradle
├── settings.gradle
└── gradle.properties
```

## Usage Instructions

1. **Launch the app**: The main screen shows a list of sample notes
2. **Add a new note**: Tap the "+" button to create a new note
3. **Edit a note**: Tap on any existing note to edit its title and content
4. **Delete a note**: Tap the trash icon on any note and confirm deletion
5. **Navigate back**: Use the back button to return to the note list

## Sample Data

The app comes with two sample notes to get you started:
- "Welcome" - Introduction to the app
- "Sample Note" - Example note content

## Future Enhancements

Potential improvements that could be added:
- Data persistence using SQLite or Room database
- Search functionality
- Note categories/tags
- Rich text formatting
- Image attachments
- Cloud synchronization
- Dark theme support

## License

This project is created for educational purposes to demonstrate Android development concepts including Fragments and RecyclerView.