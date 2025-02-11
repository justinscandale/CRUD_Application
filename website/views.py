from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
import scraper.seat_scraper
import scraper.valid_crn_scraper
from .models import Course
from . import db
import json
import scraper

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
def home():
    if(current_user):
        if request.method == 'POST':
            course = request.form.get('note')
            term = request.form.get('note-term')
            print(term)
            if len(course) != 5 or not course.isnumeric():
                flash("CRN Must be 5 Numeric Digits", category="error")
            elif scraper.valid_crn_scraper.check_available(course,term)['valid'] == 0: 
                flash(f"Failed to Add CRN {course}", category="error")
            else:
                scraper_dict = scraper.valid_crn_scraper.check_available(course,term)
                course_info = scraper_dict['course_info']
                course_name = scraper_dict['course_name']
                seats_available = scraper.seat_scraper.check_available(course,term)
                course_exsists = Course.query.filter_by(data=course,term=term,user_id=current_user.id).first()
                if(course_exsists):
                    flash(f"Course with CRN: {course} & term {term} already in database",category="error")
                else:
                    new_course = Course(data=course, course_name=course_name, seats_available= seats_available, course_info = course_info, user_id=current_user.id, term=term)
                    db.session.add(new_course)
                    db.session.commit()
                    flash("Course added!",category="success")

    return render_template("home.html", user = current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    course = json.loads(request.data)
    courseID = course['noteId']
    course = Course.query.get(courseID)
    if course:
        if course.user_id == current_user.id:
            db.session.delete(course)
            db.session.commit()
    
    return jsonify({})

@views.route('/refresh-data', methods=['POST'])
def refresh_data():
    db.session.begin()
    for course in current_user.courses:
        course.seats_available = scraper.seat_scraper.check_available(course.data,course.term)
    db.session.commit()
    # Return a success message
    return jsonify({'message': 'Data refreshed successfully'}), 200