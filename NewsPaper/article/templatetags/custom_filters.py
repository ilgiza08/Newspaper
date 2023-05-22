from django import template
 
register = template.Library()

@register.filter(name='Censor')
def Censor(value):
    text = value.lower().split()
    variants = ['скотина', 'сволочь', 'гадина', 'мурло',
'ублюдок','падла','сука','тварь','мразь','выродок' , 'отродье', 'гнида',
'подонок','погань']

    filtered_text = ' '.join([word for word in text if word not in variants])
    return filtered_text

