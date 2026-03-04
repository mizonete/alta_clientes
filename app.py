import os
import sqlite3
from datetime import datetime
import psycopg2
from urllib.parse import urlparse
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        result = urlparse(db_url)
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port,
            sslmode='require' if result.hostname != 'localhost' else 'disable'
        )
        return conn
    else:
        conn = sqlite3.connect('clientes_nuevos.db')
        conn.row_factory = sqlite3.Row
        return conn

def get_db_type():
    return 'postgres' if os.environ.get('DATABASE_URL') else 'sqlite'

def get_cursor(conn):
    if get_db_type() == 'postgres':
        import psycopg2.extras
        return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    else:
        return conn.cursor()

def _init_clientes_nuevos_table():
    try:
        conn = get_db_connection()
        cursor = get_cursor(conn)
        db_type = get_db_type()

        if db_type == 'postgres':
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes_nuevos (
                    id SERIAL PRIMARY KEY,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ejecutivo TEXT,
                    numero_registro TEXT,
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
    except Exception as e:
        print(f"[formulario_cliente] Error al crear tabla clientes_nuevos: {e}")

def _send_formulario_email(datos):
    import requests as req
    resend_api_key  = os.environ.get('RESEND_API_KEY', '').strip()
    destinatario    = os.environ.get('FORMULARIO_DESTINO', 'cotizar@infinitybox.cl').strip().lower()
    nombre_empresa  = os.environ.get('NOMBRE_EMPRESA', 'InfinityBox').strip()

    if not resend_api_key:
        print("[formulario_cliente] RESEND_API_KEY no configurada. Email no enviado.")
        return False

    try:
        html_body = f"""
        <html><body style="font-family:Arial,sans-serif;color:#222;max-width:640px;margin:auto">
        <div style="background:#C41230;color:white;padding:20px 30px;border-radius:8px 8px 0 0">
            <h2 style="margin:0">&#x1F195; Nuevo Formulario Alta Cliente</h2>
            <p style="margin:4px 0 0;opacity:.85">Recibido el {{datetime.now().strftime('%d/%m/%Y %H:%M')}}</p>
        </div>
        <div style="border:1px solid #e5e7eb;border-top:none;padding:20px 30px;border-radius:0 0 8px 8px">

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px">&#x1F3E2; Datos de la Empresa</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Raz&oacute;n Social:</td><td style="padding:4px 8px">{{datos.get('razon_social','—')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">RUT:</td><td style="padding:4px 8px">{{datos.get('rut','—')}}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Giro:</td><td style="padding:4px 8px">{{datos.get('giro','—')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Dir. Legal:</td><td style="padding:4px 8px">{{datos.get('direccion_legal','—')}}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Dir. Despacho:</td><td style="padding:4px 8px">{{datos.get('direccion_despacho','—')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Horario Recepci&oacute;n:</td><td style="padding:4px 8px">{{datos.get('horario_recepcion','—')}}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F69A; Log&iacute;stica de Despacho</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Enrolar choferes:</td><td style="padding:4px 8px">{{datos.get('enrolar_choferes','—')}} {{datos.get('detalle_enrolar','')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">App choferes:</td><td style="padding:4px 8px">{{datos.get('app_choferes','—')}} {{datos.get('detalle_app','')}}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">EPP:</td><td style="padding:4px 8px">{{datos.get('epp_choferes','—')}} {{datos.get('detalle_epp','')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Tipo cami&oacute;n:</td><td style="padding:4px 8px">{{datos.get('tipo_camion','—')}}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Agendamiento:</td><td style="padding:4px 8px">{{datos.get('agendamiento','—')}} {{datos.get('detalle_agendamiento','')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Contacto Bodega:</td><td style="padding:4px 8px">{{datos.get('contacto_bodega_nombre','—')}} | {{datos.get('contacto_bodega_tel','—')}} | {{datos.get('contacto_bodega_email','—')}}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F4E6; Descarga y Pallets</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">M&eacute;todo descarga:</td><td style="padding:4px 8px">{{datos.get('metodo_descarga','—')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Altura m&aacute;x. pallet:</td><td style="padding:4px 8px">{{datos.get('altura_pallet','—')}} m</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Acepta pallet 1x1.2m:</td><td style="padding:4px 8px">{{datos.get('acepta_pallet_estandar','—')}} {{datos.get('medida_pallet_alternativa','')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Cajas paradas:</td><td style="padding:4px 8px">{{datos.get('cajas_paradas','—')}}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Rotulaci&oacute;n:</td><td style="padding:4px 8px">{{datos.get('rotulacion','—')}} {{datos.get('detalle_rotulacion','')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Pol&iacute;tica pallets:</td><td style="padding:4px 8px">{{datos.get('politica_pallets','—')}}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F4CB; Tolerancias y Facturaci&oacute;n</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Tolerancia &plusmn;10%:</td><td style="padding:4px 8px">{{datos.get('tolerancia','—')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Facturaci&oacute;n excedente:</td><td style="padding:4px 8px">{{datos.get('facturacion_excedente','—')}} {{datos.get('obs_facturacion','')}}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F4B0; Cobranza y Pagos</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Contacto Cobranza:</td><td style="padding:4px 8px">{{datos.get('contacto_cobranza_nombre','—')}} ({{datos.get('contacto_cobranza_cargo','—')}})</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Tel / Email:</td><td style="padding:4px 8px">{{datos.get('contacto_cobranza_tel','—')}} | {{datos.get('contacto_cobranza_email','—')}}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Fechas pago:</td><td style="padding:4px 8px">{{datos.get('fechas_pago','—')}}</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Email facturaci&oacute;n:</td><td style="padding:4px 8px">{{datos.get('email_facturacion','—')}}</td></tr>
          <tr><td style="padding:4px 8px;font-weight:600">Condici&oacute;n de pago:</td><td style="padding:4px 8px">{{datos.get('condicion_pago','—')}}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F6D2; Contacto Compras</h3>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:4px 8px;font-weight:600;width:40%">Nombre:</td><td style="padding:4px 8px">{{datos.get('contacto_compras_nombre','—')}} ({{datos.get('contacto_compras_cargo','—')}})</td></tr>
          <tr style="background:#f9f9f9"><td style="padding:4px 8px;font-weight:600">Tel / Email:</td><td style="padding:4px 8px">{{datos.get('contacto_compras_tel','—')}} | {{datos.get('contacto_compras_email','—')}}</td></tr>
        </table>

        <h3 style="color:#C41230;border-bottom:2px solid #C41230;padding-bottom:6px;margin-top:20px">&#x1F4DD; Observaciones Generales</h3>
        <div style="background:#f9f9f9;padding:10px 14px;border-radius:4px">{{datos.get('obs_generales','—')}}</div>

        </div>
        <p style="text-align:center;font-size:11px;color:#999;margin-top:16px">{nombre_empresa} — Sistema de Alta Clientes Nuevos</p>
        </body></html>
        """

        pdf_b64 = datos.get('pdf_base64', '')
        if pdf_b64:
            attachments = [{
                "filename": f"Alta_Cliente_{{datos.get('rut', 'sin_rut')}}.pdf",
                "content": pdf_b64
            }]
        else:
            attachments = []

        response = req.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {{resend_api_key}}',
                'Content-Type': 'application/json'
            },
            json={
                'from': f'{nombre_empresa} Formularios <onboarding@resend.dev>',
                'to': [destinatario],
                'subject': f'Nuevo Cliente: {{datos.get("razon_social", "Sin nombre")}} — Alta {nombre_empresa}',
                'html': html_body,
                'attachments': attachments
            },
            timeout=15
        )

        if response.status_code in (200, 201):
            return True
        else:
            print(f"[formulario_cliente] Resend error {{response.status_code}}: {{response.text}}")
            return False

    except Exception as e:
        print(f"[formulario_cliente] Error al enviar email via Resend: {{e}}")
        return False

_init_clientes_nuevos_table()

@app.route('/formulario-cliente', methods=['GET', 'POST'])
def formulario_cliente():
    nombre_empresa = os.environ.get('NOMBRE_EMPRESA', 'InfinityBox').strip()
    correo_destino = os.environ.get('FORMULARIO_DESTINO', 'cotizar@infinitybox.cl').strip().lower()

    if request.method == 'GET':
        return render_template('formulario_cliente.html', nombre_empresa=nombre_empresa, correo_destino=correo_destino)

    if request.is_json:
        f = request.json
    else:
        f = request.form

    datos = {k: f.get(k, '') for k in [
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
    ]}

    try:
        conn = get_db_connection()
        cursor = get_cursor(conn)
        fields = list(datos.keys())
        values = list(datos.values())
        placeholders = ', '.join(['?' if get_db_type() != 'postgres' else '%s'] * len(fields))
        col_names = ', '.join(fields)
        query = f"INSERT INTO clientes_nuevos ({col_names}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[formulario_cliente] Error al guardar en BD: {e}")

    datos['pdf_base64'] = f.get('pdf_base64', '')
    _send_formulario_email(datos)

    if request.is_json:
        from flask import url_for
        return jsonify({"status": "success", "redirect": url_for('formulario_cliente_gracias')})
    else:
        from flask import redirect, url_for
        return redirect(url_for('formulario_cliente_gracias'))

@app.route('/formulario-cliente/gracias')
def formulario_cliente_gracias():
    nombre_empresa = os.environ.get('NOMBRE_EMPRESA', 'InfinityBox').strip()
    correo_destino = os.environ.get('FORMULARIO_DESTINO', 'cotizar@infinitybox.cl').strip().lower()
    return render_template('formulario_cliente_gracias.html', nombre_empresa=nombre_empresa, correo_destino=correo_destino)

@app.route('/api/formulario-cliente/next-registro')
def api_next_registro():
    try:
        from datetime import date
        anio_actual = date.today().year

        conn = get_db_connection()
        cursor = get_cursor(conn)

        if get_db_type() == 'postgres':
            cursor.execute(
                "SELECT numero_registro FROM clientes_nuevos "
                "WHERE numero_registro LIKE %s ORDER BY id DESC LIMIT 1",
                (f"{anio_actual}-%",)
            )
        else:
            cursor.execute(
                "SELECT numero_registro FROM clientes_nuevos "
                "WHERE numero_registro LIKE ? ORDER BY id DESC LIMIT 1",
                (f"{anio_actual}-%",)
            )

        row = cursor.fetchone()
        conn.close()

        if row and row['numero_registro']:
            partes = row['numero_registro'].split('-')
            try:
                ultimo_num = int(partes[-1])
                siguiente = ultimo_num + 1
            except ValueError:
                siguiente = 1
        else:
            siguiente = 1

        numero = f"{anio_actual}-{siguiente:03d}"
        return jsonify({'success': True, 'numero_registro': numero})

    except Exception as e:
        print(f"[formulario_cliente] Error generando next-registro: {e}")
        from datetime import date
        fallback = f"{date.today().year}-001"
        return jsonify({'success': False, 'numero_registro': fallback})

# Add redirect for root so it doesn't 404
@app.route('/')
def index():
    from flask import redirect, url_for
    return redirect(url_for('formulario_cliente'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
