import os
import re
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mysql.connector
from db_connect import get_db_connection


basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder=basedir, static_folder=basedir)
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)


def validate_password(password, username, email):
    if len(password) < 8 or len(password) > 12:
        return "Password must be 8-12 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return "Password must contain at least one special character."
    if " " in password:
        return "Password must not contain spaces."

    if username and username.lower() in password.lower():
        return "Password cannot contain your username/handle."
    if email and email.lower() in password.lower():
        return "Password cannot contain your email."

    common_passwords = ['password', '12345678', 'qwertyuiop', 'admin123', 'pass1234']
    if password.lower() in common_passwords:
        return "This password is too common."

    return None


@app.route('/style.css')
@app.route('/dashboard/style.css')
@app.route('/campaigns/style.css')
@app.route('/signup/style.css')
def serve_css(): return send_from_directory(basedir, 'style.css')

@app.route('/script.js')
@app.route('/dashboard/script.js')
def serve_js(): return send_from_directory(basedir, 'script.js')

@app.route('/images/<path:filename>')
def serve_images(filename): return send_from_directory(basedir, filename)

@app.route('/static/uploads/<filename>')
def serve_uploads(filename): return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def index(): return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('userType')
        remember = request.form.get('remember')

        conn = get_db_connection()
        if not conn: return "Database Error"
        cursor = conn.cursor(dictionary=True)

        user = None
        id_key = ''
        pic_key = ''

        if user_type == 'influencer':
            cursor.execute("SELECT * FROM INFLUENCER WHERE Handle = %s", (username,))
            user = cursor.fetchone()
            id_key = 'InfluencerID'
            pic_key = 'ProfilePic'
        elif user_type == 'brand':
            cursor.execute("SELECT * FROM BRAND WHERE Brandname = %s", (username,))
            user = cursor.fetchone()
            id_key = 'BrandID'
            pic_key = 'LogoPic'

        cursor.close()
        conn.close()

        if user:
            if user['Password'] == password or check_password_hash(user['Password'], password):
                session.permanent = True if remember else False
                session['user_id'] = user[id_key]
                session['user_name'] = username
                session['role'] = user_type
                session['profile_pic'] = user.get(pic_key)
                
                if user_type == 'influencer':
                    return redirect(url_for('influencer_dashboard'))
                else:
                    return redirect(url_for('brand_dashboard'))

        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/signup')
def signup_select(): return render_template('signup.html')

@app.route('/signup/influencer', methods=['GET', 'POST'])
def signup_influencer():
    if request.method == 'POST':
        name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        handle = request.form.get('handle')
        industry = request.form.get('industry_name')

        if password != confirm_password:
            return "Error: Passwords do not match. <a href='/signup/influencer'>Try Again</a>"

        error = validate_password(password, handle, email)
        if error:
            return f"Error: {error} <a href='/signup/influencer'>Try Again</a>"

        hashed_pw = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO INFLUENCER (InfluencerName, Email, Password, Handle, Industry, Age, Gender, Field, Followers) 
                VALUES (%s, %s, %s, %s, %s, 25, 'Other', 'General', 0)
            """, (name, email, hashed_pw, handle, industry))
            conn.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f"Database Error: {e}"
        finally:
            cursor.close()
            conn.close()

    return render_template('influencer_signup.html')

@app.route('/signup/brand', methods=['GET', 'POST'])
def signup_brand():
    if request.method == 'POST':
        name = request.form.get('brand_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        budget = request.form.get('budget')

        if password != confirm_password:
            return "Error: Passwords do not match. <a href='/signup/brand'>Try Again</a>"

        error = validate_password(password, name, email)
        if error:
            return f"Error: {error} <a href='/signup/brand'>Try Again</a>"

        hashed_pw = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO BRAND (Brandname, Email, Password, PayPackage) 
                VALUES (%s, %s, %s, %s)
            """, (name, email, hashed_pw, budget))
            conn.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f"Database Error: {e}"
        finally:
            cursor.close()
            conn.close()

    return render_template('brand_signup.html')

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    results = []
    
    if query:
        cursor.execute("SELECT BrandID as ID, Brandname as Name, LogoPic as Pic, 'Brand' as Role, PayPackage as Info FROM BRAND WHERE Brandname LIKE %s", (f"%{query}%",))
        brands = cursor.fetchall()
        for b in brands: b['Info'] = f"Budget: {b['Info']}"
        results.extend(brands)
        
        cursor.execute("SELECT InfluencerID as ID, InfluencerName as Name, ProfilePic as Pic, 'Influencer' as Role, Industry as Info FROM INFLUENCER WHERE InfluencerName LIKE %s OR Handle LIKE %s", (f"%{query}%", f"%{query}%"))
        results.extend(cursor.fetchall())
    
    conn.close()
    return jsonify(results)

@app.route('/api/application/status', methods=['POST'])
def api_update_status():
    if 'user_id' not in session or session['role'] != 'brand':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.json
    app_id = data.get('app_id')
    action = data.get('action')

    if action not in ['Approved', 'Rejected']:
        return jsonify({'success': False, 'message': 'Invalid Action'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE INFLUENCER_CAMPAIGN ic
            JOIN CAMPAIGN c ON ic.CampaignID = c.CampaignID
            SET ic.CampaignStatus = %s
            WHERE ic.CAM_ID = %s AND c.BrandID = %s
        """, (action, app_id, session['user_id']))
        conn.commit()
        success = cursor.rowcount > 0
    except Exception as e:
        success = False
    finally:
        conn.close()

    if success:
        return jsonify({'success': True, 'new_status': action})
    else:
        return jsonify({'success': False, 'message': 'Update failed'}), 500

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        user_id = session['user_id']
        role = session['role']
        
        file = request.files.get('profile_image')
        image_path = None
        
        if file and file.filename != '':
            filename = secure_filename(f"{role}_{user_id}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = url_for('static', filename='uploads/' + filename)

        if role == 'influencer':
            name = request.form.get('name')
            handle = request.form.get('handle')
            industry = request.form.get('industry')
            
            if image_path:
                cursor.execute("UPDATE INFLUENCER SET ProfilePic = %s WHERE InfluencerID = %s", (image_path, user_id))
                session['profile_pic'] = image_path

            if name and handle and industry:
                cursor.execute("""
                    UPDATE INFLUENCER 
                    SET InfluencerName = %s, Handle = %s, Industry = %s 
                    WHERE InfluencerID = %s
                """, (name, handle, industry, user_id))
                session['user_name'] = name 

        elif role == 'brand':
            name = request.form.get('name')
            email = request.form.get('email')
            budget = request.form.get('budget')

            if image_path:
                cursor.execute("UPDATE BRAND SET LogoPic = %s WHERE BrandID = %s", (image_path, user_id))
                session['profile_pic'] = image_path
            
            if name and email and budget:
                cursor.execute("""
                    UPDATE BRAND 
                    SET Brandname = %s, Email = %s, PayPackage = %s 
                    WHERE BrandID = %s
                """, (name, email, budget, user_id))
                session['user_name'] = name

        conn.commit()
        return jsonify({
            'success': True, 
            'new_image': image_path,
            'message': 'Profile updated successfully'
        })

    except Exception as e:
        print(f"Update Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
        
@app.route('/dashboard/influencer')
def influencer_dashboard():
    if 'user_id' not in session or session['role'] != 'influencer': return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as count FROM INFLUENCER_CAMPAIGN WHERE InfluencerID = %s AND CampaignStatus = 'Active'", (session['user_id'],))
    res = cursor.fetchone()
    active_count = res['count'] if res else 0

    cursor.execute("""
        SELECT b.Brandname, c.CampaignName as CampaignType, ic.StartDate as DateApplied, ic.CampaignStatus as Status
        FROM INFLUENCER_CAMPAIGN ic
        JOIN CAMPAIGN c ON ic.CampaignID = c.CampaignID
        JOIN BRAND b ON c.BrandID = b.BrandID
        WHERE ic.InfluencerID = %s LIMIT 5
    """, (session['user_id'],))
    recent_apps = cursor.fetchall()

    cursor.execute("SELECT Industry FROM INFLUENCER WHERE InfluencerID = %s", (session['user_id'],))
    user_data = cursor.fetchone()
    my_industry = user_data['Industry'] if user_data else None

    recommendations = []
    if my_industry:
        cursor.execute("""
            SELECT c.CampaignID, c.CampaignName, b.Brandname, c.EndDate, b.PayPackage
            FROM CAMPAIGN c
            JOIN BRAND b ON c.BrandID = b.BrandID
            JOIN INDUSTRY i ON c.IndustryID = i.IndustryID
            WHERE i.Industryname = %s 
              AND c.CampaignStatus = 'Active'
              AND c.CampaignID NOT IN (SELECT CampaignID FROM INFLUENCER_CAMPAIGN WHERE InfluencerID = %s)
            LIMIT 4
        """, (my_industry, session['user_id']))
        recommendations = cursor.fetchall()
    
    conn.close()
    return render_template('influencer_dashboard.html', name=session['user_name'], active_count=active_count, applications=recent_apps, recommendations=recommendations)
    
@app.route('/dashboard/brand')
def brand_dashboard():
    if 'user_id' not in session or session['role'] != 'brand': return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as count FROM CAMPAIGN WHERE BrandID = %s AND CampaignStatus = 'Active'", (session['user_id'],))
    res = cursor.fetchone()
    active_count = res['count'] if res else 0

    cursor.execute("""
        SELECT ic.CAM_ID, i.InfluencerID, i.InfluencerName, i.Handle, i.Followers, c.CampaignName, ic.CampaignStatus
        FROM INFLUENCER_CAMPAIGN ic
        JOIN INFLUENCER i ON ic.InfluencerID = i.InfluencerID
        JOIN CAMPAIGN c ON ic.CampaignID = c.CampaignID
        WHERE c.BrandID = %s
        ORDER BY ic.StartDate DESC
        LIMIT 10
    """, (session['user_id'],))
    applicants = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT i.Industryname 
        FROM CAMPAIGN c 
        JOIN INDUSTRY i ON c.IndustryID = i.IndustryID 
        WHERE c.BrandID = %s AND c.CampaignStatus = 'Active'
    """, (session['user_id'],))
    active_industries = [row['Industryname'] for row in cursor.fetchall()]

    suggestions = []
    if active_industries:
        placeholders = ', '.join(['%s'] * len(active_industries))
        query = f"""
            SELECT * FROM INFLUENCER 
            WHERE Industry IN ({placeholders}) 
            ORDER BY Followers DESC
            LIMIT 4
        """
        cursor.execute(query, tuple(active_industries))
        suggestions = cursor.fetchall()
    cursor.execute("SELECT * FROM BRAND WHERE BrandID = %s", (session['user_id'],))
    brand = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM POSTS 
        WHERE AuthorID = %s AND AuthorType = 'Brand' 
        ORDER BY CreatedAt DESC
    """, (session['user_id'],))
    posts = cursor.fetchall()

    conn.close()
    return render_template('brand_dashboard.html', 
                           name=session['user_name'], 
                           active_count=active_count, 
                           applicants=applicants, 
                           suggestions=suggestions,
                           brand=brand,
                           posts=posts)

@app.route('/search')
def search():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    results = []
    
    if query:
        cursor.execute("SELECT BrandID as ID, Brandname as Name, LogoPic as Pic, 'Brand' as Role, PayPackage as Info FROM BRAND WHERE Brandname LIKE %s", (f"%{query}%",))
        results.extend(cursor.fetchall())
        
        cursor.execute("SELECT InfluencerID as ID, InfluencerName as Name, ProfilePic as Pic, 'Influencer' as Role, Industry as Info FROM INFLUENCER WHERE InfluencerName LIKE %s OR Handle LIKE %s", (f"%{query}%", f"%{query}%"))
        results.extend(cursor.fetchall())
    
    conn.close()
    return render_template('search.html', results=results, query=query)

@app.route('/feed')
def feed():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.CampaignID as ID, c.CampaignName as Title, c.StartDate as Date, 
        b.Brandname as AuthorName, b.LogoPic as AuthorPic, b.BrandID as AuthorID, 'Brand' as AuthorType,
        'campaign' as PostType, b.PayPackage, i.Industryname
        FROM CAMPAIGN c
        JOIN BRAND b ON c.BrandID = b.BrandID
        JOIN INDUSTRY i ON c.IndustryID = i.IndustryID
        WHERE c.CampaignStatus = 'Active'
    """)
    campaigns = cursor.fetchall()

    for c in campaigns:
        if type(c['Date']) is date:
            c['Date'] = datetime.combine(c['Date'], datetime.min.time())

    cursor.execute("""
        SELECT p.PostID as ID, p.Content as Title, p.CreatedAt as Date, 
        CASE WHEN p.AuthorType = 'Brand' THEN b.Brandname ELSE i.InfluencerName END as AuthorName,
        CASE WHEN p.AuthorType = 'Brand' THEN b.LogoPic ELSE i.ProfilePic END as AuthorPic,
        p.AuthorID, p.AuthorType, 'post' as PostType, p.ImageURL as PayPackage, '' as Industryname
        FROM POSTS p
        LEFT JOIN BRAND b ON p.AuthorType = 'Brand' AND p.AuthorID = b.BrandID
        LEFT JOIN INFLUENCER i ON p.AuthorType = 'Influencer' AND p.AuthorID = i.InfluencerID
    """)
    posts = cursor.fetchall()

    full_feed = sorted(campaigns + posts, key=lambda x: x['Date'], reverse=True)
    
    conn.close()
    return render_template('find_campaigns.html', feed_items=full_feed)

@app.route('/post/create', methods=['POST'])
def create_post():
    if 'user_id' not in session: return redirect(url_for('login'))
    content = request.form.get('content')
    image = request.files.get('image')
    image_url = None
    if image and image.filename != '':
        filename = secure_filename(f"post_{session['user_id']}_{image.filename}")
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('static', filename='uploads/' + filename)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO POSTS (AuthorID, AuthorType, Content, ImageURL) VALUES (%s, %s, %s, %s)",
                   (session['user_id'], session['role'].capitalize(), content, image_url))
    conn.commit()
    conn.close()
    
    if session['role'] == 'influencer':
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('brand_dashboard'))

@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session: return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT AuthorID FROM POSTS WHERE PostID = %s", (post_id,))
        post = cursor.fetchone()

        if post:
            if post[0] == session['user_id']:
                cursor.execute("DELETE FROM POSTS WHERE PostID = %s", (post_id,))
                conn.commit()
                flash("Post deleted successfully!", "success")
            else:
                flash("You are not authorized to delete this post.", "error")
        else:
            flash("Post not found.", "error")

    except Exception as e:
        print(e)
        flash("An error occurred while deleting.", "error")
    finally:
        conn.close()

    if session.get('role') == 'influencer':
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('brand_dashboard'))

@app.route('/campaign/create', methods=['GET', 'POST'])
def create_campaign():
    if 'user_id' not in session or session['role'] != 'brand': return redirect(url_for('login'))
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT IndustryID FROM INDUSTRY WHERE Industryname = %s", (request.form.get('industry_name'),))
        ind_res = cursor.fetchone()
        ind_id = ind_res[0] if ind_res else 1
        cursor.execute("INSERT INTO CAMPAIGN (CampaignName, CampaignStatus, StartDate, EndDate, BrandID, IndustryID) VALUES (%s, 'Active', %s, %s, %s, %s)",
                       (request.form.get('title'), request.form.get('start_date'), request.form.get('end_date'), session['user_id'], ind_id))
        conn.commit()
        conn.close()
        return redirect(url_for('feed'))
    return render_template('create_campaign.html')

@app.route('/campaign/apply/<int:campaign_id>', methods=['POST'])
def apply_campaign(campaign_id):
    if 'user_id' not in session or session['role'] != 'influencer': return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM INFLUENCER WHERE InfluencerID = %s", (session['user_id'],))
    inf = cursor.fetchone()
    if inf:
        cursor.execute("SELECT * FROM INFLUENCER_CAMPAIGN WHERE InfluencerID = %s AND CampaignID = %s", (session['user_id'], campaign_id))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO INFLUENCER_CAMPAIGN (InfluencerID, CampaignID, StartDate, CampaignStatus, Handle, Industry, Age, Gender, Followers) VALUES (%s, %s, %s, 'Pending', %s, %s, %s, %s, %s)",
                           (session['user_id'], campaign_id, date.today(), inf['Handle'], inf['Industry'], inf['Age'], inf['Gender'], inf.get('Followers', 0)))
            conn.commit()
    conn.close()
    return redirect(url_for('my_applications_route'))

@app.route('/application/<int:app_id>/<action>')
def update_application_status(app_id, action):
    if 'user_id' not in session or session['role'] != 'brand': return redirect(url_for('login'))
    
    if action not in ['Approved', 'Rejected']:
        return redirect(url_for('brand_dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE INFLUENCER_CAMPAIGN ic
        JOIN CAMPAIGN c ON ic.CampaignID = c.CampaignID
        SET ic.CampaignStatus = %s
        WHERE ic.CAM_ID = %s AND c.BrandID = %s
    """, (action, app_id, session['user_id']))
    
    conn.commit()
    conn.close()
    return redirect(url_for('brand_dashboard'))

@app.route('/user/<role>/<int:id>')
def public_profile(role, id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if role == 'Brand':
        cursor.execute("SELECT * FROM BRAND WHERE BrandID = %s", (id,))
        user = cursor.fetchone()
        name = user['Brandname']
        pic = user.get('LogoPic')
        info = f"Budget: GHS {user['PayPackage']}"
    else:
        cursor.execute("SELECT * FROM INFLUENCER WHERE InfluencerID = %s", (id,))
        user = cursor.fetchone()
        name = user['InfluencerName']
        pic = user.get('ProfilePic')
        info = f"Industry: {user['Industry']} | Handle: {user['Handle']}"

    cursor.execute("""
        SELECT * FROM POSTS 
        WHERE AuthorID = %s AND AuthorType = %s 
        ORDER BY CreatedAt DESC
    """, (id, role))
    user_posts = cursor.fetchall()
    
    conn.close()
    return render_template('public_profile.html', user=user, role=role, id=id, name=name, pic=pic, info=info, posts=user_posts)

@app.route('/messages')
def messages_inbox():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    my_id, my_role = session['user_id'], session['role'].capitalize()
    
    cursor.execute("""
        SELECT * FROM MESSAGES 
        WHERE (SenderID = %s AND SenderType = %s) OR (ReceiverID = %s AND ReceiverType = %s)
        ORDER BY SentAt DESC
    """, (my_id, my_role, my_id, my_role))
    all_msgs = cursor.fetchall()
    
    inbox = []
    seen = set()
    for msg in all_msgs:
        is_me = (msg['SenderID'] == my_id and msg['SenderType'] == my_role)
        p_id = msg['ReceiverID'] if is_me else msg['SenderID']
        p_type = msg['ReceiverType'] if is_me else msg['SenderType']
        
        if f"{p_type}_{p_id}" not in seen:
            p_name = "Unknown"
            if p_type == 'Brand':
                cursor.execute("SELECT Brandname as Name FROM BRAND WHERE BrandID = %s", (p_id,))
                res = cursor.fetchone()
                if res: p_name = res['Name']
            elif p_type == 'Influencer':
                cursor.execute("SELECT InfluencerName as Name FROM INFLUENCER WHERE InfluencerID = %s", (p_id,))
                res = cursor.fetchone()
                if res: p_name = res['Name']
            
            inbox.append({
                'PartnerID': p_id, 'PartnerType': p_type,
                'PartnerName': p_name,
                'LastMessage': msg['MessageBody'], 'SentAt': msg['SentAt']
            })
            seen.add(f"{p_type}_{p_id}")
    
    conn.close()
    return render_template('messages.html', inbox=inbox, in_chat_mode=False)

@app.route('/messages/<partner_type>/<int:partner_id>', methods=['GET', 'POST'])
def chat(partner_type, partner_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    my_id, my_role = session['user_id'], session['role'].capitalize()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        body = request.form.get('message')
        if body:
            cursor.execute("INSERT INTO MESSAGES (SenderID, SenderType, ReceiverID, ReceiverType, MessageBody) VALUES (%s, %s, %s, %s, %s)",
                           (my_id, my_role, partner_id, partner_type, body))
            conn.commit()
        return redirect(url_for('chat', partner_type=partner_type, partner_id=partner_id))

    cursor.execute("""
        SELECT * FROM MESSAGES 
        WHERE (SenderID=%s AND SenderType=%s AND ReceiverID=%s AND ReceiverType=%s)
           OR (SenderID=%s AND SenderType=%s AND ReceiverID=%s AND ReceiverType=%s)
        ORDER BY SentAt ASC
    """, (my_id, my_role, partner_id, partner_type, partner_id, partner_type, my_id, my_role))
    chat_history = cursor.fetchall()
    
    p_name = "Unknown"
    if partner_type == 'Brand':
        cursor.execute("SELECT Brandname as Name FROM BRAND WHERE BrandID = %s", (partner_id,))
        res = cursor.fetchone()
        if res: p_name = res['Name']
    elif partner_type == 'Influencer':
        cursor.execute("SELECT InfluencerName as Name FROM INFLUENCER WHERE InfluencerID = %s", (partner_id,))
        res = cursor.fetchone()
        if res: p_name = res['Name']

    conn.close()
    return render_template('messages.html', inbox=None, active_chat=chat_history, partner_name=p_name, in_chat_mode=True, p_type=partner_type, p_id=partner_id)

@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM INFLUENCER WHERE InfluencerID = %s", (session['user_id'],))
    influencer = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM POSTS 
        WHERE AuthorID = %s AND AuthorType = 'Influencer' 
        ORDER BY CreatedAt DESC
    """, (session['user_id'],))
    my_posts = cursor.fetchall()

    conn.close()
    return render_template('profile.html', influencer=influencer, posts=my_posts)

@app.route('/brand_profile.html')
def brand_profile_route():
    return redirect(url_for('brand_dashboard'))

@app.route('/my_applications.html')
def my_applications_route():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.Brandname, c.CampaignName, ic.StartDate as Date_Applied, ic.CampaignStatus as Status
        FROM INFLUENCER_CAMPAIGN ic
        JOIN CAMPAIGN c ON ic.CampaignID = c.CampaignID
        JOIN BRAND b ON c.BrandID = b.BrandID
        WHERE ic.InfluencerID = %s ORDER BY ic.StartDate DESC
    """, (session['user_id'],))
    apps = cursor.fetchall()
    conn.close()
    return render_template('my_applications.html', applications=apps)

@app.route('/manage_campaigns.html')
def manage_campaigns_route():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CAMPAIGN WHERE BrandID = %s", (session['user_id'],))
    return render_template('manage_campaigns.html', campaigns=cursor.fetchall())

@app.route('/contract.html')
def contract_route(): return render_template('contract.html')
@app.route('/brand_contract.html')
def brand_contract_route(): return render_template('brand_contract.html')

@app.route('/campaign/status/<int:campaign_id>/<action>')
def update_campaign_main_status(campaign_id, action):
    if 'user_id' not in session or session['role'] != 'brand':
        return redirect(url_for('login'))
    
    if action not in ['Active', 'Completed']:
        flash("Invalid status update.", "error")
        return redirect(url_for('manage_campaigns_route'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE CAMPAIGN 
            SET CampaignStatus = %s 
            WHERE CampaignID = %s AND BrandID = %s
        """, (action, campaign_id, session['user_id']))
        conn.commit()
        flash(f"Campaign marked as {action}!", "success")
    except Exception as e:
        print(e)
        flash("Error updating status.", "error")
    finally:
        conn.close()

    return redirect(url_for('manage_campaigns_route'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
