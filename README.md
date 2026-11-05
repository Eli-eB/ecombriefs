# EcomBriefs.io

Web de EcomBriefs: implantación y mantenimiento de automatizaciones de atención a pedidos para tiendas Shopify.

HTML estático sin paso de compilación, publicado con GitHub Pages.

## Portada

- `index.html` contiene la landing completa, con estilos y script dentro del propio archivo. No usa librerías ni scripts de terceros; la única petición externa es el envío del formulario a Web3Forms.
- `es/index.html` redirige a la portada.
- La demostración de email usa datos ficticios locales. No conecta Shopify, correo, transportistas ni modelos de IA.

### Ver en local

Abre `index.html` en el navegador, o sirve la carpeta:

```bash
python -m http.server 8000
```

y visita http://localhost:8000/.

### Configuración

Al final de `index.html` está el objeto `CONFIG`:

- `CONFIG.marca`: nombre de la marca que se muestra en la página.
- `CONFIG.contacto.endpoint`: `https://api.web3forms.com/submit`.
- `CONFIG.contacto.web3formsKey`: clave de acceso de Web3Forms. Es pública por diseño (va en el navegador). El email que recibe las consultas se configura en la cuenta de Web3Forms asociada a esa clave, no en el código.
- `CONFIG.contacto.destino`: `hola@ecombriefs.ai`, la dirección que se muestra como alternativa si el envío falla.
- `CONFIG.contacto.timeoutMs`: tiempo máximo de espera del envío (15 s).

## Formulario de contacto

Se envía con Web3Forms, sin servidor propio:

1. Valida los campos en el navegador.
2. Al pulsar «Enviar consulta», hace un `fetch` (POST, JSON) a Web3Forms con:
   - Asunto: `Consulta EcomBriefs – <URL de la tienda>`.
   - Nombre, email (Web3Forms lo usa como dirección de respuesta), URL de la tienda, canal, volumen, tarea e interés.
3. Solo si la respuesta es correcta (`HTTP 2xx` y `success: true`) muestra «Consulta enviada. Te responderemos por email.» y vacía el formulario.
4. Si falla (error de red, tiempo agotado o respuesta no válida), muestra un error, conserva los datos y enseña la consulta con «Copiar consulta» para enviarla a mano a `hola@ecombriefs.ai`.

Antispam: hay un campo trampa oculto (`botcheck`). Las personas no lo ven ni llegan a él con el teclado; si viene marcado, el formulario no envía nada. Web3Forms también lo revisa en su lado.

No se guarda nada en el navegador (ni `localStorage` ni cookies).

### Antes de publicar

- Comprobar en la cuenta de Web3Forms que la clave entrega en el buzón correcto y, si se desea, restringirla al dominio `ecombriefs.io`.
- Hacer un envío de prueba real y confirmar que llega.
- Revisar la política de privacidad: los datos del formulario se envían a Web3Forms, que los reenvía por email.
