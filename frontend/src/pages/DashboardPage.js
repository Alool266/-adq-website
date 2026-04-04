import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { contentAPI } from '../services/api';
import { API_BASE } from '../services/api';

const DashboardPage = () => {
  const [activeTab, setActiveTab] = useState('hero');
  const [sections, setSections] = useState([]);
  const [projects, setProjects] = useState([]);
  const [services, setServices] = useState([]);
  const [contactInfo, setContactInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [sectionsRes, projectsRes, servicesRes, contactRes] = await Promise.all([
        contentAPI.getSections(),
        contentAPI.getProjects(),
        contentAPI.getServices(),
        contentAPI.getContactInfo(),
      ]);
      setSections(sectionsRes.data);
      setProjects(projectsRes.data);
      setServices(servicesRes.data);
      setContactInfo(contactRes.data);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    navigate('/login');
  };

  const updateSection = async (sectionKey, data) => {
    try {
      await contentAPI.updateSection(sectionKey, data);
      fetchData();
    } catch (err) {
      console.error('Error updating section:', err);
    }
  };

  const uploadImage = async (file) => {
    try {
      const response = await contentAPI.uploadImage(file);
      return response.data.url;
    } catch (err) {
      console.error('Error uploading image:', err);
      return null;
    }
  };

  const handleImageUpload = async (e, sectionKey, field) => {
    const file = e.target.files[0];
    if (file) {
      const url = await uploadImage(file);
      if (url) {
        updateSection(sectionKey, { [field]: url });
      }
    }
  };

  const getSectionByKey = (key) => {
    return sections.find(s => s.section_key === key);
  };

  const updateService = async (id, data) => {
    try {
      await contentAPI.updateService(id, data);
      fetchData();
    } catch (err) {
      console.error('Error updating service:', err);
    }
  };

  const handleServiceImageUpload = async (e, serviceId) => {
    const file = e.target.files[0];
    if (file) {
      const url = await uploadImage(file);
      if (url) {
        updateService(serviceId, { image_url: url });
      }
    }
  };

  const updateProject = async (id, data) => {
    try {
      await contentAPI.updateProject(id, data);
      fetchData();
    } catch (err) {
      console.error('Error updating project:', err);
    }
  };

  const handleProjectImageUpload = async (e, projectId) => {
    const file = e.target.files[0];
    if (file) {
      const url = await uploadImage(file);
      if (url) {
        updateProject(projectId, { image_url: url });
      }
    }
  };

  const updateContactInfo = async (data) => {
    try {
      await contentAPI.updateContactInfo(data);
      fetchData();
    } catch (err) {
      console.error('Error updating contact info:', err);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      <nav className="sidebar">
        <div className="sidebar-header">
          <h2>ADQ Admin</h2>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
        <ul className="nav-menu">
          <li className={activeTab === 'hero' ? 'active' : ''} onClick={() => setActiveTab('hero')}>
            Hero Section
          </li>
          <li className={activeTab === 'about' ? 'active' : ''} onClick={() => setActiveTab('about')}>
            About Section
          </li>
          <li className={activeTab === 'services' ? 'active' : ''} onClick={() => setActiveTab('services')}>
            Services
          </li>
          <li className={activeTab === 'projects' ? 'active' : ''} onClick={() => setActiveTab('projects')}>
            Projects
          </li>
          <li className={activeTab === 'contact' ? 'active' : ''} onClick={() => setActiveTab('contact')}>
            Contact Info
          </li>
        </ul>
      </nav>

      <main className="main-content">
        {activeTab === 'hero' && (
          <div className="section-editor">
            <h2>Hero Section</h2>
            <div className="form-group">
              <label>Title (Arabic)</label>
              <textarea
                value={getSectionByKey('hero')?.title_ar || ''}
                onChange={(e) => updateSection('hero', { title_ar: e.target.value })}
                rows={2}
              />
            </div>
            <div className="form-group">
              <label>Title (English)</label>
              <textarea
                value={getSectionByKey('hero')?.title_en || ''}
                onChange={(e) => updateSection('hero', { title_en: e.target.value })}
                rows={2}
              />
            </div>
            <div className="form-group">
              <label>Subtitle (Arabic)</label>
              <textarea
                value={getSectionByKey('hero')?.subtitle_ar || ''}
                onChange={(e) => updateSection('hero', { subtitle_ar: e.target.value })}
                rows={2}
              />
            </div>
            <div className="form-group">
              <label>Subtitle (English)</label>
              <textarea
                value={getSectionByKey('hero')?.subtitle_en || ''}
                onChange={(e) => updateSection('hero', { subtitle_en: e.target.value })}
                rows={2}
              />
            </div>
            <div className="form-group">
              <label>Hero Background Image</label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => handleImageUpload(e, 'hero', 'image_url')}
              />
              {getSectionByKey('hero')?.image_url && (
                <img src={`${API_BASE}${getSectionByKey('hero').image_url}`} alt="Hero" className="preview-image" />
              )}
            </div>
          </div>
        )}

        {activeTab === 'about' && (
          <div className="section-editor">
            <h2>About Section</h2>
            <div className="form-group">
              <label>Title (Arabic)</label>
              <input
                type="text"
                value={getSectionByKey('about')?.title_ar || ''}
                onChange={(e) => updateSection('about', { title_ar: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Title (English)</label>
              <input
                type="text"
                value={getSectionByKey('about')?.title_en || ''}
                onChange={(e) => updateSection('about', { title_en: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Content (Arabic)</label>
              <textarea
                value={getSectionByKey('about')?.content_ar || ''}
                onChange={(e) => updateSection('about', { content_ar: e.target.value })}
                rows={6}
              />
            </div>
            <div className="form-group">
              <label>Content (English)</label>
              <textarea
                value={getSectionByKey('about')?.content_en || ''}
                onChange={(e) => updateSection('about', { content_en: e.target.value })}
                rows={6}
              />
            </div>
            <div className="form-group">
              <label>About Image</label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => handleImageUpload(e, 'about', 'image_url')}
              />
              {getSectionByKey('about')?.image_url && (
                <img src={`${API_BASE}${getSectionByKey('about').image_url}`} alt="About" className="preview-image" />
              )}
            </div>
          </div>
        )}

        {activeTab === 'services' && (
          <div className="section-editor">
            <h2>Services Management</h2>
            <div className="services-list">
              {services.map(service => (
                <div key={service.id} className="service-item">
                  <div className="form-group">
                    <label>Title (Arabic)</label>
                    <input
                      type="text"
                      value={service.title_ar}
                      onChange={(e) => updateService(service.id, { title_ar: e.target.value })}
                    />
                  </div>
                  <div className="form-group">
                    <label>Title (English)</label>
                    <input
                      type="text"
                      value={service.title_en}
                      onChange={(e) => updateService(service.id, { title_en: e.target.value })}
                    />
                  </div>
                  <div className="form-group">
                    <label>Description (Arabic)</label>
                    <textarea
                      value={service.description_ar || ''}
                      onChange={(e) => updateService(service.id, { description_ar: e.target.value })}
                      rows={3}
                    />
                  </div>
                  <div className="form-group">
                    <label>Description (English)</label>
                    <textarea
                      value={service.description_en || ''}
                      onChange={(e) => updateService(service.id, { description_en: e.target.value })}
                      rows={3}
                    />
                  </div>
                  <div className="form-group">
                    <label>Service Image</label>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handleServiceImageUpload(e, service.id)}
                    />
                    {service.image_url && (
                      <img src={`${API_BASE}${service.image_url}`} alt={service.title_en} className="preview-image-small" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'projects' && (
          <div className="section-editor">
            <h2>Projects Management</h2>
            <div className="projects-list">
              {projects.map(project => (
                <div key={project.id} className="project-item">
                  <div className="form-group">
                    <label>Title (Arabic)</label>
                    <input
                      type="text"
                      value={project.title_ar}
                      onChange={(e) => updateProject(project.id, { title_ar: e.target.value })}
                    />
                  </div>
                  <div className="form-group">
                    <label>Title (English)</label>
                    <input
                      type="text"
                      value={project.title_en}
                      onChange={(e) => updateProject(project.id, { title_en: e.target.value })}
                    />
                  </div>
                  <div className="form-group">
                    <label>Category</label>
                  <select
                    value={project.category}
                    onChange={(e) => updateProject(project.id, { category: e.target.value })}
                  >
                    <option value="3d">3D Designs</option>
                    <option value="construction">Under Construction</option>
                    <option value="finished">Finished</option>
                  </select>
                  </div>
                  <div className="form-group">
                    <label>Project Image</label>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handleProjectImageUpload(e, project.id)}
                    />
                    {project.image_url && (
                      <img src={`${API_BASE}${project.image_url}`} alt={project.title_en} className="preview-image-small" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'contact' && (
          <div className="section-editor">
            <h2>Contact Information</h2>
            <div className="form-group">
              <label>Phone</label>
              <input
                type="text"
                value={contactInfo?.phone || ''}
                onChange={(e) => updateContactInfo({ phone: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>WhatsApp</label>
              <input
                type="text"
                value={contactInfo?.whatsapp || ''}
                onChange={(e) => updateContactInfo({ whatsapp: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={contactInfo?.email || ''}
                onChange={(e) => updateContactInfo({ email: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Location (Arabic)</label>
              <input
                type="text"
                value={contactInfo?.location_ar || ''}
                onChange={(e) => updateContactInfo({ location_ar: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Location (English)</label>
              <input
                type="text"
                value={contactInfo?.location_en || ''}
                onChange={(e) => updateContactInfo({ location_en: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Address (Arabic)</label>
              <textarea
                value={contactInfo?.address_ar || ''}
                onChange={(e) => updateContactInfo({ address_ar: e.target.value })}
                rows={3}
              />
            </div>
            <div className="form-group">
              <label>Address (English)</label>
              <textarea
                value={contactInfo?.address_en || ''}
                onChange={(e) => updateContactInfo({ address_en: e.target.value })}
                rows={3}
              />
            </div>
            <div className="form-group">
              <label>Google Maps URL</label>
              <input
                type="text"
                value={contactInfo?.map_url || ''}
                onChange={(e) => updateContactInfo({ map_url: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Social - WhatsApp</label>
              <input
                type="text"
                value={contactInfo?.social_whatsapp || ''}
                onChange={(e) => updateContactInfo({ social_whatsapp: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Social - Instagram</label>
              <input
                type="text"
                value={contactInfo?.social_instagram || ''}
                onChange={(e) => updateContactInfo({ social_instagram: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Social - Twitter</label>
              <input
                type="text"
                value={contactInfo?.social_twitter || ''}
                onChange={(e) => updateContactInfo({ social_twitter: e.target.value })}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default DashboardPage;
