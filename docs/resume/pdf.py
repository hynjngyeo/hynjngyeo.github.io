import markdown
import weasyprint
from jinja2 import Template

# Sample Markdown Resume Template
markdown_resume = """
# John Doe
**Data Scientist | AI Researcher**

## Contact
- **Email:** johndoe@example.com
- **Phone:** +1 234 567 8901
- **Website:** [johndoe.com](http://johndoe.com)
- **LinkedIn:** [linkedin.com/in/johndoe](http://linkedin.com/in/johndoe)

## Summary
Experienced data scientist specializing in machine learning, natural language processing, and AI-driven applications.

## Experience
### Data Scientist | ABC Corp | 2020 - Present
- Developed NLP models for sentiment analysis and text classification.
- Improved data pipeline efficiency by 30%.
- Collaborated with cross-functional teams to deploy AI solutions.

### AI Researcher | XYZ Labs | 2018 - 2020
- Conducted research on reinforcement learning algorithms.
- Published two papers in peer-reviewed AI journals.

## Education
- **M.S. in Computer Science**, University of Example, 2018
- **B.S. in Mathematics**, Example University, 2016

## Skills
- Python, TensorFlow, PyTorch, SQL, Neo4j
- Data Visualization, Statistical Analysis
- Machine Learning, NLP, Graph AI

## Projects
- **Graph-based Recommender System** - Built a recommendation engine using Neo4j.
- **Chatbot for Customer Support** - Developed a chatbot using NLP models.

## Certifications
- Google Professional Machine Learning Engineer
- AWS Certified Data Analytics - Specialty

## Languages
- English (Fluent)
- Korean (Native)
"""

# Convert Markdown to HTML
html_content = markdown.markdown(markdown_resume)

# HTML Template for Styling
html_template = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resume</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: #2C3E50;
        }
        h1 {
            text-align: center;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    {{ content }}
</body>
</html>
""")

# Render the final HTML
final_html = html_template.render(content=html_content)

# Convert HTML to PDF
pdf_file = "resume.pdf"
weasyprint.HTML(string=final_html).write_pdf(pdf_file, stylesheets=[weasyprint.CSS(string='@page { size: A4; margin: 20mm; }')])

print(f"Resume PDF generated: {pdf_file}")
