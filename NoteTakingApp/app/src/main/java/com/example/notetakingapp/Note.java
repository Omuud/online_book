package com.example.notetakingapp;

import java.util.Date;

public class Note {
    private String title;
    private String content;
    private Date timestamp;
    private long id;

    public Note(String title, String content) {
        this.title = title;
        this.content = content;
        this.timestamp = new Date();
        this.id = System.currentTimeMillis();
    }

    public Note(long id, String title, String content, Date timestamp) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.timestamp = timestamp;
    }

    // Getters and Setters
    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }
}