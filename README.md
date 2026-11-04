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
- `CONFIG.contacto.destino`: canal comercial real. Ahora es `null`.

## Antes de publicar: canal comercial

El formulario de contacto es una **demostración**: valida los campos, prepara un resumen y permite copiarlo, pero **no envía nada** ni guarda datos. La captación no está operativa.

Para activarla:

1. Decidir el canal real (servicio de formularios, endpoint propio, email…).
2. Definirlo en `CONFIG.contacto.destino`.
3. Implementar el envío en `prepararConsulta()` (está marcado con `PUNTO DE CONEXIÓN DEL CANAL COMERCIAL`).
4. Sustituir los avisos «Demostración del formulario. No se enviará ningún mensaje.» por una confirmación real solo cuando el envío funcione.
5. Revisar que la política de privacidad cubre los datos que se recogen.
