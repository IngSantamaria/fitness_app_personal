// Data Management with LocalStorage
class FitnessApp {
    constructor() {
        this.currentView = 'workout';
        this.currentUserId = localStorage.getItem('currentUserId') || null;
        this.initializeData();
        this.setupEventListeners();
        this.initTheme();
        this.initializeApp();
    }

    initializeApp() {
        // Check if there's a selected user, otherwise show user selection
        if (this.currentUserId && this.userExists(this.currentUserId)) {
            this.showMainApp();
        } else {
            this.showUserSelection();
        }
    }

    userExists(userId) {
        const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
        return users[userId] !== undefined;
    }

    showUserSelection() {
        document.getElementById('user-selection-screen').style.display = 'block';
        document.getElementById('main-app-screen').style.display = 'none';
        this.loadUsersGrid();
        this.setupThemeToggle('theme-toggle');
    }

    showMainApp() {
        document.getElementById('user-selection-screen').style.display = 'none';
        document.getElementById('main-app-screen').style.display = 'block';
        this.loadUserData();
        this.loadUserManagement();
        this.loadExercises();
        this.updateSchedule();
        this.initChart();
        this.updateCurrentUserHeader();
        this.setupThemeToggle('theme-toggle-app');
    }

    updateCurrentUserHeader() {
        const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
        const header = document.getElementById('current-user-header');
        if (header && this.currentUserId && users[this.currentUserId]) {
            header.textContent = users[this.currentUserId].name;
        }
    }

    loadUsersGrid() {
        const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
        const grid = document.getElementById('users-grid');
        
        grid.innerHTML = '';
        
        if (Object.keys(users).length === 0) {
            grid.innerHTML = '<p class="text-center text-muted">No hay usuarios registrados. Crea tu primer usuario para comenzar.</p>';
            return;
        }
        
        Object.keys(users).forEach(userId => {
            const user = users[userId];
            const userCard = document.createElement('div');
            userCard.className = 'user-card';
            userCard.onclick = () => this.selectUser(userId);
            
            // Get user stats
            const userKey = 'fitnessData_' + userId;
            const userData = JSON.parse(localStorage.getItem(userKey) || '{}');
            const workoutCount = userData.workouts?.length || 0;
            
            userCard.innerHTML = `
                <div class="user-avatar">💪</div>
                <div class="user-name">${user.name}</div>
                <div class="user-stats">${workoutCount} entrenamientos</div>
                ${userId === this.currentUserId ? '<div class="badge bg-primary mt-2">Actual</div>' : ''}
            `;
            
            grid.appendChild(userCard);
        });
    }

    selectUser(userId) {
        this.currentUserId = userId;
        localStorage.setItem('currentUserId', userId);
        this.showMainApp();
        
        const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
        this.showNotification(`Bienvenido(a) ${users[userId].name}!`);
    }

    setupThemeToggle(toggleId) {
        const themeToggle = document.getElementById(toggleId);
        if (themeToggle) {
            // Remove existing listener to avoid duplicates
            const newToggle = themeToggle.cloneNode(true);
            themeToggle.parentNode.replaceChild(newToggle, themeToggle);
            
            newToggle.addEventListener('change', () => {
                this.toggleTheme();
            });
            
            // Set current state
            const savedTheme = localStorage.getItem('theme') || 'light';
            newToggle.checked = savedTheme === 'dark';
        }
    }

    initializeData() {
        // Initialize users system
        const users = localStorage.getItem('fitnessUsers');
        if (!users) {
            localStorage.setItem('fitnessUsers', JSON.stringify({}));
        }
        
        // Default exercises data
        this.defaultExercises = {
            'pecho-espalda-A': [
                { name: 'Press de Banca', series: 4, reps: 10, rest: 120, weight: 60 },
                { name: 'Dominadas', series: 4, reps: 8, rest: 120, weight: 0 },
                { name: 'Press Inclinado con Mancuernas', series: 3, reps: 12, rest: 90, weight: 20 },
                { name: 'Remo con Barra', series: 4, reps: 10, rest: 120, weight: 70 },
                { name: 'Fondos en paralelas', series: 3, reps: 8, rest: 90, weight: 0 }
            ],
            'pecho-espalda-B': [
                { name: 'Press de Banca cerrado', series: 4, reps: 8, rest: 120, weight: 50 },
                { name: 'Jalón al pecho', series: 3, reps: 12, rest: 90, weight: 50 },
                { name: 'Aperturas en polea', series: 3, reps: 15, rest: 60, weight: 25 },
                { name: 'Remo en máquina', series: 3, reps: 12, rest: 60, weight: 40 },
                { name: 'Flexiones en paralelas', series: 3, reps: 10, rest: 90, weight: 0 }
            ],
            'brazos-A': [
                { name: 'Curl de bíceps con barra', series: 4, reps: 12, rest: 60, weight: 20 },
                { name: 'Extensiones de tríceps en polea', series: 4, reps: 12, rest: 60, weight: 25 },
                { name: 'Curl martillo con mancuernas', series: 3, reps: 10, rest: 60, weight: 15 },
                { name: 'Fondos de tríceps en banco', series: 3, reps: 15, rest: 60, weight: 0 },
                { name: 'Curl concentrado', series: 3, reps: 10, rest: 60, weight: 10 }
            ],
            'brazos-B': [
                { name: 'Curl con mancuernas alternado', series: 4, reps: 10, rest: 60, weight: 12 },
                { name: 'Press francés', series: 3, reps: 12, rest: 90, weight: 30 },
                { name: 'Curl en banco scott', series: 3, reps: 12, rest: 60, weight: 25 },
                { name: 'Extensiones overhead con mancuerna', series: 3, reps: 12, rest: 60, weight: 15 },
                { name: 'Flexiones con agarre cerrado', series: 3, reps: 10, rest: 60, weight: 0 }
            ],
            'piernas-A': [
                { name: 'Sentadillas con barra', series: 4, reps: 12, rest: 180, weight: 80 },
                { name: 'Prensa de piernas', series: 3, reps: 15, rest: 120, weight: 100 },
                { name: 'Zancadas con mancuernas', series: 3, reps: 10, rest: 90, weight: 15 },
                { name: 'Elevación de gemelos', series: 4, reps: 20, rest: 60, weight: 30 }
            ],
            'piernas-B': [
                { name: 'Peso muerto rumano', series: 4, reps: 10, rest: 120, weight: 70 },
                { name: 'Sentadilla frontal', series: 3, reps: 10, rest: 180, weight: 40 },
                { name: 'Elevación de talones', series: 4, reps: 15, rest: 60, weight: 50 },
                { name: 'Hip thrust', series: 3, reps: 12, rest: 90, weight: 60 },
                { name: 'Paternitas con mancuernas', series: 3, reps: 12, rest: 90, weight: 10 }
            ],
            'piernas-C': [
                { name: 'Sentadilla búlgara', series: 4, reps: 8, rest: 120, weight: 20 },
                { name: 'Prensa inclinada', series: 4, reps: 12, rest: 90, weight: 80 },
                { name: 'Extensiones de cuádriceps', series: 3, reps: 15, rest: 60, weight: 40 },
                { name: 'Curl femoral acostado', series: 3, reps: 12, rest: 60, weight: 25 },
                { name: 'Elevación de gemelos de pie', series: 4, reps: 20, rest: 45, weight: 40 },
                { name: 'Sentadilla sumo con mancuerna', series: 3, reps: 10, rest: 90, weight: 30 }
            ],
            'abdomen-cardio': [
                { name: 'Plancha', series: 3, reps: '60 segundos', rest: 60, weight: 0 },
                { name: 'Elevación de piernas', series: 3, reps: 15, rest: 45, weight: 0 },
                { name: 'Crunch abdominal', series: 4, reps: 20, rest: 45, weight: 0 },
                { name: 'Bicicleta abdominal', series: 3, reps: 20, rest: 45, weight: 0 },
                { name: 'Mountain climbers', series: 3, reps: 20, rest: 45, weight: 0 },
                { name: 'Salto de cuerda', series: 5, reps: '3 minutos', rest: 60, weight: 0 },
                { name: 'Burpees', series: 3, reps: 10, rest: 90, weight: 0 }
            ]
        };

        this.loadUserData();
        
        // Update current workout to today's routine if needed
        const todayRoutine = getTodaysRoutine(this.data.weekType);
        if (this.data.currentWorkout.muscleGroup !== todayRoutine && todayRoutine !== 'descanso') {
            this.data.currentWorkout.muscleGroup = todayRoutine;
            this.saveUserData();
        }
    }

    setupEventListeners() {
        // View switcher buttons - simple and direct
        document.querySelectorAll('[data-view]').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchView(button.dataset.view);
            });
        });
        
        // FAB button
        const fabButton = document.querySelector('.fab');
        if (fabButton) {
            fabButton.addEventListener('click', () => {
                this.showNotification('🔧 Función para agregar ejercicios próximamente');
            });
        }
        
        // Theme toggle is now handled per screen in setupThemeToggle function
    }

    switchView(viewName) {
        // Update button states
        document.querySelectorAll('[data-view]').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-view="${viewName}"]`).classList.add('active');

        // Update view visibility
        document.querySelectorAll('.view').forEach(view => {
            view.style.display = 'none';
        });
        document.getElementById(`${viewName}-view`).style.display = 'block';

        this.currentView = viewName;

        // Update view-specific content
        if (viewName === 'progress') {
            this.updateProgressChart();
        } else if (viewName === 'schedule') {
            this.updateSchedule();
        } else if (viewName === 'routines') {
            this.loadRoutineEditor();
        } else if (viewName === 'users') {
            this.loadUserManagement();
        }
    }

    loadExercises() {
        const exerciseList = document.getElementById('exercise-list');
        const currentWorkout = this.data.currentWorkout;
        const exercises = this.data.exercises[currentWorkout.muscleGroup] || this.data.exercises['pecho-espalda-A'];

        exerciseList.innerHTML = '';

        // Update workout title
        const workoutTitle = document.getElementById('workout-title');
        if (workoutTitle) {
            const groupNames = {
                'pecho-espalda-A': 'Día de Pecho-Espalda A',
                'pecho-espalda-B': 'Día de Pecho-Espalda B',
                'brazos-A': 'Día de Brazos A',
                'brazos-B': 'Día de Brazos B',
                'piernas-A': 'Día de Piernas A',
                'piernas-B': 'Día de Piernas B',
                'descanso': 'Día de Descanso'
            };
            
            const routineName = groupNames[currentWorkout.muscleGroup] || 'Entrenamiento';
            
            // Check for deload recommendation
            const deloadCheck = this.checkDeloadNeed();
            if (deloadCheck && deloadCheck.needed) {
                workoutTitle.innerHTML = `🎯 Hoy: ${routineName} <span class="deload-warning">⚠️ ${deloadCheck.severity === 'high' ? 'Descarga Recomendada' : 'Considera Descarga'}</span>`;
                if (deloadCheck.severity === 'high') {
                    this.showDeloadAlert(deloadCheck.reason);
                }
            } else {
                workoutTitle.textContent = `🎯 Hoy: ${routineName}`;
            }
        }

        // If it's a rest day, show different content
        if (currentWorkout.muscleGroup === 'descanso') {
            exerciseList.innerHTML = `
                <div class="text-center py-5">
                    <h3>😴 Día de Descanso</h3>
                    <p class="text-muted">Tu cuerpo necesita recuperarse para crecer más fuerte.</p>
                    <div class="mt-4">
                        <h5>Próximo entrenamiento:</h5>
                        <p class="lead">${getNextWorkoutDay(this.data.weekType).routine}</p>
                        <small class="text-muted">${getNextWorkoutDay(this.data.weekType).date.toLocaleDateString('es', { weekday: 'long', month: 'short', day: 'numeric' })}</small>
                    </div>
                </div>
            `;
            return;
        }

        exercises.forEach((exercise, index) => {
            const exerciseCard = this.createExerciseCard(exercise, index);
            exerciseList.appendChild(exerciseCard);
        });
    }
    
    showDeloadAlert(reason) {
        // Check if alert already shown today
        const today = new Date().toDateString();
        if (this.lastDeloadAlert === today) return;
        
        this.lastDeloadAlert = today;
        
        setTimeout(() => {
            this.showNotification(reason, 'warning');
        }, 2000);
    }

    getAIRecommendation(exerciseName, currentWeight) {
        const progress = this.data.progress[exerciseName];
        
        if (!progress || progress.lastWorkouts.length < 3) {
            return {
                weight: currentWeight,
                reason: 'Requiere más datos históricos',
                confidence: 0.5,
                type: 'maintain'
            };
        }

        const analysis = this.analyzePerformance(progress.lastWorkouts.slice(-5), currentWeight);
        return this.aiRecommendation(analysis, currentWeight);
    }
    
    createExerciseCard(exercise, index) {
        const card = document.createElement('div');
        card.className = 'exercise-card';
        
        // Get AI recommendation based on advanced analysis
        const recommendation = this.getAIRecommendation(exercise.name, exercise.weight);
        const recommendedWeight = recommendation.weight;
        const weightChange = recommendedWeight - exercise.weight;
        
        // Formatear recomendación
        let recommendationBadge = '';
        if (recommendation.type === 'deload') {
            recommendationBadge = `<span class="recommended-badge recommendation-deload">⚠️ DESCARGA</span>`;
        } else if (recommendation.type === 'plateau') {
            recommendationBadge = `<span class="recommended-badge recommendation-plateau">⚡ PLATEAU</span>`;
        } else if (recommendation.type === 'technique') {
            recommendationBadge = `<span class="recommended-badge recommendation-decrease">📊 TÉCNICA</span>`;
        } else if (weightChange > 0) {
            recommendationBadge = `<span class="recommended-badge recommendation-increase">+${weightChange}kg</span>`;
        } else if (weightChange < 0) {
            recommendationBadge = `<span class="recommended-badge recommendation-decrease">${weightChange}kg</span>`;
        } else {
            recommendationBadge = `<span class="recommended-badge recommendation-maintain">✓ OK</span>`;
        }
        
        card.innerHTML = `
            <div class="exercise-header" onclick="toggleExercise(${index})">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6>${exercise.name}</h6>
                        <small class="text-muted">
                            ${exercise.series} series × ${exercise.reps} reps | 
                            Descanso: ${exercise.rest}s
                        </small>
                    </div>
                    <div class="text-end">
                        ${recommendationBadge}
                        <br>
                        <small class="text-muted">${recommendedWeight}kg</small>
                        <br>
                        <small class="text-info">${recommendation.reason}</small>
                        ${recommendation.confidence ? `<br><small class="text-secondary">Confianza: ${Math.round(recommendation.confidence * 100)}%</small>` : ''}
                    </div>
                </div>
            </div>
            <div id="exercise-${index}" class="exercise-details">
                ${this.createSeriesInputs(exercise, index)}
            </div>
        `;

        return card;
    }

    createSeriesInputs(exercise, index) {
        let html = '<div class="series-inputs">';
        
        for (let i = 1; i <= exercise.series; i++) {
            html += `
                <div class="serie-input">
                    <input type="checkbox" id="serie-${index}-${i}" onchange="markSerieComplete(${index}, ${i})">
                    <label for="serie-${index}-${i}">Serie ${i}:</label>
                    <input type="number" id="reps-${index}-${i}" placeholder="Reps" value="${exercise.reps}">
                    <input type="number" id="weight-${index}-${i}" placeholder="Peso" value="${exercise.weight}" step="2.5">
                    <span class="text-muted">kg</span>
                </div>
            `;
        }
        
        html += `
            <button class="btn btn-sm btn-primary mt-2" onclick="saveExerciseData(${index})">
                💾 Guardar ${exercise.name}
            </button>
        </div>`;
        
        return html;
    }

    // IA-like Advanced Recommendation System
    getRecommendedWeight(exerciseName, currentWeight) {
        const progress = this.data.progress[exerciseName];
        
        // Si no hay historial suficiente, usar método tradicional
        if (!progress || progress.lastWorkouts.length < 3) {
            return currentWeight;
        }

        const lastWorkouts = progress.lastWorkouts.slice(-5); // Analizar últimos 5 entrenamientos
        
        // Análisis avanzado de rendimiento
        const analysis = this.analyzePerformance(lastWorkouts, currentWeight);
        
        // Aplicar algoritmo de recomendación IA-like
        const recommendation = this.aiRecommendation(analysis, currentWeight);
        
        return recommendation.weight;
    }
    
    analyzePerformance(workouts, currentWeight) {
        // Calcular métricas clave
        const avgCompletion = workouts.reduce((sum, w) => sum + w.completion, 0) / workouts.length;
        const completions = workouts.map(w => w.completion);
        
        // Tendencia de rendimiento (mejorando, estable, o empeorando)
        const recentAvg = completions.slice(-2).reduce((a, b) => a + b, 0) / 2;
        const olderAvg = completions.slice(0, -2).reduce((a, b) => a + b, 0) / (completions.length - 2);
        const trend = recentAvg - olderAvg;
        
        // Volatilidad (consistencia del rendimiento)
        const variance = completions.reduce((sum, completion) => {
            return sum + Math.pow(completion - avgCompletion, 2);
        }, 0) / completions.length;
        const volatility = Math.sqrt(variance);
        
        // Detección de plateau (sin progreso significativo)
        const plateauDetected = Math.abs(trend) < 0.02 && avgCompletion > 0.85;
        
        // Nivel de fatiga (basado en caída de rendimiento reciente)
        const fatigueLevel = this.detectFatigue(workouts);
        
        return {
            avgCompletion,
            trend,
            volatility,
            plateauDetected,
            fatigueLevel,
            consistency: 1 - volatility, // Mayor valor = más consistente
            recentPerformance: recentAvg
        };
    }
    
    detectFatigue(workouts) {
        if (workouts.length < 3) return 0;
        
        // Comparar rendimiento reciente vs rendimiento promedio histórico
        const recentWorkouts = workouts.slice(-2);
        const avgRecent = recentWorkouts.reduce((sum, w) => sum + w.completion, 0) / recentWorkouts.length;
        const avgHistorical = workouts.reduce((sum, w) => sum + w.completion, 0) / workouts.length;
        
        const performanceDrop = avgHistorical - avgRecent;
        
        if (performanceDrop > 0.15) return 'high';      // Caída significativa (>15%)
        if (performanceDrop > 0.08) return 'medium';    // Caída moderada (>8%)
        return 'low';                                     // Performance estable
    }
    
    aiRecommendation(analysis, currentWeight) {
        let adjustment = 0;
        let reason = '';
        let confidence = 0;
        
        // Detección de fatiga alta - sugerir descarga
        if (analysis.fatigueLevel === 'high') {
            return {
                weight: Math.max(0, currentWeight * 0.85), // Reducir 15%
                reason: '🚨 Alta fatiga detectada - Reduciendo carga',
                confidence: 0.9,
                type: 'deload'
            };
        }
        
        // Detección de plateau - necesitar variación
        if (analysis.plateauDetected) {
            return {
                weight: currentWeight,
                reason: '⚡ Plateau detectado - Considera cambiar ejercicio o método',
                confidence: 0.8,
                type: 'plateau'
            };
        }
        
        // Baja consistencia - enfocarse en técnica
        if (analysis.volatility > 0.15) {
            return {
                weight: Math.max(0, currentWeight * 0.95), // Reducir 5%
                reason: '📊 Rendimiento inconsistente - Mejorando técnica',
                confidence: 0.7,
                type: 'technique'
            };
        }
        
        // Rendimiento excelente con buena consistencia - progresión agresiva
        if (analysis.avgCompletion >= 0.95 && analysis.volatility < 0.08) {
            adjustment = 0.05; // Aumentar 5%
            reason = '🚀 Rendimiento excelente - Progresión acelerada';
            confidence = 0.9;
        }
        // Buen rendimiento estable - progresión moderada
        else if (analysis.avgCompletion >= 0.90 && analysis.consistency > 0.85) {
            adjustment = 0.03; // Aumentar 3%
            reason = '📈 Buen progreso - Aumento moderado';
            confidence = 0.8;
        }
        // Rendimiento aceptable - mantenimiento
        else if (analysis.avgCompletion >= 0.80) {
            reason = '⚖️ Rendimiento óptimo - Manteniendo peso';
            confidence = 0.7;
        }
        // Bajo rendimiento - reducción
        else {
            adjustment = -0.05; // Reducir 5%
            reason = '📉 Ajustando carga para mejorar técnica';
            confidence = 0.8;
        }
        
        const newWeight = Math.max(0, Math.round((currentWeight * (1 + adjustment)) * 2) / 2);
        
        return {
            weight: newWeight,
            reason,
            confidence,
            type: adjustment > 0 ? 'increase' : adjustment < 0 ? 'decrease' : 'maintain'
        };
    }
    
    checkDeloadNeed() {
        // Analizar todo el historial para detectar necesidad de descarga
        const allWorkouts = this.data.workouts || [];
        if (allWorkouts.length < 10) return null;
        
        const recentWorkouts = allWorkouts.slice(-8); // Últimas 2 semanas aproximadamente
        const exercisePerformances = {};
        
        // Analizar rendimiento por ejercicio
        recentWorkouts.forEach(workout => {
            if (!workout.completedExercises) return;
            
            workout.completedExercises.forEach(exerciseData => {
                const exerciseName = exerciseData.name;
                if (!exercisePerformances[exerciseName]) {
                    exercisePerformances[exerciseName] = [];
                }
                
                const completion = exerciseData.repsCompleted / exerciseData.repsTarget;
                exercisePerformances[exerciseName].push(completion);
            });
        });
        
        // Calcular indicadores de sobrecarga
        let totalExercises = 0;
        let decliningExercises = 0;
        let stalledExercises = 0;
        
        Object.values(exercisePerformances).forEach(performances => {
            if (performances.length < 3) return;
            
            totalExercises++;
            const recent = performances.slice(-2).reduce((a, b) => a + b) / 2;
            const older = performances.slice(0, -2).reduce((a, b) => a + b) / (performances.length - 2);
            const decline = older - recent;
            
            if (decline > 0.1) decliningExercises++; // Caída >10%
            if (Math.abs(older - recent) < 0.02) stalledExercises++; // Sin cambio
        });
        
        // Determinar necesidad de descarga
        const declineRatio = decliningExercises / totalExercises;
        const stallRatio = stalledExercises / totalExercises;
        
        if (declineRatio > 0.4) {
            return {
                needed: true,
                reason: '🚨 Múltiples ejercicios mostrando declinación significativa',
                severity: 'high'
            };
        }
        
        if (stallRatio > 0.6 || declineRatio > 0.25) {
            return {
                needed: true,
                reason: '⚠️ Estancamiento generalizado detectado',
                severity: 'medium'
            };
        }
        
        return { needed: false };
    }

    saveExerciseData(exerciseIndex) {
        const workout = this.data.currentWorkout;
        const exercises = this.data.exercises[workout.muscleGroup];
        const exercise = exercises[exerciseIndex];

        // Collect data from all series
        const seriesData = [];
        let totalReps = 0;
        let targetReps = exercise.series * exercise.reps;
        let totalWeight = 0;

        for (let i = 1; i <= exercise.series; i++) {
            const reps = parseInt(document.getElementById(`reps-${exerciseIndex}-${i}`).value) || 0;
            const weight = parseFloat(document.getElementById(`weight-${exerciseIndex}-${i}`).value) || 0;
            const completed = document.getElementById(`serie-${exerciseIndex}-${i}`).checked;

            seriesData.push({ reps, weight, completed });
            
            if (completed) {
                totalReps += reps;
                totalWeight += reps * weight;
            }
        }

        // Save to progress
        if (!this.data.progress[exercise.name]) {
            this.data.progress[exercise.name] = { lastWorkouts: [], totalWeight: 0 };
        }

        this.data.progress[exercise.name].lastWorkouts.push({
            date: new Date().toISOString(),
            reps: totalReps,
            completion: totalReps / targetReps,
            weight: totalWeight
        });

        // Keep only last 10 workouts per exercise
        if (this.data.progress[exercise.name].lastWorkouts.length > 10) {
            this.data.progress[exercise.name].lastWorkouts.shift();
        }

        // Save to localStorage
        this.saveUserData();

        // Show success feedback
        this.showNotification(`✅ ${exercise.name} guardado correctamente!`);
    }

    completeWorkout() {
        const workout = this.data.currentWorkout;
        workout.completedAt = new Date().toISOString();
        
        // Add to workouts history
        if (!this.data.workouts) this.data.workouts = [];
        this.data.workouts.push(workout);

        // Check if we need to switch to next week
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        // If tomorrow is Monday, switch week type
        if (tomorrow.getDay() === 1) {
            this.data.weekType = this.data.weekType === 'A' ? 'B' : 'A';
            this.saveUserData();
        }

        // Update current workout to today's routine
        this.data.currentWorkout = {
            date: new Date().toISOString(),
            muscleGroup: getTodaysRoutine(this.data.weekType),
            completedExercises: []
        };

        // Save and reload
        this.saveUserData();
        this.loadExercises(); // This will update title and exercises
        this.updateSchedule();
        
        this.showNotification('🎉 ¡Entrenamiento completado! Descansa bien.');
    }

    updateSchedule() {
        const scheduleList = document.getElementById('schedule-list');
        const schedule = this.generateWeeklySchedule();

        scheduleList.innerHTML = '';
        schedule.forEach(day => {
            const dayElement = document.createElement('div');
            dayElement.className = `schedule-day ${day.type}`;
            dayElement.innerHTML = `
                <strong>${day.date.toLocaleDateString('es', { weekday: 'long', month: 'short', day: 'numeric' })}</strong>
                ${day.muscleGroup ? `<br><span>${day.muscleGroup}</span>` : '<br><span>Descanso</span>'}
                ${day.completed ? '<br><small class="text-success">✅ Completado</small>' : ''}
            `;
            scheduleList.appendChild(dayElement);
        });
    }

    generateWeeklySchedule() {
        const schedule = [];
        const today = new Date();
        
        // Get user-specific schedule
        const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
        const userSchedule = users[this.currentUserId]?.schedule || this.getDefaultSchedule();
        
        const groupNames = {
            'pecho-espalda-A': 'Pecho-Espalda A',
            'pecho-espalda-B': 'Pecho-Espalda B',
            'brazos-A': 'Brazos A',
            'brazos-B': 'Brazos B',
            'piernas-A': 'Piernas A',
            'piernas-B': 'Piernas B',
            'piernas-C': 'Piernas C',
            'abdomen-cardio': 'Abdomen-Cardio'
        };

        // Get current day of week to align with user's schedule
        const daysOfWeek = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
        
        // Generate 7 days starting from today
        for (let i = 0; i < 7; i++) {
            const date = new Date(today);
            date.setDate(today.getDate() + i);
            const dayName = daysOfWeek[date.getDay()];
            
            // Find the routine for this day from user's schedule
            const dayRoutine = userSchedule.routine.find(r => r.day === dayName);
            
            if (dayRoutine && dayRoutine.muscleGroup !== 'rest') {
                schedule.push({
                    date,
                    type: 'workout',
                    muscleGroup: groupNames[dayRoutine.muscleGroup] || dayRoutine.muscleGroup,
                    completed: false
                });
            } else {
                schedule.push({
                    date,
                    type: 'rest',
                    muscleGroup: null,
                    completed: false
                });
            }
        }

        return schedule;
    }

    initChart() {
        const ctx = document.getElementById('progressChart');
        if (ctx) {
            // Simple chart fallback if Chart.js is not loaded
            if (typeof Chart === 'undefined') {
                this.createSimpleChart();
                return;
            }
            
            this.progressChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Peso Total Levantado (kg)',
                        data: [],
                        borderColor: 'rgb(37, 99, 235)',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }
    
    createSimpleChart() {
        const ctx = document.getElementById('progressChart');
        if (ctx) {
            // Create a simple progress bar instead
            ctx.innerHTML = `
                <div class="simple-progress">
                    <h6>Progreso Reciente</h6>
                    <div class="progress-stats">
                        <div class="stat-item">
                            <strong>Entrenamientos esta semana:</strong>
                            <span>3</span>
                        </div>
                        <div class="stat-item">
                            <strong>Peso total:</strong>
                            <span>2,450 kg</span>
                        </div>
                        <div class="stat-item">
                            <strong>Mejor ejercicio:</strong>
                            <span>Press de Banca</span>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    updateProgressChart() {
        if (typeof Chart === 'undefined') {
            this.updateSimpleProgress();
            return;
        }
        
        if (!this.progressChart) return;

        const workouts = this.data.workouts || [];
        const last7Workouts = workouts.slice(-7);
        
        const labels = last7Workouts.map(w => 
            new Date(w.date).toLocaleDateString('es', { month: 'short', day: 'numeric' })
        );
        
        const data = last7Workouts.map(w => {
            // Calculate total weight for this workout
            return Math.random() * 1000 + 500; // Placeholder data
        });

        this.progressChart.data.labels = labels;
        this.progressChart.data.datasets[0].data = data;
        this.progressChart.update();
    }
    
    updateSimpleProgress() {
        const ctx = document.getElementById('progressChart');
        if (!ctx) return;
        
        const workouts = this.data.workouts || [];
        const totalWorkouts = workouts.length;
        
        // Calculate progress stats
        const lastWorkout = workouts[workouts.length - 1];
        const todayWorkout = lastWorkout && 
            new Date(lastWorkout.date).toDateString() === new Date().toDateString();
        
        ctx.innerHTML = `
            <div class="simple-progress">
                <h6>📊 Tu Progreso</h6>
                <div class="progress-stats">
                    <div class="stat-item">
                        <strong>Total Entrenamientos:</strong>
                        <span class="badge bg-primary">${totalWorkouts}</span>
                    </div>
                    <div class="stat-item">
                        <strong>Entrenó Hoy:</strong>
                        <span class="badge ${todayWorkout ? 'bg-success' : 'bg-secondary'}">
                            ${todayWorkout ? 'Sí ✓' : 'No'}
                        </span>
                    </div>
                    <div class="stat-item">
                        <strong>Objetivo Semanal:</strong>
                        <span class="badge bg-info">3/3 días</span>
                    </div>
                </div>
            </div>
        `;
    }

    // Routine Editor Functions
    loadRoutineEditor() {
        const selector = document.getElementById('muscle-group-selector');
        const muscleGroup = selector.value;
        const exercisesList = document.getElementById('routine-exercises-list');
        const exercises = this.data.exercises[muscleGroup] || [];

        exercisesList.innerHTML = '';

        exercises.forEach((exercise, index) => {
            const exerciseCard = this.createEditableExerciseCard(exercise, muscleGroup, index);
            exercisesList.appendChild(exerciseCard);
        });
    }

    createEditableExerciseCard(exercise, muscleGroup, index) {
        const card = document.createElement('div');
        card.className = 'exercise-card editable-exercise';
        card.innerHTML = `
            <div class="exercise-header">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="flex-grow-1">
                        <input type="text" class="form-control form-control-sm mb-2" 
                               id="exercise-name-${index}" value="${exercise.name}" 
                               placeholder="Nombre del ejercicio">
                        
                        <div class="row g-2">
                            <div class="col-6">
                                <label class="form-label small">Series:</label>
                                <input type="number" class="form-control form-control-sm" 
                                       id="exercise-series-${index}" value="${exercise.series}" min="1" max="10">
                            </div>
                            <div class="col-6">
                                <label class="form-label small">Repeticiones:</label>
                                <input type="number" class="form-control form-control-sm" 
                                       id="exercise-reps-${index}" value="${exercise.reps}" min="1" max="50">
                            </div>
                            <div class="col-6">
                                <label class="form-label small">Descanso (seg):</label>
                                <input type="number" class="form-control form-control-sm" 
                                       id="exercise-rest-${index}" value="${exercise.rest}" min="30" max="300" step="30">
                            </div>
                            <div class="col-6">
                                <label class="form-label small">Peso (kg):</label>
                                <input type="number" class="form-control form-control-sm" 
                                       id="exercise-weight-${index}" value="${exercise.weight}" min="0" step="2.5">
                            </div>
                        </div>
                    </div>
                    <div class="ms-2">
                        <button class="btn btn-sm btn-danger" onclick="removeExercise(${index})">
                            🗑️
                        </button>
                    </div>
                </div>
            </div>
        `;

        return card;
    }

    saveRoutine() {
        const selector = document.getElementById('muscle-group-selector');
        const muscleGroup = selector.value;
        const exercises = [];

        let exerciseIndex = 0;
        while (document.getElementById(`exercise-name-${exerciseIndex}`)) {
            const exercise = {
                name: document.getElementById(`exercise-name-${exerciseIndex}`).value.trim(),
                series: parseInt(document.getElementById(`exercise-series-${exerciseIndex}`).value) || 4,
                reps: parseInt(document.getElementById(`exercise-reps-${exerciseIndex}`).value) || 10,
                rest: parseInt(document.getElementById(`exercise-rest-${exerciseIndex}`).value) || 90,
                weight: parseFloat(document.getElementById(`exercise-weight-${exerciseIndex}`).value) || 0
            };

            if (exercise.name) {
                exercises.push(exercise);
            }
            exerciseIndex++;
        }

        if (exercises.length === 0) {
            this.showNotification('❌ Debes agregar al menos un ejercicio', 'danger');
            return;
        }

        // Save to data structure
        this.data.exercises[muscleGroup] = exercises;
        this.saveUserData();

        // Reload current workout if it's the affected muscle group
        if (this.data.currentWorkout.muscleGroup === muscleGroup) {
            this.loadExercises();
        }

        this.showNotification('✅ Rutina guardada correctamente!');
    }

    showNotification(message, type = 'success') {
        // Create toast notification
        const notification = document.createElement('div');
        const alertClass = type === 'danger' ? 'alert-danger' : type === 'warning' ? 'alert-warning' : 'alert-success';
        notification.className = `position-fixed top-0 start-50 translate-middle-x mt-3 alert ${alertClass} fade-in`;
        notification.style.zIndex = '9999';
        notification.innerHTML = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Global functions for HTML onclick handlers
let app;

function toggleExercise(index) {
    const details = document.getElementById(`exercise-${index}`);
    details.classList.toggle('show');
}

function markSerie(exerciseIndex, serieIndex) {
    // Optional: Visual feedback when marking series
}

function markSerieComplete(exerciseIndex, serieNumber) {
    // Visual feedback for completed series
    const checkbox = document.getElementById(`serie-${exerciseIndex}-${serieNumber}`);
    const row = checkbox.parentElement;
    if (checkbox.checked) {
        row.style.backgroundColor = '#d4edda';
    } else {
        row.style.backgroundColor = 'transparent';
    }
}

function saveExerciseData(index) {
    app.saveExerciseData(index);
}

function completeWorkout() {
    if (confirm('¿Confirmar que has completado todo el entrenamiento?')) {
        app.completeWorkout();
    }
}

function showAddExercise() {
    // Redirect to routines view
    document.querySelector('[data-view="routines"]').click();
}

function loadRoutineEditor() {
    app.loadRoutineEditor();
}

function addNewExercise() {
    const selector = document.getElementById('muscle-group-selector');
    const muscleGroup = selector.value;
    const exercisesList = document.getElementById('routine-exercises-list');
    
    const newIndex = exercisesList.children.length;
    const newExercise = {
        name: '',
        series: 4,
        reps: 10,
        rest: 90,
        weight: 0
    };
    
    const exerciseCard = app.createEditableExerciseCard(newExercise, muscleGroup, newIndex);
    exercisesList.appendChild(exerciseCard);
    
    // Focus on the name input
    setTimeout(() => {
        document.getElementById(`exercise-name-${newIndex}`).focus();
    }, 100);
}

function removeExercise(index) {
    if (confirm('¿Estás seguro de que quieres eliminar este ejercicio?')) {
        const card = document.querySelector(`#exercise-name-${index}`).closest('.editable-exercise');
        card.style.opacity = '0';
        card.style.transform = 'translateX(-100%)';
        
        setTimeout(() => {
            card.remove();
            // Renumber remaining exercises
            const exercisesList = document.getElementById('routine-exercises-list');
            const cards = exercisesList.querySelectorAll('.editable-exercise');
            cards.forEach((card, newIndex) => {
                const inputs = card.querySelectorAll('input');
                inputs[0].id = `exercise-name-${newIndex}`;
                inputs[1].id = `exercise-series-${newIndex}`;
                inputs[2].id = `exercise-reps-${newIndex}`;
                inputs[3].id = `exercise-rest-${newIndex}`;
                inputs[4].id = `exercise-weight-${newIndex}`;
                card.querySelector('button').setAttribute('onclick', `removeExercise(${newIndex})`);
            });
        }, 300);
    }
}

// Weekly Schedule System (Global Functions)
function determineWeekType() {
    const today = new Date();
    const startOfYear = new Date(today.getFullYear(), 0, 1);
    const weekNumber = Math.floor((today - startOfYear) / (7 * 24 * 60 * 60 * 1000));
    
    // Alternar cada semana: semanas pares = Tipo A, semanas impares = Tipo B
    return weekNumber % 2 === 0 ? 'A' : 'B';
}

function getTodaysRoutine(weekType) {
    const today = new Date().getDay(); // 0 = Domingo, 1 = Lunes, etc.
    
    // Mapeo de días a rutinas
    const weekSchedule = weekType === 'A' ? {
        0: 'piernas-B',      // Domingo
        1: 'descanso',       // Lunes
        2: 'pecho-espalda-B', // Martes
        3: 'brazos-B',       // Miércoles
        4: 'descanso',       // Jueves
        5: 'piernas-A',      // Viernes
        6: 'descanso'        // Sábado
    } : {
        0: 'brazos-B',       // Domingo
        1: 'descanso',       // Lunes
        2: 'piernas-B',      // Martes
        3: 'pecho-espalda-B', // Miércoles
        4: 'descanso',       // Jueves
        5: 'brazos-A',       // Viernes
        6: 'descanso'        // Sábado
    };
    
    return weekSchedule[today] || 'descanso';
}

function getNextWorkoutDay(weekType) {
    const today = new Date();
    
    // Encontrar el próximo día de entrenamiento
    for (let i = 1; i <= 7; i++) {
        const futureDate = new Date(today);
        futureDate.setDate(today.getDate() + i);
        const dayOfWeek = futureDate.getDay();
        
        const scheduleA = {
            0: 'piernas-B', 1: 'descanso', 2: 'pecho-espalda-B', 3: 'brazos-B', 
            4: 'descanso', 5: 'piernas-A', 6: 'descanso'
        };
        const scheduleB = {
            0: 'brazos-B', 1: 'descanso', 2: 'piernas-B', 3: 'pecho-espalda-B', 
            4: 'descanso', 5: 'brazos-A', 6: 'descanso'
        };
        
        const schedule = weekType === 'A' ? scheduleA : scheduleB;
        if (schedule[dayOfWeek] !== 'descanso') {
            return {
                date: futureDate,
                routine: schedule[dayOfWeek]
            };
        }
    }
}

// Global event listeners as backup
function setupGlobalViewListeners() {
    const buttons = document.querySelectorAll('[data-view]');
    buttons.forEach(button => {
        const viewName = button.dataset.view;
        button.onclick = function() {
            switchToView(viewName);
        };
    });
}

function switchToView(viewName) {
    console.log('Global switch to:', viewName);
    
    // Update button states
    document.querySelectorAll('[data-view]').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-view="${viewName}"]`).classList.add('active');

    // Update view visibility
    document.querySelectorAll('.view').forEach(view => {
        view.style.display = 'none';
    });
    document.getElementById(`${viewName}-view`).style.display = 'block';

    if (app) {
        app.currentView = viewName;

        // Update view-specific content
        if (viewName === 'progress') {
            app.updateProgressChart();
        } else if (viewName === 'schedule') {
            app.updateSchedule();
        } else if (viewName === 'routines') {
            app.loadRoutineEditor();
        }
    }
}

function saveRoutine() {
    app.saveRoutine();
}

// Theme management
FitnessApp.prototype.initTheme = function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    this.setTheme(savedTheme);
    
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.checked = savedTheme === 'dark';
};

FitnessApp.prototype.setTheme = function(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Update toggle icon
    const toggleIcon = document.querySelector('.toggle-icon');
    if (theme === 'dark') {
        toggleIcon.textContent = '☀️';
        document.querySelector('meta[name="theme-color"]').setAttribute('content', '#1a1a1a');
    } else {
        toggleIcon.textContent = '🌙';
        document.querySelector('meta[name="theme-color"]').setAttribute('content', '#2563eb');
    }
};

FitnessApp.prototype.toggleTheme = function() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    this.setTheme(newTheme);
};

// User Management Functions
FitnessApp.prototype.loadUserData = function() {
    if (!this.currentUserId) {
        // Create default user if none exists
        const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
        const userIds = Object.keys(users);
        if (userIds.length === 0) {
            this.currentUserId = 'user_' + Date.now();
            users[this.currentUserId] = {
                name: 'Usuario Default',
                createdAt: new Date().toISOString(),
                schedule: this.getDefaultSchedule()
            };
            localStorage.setItem('fitnessUsers', JSON.stringify(users));
            localStorage.setItem('currentUserId', this.currentUserId);
        } else {
            this.currentUserId = userIds[0];
            localStorage.setItem('currentUserId', this.currentUserId);
        }
    }

    // Load user-specific data
    const userKey = 'fitnessData_' + this.currentUserId;
    let userData = localStorage.getItem(userKey);
    
    if (!userData) {
        userData = {
            exercises: this.defaultExercises,
            workouts: [],
            progress: {},
            currentWorkout: {
                date: new Date().toISOString(),
                muscleGroup: 'pecho-espalda-A',
                completedExercises: []
            },
            weekType: determineWeekType()
        };
        localStorage.setItem(userKey, JSON.stringify(userData));
    } else {
        userData = JSON.parse(userData);
    }
    
    this.data = userData;
};

FitnessApp.prototype.getDefaultSchedule = function() {
    return {
        days: 4,
        routine: [
            { day: 'Lunes', muscleGroup: 'pecho-espalda-A' },
            { day: 'Martes', muscleGroup: 'brazos-A' },
            { day: 'Miércoles', muscleGroup: 'piernas-A' },
            { day: 'Jueves', muscleGroup: 'pecho-espalda-B' },
            { day: 'Viernes', muscleGroup: 'rest' },
            { day: 'Sábado', muscleGroup: 'brazos-B' },
            { day: 'Domingo', muscleGroup: 'rest' }
        ]
    };
};

FitnessApp.prototype.loadUserManagement = function() {
    this.updateUserSelector();
    this.updateUsersList();
    this.updateCurrentUserDisplay();
    this.generateScheduleConfig();
};

FitnessApp.prototype.updateUserSelector = function() {
    const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
    const selector = document.getElementById('user-selector');
    if (!selector) return;
    
    selector.innerHTML = '<option value="">-- Seleccionar usuario --</option>';
    
    Object.keys(users).forEach(userId => {
        const user = users[userId];
        const option = document.createElement('option');
        option.value = userId;
        option.textContent = user.name;
        if (userId === this.currentUserId) {
            option.selected = true;
        }
        selector.appendChild(option);
    });
};

FitnessApp.prototype.updateUsersList = function() {
    const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
    const list = document.getElementById('users-list');
    if (!list) return;
    
    list.innerHTML = '';
    
    Object.keys(users).forEach(userId => {
        const user = users[userId];
        const userItem = document.createElement('div');
        userItem.className = 'user-item';
        userItem.innerHTML = `
            <div>
                <strong>${user.name}</strong>
                ${userId === this.currentUserId ? '<span class="badge bg-primary ms-2">Actual</span>' : ''}
            </div>
            <button class="btn btn-sm btn-danger" onclick="app.deleteUser('${userId}')">Eliminar</button>
        `;
        list.appendChild(userItem);
    });
};

FitnessApp.prototype.updateCurrentUserDisplay = function() {
    const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
    const display = document.getElementById('current-user-name');
    if (display && this.currentUserId && users[this.currentUserId]) {
        display.textContent = users[this.currentUserId].name;
    }
};

FitnessApp.prototype.createDefaultUser = function(name) {
    const userId = 'user_' + Date.now();
    const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
    
    users[userId] = {
        name: name,
        createdAt: new Date().toISOString(),
        schedule: this.getDefaultSchedule()
    };
    
    localStorage.setItem('fitnessUsers', JSON.stringify(users));
    
    // Create user data
    const userData = {
        exercises: this.defaultExercises,
        workouts: [],
        progress: {},
        currentWorkout: {
            date: new Date().toISOString(),
            muscleGroup: 'pecho-espalda-A',
            completedExercises: []
        },
        weekType: determineWeekType()
    };
    
    localStorage.setItem('fitnessData_' + userId, JSON.stringify(userData));
    
    return userId;
};

FitnessApp.prototype.generateScheduleConfig = function() {
    const container = document.getElementById('schedule-config');
    if (!container) return;
    
    const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    const muscleGroups = ['Descanso', 'pecho-espalda-A', 'pecho-espalda-B', 'brazos-A', 'brazos-B', 'piernas-A', 'piernas-B', 'piernas-C', 'abdomen-cardio'];
    
    container.innerHTML = '';
    
    days.forEach(day => {
        const dayConfig = document.createElement('div');
        dayConfig.className = 'day-config';
        dayConfig.innerHTML = `
            <label class="form-label">${day}:</label>
            <select class="form-select day-routine" data-day="${day}">
                ${muscleGroups.map(group => {
                    const value = group === 'Descanso' ? 'rest' : group;
                    const label = group === 'Descanso' ? '🛌 Descanso' : 
                                  group.includes('pecho') ? '🏋️ ' + group.replace('-', ' ').toUpperCase() :
                                  group.includes('brazos') ? '💪 ' + group.replace('-', ' ').toUpperCase() :
                                  '🦵 ' + group.replace('-', ' ').toUpperCase();
                    return `<option value="${value}">${label}</option>`;
                }).join('')}
            </select>
        `;
        container.appendChild(dayConfig);
    });
};

FitnessApp.prototype.switchUser = function() {
    const selector = document.getElementById('user-selector');
    const newUserId = selector.value;
    
    if (!newUserId) {
        this.showNotification('Por favor selecciona un usuario válido');
        return;
    }
    
    // Save current user data
    this.saveUserData();
    
    // Switch to new user
    this.currentUserId = newUserId;
    localStorage.setItem('currentUserId', newUserId);
    
    // Load new user data
    this.loadUserData();
    this.loadUserManagement();
    this.loadExercises();
    this.updateSchedule();
    
    this.showNotification(`Usuario cambiado a: ${selector.options[selector.selectedIndex].text}`);
};

FitnessApp.prototype.deleteUser = function(userId) {
    if (userId === this.currentUserId) {
        this.showNotification('No puedes eliminar el usuario actual');
        return;
    }
    
    if (confirm('¿Estás seguro de eliminar este usuario? Se perderán todos sus datos.')) {
        const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
        delete users[userId];
        localStorage.setItem('fitnessUsers', JSON.stringify(users));
        
        // Delete user data
        localStorage.removeItem('fitnessData_' + userId);
        
        this.loadUserManagement();
        this.showNotification('Usuario eliminado correctamente');
    }
};

FitnessApp.prototype.saveUserData = function() {
    const userKey = 'fitnessData_' + this.currentUserId;
    localStorage.setItem(userKey, JSON.stringify(this.data));
};

// Global functions for user management
function createNewUser() {
    const nameInput = document.getElementById('new-user-name');
    const name = nameInput.value.trim();
    
    if (!name) {
        app.showNotification('Por favor ingresa un nombre de usuario');
        return;
    }
    
    const userId = app.createDefaultUser(name);
    app.updateUserSelector();
    app.updateUsersList();
    
    nameInput.value = '';
    app.showNotification(`Usuario "${name}" creado correctamente`);
}

function createNewUserFromMain() {
    const nameInput = document.getElementById('new-user-name-main');
    const name = nameInput.value.trim();
    
    if (!name) {
        app.showNotification('Por favor ingresa un nombre de usuario');
        return;
    }
    
    const userId = app.createDefaultUser(name);
    nameInput.value = '';
    
    // Auto-select the new user
    app.selectUser(userId);
    app.showNotification(`Usuario "${name}" creado y seleccionado correctamente`);
}

function switchUser() {
    app.switchUser();
}

function showUserSelection() {
    app.showUserSelection();
}

function saveUserSchedule() {
    const users = JSON.parse(localStorage.getItem('fitnessUsers') || '{}');
    const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    
    const routine = days.map(day => {
        const select = document.querySelector(`select[data-day="${day}"]`);
        return {
            day: day,
            muscleGroup: select ? select.value : 'rest'
        };
    });
    
    users[app.currentUserId].schedule = {
        days: parseInt(document.getElementById('training-days').value),
        routine: routine
    };
    
    localStorage.setItem('fitnessUsers', JSON.stringify(users));
    app.showNotification('Configuración de rutina guardada correctamente');
    app.updateSchedule();
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app = new FitnessApp();
});