# 🚀 Board Invitation System Setup Guide

## 📋 **What You Need to Do**

### **1. Set Up Email Configuration**

Create a `.env` file in your backend directory with these variables:

```env
# Email Configuration
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:3000
```

### **2. Get Gmail App Password**

1. **Go to your Google Account settings**
2. **Enable 2-Factor Authentication** (if not already enabled)
3. **Go to Security → App passwords**
4. **Generate a new app password** for "Mail"
5. **Use this password** as `EMAIL_PASSWORD` in your `.env` file

### **3. Install Dependencies**

```bash
pip install python-dotenv email-validator
```

### **4. Run Database Migration**

```bash
python migrations/add_invitation_tables.py
```

### **5. Test Email Configuration**

```bash
python test_email.py
```

## 🔧 **Troubleshooting**

### **Email Not Sending?**

1. **Check your `.env` file** - Make sure EMAIL_USERNAME and EMAIL_PASSWORD are set
2. **Use App Password** - Don't use your regular Gmail password
3. **Check Gmail settings** - Make sure "Less secure app access" is enabled (or use App Password)
4. **Check firewall** - Make sure port 587 is not blocked

### **Database Issues?**

1. **Run the migration script** to create new tables
2. **Check database permissions** - Make sure the database is writable
3. **Check SQLite file** - Make sure `task_manager.db` exists

### **API Not Working?**

1. **Check if the server is running** - `uvicorn app.main:app --reload`
2. **Check the logs** - Look for error messages
3. **Check CORS settings** - Make sure frontend URL is allowed

## 📧 **Email Configuration Examples**

### **Gmail Configuration**
```env
EMAIL_USERNAME=yourname@gmail.com
EMAIL_PASSWORD=your-16-character-app-password
```

### **Outlook Configuration**
```env
EMAIL_USERNAME=yourname@outlook.com
EMAIL_PASSWORD=your-password
```

### **Custom SMTP**
```env
EMAIL_USERNAME=yourname@yourdomain.com
EMAIL_PASSWORD=your-password
```

## 🧪 **Testing the System**

### **1. Test Email Sending**
```bash
python test_email.py
```

### **2. Test API Endpoints**
```bash
# Send invitation
curl -X POST "http://localhost:8000/invitations/send" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"board_id": 1, "invitee_email": "test@example.com", "role": "member"}'
```

### **3. Test Frontend Integration**
1. **Open your frontend** at `http://localhost:3000`
2. **Login to your account**
3. **Go to a board**
4. **Click the Share button**
5. **Enter an email and send invitation**

## 🎯 **Expected Flow**

1. **User clicks Share** → Opens invitation modal
2. **User enters email** → Calls `/invitations/send` API
3. **Backend sends email** → User receives invitation email
4. **User clicks link** → Goes to invitation page
5. **User accepts** → Calls `/invitations/accept` API
6. **User added to board** → Can now access the board

## 🚨 **Common Issues**

### **"Email sending failed"**
- Check EMAIL_USERNAME and EMAIL_PASSWORD
- Use App Password, not regular password
- Check Gmail security settings

### **"Database error"**
- Run the migration script
- Check database file permissions
- Check SQLite installation

### **"CORS error"**
- Check CORS settings in main.py
- Make sure frontend URL is in allowed origins

### **"Token invalid"**
- Check if user is logged in
- Check JWT token expiration
- Check authentication middleware

## 📞 **Need Help?**

If you're still having issues:

1. **Check the logs** in your terminal
2. **Test email configuration** with the test script
3. **Verify database tables** are created
4. **Check API endpoints** with curl or Postman

The system should work once you have the email configuration set up correctly! 🎉
