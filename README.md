# EcomBriefs.io

Web de EcomBriefs: implantación y mantenimiento de automatizaciones de atención a pedidos para tiendas Shopify.

HTML estático sin paso de compilación, alojado en Cloudflare Pages.

## Alojamiento: Cloudflare Pages

- Proyecto conectado a este repositorio, rama de producción `main`.
- Configuración de compilación: sin framework, sin comando de compilación y con la raíz del repositorio como directorio de salida.
- El dominio `ecombriefs.io` se configura en el panel de Cloudflare Pages (dominios personalizados). El archivo `CNAME` de GitHub Pages ya no se usa y se ha eliminado.
- Si se activan funciones de Cloudflare como Web Analytics, la protección contra bots o Turnstile, hay que revisar antes la política de cookies y la de privacidad: algunas pueden instalar cookies o tratar datos adicionales.

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
3. Solo si la respuesta es correcta (`HTTP 2xx` y `success: true`) muestra «Hemos recibido tu consulta. Te responderemos en el email que has indicado.» y vacía el formulario.
4. Si falla (error de red, tiempo agotado o respuesta no válida), muestra un error, conserva los datos y enseña la consulta con «Copiar consulta» para enviarla a mano a `hola@ecombriefs.ai`.

Antispam: hay un campo trampa oculto (`botcheck`). Las personas no lo ven ni llegan a él con el teclado; si viene marcado, el formulario no envía nada. Web3Forms también lo revisa en su lado.

No se guarda nada en el navegador (ni `localStorage` ni cookies).

## Páginas legales

- `aviso-legal.html`, `privacidad.html` y `cookies.html`, con el mismo estilo que la portada. El texto de privacidad básico está junto al formulario de `index.html`.
- Si en el futuro hay que dejar un dato pendiente, se marca como `[ENTRE_CORCHETES]` resaltado en amarillo (`<mark class="pendiente">`). Ahora no queda ninguno.
- La política de privacidad identifica a Cloudflare, Inc. como proveedor de alojamiento. Si cambia el alojamiento, hay que actualizarla, igual que el texto junto al formulario.
- `privacy.html`, `terms.html`, `es/privacy.html` y `es/terms.html` redirigen a la página nueva correspondiente.
- La política de cookies usa la alternativa «sin cookies». Si se añade analítica, CAPTCHA, fuentes o scripts externos, hay que revisarla antes.

### Antes de publicar

- Una vez publicada en Cloudflare, comprobar en el navegador que la web sigue sin cookies ni almacenamiento local.
- Comprobar en la cuenta de Web3Forms el buzón de destino y, si se desea, restringir la clave al dominio `ecombriefs.io`.
- Desactivar GitHub Pages en el repositorio cuando Cloudflare Pages sirva el dominio, para no tener dos copias publicadas.
