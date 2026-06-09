package main

import "testing"

func TestEnvOrDefault(t *testing.T) {
	if got := envOrDefault("NONEXISTENT_VAR_XYZ", "fallback"); got != "fallback" {
		t.Errorf("expected fallback, got %s", got)
	}
}