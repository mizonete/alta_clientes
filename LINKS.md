# Enlaces de Producción (Railway)

Este proyecto (`alta_clientes`) se encuentra desplegado en dos instancias (aplicaciones) distintas en Railway, respondiendo cada una a correos diferentes para la gestión de clientes.

### 1. Infinity (Cotizaciones)
- **Link del formulario:** [https://web-production-96240.up.railway.app/formulario-cliente](https://web-production-96240.up.railway.app/formulario-cliente)
- **Correo de destino (FORMULARIO_DESTINO):** `cotizar@infinitybox.cl`

### 2. Infinity Pablo (Ventas)
- **Link del formulario:** [https://web-production-f234d.up.railway.app/formulario-cliente](https://web-production-f234d.up.railway.app/formulario-cliente)
- **Correo de destino (FORMULARIO_DESTINO):** `ventas@infinitybox.cl`

### 3. Infinity Vendedor Externo (Nuevo)
- **Link del formulario:** [https://web-production-410d8.up.railway.app/formulario-cliente](https://web-production-410d8.up.railway.app/formulario-cliente)
- **Correo de destino (FORMULARIO_DESTINO):** `jcruz@infinitybox.cl`

---
*Nota sobre Base de Datos: Actualmente cada instancia se maneja como un proyecto 100% independiente en Railway. Cada una tiene su propio servicio de PostgreSQL conectado (`DATABASE_URL`), lo que significa que cada formulario lleva su propia secuencia de "N° de Registro" empezando desde el 2026-001.*
