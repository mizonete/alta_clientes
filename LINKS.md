# Enlaces de Producción (Railway)

Este proyecto (`alta_clientes`) se encuentra desplegado en dos instancias (aplicaciones) distintas en Railway, respondiendo cada una a correos diferentes para la gestión de clientes.

### 1. Infinity (Cotizaciones)
- **Link del formulario:** [https://web-production-96240.up.railway.app/formulario-cliente](https://web-production-96240.up.railway.app/formulario-cliente)
- **Correo de destino (FORMULARIO_DESTINO):** `cotizar@infinitybox.cl`

### 2. Infinity Pablo (Ventas)
- **Link del formulario:** [https://web-production-f234d.up.railway.app/formulario-cliente](https://web-production-f234d.up.railway.app/formulario-cliente)
- **Correo de destino (FORMULARIO_DESTINO):** `ventas@infinitybox.cl`

### 3. Infinity Vendedor Externo (Nuevo)
- **Link del formulario:** *(Se generará al desplegar en Railway)*
- **Correo de destino (FORMULARIO_DESTINO):** `[CORREO_A_DEFINIR]` (Ej: vendedor@infinitybox.cl)

---
*Nota: Para que todas las instancias compartan el mismo correlativo de **N° de Registro**, asegúrate de que todas apunten a la misma `DATABASE_URL` en Railway.*
