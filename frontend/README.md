## Humble Frontend

Interfaz Vue 3 + Vite que replica la estética de `simpleAbout` y consume el backend FastAPI del ETL.

### Requisitos

- Node 20+
- Backend corriendo (`uvicorn api.main:app --reload`) o endpoint público.

### Configuración

```bash
cd frontend
npm install # o pnpm/yarn
```

Crear `.env` (opcional):

```bash
VITE_API_BASE_URL=http://127.0.0.1:5002
```

### Scripts

- `npm run dev` – Vite dev server (http://localhost:3002, falla si el puerto está ocupado)
- `npm run build` – build producción
- `npm run preview` – previsualización del build

### Características

- Tema claro/oscuro y tipografía Monofur heredados del proyecto original.
- Header responsive con navegación a secciones locales y enlaces externos.
- Secciones `Featured` y listado de bundles conectados a `/bundles` y `/bundles/featured`.
- Layout Mobile/Desktop automático vía `useResponsiveQueryEvent`.

