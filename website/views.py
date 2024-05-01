from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
import scraper.seat_scraper
import scraper.valid_crn_scraper
from .models import Note
from . import db
import json
import scraper

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
def home():
    if(current_user):
        if request.method == 'POST':
            note = request.form.get('note')
            term = request.form.get('note-term')
            print(term)
            if len(note) != 5 or not note.isnumeric():
                flash("CRN Must be 5 Numeric Digits", category="error")
            elif scraper.valid_crn_scraper.check_available(note,term)['valid'] == 0: 
                flash(f"Failed to Add CRN {note}", category="error")
            else:
                scraper_dict = scraper.valid_crn_scraper.check_available(note,term)
                course_info = scraper_dict['course_info']
                course_name = scraper_dict['course_name']
                seats_available = scraper.seat_scraper.check_available(note,term)
                note_exsists = Note.query.filter_by(data=note,term=term,user_id=current_user.id).first()
                if(note_exsists):
                    flash(f"Course with CRN: {note} & term {term} already in database",category="error")
                else:
                    new_note = Note(data=note, course_name=course_name, seats_available= seats_available, course_info = course_info, user_id=current_user.id, term=term)
                    db.session.add(new_note)
                    db.session.commit()
                    flash("Course added!",category="success")

    return render_template("home.html", user = current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteId']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/refresh-data', methods=['POST'])
def refresh_data():
    db.session.begin()
    for note in current_user.notes:
        note.seats_available = scraper.seat_scraper.check_available(note.data,note.term)
    db.session.commit()
    # Return a success message
    return jsonify({'message': 'Data refreshed successfully'}), 200