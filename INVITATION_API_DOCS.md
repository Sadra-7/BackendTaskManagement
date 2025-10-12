# Board Invitation API Documentation

## Overview
This API provides functionality for inviting users to boards, managing board members, and handling invitation acceptance/decline.

## Base URL
```
http://localhost:8000/invitations
```

## Authentication
All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### 1. Send Invitation
**POST** `/invitations/send`

Send an invitation to join a board.

**Request Body:**
```json
{
  "board_id": 1,
  "invitee_email": "user@example.com",
  "role": "member"
}
```

**Response:**
```json
{
  "id": 1,
  "token": "uuid-token-here",
  "board_id": 1,
  "inviter_id": 2,
  "invitee_email": "user@example.com",
  "role": "member",
  "status": "pending",
  "expires_at": "2024-01-15T10:30:00",
  "created_at": "2024-01-08T10:30:00",
  "accepted_at": null
}
```

### 2. Accept Invitation
**POST** `/invitations/accept`

Accept a board invitation.

**Request Body:**
```json
{
  "token": "uuid-token-here"
}
```

**Response:**
```json
{
  "id": 1,
  "board_id": 1,
  "user_id": 3,
  "role": "member",
  "joined_at": "2024-01-08T10:30:00",
  "user": {
    "id": 3,
    "username": "newuser",
    "email": "user@example.com",
    "full_name": "New User"
  }
}
```

### 3. Decline Invitation
**POST** `/invitations/decline`

Decline a board invitation.

**Request Body:**
```json
{
  "token": "uuid-token-here"
}
```

**Response:**
```json
{
  "message": "Invitation declined successfully"
}
```

### 4. Get Board Invitations
**GET** `/invitations/board/{board_id}`

Get all invitations for a board.

**Response:**
```json
[
  {
    "id": 1,
    "token": "uuid-token-here",
    "board_id": 1,
    "inviter_id": 2,
    "invitee_email": "user@example.com",
    "role": "member",
    "status": "pending",
    "expires_at": "2024-01-15T10:30:00",
    "created_at": "2024-01-08T10:30:00",
    "accepted_at": null
  }
]
```

### 5. Cancel Invitation
**DELETE** `/invitations/{invitation_id}`

Cancel/delete an invitation.

**Response:**
```json
{
  "message": "Invitation cancelled successfully"
}
```

### 6. Get Board Members
**GET** `/invitations/board/{board_id}/members`

Get all members of a board.

**Response:**
```json
[
  {
    "id": 1,
    "board_id": 1,
    "user_id": 2,
    "role": "admin",
    "joined_at": "2024-01-08T10:30:00",
    "user": {
      "id": 2,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Admin User"
    }
  }
]
```

### 7. Remove Board Member
**DELETE** `/invitations/board/{board_id}/members/{user_id}`

Remove a member from a board.

**Response:**
```json
{
  "message": "Member removed successfully"
}
```

### 8. Update Member Role
**PUT** `/invitations/board/{board_id}/members/{user_id}/role`

Update a member's role in a board.

**Request Body:**
```json
{
  "new_role": "admin"
}
```

**Response:**
```json
{
  "message": "Member role updated successfully"
}
```

## Role Types
- `viewer`: Can view the board but cannot edit
- `member`: Can view and edit the board
- `admin`: Full access including board settings

## Status Types
- `pending`: Invitation sent, waiting for response
- `accepted`: Invitation accepted, user joined the board
- `declined`: Invitation declined by user
- `expired`: Invitation expired (7 days)

## Error Responses

### 400 Bad Request
```json
{
  "detail": "User is already a member of this board"
}
```

### 403 Forbidden
```json
{
  "detail": "You don't have permission to invite members to this board"
}
```

### 404 Not Found
```json
{
  "detail": "Board not found"
}
```

## Email Configuration

Add these environment variables to your `.env` file:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@taskmanager.com
FROM_NAME=Task Manager

# Frontend URL (for invitation links)
FRONTEND_URL=http://localhost:3000
```

## Frontend Integration

### 1. Send Invitation
```javascript
const sendInvitation = async (boardId, email, role) => {
  const response = await fetch('/api/invitations/send', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      board_id: boardId,
      invitee_email: email,
      role: role
    })
  });
  return response.json();
};
```

### 2. Accept Invitation
```javascript
const acceptInvitation = async (token) => {
  const response = await fetch('/api/invitations/accept', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ token })
  });
  return response.json();
};
```

## Database Schema

### board_invitations
- `id`: Primary key
- `token`: Unique invitation token
- `board_id`: Foreign key to boards table
- `inviter_id`: Foreign key to users table
- `invitee_email`: Email of invited user
- `role`: Member role (viewer/member/admin)
- `status`: Invitation status (pending/accepted/declined/expired)
- `expires_at`: Expiration timestamp
- `created_at`: Creation timestamp
- `accepted_at`: Acceptance timestamp

### board_members
- `id`: Primary key
- `board_id`: Foreign key to boards table
- `user_id`: Foreign key to users table
- `role`: Member role (viewer/member/admin)
- `joined_at`: Join timestamp

## Testing

Use the following curl commands to test the API:

```bash
# Send invitation
curl -X POST "http://localhost:8000/invitations/send" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"board_id": 1, "invitee_email": "user@example.com", "role": "member"}'

# Accept invitation
curl -X POST "http://localhost:8000/invitations/accept" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"token": "your-invitation-token"}'
```
