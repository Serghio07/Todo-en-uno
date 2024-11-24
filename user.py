from flask import Blueprint, render_template, request, session

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

@user_bp.route('/informes')
def informes():
    return render_template('F_user/Informes.html')

@user_bp.route('/InfoUsuario')
def InfoUsuario():
    return render_template('info_user.html')

@user_bp.route('/software')
def software():
    return render_template('F_user/Software.html')

@user_bp.route('/soporte')
def soporte():
    return render_template('F_user/Soporte.html')

@user_bp.route('/version_freemium')
def version_freemium():
    return render_template('VersionFreemium.html')


@user_bp.route('/panel_control')
def user_panel_control():
    return render_template('F_user/UserPanelControl.html')

@user_bp.route('/comprar_software')
def comprar_software():
    software_id = request.args.get('software_id')
    user = session.get('user')
    if not user:
        return "Usuario no autenticado", 403
    return render_template('F_user/comprarSoftware.html', software_id=software_id, user=user)

@user_bp.route('/canjear')
def canjear():
    # Esta ruta renderiza la página donde se introduce el código
    return render_template('F_user/canjear_codigo.html')
