# 🏋️ Mi Entrenador Fitness

Una aplicación web progresiva (PWA) para seguimiento personal de entrenamiento y progreso fitness.

## 🚀 Características

- **Seguimiento inteligente de ejercicios**: Registra series, repeticiones y peso
- **Sobrecarga progresiva automática**: Sugiere incrementos de peso basados en tu rendimiento
- **Sistema de descanso inteligente**: Recomienda días de descanso óptimos
- **Gráficos de progreso**: Visualiza tu evolución con Chart.js
- **Funciona offline**: Guarda todos tus datos localmente
- **Diseño móvil-first**: Optimizado para usar en el gym

## 📱 Instalación en tu dispositivo

### Para iPhone/iPad:
1. Abre Safari en tu dispositivo
2. Navega a la URL de tu app
3. Toca el botón **Compartir** (cuadro con flecha)
4. Selecciona **"Añadir a pantalla de inicio"**
5. Confirma el nombre y listo

### Para Android:
1. Abre Chrome en tu dispositivo
2. Navega a la URL de tu app
3. Toca el menú de tres puntos
4. Selecciona **"Añadir a pantalla de inicio"**
5. Confirma y listo

## 🏠 Despliegue

Opciones gratuitas para publicar tu app:

### GitHub Pages (Recomendado)
1. Sube todos los archivos a un repositorio GitHub
2. En Settings → Pages, selecciona rama `main` y carpeta `/root`
3. Tu app estará disponible en `https://[tu-username].github.io/[repo-name]`

### Netlify
1. Arrastra y suelta la carpeta en [netlify.com](https://netlify.com)
2. Obtienes una URL instantánea

### Vercel
1. Conecta tu repositorio GitHub
2. Despliegue automático en cada cambio

## 📁 Estructura de archivos

```
├── index.html          # Página principal
├── style.css          # Estilos responsive
├── script.js          # Lógica de la app
├── manifest.json      # Configuración PWA
├── sw.js             # Service Worker para offline
├── icon-192.png      # Ícono 192x192 (crear)
├── icon-512.png      # Ícono 512x512 (crear)
└── README.md         # Este archivo
```

## 💾 Datos

Todos tus datos se guardan **localmente** en tu dispositivo usando `localStorage`:
- Historial de entrenamientos
- Progreso por ejercicio
- Configuración personal
- Gráficos y estadísticas

## 🔧 Personalización

### Agregar nuevos ejercicios
Edita `script.js` en la función `initializeData()`:

```javascript
this.defaultExercises = {
    'nuevo_grupo': [
        { name: 'Nuevo Ejercicio', series: 4, reps: 10, rest: 120, weight: 50 }
    ]
};
```

### Cambiar colores
Modifica `style.css` en las variables:
```css
:root {
    --primary-color: #2563eb;
    --success-color: #28a745;
    --accent-color: #667eea;
}
```

## 🎯 Uso

1. **Entrenamiento día**: Completa las series y pesos
2. **Progreso**: Visualiza tu evolución
3. **Calendario**: Planifica tus entrenamientos

La app automáticamente:
- Ajusta los pesos recomendados
- Sugiere días de descanso
- Guarda todo tu progreso

## 🔐 Privacidad

- **100% privado**: Tus datos nunca salen de tu dispositivo
- **Sin tracking**: No hay analíticas ni publicidad
- **Offline completo**: Funciona sin conexión

## 🐛 Problemas comunes

**No se instala en iOS**: Asegúrate de usar Safari (no Chrome/Firefox)

**Los datos se pierden**: Usa el mismo navegador y no limpies caché

**No funciona offline**: Verifica que el Service Worker esté activo

---

**Creado con ❤️ para entrenamiento personal**