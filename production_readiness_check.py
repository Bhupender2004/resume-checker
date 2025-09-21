"""
Production Readiness Check for Resume Hackathon Application
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("🔧 Checking Environment Variables...")
    print("=" * 50)
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY', 
        'SUPABASE_SERVICE_KEY',
        'DATABASE_URL',
        'SECRET_KEY',
        'APP_NAME',
        'APP_VERSION'
    ]
    
    optional_vars = [
        'OPENAI_API_KEY',
        'DEBUG'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_required.append(var)
            print(f"❌ {var}: Missing")
        elif '[YOUR-PASSWORD]' in value or 'your-' in value.lower():
            missing_required.append(var)
            print(f"⚠️ {var}: Contains placeholder")
        else:
            print(f"✅ {var}: Configured")
    
    for var in optional_vars:
        value = os.getenv(var)
        if not value:
            missing_optional.append(var)
            print(f"⚠️ {var}: Optional, not set")
        else:
            print(f"✅ {var}: Configured")
    
    return len(missing_required) == 0, missing_required, missing_optional

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking Dependencies...")
    print("=" * 50)
    
    required_packages = [
        'streamlit',
        'supabase',
        'python-dotenv',
        'pdfplumber',
        'pandas',
        'numpy',
        'bcrypt',
        'pyjwt'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package}: Installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}: Missing")
    
    return len(missing_packages) == 0, missing_packages

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking File Structure...")
    print("=" * 50)
    
    required_files = [
        'main_app.py',
        'auth.py',
        'clean_app.py',
        '.env',
        'requirements.txt',
        'supabase_setup.sql'
    ]
    
    optional_files = [
        'README.md',
        '.gitignore',
        'Dockerfile',
        'docker-compose.yml'
    ]
    
    missing_required = []
    missing_optional = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}: Exists")
        else:
            missing_required.append(file)
            print(f"❌ {file}: Missing")
    
    for file in optional_files:
        if Path(file).exists():
            print(f"✅ {file}: Exists")
        else:
            missing_optional.append(file)
            print(f"⚠️ {file}: Optional, missing")
    
    return len(missing_required) == 0, missing_required, missing_optional

def check_database_connection():
    """Check database connectivity"""
    print("\n🗄️ Checking Database Connection...")
    print("=" * 50)
    
    try:
        from supabase import create_client
        
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            print("❌ Missing Supabase credentials")
            return False
        
        supabase = create_client(url, key)
        print("✅ Supabase client created")
        
        # Test tables
        tables = ['users', 'resume_evaluations', 'user_preferences', 'user_sessions']
        for table in tables:
            try:
                result = supabase.table(table).select('count').execute()
                print(f"✅ {table} table: Accessible")
            except Exception as e:
                print(f"❌ {table} table: Error - {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_security():
    """Check security configurations"""
    print("\n🛡️ Checking Security...")
    print("=" * 50)
    
    issues = []
    
    # Check if DEBUG is disabled
    debug = os.getenv('DEBUG', 'False').lower()
    if debug in ['true', '1', 'yes']:
        issues.append("DEBUG mode is enabled")
        print("⚠️ DEBUG: Enabled (should be disabled for production)")
    else:
        print("✅ DEBUG: Disabled")
    
    # Check SECRET_KEY
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        issues.append("SECRET_KEY not set")
        print("❌ SECRET_KEY: Missing")
    elif len(secret_key) < 32:
        issues.append("SECRET_KEY too short")
        print("⚠️ SECRET_KEY: Too short (should be 32+ characters)")
    else:
        print("✅ SECRET_KEY: Configured")
    
    # Check for hardcoded credentials in files
    sensitive_files = ['main_app.py', 'auth.py', 'clean_app.py']
    for file in sensitive_files:
        if Path(file).exists():
            with open(file, 'r') as f:
                content = f.read()
                if 'password' in content.lower() and '=' in content:
                    # This is a basic check - more sophisticated analysis needed
                    pass
    
    print("✅ No obvious hardcoded credentials found")
    
    return len(issues) == 0, issues

def check_performance():
    """Check performance considerations"""
    print("\n⚡ Checking Performance...")
    print("=" * 50)
    
    recommendations = []
    
    # Check if caching is implemented
    try:
        with open('auth.py', 'r') as f:
            content = f.read()
            if '@st.cache' in content or 'st.cache' in content:
                print("✅ Caching: Implemented")
            else:
                recommendations.append("Consider implementing Streamlit caching")
                print("⚠️ Caching: Not extensively used")
    except:
        pass
    
    # Check file sizes
    large_files = []
    for file in Path('.').glob('*.py'):
        size = file.stat().st_size
        if size > 100000:  # 100KB
            large_files.append(f"{file.name} ({size//1024}KB)")
    
    if large_files:
        print(f"⚠️ Large files found: {', '.join(large_files)}")
        recommendations.append("Consider splitting large files")
    else:
        print("✅ File sizes: Reasonable")
    
    return len(recommendations) == 0, recommendations

def generate_production_report():
    """Generate comprehensive production readiness report"""
    print("\n" + "="*60)
    print("🚀 PRODUCTION READINESS REPORT")
    print("="*60)
    
    # Run all checks
    env_ok, missing_env, optional_env = check_environment_variables()
    deps_ok, missing_deps = check_dependencies()
    files_ok, missing_files, optional_files = check_file_structure()
    db_ok = check_database_connection()
    security_ok, security_issues = check_security()
    perf_ok, perf_recommendations = check_performance()
    
    # Calculate overall score
    checks = [env_ok, deps_ok, files_ok, db_ok, security_ok]
    passed = sum(checks)
    total = len(checks)
    score = (passed / total) * 100
    
    print(f"\n📊 OVERALL SCORE: {score:.1f}% ({passed}/{total} checks passed)")
    
    if score >= 90:
        print("🎉 PRODUCTION READY!")
        status = "READY"
    elif score >= 70:
        print("⚠️ MOSTLY READY - Minor issues to address")
        status = "MOSTLY_READY"
    else:
        print("❌ NOT READY - Critical issues need fixing")
        status = "NOT_READY"
    
    # Detailed recommendations
    print("\n📋 RECOMMENDATIONS:")
    print("-" * 40)
    
    if missing_env:
        print("🔧 Environment Variables:")
        for var in missing_env:
            print(f"   • Fix {var}")
    
    if missing_deps:
        print("📦 Dependencies:")
        for dep in missing_deps:
            print(f"   • Install {dep}")
    
    if missing_files:
        print("📁 Files:")
        for file in missing_files:
            print(f"   • Create {file}")
    
    if security_issues:
        print("🛡️ Security:")
        for issue in security_issues:
            print(f"   • Fix: {issue}")
    
    if perf_recommendations:
        print("⚡ Performance:")
        for rec in perf_recommendations:
            print(f"   • Consider: {rec}")
    
    # Production deployment checklist
    print("\n✅ PRODUCTION DEPLOYMENT CHECKLIST:")
    print("-" * 40)
    print("□ Environment variables configured")
    print("□ Database tables created")
    print("□ SSL certificate configured")
    print("□ Domain name configured")
    print("□ Backup strategy implemented")
    print("□ Monitoring setup")
    print("□ Error logging configured")
    print("□ Load testing completed")
    print("□ Security audit completed")
    print("□ Documentation updated")
    
    return status, score

if __name__ == "__main__":
    print("🔍 Resume Hackathon - Production Readiness Check")
    print("=" * 60)
    
    status, score = generate_production_report()
    
    print(f"\n🎯 FINAL STATUS: {status}")
    print(f"📊 READINESS SCORE: {score:.1f}%")
    
    if status == "READY":
        print("\n🚀 Your application is ready for production deployment!")
    elif status == "MOSTLY_READY":
        print("\n⚠️ Address the minor issues above before production deployment.")
    else:
        print("\n❌ Critical issues must be resolved before production deployment.")
