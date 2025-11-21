# Patrón de URLs de Imágenes de Humble Bundle

## Resumen

Este documento describe los patrones de URLs de imágenes que utiliza Humble Bundle para sus bundles y libros.

## Patrones Identificados

### 1. Imágenes de Libros (Book List)

**Patrón:**
```
/images/popups/{machine_name}_slideout.jpg
```

**URL Completa:**
```
https://www.humblebundle.com/images/popups/{machine_name}_slideout.jpg
```

**Descripción:**
- Todas las imágenes de libros en la lista de items de un bundle siguen este patrón
- El `{machine_name}` es el identificador único del libro que viene del JSON del bundle
- La extensión es siempre `.jpg`
- El sufijo es siempre `_slideout.jpg`

**Ejemplos:**
- `spaceghost2024_issue12` → `https://www.humblebundle.com/images/popups/spaceghost2024_issue12_slideout.jpg`
- `herculoids_issue1` → `https://www.humblebundle.com/images/popups/herculoids_issue1_slideout.jpg`
- `thundercats_apex` → `https://www.humblebundle.com/images/popups/thundercats_apex_slideout.jpg`

**Extracción:**
Las URLs se extraen del HTML del bundle usando BeautifulSoup, buscando en:
- Etiquetas `<img>` con atributos `src`, `data-src`, `data-lazy-src`, `data-original`
- Atributos `style` con `background-image: url(...)`
- Atributos `data-image`
- Regex en el contenido HTML como respaldo

### 2. Featured Image (Logo del Bundle)

**Patrón:**
Depende del tipo de imagen:

**Opción A - Imgix CDN:**
```
https://hb.imgix.net/{hash}.{ext}?auto=compress,format&h={height}&w={width}&s={signature}
```

**Opción B - URL Directa:**
```
{url_directa_del_json}
```

**Descripción:**
- La imagen destacada del bundle viene del campo `logo` en `basic_data` del JSON
- Puede usar el servicio de CDN imgix de Humble Bundle
- Los parámetros de imgix incluyen dimensiones y compresión automática

**Ejemplo:**
```
https://hb.imgix.net/a3f1903aee43441e9bbc0ad6cf207698dac696d6.png?auto=compress,format&h=340&w=1200&s=71909e2bb3f147ab7d76471b89901996
```

**Extracción:**
La URL viene directamente del JSON del bundle en el campo `bundleData.basic_data.logo`.

## Implementación

### Backend (Spider)

El código de extracción se encuentra en:
- `spider/scrapers/image_scraper.py`:
  - `_extract_jpg_urls_from_html()`: Extrae URLs del HTML usando BeautifulSoup
  - `_resolve_image_url()`: Resuelve URLs usando el mapeo extraído del HTML

### Frontend

El frontend debe usar las URLs directamente desde el JSON del bundle, sin necesidad de construcción adicional.

**Estructura de datos:**
```typescript
interface BookItem {
  machine_name: string;
  title: string;
  image: string; // URL completa de la imagen
  // ... otros campos
}

interface Bundle {
  featured_image: string; // URL completa de la imagen destacada
  book_list: BookItem[];
  // ... otros campos
}
```

## Notas Técnicas

1. **URLs Absolutas**: Todas las URLs retornadas son absolutas (completas), no necesitan construcción adicional.

2. **CORS**: Las imágenes de Humble Bundle están servidas con los headers CORS apropiados, permitiendo cargarlas directamente desde cualquier dominio.

3. **Cache**: Las imágenes pueden ser cacheadas por el navegador normalmente.

4. **Fallback**: Si una URL no se encuentra en el HTML, el sistema construye la URL estándar usando el patrón conocido.

5. **Validación**: El código verifica que las URLs sean válidas antes de almacenarlas en la base de datos.

## Referencias

- Base URL de Humble Bundle: `https://www.humblebundle.com`
- CDN de Imágenes: `https://hb.imgix.net`
- Estructura de directorios de imágenes: `/images/popups/`

