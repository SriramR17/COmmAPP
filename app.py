from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

load_dotenv()
# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USERNAME") # Replace with your email
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")  # Replace with your app password

mail = Mail(app)



# Routes for navigating through the form
@app.route('/')
def index():
    return redirect(url_for('domain'))

@app.route('/domain', methods=['GET', 'POST'])
def domain():
    if request.method == 'POST':
        session['domain'] = request.form.get('domain')
        return redirect(url_for('categories'))
    selected_domain = session.get('domain')
    return render_template('domain.html', selected_domain=selected_domain)

@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        session['categories'] = request.form.getlist('categories')
        return redirect(url_for('platform'))
    selected_categories = session.get('categories', [])
    return render_template('categories.html', selected_categories=selected_categories)

@app.route('/platform', methods=['GET', 'POST'])
def platform():
    if request.method == 'POST':
        session['platform'] = request.form.get('platform')
        return redirect(url_for('functional_requirements'))
    selected_platform = session.get('platform')
    return render_template('platform.html', selected_platform=selected_platform)

@app.route('/functional-requirements', methods=['GET', 'POST'])
def functional_requirements():
    if request.method == 'POST':
        session['functional_requirements'] = request.form.getlist('functional_requirements')
        return redirect(url_for('non_functional_requirements'))
    selected_functional_requirements = session.get('functional_requirements', [])
    return render_template('functional_requirements.html', selected_functional_requirements=selected_functional_requirements)

@app.route('/non-functional-requirements', methods=['GET', 'POST'])
def non_functional_requirements():
    if request.method == 'POST':
        session['non_functional_requirements'] = request.form.getlist('non_functional_requirements')
        return redirect(url_for('summary'))
    selected_non_functional_requirements = session.get('non_functional_requirements', [])
    return render_template('non_functional_requirements.html', selected_non_functional_requirements=selected_non_functional_requirements)

@app.route('/summary', methods=['GET', 'POST'])
def summary():
    data = {
        'domain': session.get('domain'),
        'categories': session.get('categories', []),
        'platform': session.get('platform'),
        'functional_requirements': session.get('functional_requirements', []),
        'non_functional_requirements': session.get('non_functional_requirements', [])
    }
    return render_template('summary.html', data=data)

@app.route('/send_summary', methods=['POST'])
def send_summary():
    # Get manager email and additional details from form
    manager_email = request.form.get('manager_email')
    reference_images = request.files.getlist('reference_images')
    additional_links = request.form.get('additional_links')

    # Collecting data from the session for email content
    data = {
        'domain': session.get('domain'),
        'categories': session.get('categories', []),
        'platform': session.get('platform'),
        'functional_requirements': session.get('functional_requirements', []),
        'non_functional_requirements': session.get('non_functional_requirements', [])
    }

    # Save reference images if uploaded
    image_dir = 'uploaded_images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    reference_image_paths = []
    for image in reference_images:
        image_path = os.path.join(image_dir, image.filename)
        image.save(image_path)
        reference_image_paths.append(image_path)

    # Send email with the data, images, and links
    try:
        send_email_with_details(manager_email, data, reference_image_paths, additional_links)
        email_status = "success"
    except Exception as e:
        email_status = f"failure: {str(e)}"

    # Pass data and status to the template
    return render_template('summary.html', data=data, email_status=email_status)  # Render the template with data and status



def send_email_with_details(manager_email, data, reference_image_paths, additional_links):
    msg = Message('Product Requirements Summary', recipients=[manager_email])
    msg.body = f"""
    Dear Manager,
    
    Here is the summary of the product requirements:
    
    Domain: {data['domain']}
    Categories: {', '.join(data['categories'])}
    Platform: {data['platform']}
    Functional Requirements: {', '.join(data['functional_requirements'])}
    Non-Functional Requirements: {', '.join(data['non_functional_requirements'])}

    Additional Links: {additional_links if additional_links else 'None provided'}
    """

    # Attach the reference images
    for image_path in reference_image_paths:
        with app.open_resource(image_path) as fp:
            msg.attach(os.path.basename(image_path), 'image/png', fp.read())

    mail.send(msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
