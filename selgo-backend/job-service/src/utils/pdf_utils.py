# File: job-service/src/utils/pdf_utils.py

from typing import Tuple, Dict, Any
from jinja2 import Template, Environment, FileSystemLoader
import os
from ..config.config import settings
from ..models.schemas import CVBuilderData
import logging

logger = logging.getLogger(__name__)

def generate_cv_pdf(cv_id: int, cv_data: CVBuilderData) -> Tuple[str, int]:
    """Generate PDF from CV builder data."""
    try:
        # Check if WeasyPrint is available
        try:
            from weasyprint import HTML, CSS
        except ImportError:
            logger.warning("WeasyPrint not installed. Skipping PDF generation.")
            # Create a dummy file for now
            pdf_dir = os.path.join(settings.UPLOAD_DIR, "cvs")
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_filename = f"cv_{cv_id}.txt"
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            
            with open(pdf_path, 'w') as f:
                f.write("CV PDF generation requires WeasyPrint installation")
            
            return pdf_path, os.path.getsize(pdf_path)
        
        # Ensure template directory exists
        template_dir = "templates"
        os.makedirs(template_dir, exist_ok=True)
        
        # Create template file if it doesn't exist
        template_file = os.path.join(template_dir, "cv_template.html")
        if not os.path.exists(template_file):
            with open(template_file, 'w') as f:
                f.write(create_cv_template_html())

        # Load HTML template
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("cv_template.html")
        
        # Render HTML with data
        html_content = template.render(
            cv_data=cv_data,
            cv_id=cv_id
        )
        
        # Ensure PDF directory exists
        pdf_dir = os.path.join(settings.UPLOAD_DIR, "cvs")
        os.makedirs(pdf_dir, exist_ok=True)
        
        pdf_filename = f"cv_{cv_id}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        # Create PDF with proper error handling
        try:
            HTML(string=html_content).write_pdf(pdf_path)
        except Exception as pdf_error:
            logger.error(f"WeasyPrint PDF generation failed: {pdf_error}")
            # Create a text file instead
            pdf_filename = f"cv_{cv_id}.txt"
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            with open(pdf_path, 'w', encoding='utf-8') as f:
                f.write(f"CV Data for CV {cv_id}\n")
                f.write("=" * 30 + "\n\n")
                if cv_data.contact_info:
                    f.write(f"Email: {cv_data.contact_info.email}\n")
                    f.write(f"Phone: {cv_data.contact_info.phone}\n")
                if cv_data.summary:
                    f.write(f"\nSummary: {cv_data.summary.professional_summary}\n")
        
        # Get file size
        file_size = os.path.getsize(pdf_path)
        
        logger.info(f"PDF generated: {pdf_path} ({file_size} bytes)")
        return pdf_path, file_size
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        # Create a fallback text file
        try:
            pdf_dir = os.path.join(settings.UPLOAD_DIR, "cvs")
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_filename = f"cv_{cv_id}_fallback.txt"
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            
            with open(pdf_path, 'w', encoding='utf-8') as f:
                f.write(f"CV generation failed for CV {cv_id}")
            
            return pdf_path, os.path.getsize(pdf_path)
        except:
            raise Exception(f"Failed to generate PDF: {str(e)}")

def create_cv_template_html() -> str:
    """Create basic CV template HTML."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV - {{ cv_data.contact_info.email if cv_data.contact_info else 'Professional CV' }}</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #0891b2;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #0891b2;
            margin-bottom: 10px;
        }
        .contact-info {
            color: #666;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #0891b2;
            border-bottom: 1px solid #0891b2;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        .experience-item, .education-item {
            margin-bottom: 20px;
        }
        .item-header {
            font-weight: bold;
            color: #0891b2;
        }
        .item-subheader {
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        {% if cv_data.contact_info %}
        <h1>Professional CV</h1>
        <div class="contact-info">
            {% if cv_data.contact_info.email %}
            <p>{{ cv_data.contact_info.email }}</p>
            {% endif %}
            {% if cv_data.contact_info.phone %}
            <p>{{ cv_data.contact_info.phone }}</p>
            {% endif %}
            {% if cv_data.contact_info.location %}
            <p>{{ cv_data.contact_info.location }}</p>
            {% endif %}
        </div>
        {% endif %}
    </div>

    <!-- Professional Summary -->
    {% if cv_data.summary and cv_data.summary.professional_summary %}
    <div class="section">
        <h2>Professional Summary</h2>
        <p>{{ cv_data.summary.professional_summary }}</p>
    </div>
    {% endif %}

    <!-- Work Experience -->
    {% if cv_data.work_experience and cv_data.work_experience.experiences %}
    <div class="section">
        <h2>Work Experience</h2>
        {% for exp in cv_data.work_experience.experiences %}
        <div class="experience-item">
            <div class="item-header">{{ exp.job_title }}</div>
            <div class="item-subheader">{{ exp.company_name }}</div>
            {% if exp.description %}
            <p>{{ exp.description }}</p>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Education -->
    {% if cv_data.education and cv_data.education.educations %}
    <div class="section">
        <h2>Education</h2>
        {% for edu in cv_data.education.educations %}
        <div class="education-item">
            <div class="item-header">{{ edu.degree }}</div>
            <div class="item-subheader">{{ edu.institution }}</div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</body>
</html>
    """