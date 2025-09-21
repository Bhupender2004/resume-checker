# 🚀 Supabase Authentication Setup Guide

## 📋 **Complete Setup Instructions**

### **Step 1: Create Supabase Project**

1. **Go to Supabase**: Visit [https://supabase.com](https://supabase.com)
2. **Sign Up/Login**: Create account or login
3. **Create New Project**:
   - Click "New Project"
   - Choose organization
   - Enter project name: "Resume Hackathon"
   - Enter database password (save this!)
   - Select region closest to you
   - Click "Create new project"

### **Step 2: Get Project Credentials**

1. **Go to Project Settings**:
   - Click on your project
   - Go to Settings → API
   
2. **Copy These Values**:
   ```
   Project URL: https://your-project-id.supabase.co
   Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   Service Role Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### **Step 3: Setup Database Schema**

1. **Go to SQL Editor**:
   - In your Supabase dashboard
   - Click "SQL Editor" in sidebar
   
2. **Run Setup Script**:
   - Copy the entire content from `supabase_setup.sql`
   - Paste into SQL Editor
   - Click "Run" to execute

### **Step 4: Configure Environment Variables**

1. **Create .env file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file** with your actual values:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your-actual-anon-key
   SUPABASE_SERVICE_KEY=your-actual-service-key
   ```

### **Step 5: Install Required Packages**

```bash
pip install supabase python-dotenv bcrypt pyjwt
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### **Step 6: Test Authentication**

1. **Run Main Application**:
   ```bash
   streamlit run main_app.py --server.port 8506
   ```

2. **Test Signup**:
   - Go to http://localhost:8506
   - Click "Sign Up" tab
   - Create test account
   - Verify account creation

3. **Test Login**:
   - Use created credentials
   - Verify successful login
   - Check user menu in sidebar

---

## 🔧 **Database Schema Overview**

### **Tables Created:**

1. **`users`** - User accounts
   - `id` (UUID, Primary Key)
   - `email` (Unique)
   - `password_hash`
   - `full_name`
   - `created_at`
   - `last_login`
   - `is_active`

2. **`resume_evaluations`** - Processing history
   - `id` (UUID, Primary Key)
   - `user_id` (Foreign Key)
   - `resume_name`
   - `job_description_name`
   - `total_score`
   - `verdict`
   - `missing_skills`
   - `feedback`
   - `processing_time`
   - `created_at`

3. **`user_preferences`** - User settings
   - `user_id` (Foreign Key)
   - `theme`
   - `fast_mode_default`
   - `email_notifications`

4. **`user_sessions`** - Session management
   - `user_id` (Foreign Key)
   - `session_token`
   - `expires_at`

---

## 🎯 **Authentication Features**

### **✅ Implemented Features:**

1. **User Registration**:
   - Email validation
   - Password strength requirements
   - Duplicate email prevention
   - Terms acceptance

2. **User Login**:
   - Email/password authentication
   - Session management
   - Last login tracking
   - Account status checking

3. **Security Features**:
   - Password hashing (SHA256)
   - Row Level Security (RLS)
   - Session token management
   - Input validation

4. **User Experience**:
   - Clean login/signup forms
   - Error handling with user feedback
   - Success messages
   - Automatic redirects

### **🔒 Security Measures:**

1. **Password Requirements**:
   - Minimum 8 characters
   - At least 1 uppercase letter
   - At least 1 lowercase letter
   - At least 1 number

2. **Database Security**:
   - Row Level Security enabled
   - Users can only access their own data
   - Secure password hashing
   - SQL injection prevention

3. **Session Management**:
   - Secure session tokens
   - Session expiration
   - Automatic logout on close

---

## 🌐 **Application Integration**

### **Updated Applications:**

1. **`main_app.py`** - Main authenticated app
   - Login/signup interface
   - User dashboard
   - Navigation between apps
   - User analytics

2. **`clean_app.py`** - Enhanced with auth
   - Authentication check
   - User menu in sidebar
   - User-specific data storage

3. **`app.py`** & **`streamlit_app.py`** - Ready for auth
   - Can be updated similarly
   - Will inherit user context

### **New Features Available:**

1. **User Dashboard**:
   - Personal analytics
   - Processing history
   - Performance metrics
   - Account management

2. **Data Persistence**:
   - User-specific resume history
   - Saved job descriptions
   - Processing preferences
   - Performance tracking

3. **Multi-User Support**:
   - Isolated user data
   - Secure access control
   - Scalable architecture
   - Admin capabilities

---

## 🚀 **Getting Started**

### **Quick Start:**

1. **Setup Supabase** (Steps 1-3 above)
2. **Configure Environment** (Step 4)
3. **Install Packages** (Step 5)
4. **Run Application**:
   ```bash
   streamlit run main_app.py --server.port 8506
   ```
5. **Create Account** and start using!

### **Application URLs:**

- **Main Authenticated App**: http://localhost:8506
- **Clean App (with auth)**: http://localhost:8507
- **Original Apps**: http://localhost:8504, http://localhost:8505

### **Default Test Account:**
After setup, create your first account through the signup form.

---

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"Database connection failed"**:
   - Check SUPABASE_URL in .env
   - Verify project is active
   - Check internet connection

2. **"Authentication module not available"**:
   - Install required packages: `pip install supabase python-dotenv`
   - Check import statements
   - Verify .env file exists

3. **"Invalid email or password"**:
   - Check email format
   - Verify password meets requirements
   - Ensure account exists

4. **"User with this email already exists"**:
   - Use different email
   - Or try logging in instead
   - Check Supabase users table

### **Debug Steps:**

1. **Check Environment Variables**:
   ```python
   import os
   print(os.getenv('SUPABASE_URL'))
   print(os.getenv('SUPABASE_ANON_KEY'))
   ```

2. **Test Database Connection**:
   ```python
   from supabase import create_client
   supabase = create_client(url, key)
   result = supabase.table('users').select('*').limit(1).execute()
   print(result)
   ```

3. **Check Logs**:
   - Supabase Dashboard → Logs
   - Streamlit terminal output
   - Browser developer console

---

## 🎉 **Success Indicators**

### **✅ Setup Complete When:**

1. **Supabase Project**: Created and accessible
2. **Database Schema**: Tables created successfully
3. **Environment**: Variables configured correctly
4. **Packages**: All dependencies installed
5. **Authentication**: Login/signup working
6. **Applications**: Running with user context

### **✅ Ready to Use:**

- 🔐 **Secure user authentication**
- 👤 **User-specific data isolation**
- 📊 **Personal analytics dashboard**
- 🚀 **All resume processing features**
- 💾 **Persistent data storage**
- 🎯 **Professional user experience**

---

**🎯 Your Resume Hackathon application now has enterprise-grade authentication! 🎯**
