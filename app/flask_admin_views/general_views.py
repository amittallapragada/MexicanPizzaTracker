from flask_admin import BaseView, expose
from flask_admin.contrib.mongoengine import ModelView
from supported_restaurants import SUPPORTED_RESTAURANTS


class ItemView(ModelView):
    pass

class SearchItemsView(BaseView):
    @expose("/")
    def index(self):
        menus = {}
        for key, restaurant in SUPPORTED_RESTAURANTS.items():

            menus[key] = restaurant['handler'].get_default_menu()

        return self.render('admin/search_items.html', menus=menus)

