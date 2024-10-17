from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from . import forms           # Si "from .forms import LoginForm, SignupForm" => form = LoginForm()
from django.views.generic import View





class LoginPage(View):      #"view" =class prédéfinie dans django
    form_class = forms.LoginForm
    template_name ='authentification/connexion.html'
    
    # méthode qui envoie un formulaire vierge (page web), il attend q l'user clique sur connexion (input)
    def get(self, request):        #self=classe (attributs de la classe: view, from_class, temlate_class)
        form = self.form_class()          #instance=objet (self représente l'instance actuelle de cette classe)
        #return permet de retourner le formulaire fait dans le html 
        return render(request, self.template_name, {'form': form})      
                
        
      
            
     #     en cliquant sur l'input (connexion), il appelle la méthode POST  
    def post(self, request):  #dans cette méthode, les 2 var du formulaire sont remplis dans l'objet POST
        form = self.form_class(request.POST)   #resquest.POST=objet dynamique qui a 2 éléments : "user" ,"pswd"
        if form.is_valid(): # condition de la forme du formulaire
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:  
                login(request, user)
                return redirect('accueil')  
            else:
                form.add_error(None, "Identifiants invalides.")
        
        return render(request, self.template_name, {'form': form})
                
        

          
          
class SignupPage(View):     
    form_class=forms.SignupForm             #Signup=attribut de "forms"
    template_name='authentification/inscription.html'
    
    def get(self, request):        
        form = self.form_class()         
        return render(request, self.template_name, {'form': form})
         
        
    def post(self, request):  
        form = self.form_class(request.POST)  
        if form.is_valid(): 
            user = form.save()
            login(request, user)
            return redirect('accueil') # lien vers la vue de la page d'accueil
        return render(request, self.template_name, {'form': form})
            
    
def logout_user(request):
    logout(request)
    return redirect('login')   
            
            

            
    
            
        