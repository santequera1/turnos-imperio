# Imperio Motos — Sistema de Turnos

## Contexto
Este proyecto es un **clon del sistema de turnos de Motos Top** (`turnos-django`), adaptado para un nuevo cliente: **Imperio Motos**. El sistema original ya está en producción en `https://turnos.motostop.com.co`. Este clon debe funcionar igual pero con la identidad visual de Imperio Motos.

## Qué es este sistema
- Sistema de gestión de turnos para taller de motos (Django 3.2+)
- Funcionalidades: agendar turnos, atender turnos, clientes frecuentes, búsqueda de motos, impresión de datos, notificaciones SMS (Twilio)
- Frontend: templates Django con Tailwind CSS (via CDN), jQuery
- Base de datos: SQLite
- Deploy: VPS Ubuntu con Gunicorn + Nginx

## Qué hay que cambiar (rebranding)

### 1. Logos
Los logos nuevos ya están en la raíz del proyecto:
- `logo-horizontal.png` — para navbar y encabezados
- `logo-vertical.png` — para login y pantallas principales

Deben reemplazar los logos actuales en `turnos_app/static/turnos_app/img/` (o donde se referencien en los templates).

### 2. Paleta de colores
Reemplazar la paleta actual (Motos Top usa azul/slate) por la de Imperio Motos:

| Rol | HEX |
|-----|-----|
| Fondo principal | `#000000` |
| Fondo secundario | `#0D0D0D` / `#111111` |
| Fondo de tarjetas | `#1A1A1A` / `#1C1C1C` |
| Acento primario | `#39FF14` (verde neón) |
| Acento secundario | `#4DC800` (verde lima) |
| Verde oscuro (sombras) | `#1A5C00` |
| Texto principal | `#FFFFFF` |
| Texto secundario | `#CCCCCC` |

#### Gradientes CSS
```css
/* Fondo general */
background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);

/* Banner destacado */
background: linear-gradient(135deg, #0d0d0d 0%, #1c1c1c 50%, #111111 100%);

/* Botones y badges (highlight verde neón) */
background: linear-gradient(90deg, #39FF14 0%, #00CC00 100%);

/* Overlay sobre imágenes */
background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.85) 100%);

/* Borde/acento lateral verde */
background: linear-gradient(180deg, #39FF14 0%, #1A5C00 100%);

/* Tarjeta con brillo verde sutil */
background: linear-gradient(135deg, #1a1a1a 0%, #0d2200 100%);
```

#### Efectos decorativos
- Bordes verdes en elementos destacados: `border: 3px solid #39FF14`
- Efecto glow en títulos/logos: `text-shadow: 0 0 10px #39FF14`
- Texto en mayúsculas con tipografía bold condensada donde aplique

### 3. Textos y referencias
Reemplazar toda mención de "Motos Top" o "MOTOS TOP" por **"Imperio Motos"** o **"IMPERIO MOTOS"** en:
- Templates HTML (`turnos_app/templates/turnos_app/`)
- Títulos de página (`<title>`)
- Textos en navbar, footer, login
- `settings.py` si hay alguna referencia

### 4. Catálogo de motos
El archivo `turnos_app/static/turnos_app/js/motos_data.js` contiene el catálogo de motos para autocompletado. Puede necesitar ajustes según las marcas que maneje Imperio Motos (el dueño proporcionará la lista).

### 5. Base de datos
- Limpiar la DB (`db.sqlite3`) o crear una nueva con `python manage.py migrate`
- Crear un superusuario nuevo para Imperio Motos
- NO copiar los clientes de Motos Top

## Archivos clave a modificar
- `turnos_app/templates/turnos_app/*.html` — todos los templates (colores, logos, textos)
- `turnos_app/static/turnos_app/img/` — logos
- `turnos_app/static/turnos_app/css/` — estilos si los hay
- `turnos_app/static/turnos_app/js/motos_data.js` — catálogo de motos
- `TurneroProyecto/settings.py` — nombre del proyecto, ALLOWED_HOSTS

## Deploy en producción
Este proyecto se desplegará en el **mismo VPS** que Motos Top (`51.195.109.26`) pero como servicio independiente:
- Carpeta: `~/apps/turnosimperio/`
- Socket: `turnosimperio.sock`
- Servicio systemd: `turnosimperio.service`
- Subdominio: (pendiente por definir, ej: `turnos.imperiomotos.com`)
- Nginx: bloque server separado apuntando al socket

## Notas importantes
- NO modificar la lógica de negocio, solo la identidad visual
- El Tailwind se usa via CDN con clases utilitarias directamente en los templates
- Los colores actuales usan clases de Tailwind como `bg-slate-800`, `bg-blue-600`, etc. Hay que reemplazarlas por las equivalentes o usar estilos inline/custom CSS para los colores de Imperio Motos (ya que verde neón `#39FF14` no existe en Tailwind por defecto)
- Para colores custom que Tailwind no tiene, usar `style="background-color: #39FF14"` o agregar una hoja CSS custom
