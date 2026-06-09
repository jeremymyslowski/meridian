package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	_ "github.com/lib/pq"
)

type AssignmentEvent struct {
	ID         string
	TaskID     string
	AssigneeID string
	AssignedBy string
}

func main() {
	dbURL := envOrDefault("DATABASE_URL", "postgresql://meridian:meridian@localhost:5432/meridian")
	intervalSec, _ := strconv.Atoi(envOrDefault("WORKER_POLL_INTERVAL_SECONDS", "5"))

	db, err := sql.Open("postgres", dbURL)
	if err != nil {
		log.Fatalf("failed to connect to database: %v", err)
	}
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Fatalf("database ping failed: %v", err)
	}

	log.Printf("Meridian worker started (poll interval: %ds)", intervalSec)

	ticker := time.NewTicker(time.Duration(intervalSec) * time.Second)
	defer ticker.Stop()

	for {
		if err := processEvents(db); err != nil {
			log.Printf("error processing events: %v", err)
		}
		<-ticker.C
	}
}

func processEvents(db *sql.DB) error {
	events, err := fetchUnprocessedEvents(db)
	if err != nil {
		return err
	}

	for _, event := range events {
		if err := handleAssignment(db, event); err != nil {
			log.Printf("failed to handle event %s: %v", event.ID, err)
			continue
		}
		if err := markProcessed(db, event.ID); err != nil {
			return err
		}
		log.Printf("processed assignment event %s for task %s", event.ID, event.TaskID)
	}

	return nil
}

func fetchUnprocessedEvents(db *sql.DB) ([]AssignmentEvent, error) {
	rows, err := db.Query(`
		SELECT id, task_id, assignee_id, assigned_by
		FROM task_assignment_events
		WHERE processed = FALSE
		ORDER BY created_at ASC
		LIMIT 10
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []AssignmentEvent
	for rows.Next() {
		var e AssignmentEvent
		if err := rows.Scan(&e.ID, &e.TaskID, &e.AssigneeID, &e.AssignedBy); err != nil {
			return nil, err
		}
		events = append(events, e)
	}
	return events, rows.Err()
}

func handleAssignment(db *sql.DB, event AssignmentEvent) error {
	var taskTitle string
	err := db.QueryRow("SELECT title FROM tasks WHERE id = $1", event.TaskID).Scan(&taskTitle)
	if err != nil {
		return fmt.Errorf("fetch task title: %w", err)
	}

	_, err = db.Exec(`
		INSERT INTO notifications (user_id, type, title, body, metadata)
		VALUES ($1, 'task_assigned', $2, $3, $4)
	`,
		event.AssigneeID,
		fmt.Sprintf("Task assigned: %s", taskTitle),
		"You have been assigned a new task.",
		fmt.Sprintf(`{"task_id": "%s", "assigned_by": "%s"}`, event.TaskID, event.AssignedBy),
	)
	return err
}

func markProcessed(db *sql.DB, eventID string) error {
	_, err := db.Exec("UPDATE task_assignment_events SET processed = TRUE WHERE id = $1", eventID)
	return err
}

func envOrDefault(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}