from flask import Flask, flash, render_template, request
import sqlite3


dataBase = sqlite3.connect('DB.db', check_same_thread=False)
base_cursor = dataBase.cursor()
user_date = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'contraseñasecreta'

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def Iniciar_sesion():
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']

    base_cursor.execute(f'SELECT contraseña FROM login WHERE usuario="{usuario}"')
    contraseña_user = base_cursor.fetchall()
        
    contraseñaCorrecta = False

    for buscarContraseña in contraseña_user:
        for filtrarContraseña in buscarContraseña:
            if filtrarContraseña == contraseña:
                contraseñaCorrecta = True
                flash(f'bienvenido {usuario}', 'success')

            elif contraseña not in filtrarContraseña:
                contraseñaCorrecta = True
                flash('La contraseña es incorrecta', 'danger')
                
        if contraseñaCorrecta == True:
            break
    if contraseñaCorrecta == False:
        flash('El usuario ingresado es incorrecto', 'danger')
        
    return render_template('index.html')

@app.route('/registrar')
def register():
    return render_template('crearusuario.html')

@app.route('/login/registrarse', methods=['POST'])
def registrarse():
    usuario = request.form['usuario']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    
    user_register = usuario, correo, contraseña
    usuarioDB = base_cursor.execute('SELECT usuario FROM login')
    datos_usuario = usuarioDB.fetchall()
        
    correoDB = base_cursor.execute('SELECT correo FROM login')
    datos_correo = correoDB.fetchall()
        
    verificarUsuario = True
        
    for buscarUsuario in datos_usuario:
        for limpiarDatos in buscarUsuario:
            if limpiarDatos == usuario:
                verificarUsuario = False
                flash('El usuario ingresado ya esta en uso', 'danger')
            
        if verificarUsuario == False:
            break
    if verificarUsuario == True:
        verificarCorreo = True
        for buscarCorreo in datos_correo:
            for limpiarCorreo in buscarCorreo:
                if limpiarCorreo == correo:
                    verificarCorreo = False
                    flash('El correo ingresado ya esta en uso', 'danger')
                
            if verificarCorreo == False:
                break
        if verificarCorreo == True:
            base_cursor.execute('INSERT into login(usuario, correo, contraseña) VALUES(?,?,?)', user_register)
            dataBase.commit()
            flash('Registrado con exito!', 'success')
            return render_template('index.html')
            
    return render_template('crearusuario.html')

@app.route('/verificarcorreo')
def verificarPass():
    return render_template('verificarpass.html')

@app.route('/login/verificacion', methods=['POST'])
def verificacion():
    usuario = request.form['usuario']
    correo = request.form['correo']
    
    usuarioDB = base_cursor.execute(f'SELECT usuario FROM login WHERE correo="{correo}"')
    datos_usuario = usuarioDB.fetchall()
        
    confirmarUsuario = False
    for buscarUsuario in datos_usuario:
        for limpiarUsuario in buscarUsuario:
            if limpiarUsuario == usuario:
                confirmarUsuario = True
                user_date.append(usuario)
                flash('correo verificado con exito', 'success')
                return render_template('cambiarpass.html')
            
        if confirmarUsuario == True:
            break
    if confirmarUsuario == False:
        flash('Los datos ingresados son erroneos', 'danger')

    return render_template('verificarpass.html')

@app.route('/cambiarcontraseña')
def indexPass():
    return render_template('cambiarpass.html')

@app.route('/login/verificacion/cambiarcontraseña', methods=['POST'])
def cambiarContraseña():
    contraseña = request.form['contraseña']
    confirmarPass = request.form['confirmarPass']
    
    userJoin = ''.join(user_date)
    
    
    contraseñaDB = base_cursor.execute(f'SELECT contraseña FROM login WHERE usuario="{userJoin}"')
    datos_contraseña = contraseñaDB.fetchall()
        
    contraseñaCorrecta = True
        
    passwordContainer = ''
    for buscarContraseña in datos_contraseña:
        for limpiarDatos in buscarContraseña:
            passwordContainer = passwordContainer.join(limpiarDatos)
            
                    

            if confirmarPass == passwordContainer:
                flash('esta contraseña ya la utilizaste, usa otra!', 'danger')
                contraseñaCorrecta = False
                            
            elif contraseñaCorrecta == True:
                if contraseña == confirmarPass:
                    base_cursor.execute(f' UPDATE login SET contraseña="{confirmarPass}" WHERE usuario="{userJoin}"')
                    dataBase.commit()
                    flash('contraseña cambiada con exito!', 'success')
                    user_date.clear()
                    return render_template('index.html')
                                
                else:
                    flash('las contraseñas no coinciden', 'danger')
                
    return render_template('cambiarpass.html')

if __name__=='__main__':
    app.run(debug=True, port=150)
                    
                                  
        