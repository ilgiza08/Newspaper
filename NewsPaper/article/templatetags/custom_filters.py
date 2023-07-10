from django import template
register = template.Library()


variants = ['скотина', 'сволочь', 'гадина', 'мурло',
            'ублюдок', 'падла', 'сука', 'тварь', 'мразь', 'выродок',
            'отродье', 'гнида', 'подонок', 'погань']


@register.filter(name='Censor')
def Censor(value):
    text = value.lower().split()
    filtered_text = ' '.join([word for word in text if word not in variants])
    return filtered_text


@register.filter(name='replace_letters')
def replace_letters(text):
    text = text.lower().split()
    result = []
    for word in text:
        if word in variants:
            result.append(word[0] + '*'*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)
