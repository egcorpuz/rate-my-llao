from datetime import date, datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Float, and_, func, desc
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreateCombo, RegisterForm, LoginForm, RatingForm, TOPPINGS_DICT
import os

YEAR=date.today().strftime("%Y")

# implements admin only on some routes
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.name not in ['AdminGian', 'AdminRey']:
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated_function

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
Bootstrap5(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

login_manager = LoginManager()
login_manager.init_app(app)


# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# Configure Tables and Create Database
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = "llao_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    #This will act like a List of Combo objects attached to each User.
    #The "author" refers to the author property in the LlaoCombo class.
    combos = relationship("LlaoCombo", back_populates="author")
    ratings = relationship("Rating", back_populates="rating_author")


class LlaoCombo(db.Model):
    __tablename__ = "llaollao_combos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Create Foreign Key, "llao_users.id" the llao_users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("llao_users.id"))
    # Create reference to the User object. The "combos" refers to the combos property in the User class.
    author = relationship("User", back_populates="combos")
    
    # these values are calculated later
    # ranking -> should be updated every new rating is posted, or when home is reloaded
    # overall_rating -> average of combo_ratings per combo_id
    overall_rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    number_of_ratings: Mapped[int] = mapped_column(Integer, nullable=True)
    
    combo_name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    tub_type: Mapped[str] = mapped_column(String(20), nullable=False)
    tub_size: Mapped[str] = mapped_column(String(20), nullable=False)
    toppings: Mapped[str] = mapped_column(String(500), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)

    combo_ratings = relationship("Rating", back_populates="parent_combo", lazy="dynamic")

class Rating(db.Model):
    __tablename__ = "ratings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("llao_users.id"))
    rating_author = relationship("User", back_populates="ratings")

    # Create Foreign Key, "llao_users.id" the llao_users refers to the tablename of User.
    # Create reference to the User object. The "combos" refers to the combos property in the User class.
    combo_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("llaollao_combos.id"))
    # comment
    text: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)

    parent_combo = relationship("LlaoCombo", back_populates="combo_ratings")


with app.app_context():
    db.create_all()
    
# Calculate overall rating and ranking
def reorder_combo():
    result = db.session.execute(db.select(LlaoCombo))
    # ranking code should happen here through query

    combos = result.scalars().all()
    # implement averaging of all ratings of combo
    for combo in combos:
        rating_count_query = db.session.query(Rating.rating).filter_by(combo_id=combo.id).count()
        rating_count_result = rating_count_query
        if rating_count_result:
            combo.number_of_ratings = rating_count_result
        else:
            combo.number_of_rating = 0
        average_rating_query = db.session.query(func.avg(Rating.rating)).filter_by(combo_id=combo.id)
        average_rating_result = average_rating_query.scalar()
        if average_rating_result:
            combo.overall_rating = average_rating_result
        else:
            combo.overall_rating = 0
        db.session.commit()
    # implement ranking
    ordered_result = db.session.execute(db.select(LlaoCombo).order_by(desc(LlaoCombo.overall_rating)))
    ordered_combos = ordered_result.scalars().all()
    rank = 0
    for ordered_combo in ordered_combos:
        rank += 1
        ordered_combo.ranking = rank
        db.session.commit()

@app.route('/')
def secrets():
    return render_template("easteregg.html")

@app.route('/my-portfolio')
def my_portfolio():
    return render_template("portfoliopage.html")

@app.route('/buildllao')
def build_llao():
    result = db.session.execute(db.select(LlaoCombo))
    # ranking code should happen here through query

    combos = result.scalars().all()
    # implement averaging of all ratings of combo
    for combo in combos:
        rating_count_query = db.session.query(Rating.rating).filter_by(combo_id=combo.id).count()
        rating_count_result = rating_count_query
        if rating_count_result:
            combo.number_of_ratings = rating_count_result
        else:
            combo.number_of_rating = 0
        average_rating_query = db.session.query(func.avg(Rating.rating)).filter_by(combo_id=combo.id)
        average_rating_result = average_rating_query.scalar()
        if average_rating_result:
            combo.overall_rating = average_rating_result
        else:
            combo.overall_rating = 0
        db.session.commit()
    # implement ranking
    ordered_result = db.session.execute(db.select(LlaoCombo).order_by(desc(LlaoCombo.overall_rating)))
    ordered_combos = ordered_result.scalars().all()
    rank = 0
    for ordered_combo in ordered_combos:
        rank += 1
        ordered_combo.ranking = rank
        db.session.commit()
    if len(ordered_combos) < 2:
        return render_template("index0.html")
    if len(ordered_combos) > 20:
        ordered_combos = ordered_combos[:20]
        
    return render_template("index.html", all_combos=ordered_combos, current_year=YEAR, color_dict=TOPPINGS_DICT)

@app.route('/buildllao/TubsOnly')
def tubs_only():
    reorder_combo()
    query = db.session.query(LlaoCombo).filter(LlaoCombo.tub_type == 'Tub').order_by(desc(LlaoCombo.overall_rating))
    tub_combos = query.all()
    if len(tub_combos) < 2:
        return render_template("index0.html")
    if len(tub_combos) > 20:
        tub_combos = tub_combos[:20]
        
    return render_template("tubsorsanumonly.html", all_combos=tub_combos, current_year=YEAR, color_dict=TOPPINGS_DICT, text_to_show="Tubs")

@app.route('/buildllao/SanumOnly')
def sanum_only():
    reorder_combo()
    query = db.session.query(LlaoCombo).filter(LlaoCombo.tub_type == 'Sanum').order_by(desc(LlaoCombo.overall_rating))
    sanum_combos = query.all()
    if len(sanum_combos) < 2:
        return render_template("index0.html")
    if len(sanum_combos) > 20:
        sanum_combos = sanum_combos[:20]
        
    return render_template("tubsorsanumonly.html", all_combos=sanum_combos, current_year=YEAR, color_dict=TOPPINGS_DICT, text_to_show="Sanum")

@app.route('/buildllao/ViewAll')
def view_all():
    result = db.session.execute(db.select(LlaoCombo))
    # ranking code should happen here through query

    combos = result.scalars().all()
    if not combos:
        flash("Create more combos.")
        return redirect(url_for('build_llao'))
    # implement averaging of all ratings of combo
    for combo in combos:
        rating_count_query = db.session.query(Rating.rating).filter_by(combo_id=combo.id).count()
        rating_count_result = rating_count_query
        if rating_count_result:
            combo.number_of_ratings = rating_count_result
        else:
            combo.number_of_rating = 0
        average_rating_query = db.session.query(func.avg(Rating.rating)).filter_by(combo_id=combo.id)
        average_rating_result = average_rating_query.scalar()
        if average_rating_result:
            combo.overall_rating = average_rating_result
        else:
            combo.overall_rating = 0
        db.session.commit()
    # implement ranking
    ordered_result = db.session.execute(db.select(LlaoCombo).order_by(desc(LlaoCombo.overall_rating)))
    ordered_combos = ordered_result.scalars().all()
    rank = 0
    for ordered_combo in ordered_combos:
        rank += 1
        ordered_combo.ranking = rank
        db.session.commit()
    if len(ordered_combos) < 2:
        flash("Create more combos.")
        return redirect(url_for('build_llao'))
    return render_template("allcombos.html", all_combos=ordered_combos, current_year=YEAR)

@app.route("/buildllao/combo/<int:combo_id>", methods=["GET", "POST"])
def show_combo(combo_id):
    requested_combo = db.get_or_404(LlaoCombo, combo_id)
    rating_form = RatingForm()
    if current_user.is_authenticated:
        user_rating = Rating.query.filter(and_(Rating.author_id == current_user.id, Rating.combo_id == combo_id)).first()
        # get user rating 
        if not user_rating:
            user_has_rated = False
        else:
            user_has_rated = True
    else:
        user_rating = None
        user_has_rated = None
    if rating_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or sign up to rate.")
            return redirect(url_for("login"))
        
        if rating_form.rating.data < 1 or rating_form.rating.data > 10:
            flash("Rating can only be between 1 to 10.")
            return redirect(url_for('show_combo', combo_id=requested_combo.id))
        

        new_rating = Rating(
            text=rating_form.comment.data.strip(),
            rating=rating_form.rating.data,
            rating_author=current_user,
            parent_combo=requested_combo,
            date=datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
        )
        db.session.add(new_rating)
        db.session.commit()
        reorder_combo()
        return redirect(url_for('show_combo', combo_id=requested_combo.id))
    return render_template("combopage.html", combo=requested_combo, is_edit=False, form=rating_form, user_rating=user_rating, current_year=YEAR, current_user_has_rated=user_has_rated)

@app.route("/buildllao/edit-rating/<int:rating_id>", methods=['GET', 'POST'])
def edit_rating(rating_id):
    # edit-rating/<rating_id>?combo_id=<combo_id> # 
    current_rating = db.get_or_404(Rating, rating_id)
    combo_id = request.args.get('combo_id')
    if current_user.id != current_rating.author_id:
        flash("Not allowed! You can't modify someone else's rating by just knowing the routes. :P")
        return redirect(url_for('show_combo', combo_id=combo_id))
    current_combo = db.get_or_404(LlaoCombo, combo_id)
    rating_to_edit = db.get_or_404(Rating, rating_id)
    rating_form = RatingForm(
        comment=rating_to_edit.text,
        rating=rating_to_edit.rating
    )
    if rating_form.validate_on_submit():
        if rating_form.rating.data < 1 or rating_form.rating.data > 10:
            flash("Rating can only be between 1 to 10.")
            return redirect(url_for('show_combo', combo_id=current_combo.id))
        rating_to_edit.text = rating_form.comment.data.strip()
        rating_to_edit.rating = rating_form.rating.data
        rating_to_edit.rating_author = current_user
        rating_to_edit.date=datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
        db.session.commit()
        reorder_combo()
        return redirect(url_for("show_combo", combo_id=current_combo.id))
    return render_template("combopage.html", combo=current_combo, form=rating_form, is_edit=True, user_rating=None, current_year=YEAR, current_user_has_rated=None)

@app.route("/buildllao/delete-rating/<int:rating_id>")
def delete_rating(rating_id):
    # delete-rating/<rating_id>?combo_id=<combo_id>
    current_rating = db.get_or_404(Rating, rating_id)
    combo_id = request.args.get('combo_id')
    if current_user.id != current_rating.author_id:
        flash("Not allowed! You can't modify someone else's rating by just knowing the routes. :P")
        return redirect(url_for('show_combo', combo_id=combo_id))
    current_combo = db.get_or_404(LlaoCombo, combo_id)
    rating_to_delete = db.get_or_404(Rating, rating_id)
    db.session.delete(rating_to_delete)
    db.session.commit()
    reorder_combo()
    return redirect(url_for("show_combo", combo_id=current_combo.id))

@app.route("/buildllao/MixEm", methods=['GET', 'POST'])
def create_combo():
    if not current_user.is_authenticated:
        flash("You need to login or sign up to submit a combo.")
        return redirect(url_for("login"))
    choose_form = CreateCombo()
    if choose_form.validate_on_submit():
        container_type = choose_form.category.data
        if container_type == 'Tub':
            container_size = choose_form.subcategory_tub.data
            toppings = []
            topping1 = choose_form.topping1.data
            toppings.append(topping1)
            if container_size != 'Small':
                topping2 = choose_form.topping2.data
                toppings.append(topping2)
                topping3 = choose_form.topping3.data
                toppings.append(topping3)
            
            # Checks if tub type, size, and topping combination already exists
            existing_combo_tub_size = LlaoCombo.query.filter_by(tub_size=container_size).first()
            existing_combo_toppings = LlaoCombo.query.filter_by(toppings=str(toppings)).first() 
            if existing_combo_tub_size and existing_combo_toppings:
                flash(f'Would you believe? This tub size and toppings combo already exists here.'
                      f'The combo is under {existing_combo_toppings.combo_name}.\n' 
                      f'Try and search this combo in the all combos pages.')
                return redirect(url_for('create_combo'))   
            # Checks if combo name already exists    
            existing_combo = LlaoCombo.query.filter_by(combo_name=choose_form.combo_name.data).first()
            if existing_combo:
                flash('Sorry, that combo name already exists. Choose another.')
                return redirect(url_for('create_combo'))

            new_combo = LlaoCombo(
                combo_name = choose_form.combo_name.data,
                tub_type = container_type,
                tub_size = container_size,
                toppings = str(toppings),
                author = current_user,
                date=date.today().strftime("%B %d, %Y")
            )

            db.session.add(new_combo)
            db.session.flush()
            get_id = new_combo.id
            db.session.commit()
            return redirect(url_for("show_combo", combo_id=get_id))
        elif container_type == 'Sanum':
            toppings = []
            container_size = choose_form.subcategory_sanum.data
            fruit1 = choose_form.fruit1.data
            fruit2 = choose_form.fruit2.data
            crunch1 = choose_form.crunch1.data
            sauce1 = choose_form.sauce1.data
            toppings.append(fruit1)
            toppings.append(fruit2)
            toppings.append(crunch1)
            toppings.append(sauce1)
            if container_size != 'Petit':
                fruit3 = choose_form.fruit3.data
                crunch2 = choose_form.crunch2.data
                toppings.append(fruit3)
                toppings.append(crunch2)
                
            # Checks if tub type, size, and topping combination already exists
            existing_combo_tub_size = LlaoCombo.query.filter_by(tub_size=container_size).first()
            existing_combo_toppings = LlaoCombo.query.filter_by(toppings=str(toppings)).first() 
            if existing_combo_tub_size and existing_combo_toppings:
                flash(f'Would you believe? This sanum size and toppings combo already exists here.'
                      f'The combo is under {existing_combo_toppings.combo_name}.\n' 
                      f'Try and search this combo in the all combos pages.')
                return redirect(url_for('create_combo'))            
            # Checks if combo name already exists
            existing_combo = LlaoCombo.query.filter_by(combo_name=choose_form.combo_name.data).first()
            if existing_combo:
                flash('That combo name already exists. Choose another.')
                return redirect(url_for('create_combo'))

            new_combo = LlaoCombo(
                combo_name = choose_form.combo_name.data,
                tub_type = container_type,
                tub_size = container_size,
                toppings = str(toppings),
                author = current_user,
                date=date.today().strftime("%B %d, %Y")
            )

            db.session.add(new_combo)
            db.session.flush()
            get_id = new_combo.id
            db.session.commit()
            return redirect(url_for("show_combo", combo_id=get_id))
    return render_template("tuborsanum.html", form=choose_form, display="none", current_year=YEAR)

@app.route('/buildllao/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already registered!")
        return redirect(url_for("home"))
    register_form = RegisterForm()
    if  register_form.validate_on_submit():
        # Hashing and salting the password entered by the user
        hash_and_salted_password = generate_password_hash(
            register_form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        # Check if username has spaces:
        if ' ' in register_form.name.data:
            flash('Spaces in username not allowed.')
            return redirect(url_for('register'))
        # Check if user already exists
        existing_user = User.query.filter_by(name=register_form.name.data).first()
        if existing_user:
            flash('You have already signed up with this username. Please log in instead.')
            return redirect(url_for('login'))
        # else
        # Storing the hashed password in our database together with the new user
        new_user = User(
            name=register_form.name.data,
            password=hash_and_salted_password,
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('build_llao'))
    return render_template("register.html", form=register_form, current_year=YEAR)

@app.route('/buildllao/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for("home"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        name = login_form.name.data
        password = login_form.password.data
        result = db.session.execute(db.select(User).where(User.name == name))
        # Note, combo name in db is unique so will only have one result.
        user = result.scalar()
        if not user:
            flash("Username does not exist!")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect!")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('build_llao'))
    return render_template("login.html", form=login_form, current_year=YEAR)

@app.route('/buildllao/delete-combo/<int:combo_id>')
@admin_only
def delete_combo(combo_id):
    combo_to_delete = db.get_or_404(LlaoCombo, combo_id)
    # ratings_to_delete = db.session.query(Rating.rating).filter_by(combo_id=combo_id)
    query = db.session.query(Rating).filter(Rating.combo_id == combo_id)
    ratings_to_delete = query.all()
    if ratings_to_delete:
        for rating in ratings_to_delete:
            db.session.delete(rating)
            db.session.commit()
    db.session.delete(combo_to_delete)
    db.session.commit()
    return redirect(url_for('view_all'))

@app.route('/buildllao/logout')
def logout():
    logout_user()
    return redirect(url_for('build_llao'))


if __name__ == "__main__":
    app.run(debug=False)
