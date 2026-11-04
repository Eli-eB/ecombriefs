# EcomBriefs.io

Web de EcomBriefs: implantación y mantenimiento de automatizaciones de atención a pedidos para tiendas Shopify.

HTML estático sin paso de compilación, publicado con GitHub Pages.

## Portada

- `index.html` contiene la landing completa, con estilos y script dentro del propio archivo. No usa librerías ni scripts de terceros.
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
- `CONFIG.contacto.destino`: dirección que recibe las consultas (`hola@ecombriefs.ai`).
- `CONFIG.contacto.maxCuerpo`: límite de caracteres del cuerpo del email (1.500).

## Formulario de contacto

Funciona sin servidor:

1. Valida los campos en el navegador.
2. Al pulsar «Enviar por email», muestra el resumen de la consulta y abre el programa de correo del visitante con un `mailto` a `CONFIG.contacto.destino`.
   - Asunto: `Consulta EcomBriefs – <URL de la tienda>`.
   - Cuerpo: el resumen en texto plano, siempre por debajo de 1.500 caracteres (los campos tienen `maxlength` y la tarea se recorta si hiciera falta).
3. «Copiar consulta» queda como alternativa si no se abre ningún programa de correo.

No se muestra confirmación de envío: no podemos saber si la persona llega a enviar el email. No se guarda nada en el navegador ni se hace ninguna petición externa.

Limitación: si el visitante no tiene un programa de correo configurado, el `mailto` no hará nada visible; por eso se muestra la alternativa de copiar. Para recibir consultas sin depender del correo del visitante haría falta un servicio de formularios o un endpoint propio.
