from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DateRequired
from company_blog.models import BlogCategory


class BlogCategoryForm(FlaskForm):
    category = StringField('カテゴリ名', validators=[DateRequired()])
    submit = SubmitField('保存')

    def validate_category(self, field):
        if BlogCategory.query.filter_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリ名は既に使われています')
