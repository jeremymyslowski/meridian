/**
 * DECOY — legacy frontend user service stub.
 * Production user logic lives in apps/api/meridian_api/services/user_service.py
 */

export interface User {
  id: string
  email: string
  name: string
}

export class UserService {
  async getUser(id: string): Promise<User | null> {
    console.warn('UserService.ts is a QA fixture decoy — not wired to the API')
    return null
  }

  async getUserByEmail(email: string): Promise<User | null> {
    return null
  }
}