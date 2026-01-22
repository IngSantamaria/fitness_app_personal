// Data Management with LocalStorage
class FitnessApp {
    constructor() {
        this.currentView = 'workout';
        this.initializeData();
        this.setupEventListeners();
        this.loadExercises();
        this.updateSchedule();
        this.initChart();
    }

    initializeData() {
        // Default exercises data
        this.defaultExercises = {
            'pecho': [
                { name: 'Press de Banca', series: 4, reps: 10, rest: 120, weight: 60 },
                { name: 'Press Inclinado con Mancuernas', series: 3, reps: 12, rest: 90, weight: 20 },
                { name: 'Aperturas en polea', series: 3, reps: 15, rest: 60, weight: 25 },
                { name: 'Fondos en paralelas', series: 3, reps: 8, rest: 90, weight: 0 }
            ],
            'espalda': [
                { name: 'Dominadas', series: 4, reps: 8, rest: 120, weight: 0 },
                { name: 'Remo con Barra', series: 4, reps: 10, rest: 120, weight: 70 },
                { name: 'Jalón al pecho', series: 3, reps: 12, rest: 90, weight: 50 },
                { name: 'Remo en máquina', series: 3, reps: 12, rest: 60, weight: 40 }
            ],
            'piernas': [
                { name: 'Sentadillas con barra', series: 4, reps: 12, rest: 180, weight: 80 },
                { name: 'Prensa de piernas', series: 3, reps: 15, rest: 120, weight: 100 },
                { name: 'Zancadas con mancuernas', series: 3, reps: 10, rest: 90, weight: 15 },
                { name: 'Elevación de gemelos', series: 4, reps: 20, rest: 60, weight: 30 }
            ]
        };

        // Check if data exists in localStorage
        if (!localStorage.getItem('fitnessData')) {
            const initialData = {
                exercises: this.defaultExercises,
                workouts: [],
                progress: {},
                currentWorkout: {
                    date: new Date().toISOString(),
                    muscleGroup: 'pecho',
                    completedExercises: []
                }
            };
            localStorage.setItem('fitnessData', JSON.stringify(initialData));
        }

        this.data = JSON.parse(localStorage.getItem('fitnessData'));
    }

    setupEventListeners() {
        // View switcher buttons
        document.querySelectorAll('[data-view]').forEach(button => {
            button.addEventListener('click', (e) => {
                this.switchView(e.target.dataset.view);
            });
        });
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
        }
    }

    loadExercises() {
        const exerciseList = document.getElementById('exercise-list');
        const currentWorkout = this.data.currentWorkout;
        const exercises = this.data.exercises[currentWorkout.muscleGroup] || this.data.exercises.pecho;

        exerciseList.innerHTML = '';

        exercises.forEach((exercise, index) => {
            const exerciseCard = this.createExerciseCard(exercise, index);
            exerciseList.appendChild(exerciseCard);
        });
    }

    createExerciseCard(exercise, index) {
        const card = document.createElement('div');
        card.className = 'exercise-card';
        
        // Get recommended weight based on progress
        const recommendedWeight = this.getRecommendedWeight(exercise.name, exercise.weight);
        const weightChange = recommendedWeight - exercise.weight;
        
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
                        ${weightChange !== 0 ? `
                            <span class="recommended-badge">
                                ${weightChange > 0 ? '+' : ''}${weightChange}kg
                            </span>
                        ` : ''}
                        <br>
                        <small class="text-muted">Recomendado: ${recommendedWeight}kg</small>
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

    getRecommendedWeight(exerciseName, currentWeight) {
        const progress = this.data.progress[exerciseName];
        if (!progress || progress.lastWorkouts.length < 2) {
            return currentWeight; // No change for beginners
        }

        // Calculate if should increase weight
        const lastWorkouts = progress.lastWorkouts.slice(-3);
        const avgCompletion = lastWorkouts.reduce((sum, w) => sum + w.completion, 0) / lastWorkouts.length;
        
        if (avgCompletion >= 0.95) { // Completed 95% or more of reps
            return Math.round((currentWeight + 2.5) * 2) / 2; // Increase by 2.5kg
        } else if (avgCompletion < 0.80) { // Struggling with current weight
            return Math.max(0, Math.round((currentWeight - 2.5) * 2) / 2); // Decrease by 2.5kg
        }
        
        return currentWeight; // Keep same weight
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
        localStorage.setItem('fitnessData', JSON.stringify(this.data));

        // Show success feedback
        this.showNotification(`✅ ${exercise.name} guardado correctamente!`);
    }

    completeWorkout() {
        const workout = this.data.currentWorkout;
        workout.completedAt = new Date().toISOString();
        
        // Add to workouts history
        if (!this.data.workouts) this.data.workouts = [];
        this.data.workouts.push(workout);

        // Reset for next workout
        const muscleGroups = Object.keys(this.data.exercises);
        const currentIndex = muscleGroups.indexOf(workout.muscleGroup);
        const nextIndex = (currentIndex + 1) % muscleGroups.length;
        
        workout.muscleGroup = muscleGroups[nextIndex];
        workout.date = new Date().toISOString();
        workout.completedExercises = [];

        // Save and reload
        localStorage.setItem('fitnessData', JSON.stringify(this.data));
        this.loadExercises();
        this.updateSchedule();
        
        this.showNotification('🎉 ¡Entrenamiento completado! Descansa bien.');
    }

    updateSchedule() {
        const scheduleList = document.getElementById('schedule-list');
        const muscleGroups = Object.keys(this.data.exercises);
        const schedule = this.generateWeeklySchedule(muscleGroups);

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

    generateWeeklySchedule(muscleGroups) {
        const schedule = [];
        const today = new Date();
        let dayIndex = 0;
        let muscleIndex = muscleGroups.indexOf(this.data.currentWorkout.muscleGroup);

        // Generate 7 days
        for (let i = 0; i < 7; i++) {
            const date = new Date(today);
            date.setDate(today.getDate() + i);
            
            // Simple schedule: 2 days training, 1 rest, repeat
            if (dayIndex % 3 === 2) {
                schedule.push({
                    date,
                    type: 'rest',
                    muscleGroup: null,
                    completed: false
                });
            } else {
                schedule.push({
                    date,
                    type: 'workout',
                    muscleGroup: muscleGroups[muscleIndex],
                    completed: false
                });
                muscleIndex = (muscleIndex + 1) % muscleGroups.length;
            }
            
            dayIndex++;
        }

        return schedule;
    }

    initChart() {
        const ctx = document.getElementById('progressChart');
        if (ctx) {
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

    updateProgressChart() {
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

    showNotification(message) {
        // Create toast notification
        const notification = document.createElement('div');
        notification.className = 'position-fixed top-0 start-50 translate-middle-x mt-3 alert alert-success fade-in';
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
    // Placeholder for adding custom exercises
    app.showNotification('🔧 Función para agregar ejercicios próximamente');
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app = new FitnessApp();
});