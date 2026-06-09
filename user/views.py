from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect, render


def register_view(request):

    if request.method == 'POST': #verifica se o método da requisição é POST, ou seja, se o formulário foi enviado
        user_form = UserCreationForm(request.POST) #cria uma instância do formulário de criação de usuário, preenchendo-o com os dados enviados pelo usuário
        if user_form.is_valid(): #verifica se os dados do formulário são válidos, ou seja, se atendem aos requisitos de validação definidos no formulário
            user_form.save() #salva o novo usuário no banco de dados
            return redirect('pj_list') #redireciona o usuário para a página de login após o registro bem-sucedido
    else:
        user_form = UserCreationForm() #cria uma instância do formulário de criação de usuário, que é fornecido pelo Django
    return render(
        request,
        'register.html',
        {'user_form': user_form} #dicionário de contexto, onde a chave 'user_form' é usada para acessar os dados no template, e o valor é a instância do formulário de criação de usuário
    )

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username") #obtém o nome de usuário enviado pelo formulário de login
        password = request.POST.get("password") #obtém a senha enviada pelo formulário de login
        user = authenticate(request, username=username, password=password) #autentica o usuário usando as credenciais fornecidas

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            login_form = AuthenticationForm()
        
    else:
        login_form = AuthenticationForm()
    
    return render(request, 'login.html', {'login_form':login_form})

def logout_view(request):
    logout(request)
    return redirect('home')