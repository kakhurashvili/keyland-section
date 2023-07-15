from .models import Cart ,Main_Category, SavedItem
import uuid

def saved_item(request):
    saveditems = []
    if request.user.is_authenticated:
        customer = request.user.customer
        saveditems = SavedItem.objects.filter(owner=customer)
    return {
        'saveditems': saveditems
    }



def cart_renderer(request):
      try:
         cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
      except:
         request.session['nonuser'] = str(uuid.uuid4())
         cart = Cart.objects.create(session_id = request.session['nonuser'], completed=False)
         
      return {
         'cart': cart
      }
def main_category(request):
   main_categories = Main_Category.objects.all()

   return{
       'main':main_categories
   }