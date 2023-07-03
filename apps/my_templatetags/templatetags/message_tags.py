from django import template


register = template.Library()


@register.filter(name='bootstrap')
def bootstrap(message):
    """
    Заменяет значения тегов сообщений Django на значения Bootstrap
    """

    mapping = {'error': 'danger',
               'success': 'success'}
    return mapping.get(str(message), '')