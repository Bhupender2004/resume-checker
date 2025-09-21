# 🚀 Resume Hackathon - AI-Powered Resume Screening Platform

## 📋 Overview

Resume Hackathon is a comprehensive AI-powered resume screening platform that helps recruiters and HR professionals efficiently evaluate resumes against job descriptions. The platform features advanced authentication, real-time analytics, and intelligent matching algorithms.

## ✨ Features

### 🔐 Authentication System
- **User Registration & Login**: Secure account creation and authentication
- **Session Management**: Persistent login sessions with secure token handling
- **User Profiles**: Personal dashboards with customizable preferences
- **Multi-User Support**: Isolated data for each user with role-based access

### 🎯 Resume Processing
- **AI-Powered Analysis**: Advanced algorithms for resume-job description matching
- **Skill Extraction**: Automatic identification of technical and soft skills
- **Scoring System**: Comprehensive evaluation with detailed feedback
- **Fast Mode**: Optimized processing for quick results
- **Batch Processing**: Handle multiple resumes simultaneously

### 📊 Analytics & Reporting
- **Personal Dashboard**: User-specific metrics and performance tracking
- **Processing History**: Complete audit trail of all evaluations
- **Performance Trends**: Visual analytics and improvement insights
- **Export Capabilities**: Download results in multiple formats

### 🎨 User Experience
- **Modern Interface**: Professional design with responsive layout
- **Multiple Themes**: Light and dark mode support
- **Real-time Feedback**: Instant processing status and results
- **Mobile Friendly**: Optimized for all device sizes

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core application logic
- **Streamlit**: Web application framework
- **Supabase**: Database and authentication backend
- **PostgreSQL**: Relational database for data persistence

### AI/ML
- **spaCy**: Natural language processing
- **NLTK**: Text processing and analysis
- **Sentence Transformers**: Semantic similarity matching
- **OpenAI API**: Enhanced feedback generation
- **FAISS**: Vector similarity search

### Security
- **bcrypt**: Password hashing
- **JWT**: Token-based authentication
- **Row Level Security**: Database-level access control
- **Input Validation**: Comprehensive data sanitization

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Supabase account
- Git

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd resumehackathon
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

4. **Set up database**:
- Go to your Supabase project dashboard
- Open SQL Editor
- Run the SQL from `supabase_setup.sql`

5. **Run the application**:
```bash
streamlit run main_app.py --server.port 8506
```

6. **Access the application**:
- Open http://localhost:8506
- Create your account and start processing resumes

## 📁 Project Structure

```
resumehackathon/
├── main_app.py              # Main authenticated application
├── auth.py                  # Authentication module
├── clean_app.py             # Enhanced resume processing app
├── app.py                   # Original simple app
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration
├── supabase_setup.sql       # Database schema
├── script/                  # Core processing modules
│   ├── pipeline.py          # Main processing pipeline
│   ├── parse_resume.py      # Resume text extraction
│   ├── parse_jd.py          # Job description parsing
│   ├── semantic_match.py    # AI matching algorithms
│   ├── hard_match.py        # Keyword matching
│   ├── final_score.py       # Scoring calculations
│   └── feedback.py          # Feedback generation
└── data/                    # Sample data and uploads
    ├── resumes/             # Sample resume files
    └── jds/                 # Sample job descriptions
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
DATABASE_URL=your_postgresql_connection_string

# Application Settings
APP_NAME=Resume Hackathon
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=your_secret_key_32_chars_minimum

# Optional: OpenAI API Key for enhanced feedback
OPENAI_API_KEY=your_openai_api_key
```

### Database Setup

1. Create a Supabase project at https://supabase.com
2. Copy your project URL and API keys
3. Run the SQL setup script in Supabase SQL Editor:
   - Copy content from `supabase_setup.sql`
   - Paste and execute in SQL Editor
4. Verify tables are created: users, resume_evaluations, user_preferences, user_sessions

## 🎯 Usage

### For Recruiters

1. **Create Account**: Register with your email and secure password
2. **Upload Resume**: Select candidate's resume file (PDF, DOCX, TXT)
3. **Add Job Description**: Paste or upload the job requirements
4. **Process**: Click analyze to get AI-powered evaluation
5. **Review Results**: Get detailed scoring, skill gaps, and recommendations
6. **Track History**: Access all previous evaluations in your dashboard

### For HR Teams

1. **Multi-User Setup**: Each team member gets their own account
2. **Batch Processing**: Process multiple resumes for the same position
3. **Analytics**: Track hiring metrics and candidate quality trends
4. **Export Data**: Download results for reporting and record-keeping
5. **Collaboration**: Share insights and maintain evaluation standards

## 📊 Scoring System

### Evaluation Criteria
- **Skill Match**: Technical and soft skills alignment (40%)
- **Experience Level**: Years and relevance of experience (30%)
- **Education**: Degree requirements and certifications (20%)
- **Keywords**: Job-specific terminology and requirements (10%)

### Score Ranges
- **90-100%**: Excellent match - Highly recommended
- **80-89%**: Good match - Recommended with minor gaps
- **70-79%**: Fair match - Consider with reservations
- **60-69%**: Poor match - Significant skill gaps
- **Below 60%**: Not recommended - Major misalignment

## 🔒 Security

### Data Protection
- **Encryption**: All sensitive data encrypted at rest and in transit
- **Access Control**: Row-level security ensures data isolation
- **Authentication**: Secure password hashing with bcrypt
- **Session Management**: JWT tokens with expiration handling

### Privacy
- **User Data**: Each user can only access their own data
- **File Handling**: Uploaded files processed securely and not permanently stored
- **Audit Trail**: Complete logging of all user actions
- **GDPR Compliance**: User data deletion and export capabilities

## 🚀 Deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] Database tables created and secured
- [ ] SSL certificate installed
- [ ] Domain name configured
- [ ] Backup strategy implemented
- [ ] Monitoring and logging setup
- [ ] Load testing completed
- [ ] Security audit performed

### Deployment Options
1. **Streamlit Cloud**: Easy deployment with GitHub integration
2. **Heroku**: Platform-as-a-Service with PostgreSQL add-on
3. **AWS/GCP/Azure**: Full cloud deployment with container orchestration
4. **Docker**: Containerized deployment for any platform

## 📈 Performance

### Optimization Features
- **Fast Mode**: Quick processing for time-sensitive evaluations
- **Caching**: Intelligent caching of processed data
- **Async Processing**: Non-blocking operations for better UX
- **Database Indexing**: Optimized queries for large datasets

### Scalability
- **Multi-User**: Supports thousands of concurrent users
- **Database**: PostgreSQL with connection pooling
- **Horizontal Scaling**: Stateless design for easy scaling
- **CDN Ready**: Static assets can be served from CDN

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Documentation
- **Setup Guide**: `SUPABASE_SETUP_GUIDE.md`
- **Authentication**: `AUTHENTICATION_IMPLEMENTATION.md`
- **Deployment**: `DEPLOYMENT_READINESS_REPORT.md`

### Contact
- **Issues**: Create a GitHub issue for bugs or feature requests
- **Email**: [Your contact email]
- **Documentation**: Check the docs/ folder for detailed guides

## 🎉 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **Supabase**: For the powerful backend-as-a-service
- **OpenAI**: For AI-powered feedback capabilities
- **spaCy**: For natural language processing
- **Contributors**: All the developers who made this possible

---

**🚀 Ready to revolutionize your hiring process? Get started with Resume Hackathon today!**
#   r e s u m e - c h e c k e r  
 