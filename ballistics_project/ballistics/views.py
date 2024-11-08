from django.shortcuts import render
from .forms import BallisticsForm
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Константы
GRAVITY = 9.81
AIR_DENSITY = 1.2
DRAG_COEFFICIENT = 0.295
TIME_STEP = 0.01

def calculate_ballistics(initial_velocity, mass, angle_rad, cross_sectional_area, initial_height=0):
    velocity_x = initial_velocity * np.cos(angle_rad)
    velocity_y = initial_velocity * np.sin(angle_rad)

    positions = []
    drag_constants = 0.5 * DRAG_COEFFICIENT * AIR_DENSITY * cross_sectional_area / mass

    x, y = 0, initial_height
    while y >= 0:
        speed_sq = velocity_x ** 2 + velocity_y ** 2
        drag_force = drag_constants * speed_sq
        acceleration_x = -drag_force * velocity_x / np.sqrt(speed_sq)
        acceleration_y = -GRAVITY - drag_force * velocity_y / np.sqrt(speed_sq)
        velocity_x += acceleration_x * TIME_STEP
        velocity_y += acceleration_y * TIME_STEP
        x += velocity_x * TIME_STEP
        y += velocity_y * TIME_STEP
        positions.append([x, y])

    return np.array(positions)

def plot_trajectory(positions, initial_velocity, mass, angle_deg, diameter):
    plt.figure()
    plt.plot(positions[:, 0], positions[:, 1], label='Траектория снаряда', color='b')
    plt.xlabel('Дальность (м)')
    plt.ylabel('Высота (м)')
    plt.title('Траектория снаряда')
    plt.grid(True)
    plt.scatter(positions[0, 0], positions[0, 1], color='red', zorder=5)
    plt.scatter(positions[-1, 0], positions[-1, 1], color='red', zorder=5)
    plt.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def ballistics_view(request):
    if request.method == 'POST':
        form = BallisticsForm(request.POST)
        if form.is_valid():
            initial_velocity = form.cleaned_data['initial_velocity']
            mass = form.cleaned_data['mass'] / 1000  # Конвертация в кг
            diameter = form.cleaned_data['diameter'] / 1000  # Конвертация в метры
            angle_deg = form.cleaned_data['angle_deg']
            initial_height = form.cleaned_data['initial_height'] or 0

            angle_rad = np.radians(angle_deg)
            cross_sectional_area = np.pi * (diameter / 2) ** 2

            positions = calculate_ballistics(initial_velocity, mass, angle_rad, cross_sectional_area, initial_height)
            chart = plot_trajectory(positions, initial_velocity, mass, angle_deg, diameter)

            return render(request, 'ballistics/result.html', {
                'form': form,
                'chart': chart,
            })
    else:
        form = BallisticsForm()
    return render(request, 'ballistics/index.html', {'form': form})