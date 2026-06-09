// DECOY — prototype Go user package. Production worker does not import this.
package user

import "fmt"

type User struct {
	ID    string
	Email string
	Name  string
}

func FindByID(id string) (*User, error) {
	return nil, fmt.Errorf("qa-fixtures decoy: use apps/api meridian_api/services/user_service.py")
}