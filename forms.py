from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, URL, Optional, Length
from flask_ckeditor import CKEditorField

fruit = [('watermelon', 'watermelon'), ('Dragonfruit', 'Dragonfruit'), ('banana', 'banana'), ('pineapple', 'pineapple'),
         ('melon', 'melon'), ('mango', 'mango'), ('kiwi', 'kiwi'),
         ('pomegranate', 'pomegranate'), ('strawberry', 'strawberry')]
crunch = [('almond crocanti', 'almond crocanti'), ('chips ahoy!', 'chips ahoy!'),
          ('dark conguitos', 'dark conguitos'), ('oreo crumbs', 'oreo crumbs'),
          ('Honey Quinoa Granola', 'Honey Quinoa Granola'), ('Mini Cookies', 'Mini Cookies'),
          ('Lotus Crushed Caramel Biscoff Biscquit', 'Lotus Crushed Caramel Biscoff Biscquit'),
          ('Lacasitos', 'Lacasitos')]
sauce = [('white chococrock','white chococrock'), ('dark chocolate', 'dark chocolate'),
         ('dulce de leche', 'dulce de leche'), ('white chocolate', 'white chocolate'),
         ('fruit of the forest', 'fruit of the forest'), ('wild strawberries', 'wild strawberries'),
         ('mango sauce', 'mango sauce'), ('green apple', 'green apple'), ('passion fruit', 'passion fruit'),
         ('honey', 'honey'), ('nocilla/hazelnut', 'nocilla/hazelnut'), ('coffee', 'coffee'),
         ('cherry', 'cherry'), ('Lotus Biscoff Cookie Sauce', 'Lotus Biscoff Cookie Sauce'),
         ('Ovaltime Crunchy Cream', 'Ovaltime Crunchy Cream'), ('Pistachio', 'Pistachio')]
TOPPINGS_DICT = {
    'watermelon': '#FFE3EB',
    'Dragonfruit': '#C13969',
    'banana': '#FFE36D',
    'pineapple': '#FFF547',
    'melon': '#EEDB69',
    'mango': '#FFDCB4',
    'kiwi': '#A9C77E',
    'pomegranate': '#DF5555',
    'strawberry': '#FF8F8F',
    'almond crocanti': '#FACF81',
    'chips ahoy!': '#C39D97',
    'dark conguitos': '#6B3D38',
    'oreo crumbs': '#2C2E32',
    'Honey Quinoa Granola': '#D7C0A2',
    'Mini Cookies': '#AA7733',
    'Lotus Crushed Caramel Biscoff Biscquit': '#DDAD75',
    'Lacasitos': '#FFB22C',
    'white chococrock': '#C0C6B5',
    'dark chocolate': '#2D1903',
    'dulce de leche': '#A97947',
    'white chocolate': '#EDE6D6',
    'fruit of the forest': '#ED92BF',
    'wild strawberries': '#FF8F8F',
    'mango sauce': '#FFBF34',
    'green apple': '#76DB6B',
    'passion fruit': '#DD718D',
    'honey': '#E79A3F',
    'nocilla/hazelnut': '#763814',
    'coffee': '#6F4E37',
    'cherry': '#B62625',
    'Lotus Biscoff Cookie Sauce': '#DDAD75',
    'Ovaltime Crunchy Cream': '#F25D1D',
    'Pistachio': '#93C572',
}
all_toppings = sauce + crunch + fruit

# WTForm for creating a combo
class CreateCombo(FlaskForm):
    category = SelectField('Choose: Tub or Sanum', choices = [('...', '...'), ('Tub', 'Tub'), ('Sanum', 'Sanum')], render_kw={'onchange': "myFunction()"}, validators=[DataRequired()])
    subcategory_sanum = SelectField('Pick a size', choices = [('...', '...'), ('Petit', 'Petit'), ('Regular', 'Regular')], render_kw={'onchange': "myFunction2()"}, validators=[DataRequired()])
    subcategory_tub = SelectField('Pick a size', choices = [('...', '...'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], render_kw={'onchange': "myFunction3()"}, validators=[DataRequired()])
    # sanum toppings
    fruit1 = SelectField('Choose Fruit 1', choices=fruit, validators=[DataRequired()])
    fruit2 = SelectField('Choose Fruit 2', choices=fruit, validators=[DataRequired()])
    fruit3 = SelectField('Choose Fruit 3', choices=fruit, validators=[DataRequired()])
    crunch1 = SelectField('Choose Crunch 1', choices=crunch, validators=[DataRequired()])
    crunch2 = SelectField('Choose Crunch 2', choices=crunch, validators=[DataRequired()])
    sauce1 = SelectField('Choose a Sauce', choices=sauce, validators=[DataRequired()])
    # tub toppings
    topping1 = SelectField('Choose topping 1', choices=all_toppings, validators=[DataRequired()])
    topping2 = SelectField('Choose topping 2', choices=all_toppings, validators=[DataRequired()])
    topping3 = SelectField('Choose topping 3', choices=all_toppings, validators=[DataRequired()])

    ask_user = SelectField('Satisfied?', choices=[('...', '...'), ('yes', 'yes')], validators=[DataRequired()], render_kw={'onchange': "myFunction4()"})
    combo_name = StringField("Your name for your combination e.g. ChocoDelightx2", validators=[DataRequired(), Length(min=1, max=25)])
    # rating = DecimalField('Your rating:', places=2, validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create a form to register new users
class RegisterForm(FlaskForm):
    name = StringField("Your Username e.g. Earl or XCalibur100 without spaces", validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField("Sign Me Up!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    name = StringField("Your Username e.g. Earl or XCalibur100 without spaces", validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField("Let Me In!")


# Create a form to add ratings
class RatingForm(FlaskForm):
    rating = DecimalField('Your rating over 10:', places=2, validators=[DataRequired()])
    comment = TextAreaField('Brief comment...', validators=[Optional(), Length(max=200)])
    submit = SubmitField("Submit Rating", validators=[DataRequired()], render_kw={'onclick': "myFunction6()"})
