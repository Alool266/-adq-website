# ADQ Website Admin Panel

Complete admin panel for managing the ADQ (Architectural Details of Projects) website with full bilingual (Arabic/English) content management and image upload capabilities.

## Features

- **Secure Authentication** - JWT-based admin login
- **Bilingual Content Management** - Edit all content in both Arabic and English
- **Image Upload** - Upload and manage website images
- **Section Management** - Control hero, about, vision, mission sections
- **Projects Management** - Add, edit, and manage project portfolio
- **Services Management** - Manage services with images and descriptions
- **Contact Information** - Update contact details and social links
- **Real-time Updates** - Changes reflect immediately on the website

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React 18 + React Router + Axios
- **Authentication**: JWT tokens
- **Database**: SQLite (easily upgradeable to PostgreSQL)

## Project Structure

```
-adq-website/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── routers/
│   │       ├── admin.py
│   │       └── content.py
│   ├── init_db.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   ├── pages/
│   │   │   ├── LoginPage.js
│   │   │   └── DashboardPage.js
│   │   └── services/
│   │       └── api.js
│   ├── package.json
│   └── ... (other React files)
├── uploads/ (created automatically)
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd -adq-website/backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database with default data:
   ```bash
   python init_db.py
   ```

5. Run the server:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

6. The API will be available at:
   - API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs
   - Uploaded images: http://localhost:8001/uploads/

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd -adq-website/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. The admin panel will be available at: http://localhost:3000

## Admin Access

### Default Credentials
- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password after first login!

### Creating Additional Admins
Use the admin API endpoint to create more admin users:
```bash
POST /api/v1/admin/create
{
  "username": "newadmin",
  "email": "admin@example.com",
  "password": "securepassword"
}
```

## API Endpoints

### Authentication
- `POST /api/v1/admin/login` - Admin login
- `GET /api/v1/admin/me` - Get current admin info
- `POST /api/v1/admin/create` - Create new admin (admin only)

### Content Management
- `GET /api/v1/content/sections` - Get all sections
- `PUT /api/v1/content/sections/{key}` - Update section
- `GET /api/v1/content/projects` - Get all projects
- `POST /api/v1/content/projects` - Create project
- `PUT /api/v1/content/projects/{id}` - Update project
- `DELETE /api/v1/content/projects/{id}` - Delete project
- `GET /api/v1/content/services` - Get all services
- `POST /api/v1/content/services` - Create service
- `PUT /api/v1/content/services/{id}` - Update service
- `DELETE /api/v1/content/services/{id}` - Delete service
- `GET /api/v1/content/contact` - Get contact info
- `PUT /api/v1/content/contact` - Update contact info
- `POST /api/v1/content/upload-image` - Upload image

Full API documentation available at: http://localhost:8001/docs

## Managing Website Content

### Hero Section
- Edit title and subtitle in both Arabic and English
- Upload hero background image (recommended: 1920x1080px)

### About Section
- Edit title, content, and image
- Content supports rich text (plain text for now)

### Services
- Add/remove services with titles, descriptions, and images
- Reorder by changing the `order` field

### Projects
- Add portfolio projects with titles, descriptions, categories
- Categories: 3D Designs, Under Construction, Finished
- Upload project images (recommended: 800x600px)

### Contact Information
- Update phone, WhatsApp, email
- Edit location in both languages
- Update address and Google Maps embed URL
- Manage social media links

## Image Guidelines

- **Hero Images**: 1920x1080px (16:9 ratio)
- **About Image**: 800x600px (4:3 ratio)
- **Service Images**: 400x300px (4:3 ratio)
- **Project Images**: 800x600px (4:3 ratio)
- **Supported formats**: JPG, JPEG, PNG, GIF, WebP
- **Max file size**: 5MB (configurable in backend)

## Deployment

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Manual Deployment
1. Set up a production database (PostgreSQL recommended)
2. Update `database.py` with production database URL
3. Change `SECRET_KEY` in `auth.py` to a secure random string
4. Use a production ASGI server (e.g., Gunicorn with Uvicorn workers)
5. Configure nginx as reverse proxy
6. Build React frontend: `npm run build` and serve with nginx

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secure-secret-key-here
DATABASE_URL=sqlite:///./adq_website.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Security Notes

- Change the default admin password immediately
- Use a strong `SECRET_KEY` in production
- Enable HTTPS in production
- Implement rate limiting
- Use environment variables for sensitive data
- Regularly update dependencies

## Contributing

This project was developed by **Ali Hasan**.
GitHub: https://github.com/Alool266

## License

MIT License - Free to use for personal and commercial projects.

## Support

For issues or questions, please open an issue on GitHub.
