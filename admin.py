from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/generacion_informes')
def generacion_informes():
    return render_template('F_admin/GeneracionInformes.html')

@admin_bp.route('/gestion_inventarios')
def gestion_inventarios():
    return render_template('F_admin/GestionInventarios.html')

@admin_bp.route('/gestion_software')
def gestion_software():
    return render_template('F_admin/GestionSoftware.html')

@admin_bp.route('/informe_seguridad')
def informe_seguridad():
    return render_template('F_admin/mensajes_soporte.html')

@admin_bp.route('/panel_control')
def panel_control():
    return render_template('F_admin/PanelControl.html')

@admin_bp.route('/modulo_contable')
def modulo_contable():
    return render_template('F_admin/ModuloContable.html')
