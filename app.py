import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB para aceptar PDF base64

# ── Configuracion Multi-Empresa ──────────────────────────────
NOMBRE_EMPRESA    = os.environ.get('NOMBRE_EMPRESA', 'InfinityBox').strip()
FORMULARIO_DESTINO = os.environ.get('FORMULARIO_DESTINO', 'cotizar@infinitybox.cl').strip().lower()
RESEND_API_KEY     = os.environ.get('RESEND_API_KEY', '').strip()

# ── Base de datos ─────────────────────────────────────────────
def get_db_type():
    return 'postgres' if os.environ.get('DATABASE_URL', '').strip() else 'sqlite'

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL', '').strip()
    if db_url:
        import psycopg
        conn = psycopg.connect(db_url)
        return conn
    else:
        conn = sqlite3.connect('clientes_nuevos.db')
        conn.row_factory = sqlite3.Row
        return conn

def get_cursor(conn):
    if get_db_type() == 'postgres':
        import psycopg.rows
        return conn.cursor(row_factory=psycopg.rows.dict_row)
    else:
        return conn.cursor()

def _init_clientes_nuevos_table():
    try:
        conn = get_db_connection()
        cursor = get_cursor(conn)
        db_type = get_db_type()

        if db_type == 'postgres':
            # Migración: agregar columnas que pueden faltar en tablas existentes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes_nuevos (
                    id SERIAL PRIMARY KEY,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Agregar todas las columnas necesarias (ignora si ya existen)
            columnas_requeridas = [
                'ejecutivo', 'numero_registro', 'responsable_formulario', 'razon_social',
                'rut', 'giro', 'direccion_legal', 'direccion_despacho', 'horario_recepcion',
                'enrolar_choferes', 'detalle_enrolar', 'app_choferes', 'detalle_app',
                'epp_choferes', 'detalle_epp', 'tipo_camion', 'agendamiento',
                'detalle_agendamiento', 'contacto_bodega_nombre', 'contacto_bodega_tel',
                'contacto_bodega_email', 'metodo_descarga', 'obs_descarga', 'altura_pallet',
                'acepta_pallet_estandar', 'medida_pallet_alternativa', 'cajas_paradas',
                'rotulacion', 'detalle_rotulacion', 'tolerancia', 'facturacion_excedente',
                'detalle_excedente', 'obs_facturacion', 'contacto_cobranza_nombre',
                'contacto_cobranza_cargo', 'contacto_cobranza_tel', 'contacto_cobranza_email',
                'fechas_pago', 'portal_pago', 'detalle_portal', 'guia_con_factura',
                'email_facturacion', 'condicion_pago', 'etiqueta_caja', 'detalle_etiqueta',
                'contacto_compras_nombre', 'contacto_compras_cargo', 'contacto_compras_tel',
                'contacto_compras_email', 'politica_pallets', 'politica_condiciones',
                'conocimiento_credito', 'obs_generales'
            ]
            for col in columnas_requeridas:
                try:
                    cursor.execute(f"ALTER TABLE clientes_nuevos ADD COLUMN {col} TEXT")
                except Exception:
                    conn.rollback()  # Ignora error si columna ya existe
            conn.commit()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes_nuevos (
                    id SERIAL PRIMARY KEY,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ejecutivo TEXT,
                    numero_registro TEXT,
                    responsable_formulario TEXT,
                    razon_social TEXT,
                    rut TEXT,
                    giro TEXT,
                    direccion_legal TEXT,
                    direccion_despacho TEXT,
                    horario_recepcion TEXT,
                    enrolar_choferes TEXT,
                    detalle_enrolar TEXT,
                    app_choferes TEXT,
                    detalle_app TEXT,
                    epp_choferes TEXT,
                    detalle_epp TEXT,
                    tipo_camion TEXT,
                    agendamiento TEXT,
                    detalle_agendamiento TEXT,
                    contacto_bodega_nombre TEXT,
                    contacto_bodega_tel TEXT,
                    contacto_bodega_email TEXT,
                    metodo_descarga TEXT,
                    obs_descarga TEXT,
                    altura_pallet TEXT,
                    acepta_pallet_estandar TEXT,
                    medida_pallet_alternativa TEXT,
                    cajas_paradas TEXT,
                    rotulacion TEXT,
                    detalle_rotulacion TEXT,
                    tolerancia TEXT,
                    facturacion_excedente TEXT,
                    detalle_excedente TEXT,
                    obs_facturacion TEXT,
                    contacto_cobranza_nombre TEXT,
                    contacto_cobranza_cargo TEXT,
                    contacto_cobranza_tel TEXT,
                    contacto_cobranza_email TEXT,
                    fechas_pago TEXT,
                    portal_pago TEXT,
                    detalle_portal TEXT,
                    guia_con_factura TEXT,
                    email_facturacion TEXT,
                    condicion_pago TEXT,
                    etiqueta_caja TEXT,
                    detalle_etiqueta TEXT,
                    contacto_compras_nombre TEXT,
                    contacto_compras_cargo TEXT,
                    contacto_compras_tel TEXT,
                    contacto_compras_email TEXT,
                    politica_pallets TEXT,
                    politica_condiciones TEXT,
                    conocimiento_credito TEXT,
                    obs_generales TEXT
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes_nuevos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ejecutivo TEXT,
                    numero_registro TEXT,
                    responsable_formulario TEXT,
                    razon_social TEXT,
                    rut TEXT,
                    giro TEXT,
                    direccion_legal TEXT,
                    direccion_despacho TEXT,
                    horario_recepcion TEXT,
                    enrolar_choferes TEXT,
                    detalle_enrolar TEXT,
                    app_choferes TEXT,
                    detalle_app TEXT,
                    epp_choferes TEXT,
                    detalle_epp TEXT,
                    tipo_camion TEXT,
                    agendamiento TEXT,
                    detalle_agendamiento TEXT,
                    contacto_bodega_nombre TEXT,
                    contacto_bodega_tel TEXT,
                    contacto_bodega_email TEXT,
                    metodo_descarga TEXT,
                    obs_descarga TEXT,
                    altura_pallet TEXT,
                    acepta_pallet_estandar TEXT,
                    medida_pallet_alternativa TEXT,
                    cajas_paradas TEXT,
                    rotulacion TEXT,
                    detalle_rotulacion TEXT,
                    tolerancia TEXT,
                    facturacion_excedente TEXT,
                    detalle_excedente TEXT,
                    obs_facturacion TEXT,
                    contacto_cobranza_nombre TEXT,
                    contacto_cobranza_cargo TEXT,
                    contacto_cobranza_tel TEXT,
                    contacto_cobranza_email TEXT,
                    fechas_pago TEXT,
                    portal_pago TEXT,
                    detalle_portal TEXT,
                    guia_con_factura TEXT,
                    email_facturacion TEXT,
                    condicion_pago TEXT,
                    etiqueta_caja TEXT,
                    detalle_etiqueta TEXT,
                    contacto_compras_nombre TEXT,
                    contacto_compras_cargo TEXT,
                    contacto_compras_tel TEXT,
                    contacto_compras_email TEXT,
                    politica_pallets TEXT,
                    politica_condiciones TEXT,
                    conocimiento_credito TEXT,
                    obs_generales TEXT
                )
            """)
        conn.commit()
        conn.close()
        print(f"[alta_clientes] Tabla clientes_nuevos lista ({db_type}).")
    except Exception as e:
        print(f"[alta_clientes] Error al crear tabla clientes_nuevos: {e}")


def _send_formulario_email(datos):
    """Envia email de notificacion via Resend API."""
    import requests as req

    if not RESEND_API_KEY:
        print("[alta_clientes] RESEND_API_KEY no configurada. Email no enviado.")
        return False

    try:
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
        razon = datos.get('razon_social', '—')
        rut = datos.get('rut', '—')
        giro = datos.get('giro', '—')
        dir_legal = datos.get('direccion_legal', '—')
        dir_despacho = datos.get('direccion_despacho', '—')
        horario = datos.get('horario_recepcion', '—')
        enrolar = datos.get('enrolar_choferes', '—')
        det_enrolar = datos.get('detalle_enrolar', '')
        app_chof = datos.get('app_choferes', '—')
        det_app = datos.get('detalle_app', '')
        epp = datos.get('epp_choferes', '—')
        det_epp = datos.get('detalle_epp', '')
        tipo_cam = datos.get('tipo_camion', '—')
        agend = datos.get('agendamiento', '—')
        det_agend = datos.get('detalle_agendamiento', '')
        bod_nombre = datos.get('contacto_bodega_nombre', '—')
        bod_tel = datos.get('contacto_bodega_tel', '—')
        bod_email = datos.get('contacto_bodega_email', '—')
        met_desc = datos.get('metodo_descarga', '—')
        alt_pallet = datos.get('altura_pallet', '—')
        acepta_pall = datos.get('acepta_pallet_estandar', '—')
        med_alt = datos.get('medida_pallet_alternativa', '')
        cajas_par = datos.get('cajas_paradas', '—')
        rotul = datos.get('rotulacion', '—')
        det_rotul = datos.get('detalle_rotulacion', '')
        pol_pallets = datos.get('politica_pallets', '—')
        toler = datos.get('tolerancia', '—')
        fact_exc = datos.get('facturacion_excedente', '—')
        obs_fact = datos.get('obs_facturacion', '')
        cob_nombre = datos.get('contacto_cobranza_nombre', '—')
        cob_cargo = datos.get('contacto_cobranza_cargo', '—')
        cob_tel = datos.get('contacto_cobranza_tel', '—')
        cob_email = datos.get('contacto_cobranza_email', '—')
        f_pago = datos.get('fechas_pago', '—')
        email_fact = datos.get('email_facturacion', '—')
        cond_pago = datos.get('condicion_pago', '—')
        comp_nombre = datos.get('contacto_compras_nombre', '—')
        comp_cargo = datos.get('contacto_compras_cargo', '—')
        comp_tel = datos.get('contacto_compras_tel', '—')
        comp_email = datos.get('contacto_compras_email', '—')
        obs_gen = datos.get('obs_generales', '—')

        html_body = f"""
        <html><body style="font-family:Arial,sans-serif;color:#222;max-width:640px;margin:auto">
        <div style="background:#C41230;color:white;padding:20px 30px;border-radius:8px 8px 0 0">
            <h2 style="margin:0">&#x1F195; Nuevo Formulario Alta Cliente</h2>
            <p style="margin:4px 0 0;opacity:.85">Recibido el {fecha_actual}</p>
        </div>
        <div style="border:1px solid #e5e7eb;border-top:none;padding:20px 30px;border-radius:0 0 8px 8px">

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px">&#x1F3E2; Datos de la Empresa</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Raz&oacute;n Social:</td><td style="padding:4px 8px">{razon}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">RUT:</td><td style="padding:4px 8px">{rut}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Giro:</td><td style="padding:4px 8px">{giro}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Dir. Legal:</td><td style="padding:4px 8px">{dir_legal}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Dir. Despacho:</td><td style="padding:4px 8px">{dir_despacho}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Horario Recepci&oacute;n:</td><td style="padding:4px 8px">{horario}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F69A; Log&iacute;stica de Despacho</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Enrolar choferes:</td><td style="padding:4px 8px">{enrolar} {det_enrolar}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">App choferes:</td><td style="padding:4px 8px">{app_chof} {det_app}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">EPP:</td><td style="padding:4px 8px">{epp} {det_epp}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Tipo cami&oacute;n:</td><td style="padding:4px 8px">{tipo_cam}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Agendamiento:</td><td style="padding:4px 8px">{agend} {det_agend}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Contacto Bodega:</td><td style="padding:4px 8px">{bod_nombre} | {bod_tel} | {bod_email}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F4E6; Descarga y Pallets</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">M&eacute;todo descarga:</td><td style="padding:4px 8px">{met_desc}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Altura m&aacute;x. pallet:</td><td style="padding:4px 8px">{alt_pallet} m</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Acepta pallet 1x1.2m:</td><td style="padding:4px 8px">{acepta_pall} {med_alt}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Cajas paradas:</td><td style="padding:4px 8px">{cajas_par}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Rotulaci&oacute;n:</td><td style="padding:4px 8px">{rotul} {det_rotul}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Pol&iacute;tica pallets:</td><td style="padding:4px 8px">{pol_pallets}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F4CB; Tolerancias y Facturaci&oacute;n</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Tolerancia &plusmn;10%:</td><td style="padding:4px 8px">{toler}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Facturaci&oacute;n excedente:</td><td style="padding:4px 8px">{fact_exc} {obs_fact}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F4B0; Cobranza y Pagos</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Contacto Cobranza:</td><td style="padding:4px 8px">{cob_nombre} ({cob_cargo})</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Tel / Email:</td><td style="padding:4px 8px">{cob_tel} | {cob_email}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Fechas pago:</td><td style="padding:4px 8px">{f_pago}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Email facturaci&oacute;n:</td><td style="padding:4px 8px">{email_fact}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Condici&oacute;n de pago:</td><td style="padding:4px 8px">{cond_pago}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F6D2; Contacto Compras</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Nombre:</td><td style="padding:4px 8px">{comp_nombre} ({comp_cargo})</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Tel / Email:</td><td style="padding:4px 8px">{comp_tel} | {comp_email}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F4DD; Observaciones Generales</h3>
        <div style="background:#f9f9f9;padding:10px 14px;border-radius:4px">{obs_gen}</div>

        </div>
        <p style="text-align:center;font-size:11px;color:#999;margin-top:16px">{NOMBRE_EMPRESA} — Sistema de Alta Clientes Nuevos</p>
        </body></html>
        """

        pdf_b64 = datos.get('pdf_base64', '')
        attachments = []
        if pdf_b64:
            attachments = [{
                "filename": f"Alta_Cliente_{rut}.pdf",
                "content": pdf_b64
            }]

        response = req.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {RESEND_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'from': f'{NOMBRE_EMPRESA} Formularios <onboarding@resend.dev>',
                'to': [FORMULARIO_DESTINO],
                'subject': f'Nuevo Cliente: {razon} — Alta {NOMBRE_EMPRESA}',
                'html': html_body,
                'attachments': attachments
            },
            timeout=15
        )

        if response.status_code in (200, 201):
            print(f"[alta_clientes] Email enviado a {FORMULARIO_DESTINO}")
            return True
        else:
            print(f"[alta_clientes] Resend error {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"[alta_clientes] Error al enviar email: {e}")
        return False


# Inicializar tabla al arrancar
_init_clientes_nuevos_table()


# ── Rutas ─────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('formulario_cliente'))


@app.route('/formulario-cliente', methods=['GET', 'POST'])
def formulario_cliente():
    if request.method == 'GET':
        return render_template('formulario_cliente.html',
                               nombre_empresa=NOMBRE_EMPRESA,
                               correo_destino=FORMULARIO_DESTINO)

    # POST: guardar datos
    if request.is_json:
        f = request.json
    else:
        f = request.form

    campos = [
        'ejecutivo', 'numero_registro', 'responsable_formulario', 'razon_social',
        'rut', 'giro', 'direccion_legal', 'direccion_despacho', 'horario_recepcion',
        'enrolar_choferes', 'detalle_enrolar', 'app_choferes', 'detalle_app',
        'epp_choferes', 'detalle_epp', 'tipo_camion', 'agendamiento',
        'detalle_agendamiento', 'contacto_bodega_nombre', 'contacto_bodega_tel',
        'contacto_bodega_email', 'metodo_descarga', 'obs_descarga', 'altura_pallet',
        'acepta_pallet_estandar', 'medida_pallet_alternativa', 'cajas_paradas',
        'rotulacion', 'detalle_rotulacion', 'tolerancia', 'facturacion_excedente',
        'detalle_excedente', 'obs_facturacion', 'contacto_cobranza_nombre',
        'contacto_cobranza_cargo', 'contacto_cobranza_tel', 'contacto_cobranza_email',
        'fechas_pago', 'portal_pago', 'detalle_portal', 'guia_con_factura',
        'email_facturacion', 'condicion_pago', 'etiqueta_caja', 'detalle_etiqueta',
        'contacto_compras_nombre', 'contacto_compras_cargo', 'contacto_compras_tel',
        'contacto_compras_email', 'politica_pallets', 'politica_condiciones',
        'conocimiento_credito', 'obs_generales'
    ]

    datos = {k: f.get(k, '') for k in campos}

    # Guardar en BD
    try:
        conn = get_db_connection()
        cursor = get_cursor(conn)
        fields = list(datos.keys())
        values = list(datos.values())
        ph = '%s' if get_db_type() == 'postgres' else '?'
        placeholders = ', '.join([ph] * len(fields))
        col_names = ', '.join(fields)
        query = f"INSERT INTO clientes_nuevos ({col_names}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[alta_clientes] Error al guardar en BD: {e}")

    # Enviar email
    datos['pdf_base64'] = f.get('pdf_base64', '')
    _send_formulario_email(datos)

    if request.is_json:
        return jsonify({"status": "success", "redirect": url_for('formulario_cliente_gracias')})
    else:
        return redirect(url_for('formulario_cliente_gracias'))


@app.route('/formulario-cliente/gracias')
def formulario_cliente_gracias():
    return render_template('formulario_cliente_gracias.html',
                           nombre_empresa=NOMBRE_EMPRESA,
                           correo_destino=FORMULARIO_DESTINO)


@app.route('/api/formulario-cliente/next-registro')
def api_next_registro():
    try:
        from datetime import date
        anio_actual = date.today().year
        conn = get_db_connection()
        cursor = get_cursor(conn)

        ph = '%s' if get_db_type() == 'postgres' else '?'
        cursor.execute(
            f"SELECT numero_registro FROM clientes_nuevos "
            f"WHERE numero_registro LIKE {ph} ORDER BY id DESC LIMIT 1",
            (f"{anio_actual}-%",)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            nr = row['numero_registro'] if isinstance(row, dict) else row[0]
            if nr:
                partes = nr.split('-')
                try:
                    siguiente = int(partes[-1]) + 1
                except ValueError:
                    siguiente = 1
            else:
                siguiente = 1
        else:
            siguiente = 1

        numero = f"{anio_actual}-{siguiente:03d}"
        return jsonify({'success': True, 'numero_registro': numero})

    except Exception as e:
        print(f"[alta_clientes] Error generando next-registro: {e}")
        from datetime import date
        fallback = f"{date.today().year}-001"
        return jsonify({'success': False, 'numero_registro': fallback, 'error': str(e)})


@app.route('/test-email')
def test_email():
    """Endpoint de diagnostico — muestra resultado en el navegador."""
    import requests as req
    resultado = {
        'api_key_set': bool(RESEND_API_KEY),
        'api_key_preview': RESEND_API_KEY[:10] + '...' if RESEND_API_KEY else 'NO CONFIGURADA',
        'destinatario': FORMULARIO_DESTINO,
        'nombre_empresa': NOMBRE_EMPRESA,
        'db_type': get_db_type(),
    }
    if not RESEND_API_KEY:
        resultado['error'] = 'RESEND_API_KEY no configurada'
        return jsonify(resultado)
    try:
        response = req.post(
            'https://api.resend.com/emails',
            headers={'Authorization': f'Bearer {RESEND_API_KEY}', 'Content-Type': 'application/json'},
            json={
                'from': f'{NOMBRE_EMPRESA} <onboarding@resend.dev>',
                'to': [FORMULARIO_DESTINO],
                'subject': f'Test {NOMBRE_EMPRESA} desde Railway',
                'html': '<p>Email de prueba desde el nuevo servicio Alta Clientes ✅</p>'
            },
            timeout=15
        )
        resultado['status_code'] = response.status_code
        resultado['response'] = response.text
        resultado['resultado'] = 'OK ✅ Email enviado!' if response.status_code in (200, 201) else 'Error ❌'
    except Exception as e:
        resultado['error'] = str(e)
    return jsonify(resultado)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
