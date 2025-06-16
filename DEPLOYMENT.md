# Disease Prediction App - Deployment Guide

## 📋 Overview
This guide provides instructions for deploying the Disease Risk Prediction Streamlit application using Docker.

## 📦 Required Files for Deployment

Ensure you have all these files in your deployment directory:

```
disease_pred/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose configuration
├── deploy.sh             # Automated deployment script
├── .dockerignore         # Docker build optimization
├── .streamlit/           # Streamlit theme configuration
│   └── config.toml       # Theme colors and settings
├── assets/               # Application assets
│   ├── GENME_LIFE.png
│   ├── Kalscanner69.png
│   ├── MCU.jpg
│   └── StrokeGENME.png
└── DEPLOYMENT.md         # This file
```

## 🔧 Prerequisites

### On the Server:
1. **Docker** (version 20.10 or higher)
2. **Docker Compose** (version 1.27 or higher)
3. **Git** (for cloning the repository)

### Installation Commands (Ubuntu/Debian):
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
```

## 🚀 Deployment Methods

### Method 1: Automated Deployment (Recommended)

1. **Clone or copy all files to the server**
2. **Navigate to the project directory**
   ```bash
   cd disease_pred
   ```
3. **Run the deployment script**
   ```bash
   ./deploy.sh
   ```

The script will:
- Check prerequisites
- Stop any existing containers
- Build the Docker image
- Start the application
- Verify deployment success

### Method 2: Manual Deployment

1. **Build and start with Docker Compose**
   ```bash
   docker-compose up --build -d
   ```

2. **Verify the deployment**
   ```bash
   docker-compose ps
   docker-compose logs
   ```

### Method 3: Direct Docker Commands

1. **Build the image**
   ```bash
   docker build -t disease-prediction-app .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 8501:8501 --name disease-app disease-prediction-app
   ```

## 🌐 Accessing the Application

Once deployed, the application will be available at:
- **Main App**: `http://your-server-ip:8501`
- **Health Check**: `http://your-server-ip:8501/_stcore/health`

## 🔍 Monitoring and Management

### View Application Logs
```bash
docker-compose logs -f disease-prediction-app
```

### Check Container Status
```bash
docker-compose ps
```

### Restart the Application
```bash
docker-compose restart
```

### Stop the Application
```bash
docker-compose down
```

### Update the Application
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

## 🔧 Configuration Options

### Environment Variables
You can modify these in `docker-compose.yml`:

- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Bind address (default: 0.0.0.0)
- `STREAMLIT_SERVER_HEADLESS`: Run without browser (default: true)

### Port Configuration
To change the external port, modify the ports section in `docker-compose.yml`:
```yaml
ports:
  - "9000:8501"  # External port 9000 -> Internal port 8501
```

## 🛡️ Security Considerations

1. **Firewall**: Ensure port 8501 is accessible from your network
2. **Reverse Proxy**: Consider using nginx for production deployments
3. **SSL/TLS**: Implement HTTPS for production use
4. **Access Control**: Implement authentication if needed

## 🐛 Troubleshooting

### Common Issues:

**1. Port Already in Use**
```bash
# Find and stop process using port 8501
sudo lsof -i :8501
sudo kill -9 <PID>
```

**2. Permission Denied**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Then logout and login again
```

**3. Container Fails to Start**
```bash
# Check logs for errors
docker-compose logs disease-prediction-app
```

**4. Assets Not Loading**
- Ensure the `assets/` directory is copied correctly
- Check file permissions
- Verify image file paths in the application

### Health Check
The application includes a health check endpoint:
```bash
curl http://localhost:8501/_stcore/health
```

## 📞 Support

If you encounter issues:
1. Check the application logs: `docker-compose logs -f`
2. Verify all required files are present
3. Ensure Docker and Docker Compose are properly installed
4. Check network connectivity and firewall settings

## 📝 Notes

- The application runs as a non-root user for security
- Container automatically restarts unless manually stopped
- Health checks monitor application status
- Logs are accessible through Docker Compose commands

---

**Deployment completed successfully!** 🎉

The Disease Risk Prediction application should now be accessible at your server's IP address on port 8501.

