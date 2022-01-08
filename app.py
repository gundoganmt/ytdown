from ytdown import create_app
from ytdown import db
#from ytdown.models import Admin
from ytdown.models import Video, Resolutions
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash

app = create_app()

# @app.before_first_request
# def populateDb():
#     admin = db.session.query(Admin).first()
#     if not admin:
#         admin = Admin(username='admin', email="admin@gmail.com", full_name="John Doe",
#             password=generate_password_hash("123456", method='sha256', salt_length=7))
#         db.session.add(admin)
#         db.session.commit()
#     return True

class MyModelView(ModelView):

    def is_accessible(self):
        return True

    # can_edit = True
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    details_modal = True

admin = Admin(app, name='ytdown', template_mode='bootstrap3')
admin.add_view(MyModelView(Video, db.session))
admin.add_view(MyModelView(Resolutions, db.session))

if __name__ == '__main__':
    app.run(debug=True)
