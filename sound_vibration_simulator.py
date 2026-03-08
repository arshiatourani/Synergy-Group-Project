import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False


def get_wave_data(wave_type, amplitude, frequency, phase_deg):
    t = np.linspace(0, 1, 1000)
    phase_rad = np.radians(phase_deg)

    if wave_type == "Sine":
        y = amplitude * np.sin(2 * np.pi * frequency * t + phase_rad)
    elif wave_type == "Square":
        y = amplitude * np.sign(np.sin(2 * np.pi * frequency * t + phase_rad))
    elif wave_type == "Triangle":
        y = amplitude * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * frequency * t + phase_rad))
    elif wave_type == "Sawtooth":
        y = amplitude * (2 * ((frequency * t + phase_deg / 360) % 1) - 1)
    else:
        y = amplitude * np.sin(2 * np.pi * frequency * t + phase_rad)

    return t, y


def get_equation_text(wave_type, amplitude, frequency, phase):
    if wave_type == "Sine":
        return f"y = {amplitude} sin(2π × {frequency}t + {phase}°)"
    elif wave_type == "Square":
        return f"Square wave | A = {amplitude}, f = {frequency} Hz"
    elif wave_type == "Triangle":
        return f"Triangle wave | A = {amplitude}, f = {frequency} Hz"
    elif wave_type == "Sawtooth":
        return f"Sawtooth wave | A = {amplitude}, f = {frequency} Hz"
    else:
        return "Unknown wave"


def get_wave_info(wave_type):
    if wave_type == "Sine":
        return "Sine wave: smooth wave often used to represent pure sound."
    elif wave_type == "Square":
        return "Square wave: switches sharply between high and low values."
    elif wave_type == "Triangle":
        return "Triangle wave: rises and falls linearly."
    elif wave_type == "Sawtooth":
        return "Sawtooth wave: gradual rise followed by a sudden drop."
    else:
        return ""


def update_graph():
    wave_type = wave_var.get()
    amplitude = amp_scale.get()
    frequency = freq_scale.get()
    phase = phase_scale.get()

    t, y = get_wave_data(wave_type, amplitude, frequency, phase)

    ax.clear()
    ax.plot(t, y, linewidth=2, label=wave_type, color="#1d4ed8")

    if compare_var.get() == 1:
        compare_y = amplitude * np.sin(2 * np.pi * frequency * t)
        ax.plot(t, compare_y, linestyle="--", linewidth=2, label="Reference Sine", color="#60a5fa")

    ax.set_title("Waveform Display", fontsize=14, fontweight="bold")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.4)
    ax.legend()

    max_y = max(10, amplitude + 10)
    ax.set_ylim(-max_y, max_y)

    canvas.draw()

    period = 1 / frequency

    equation_label.config(
        text=f"Equation\n\n{get_equation_text(wave_type, amplitude, frequency, phase)}"
    )

    measurement_label.config(
        text=(
            f"Measurements\n\n"
            f"Amplitude = {amplitude}\n"
            f"Frequency = {frequency:.2f} Hz\n"
            f"Period = {period:.2f} s\n"
            f"Phase = {phase}°"
        )
    )

    info_label.config(
        text=f"Wave Information\n\n{get_wave_info(wave_type)}"
    )

    summary_label.config(
        text=f"Current Wave: {wave_type} | Amplitude: {amplitude} | Frequency: {frequency:.2f} Hz"
    )

    status_label.config(text="Graph updated successfully")


def reset_values():
    global phase_animation
    wave_var.set("Sine")
    amp_scale.set(50)
    freq_scale.set(2)
    phase_scale.set(0)
    compare_var.set(0)
    phase_animation = 0
    update_graph()
    status_label.config(text="Values reset to default")


def play_tone():
    if SOUND_AVAILABLE:
        frequency = freq_scale.get() * 100
        frequency = max(37, min(2000, frequency))
        winsound.Beep(int(frequency), 500)
        status_label.config(text="Tone played")
    else:
        status_label.config(text="Sound works only on Windows")


def save_graph():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if file_path:
        fig.savefig(file_path)
        status_label.config(text="Graph saved successfully")


def start_animation():
    global animation_running
    if not animation_running:
        animation_running = True
        animate_loop()


def stop_animation():
    global animation_running
    animation_running = False
    status_label.config(text="Animation stopped")


def animate_loop():
    global animation_running
    global phase_animation

    if animation_running:
        phase_animation += 10
        if phase_animation > 360:
            phase_animation = 0

        phase_scale.set(phase_animation)
        update_graph()
        root.after(100, animate_loop)


def set_preset(wave, amp, freq, phase):
    global phase_animation
    phase_animation = phase
    wave_var.set(wave)
    amp_scale.set(amp)
    freq_scale.set(freq)
    phase_scale.set(phase)
    update_graph()
    status_label.config(text=f"Preset loaded: {wave}")


def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Help - Concepts and Criteria")
    help_window.geometry("700x600")
    help_window.configure(bg="#dbeafe")

    title = tk.Label(
        help_window,
        text="Sound and Vibration Concepts",
        font=("Arial", 16, "bold"),
        bg="#1e3a8a",
        fg="white",
        pady=10
    )
    title.pack(fill="x")

    help_text = tk.Text(
        help_window,
        wrap="word",
        font=("Arial", 11),
        bg="white"
    )
    help_text.pack(fill="both", expand=True, padx=15, pady=15)

    content = """
MAIN CONCEPTS

Amplitude
Amplitude is the maximum height of the wave from the centre line.
Higher amplitude means stronger vibration or louder sound.

Frequency
Frequency is the number of cycles per second.
It is measured in Hertz (Hz).
Higher frequency means higher pitch.

Period
The period is the time required for one full wave cycle.

Period = 1 / Frequency

Phase
Phase determines where the wave starts from.
Changing phase shifts the wave left or right.


WAVE TYPES

Sine Wave
A smooth wave that represents pure sound.

Square Wave
A signal that jumps between high and low values.

Triangle Wave
A wave that increases and decreases in straight lines.

Sawtooth Wave
A wave that increases gradually and drops suddenly.


HOW TO USE THE APP

1. Select a wave type.
2. Adjust amplitude, frequency and phase using the sliders.
3. The graph updates automatically.
4. Use "Compare with sine wave" to compare signals.
5. Use presets for quick examples.
6. Use "Play Tone" to hear a simple sound.
7. Use "Save Graph" to save the current graph.
8. Use animation buttons to see the phase changing live.


WHAT THIS PROJECT DEMONSTRATES

• Python GUI programming with Tkinter
• Scientific graph plotting using Matplotlib
• Understanding of vibration and sound waves
• Interactive simulation of wave behaviour


ASSESSMENT CRITERIA

Technical Development
The program contains a working graphical interface and interactive controls.

Scientific Understanding
The project demonstrates amplitude, frequency, phase and waveform behaviour.

User Interaction
Users can modify parameters and immediately observe changes in the graph.

Visual Design
The interface includes clear controls, graph display and information panels.

Problem Solving
The application dynamically calculates wave data and updates the display.
"""

    help_text.insert("1.0", content)
    help_text.config(state="disabled")

    close_button = tk.Button(
        help_window,
        text="Close",
        font=("Arial", 11, "bold"),
        bg="#1d4ed8",
        fg="white",
        command=help_window.destroy
    )
    close_button.pack(pady=10)


def set_status(message):
    status_label.config(text=message)


root = tk.Tk()
root.title("Sound and Vibration Simulator")
root.geometry("1250x730")
root.configure(bg="#dbeafe")

animation_running = False
phase_animation = 0

title_label = tk.Label(
    root,
    text="Sound and Vibration Simulator",
    font=("Arial", 24, "bold"),
    bg="#1e3a8a",
    fg="white",
    pady=12
)
title_label.pack(fill="x")

summary_label = tk.Label(
    root,
    text="Current Wave: Sine | Amplitude: 50 | Frequency: 2.00 Hz",
    font=("Arial", 11),
    bg="#bfdbfe",
    fg="black",
    pady=6
)
summary_label.pack(fill="x")

main_frame = tk.Frame(root, bg="#dbeafe")
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

left_frame = tk.Frame(main_frame, bg="#93c5fd", bd=2, relief="ridge")
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

wave_var = tk.StringVar(value="Sine")
compare_var = tk.IntVar(value=0)

control_title = tk.Label(
    left_frame,
    text="Controls",
    font=("Arial", 16, "bold"),
    bg="#93c5fd",
    fg="#0f172a"
)
control_title.pack(pady=10)

tk.Label(left_frame, text="Wave Type", font=("Arial", 11, "bold"), bg="#93c5fd").pack(anchor="w", padx=10)
wave_menu = ttk.Combobox(
    left_frame,
    textvariable=wave_var,
    values=["Sine", "Square", "Triangle", "Sawtooth"],
    state="readonly"
)
wave_menu.pack(fill="x", padx=10, pady=5)
wave_menu.bind("<<ComboboxSelected>>", lambda e: update_graph())

tk.Label(left_frame, text="Amplitude", font=("Arial", 11, "bold"), bg="#93c5fd").pack(anchor="w", padx=10, pady=(10, 0))
amp_scale = tk.Scale(
    left_frame,
    from_=10,
    to=100,
    orient="horizontal",
    bg="#93c5fd",
    highlightthickness=0,
    command=lambda e: update_graph()
)
amp_scale.set(50)
amp_scale.pack(fill="x", padx=10)

tk.Label(left_frame, text="Frequency", font=("Arial", 11, "bold"), bg="#93c5fd").pack(anchor="w", padx=10, pady=(10, 0))
freq_scale = tk.Scale(
    left_frame,
    from_=1,
    to=10,
    orient="horizontal",
    bg="#93c5fd",
    highlightthickness=0,
    command=lambda e: update_graph()
)
freq_scale.set(2)
freq_scale.pack(fill="x", padx=10)

tk.Label(left_frame, text="Phase", font=("Arial", 11, "bold"), bg="#93c5fd").pack(anchor="w", padx=10, pady=(10, 0))
phase_scale = tk.Scale(
    left_frame,
    from_=0,
    to=360,
    orient="horizontal",
    bg="#93c5fd",
    highlightthickness=0,
    command=lambda e: update_graph()
)
phase_scale.set(0)
phase_scale.pack(fill="x", padx=10)

compare_check = tk.Checkbutton(
    left_frame,
    text="Compare with sine wave",
    variable=compare_var,
    bg="#93c5fd",
    font=("Arial", 10),
    command=update_graph
)
compare_check.pack(anchor="w", padx=10, pady=10)

preset_title = tk.Label(
    left_frame,
    text="Quick Presets",
    font=("Arial", 13, "bold"),
    bg="#93c5fd"
)
preset_title.pack(anchor="w", padx=10, pady=(10, 5))

preset_frame = tk.Frame(left_frame, bg="#93c5fd")
preset_frame.pack(padx=10, fill="x")

tk.Button(preset_frame, text="Sine", width=8, command=lambda: set_preset("Sine", 50, 2, 0)).grid(row=0, column=0, padx=3, pady=3)
tk.Button(preset_frame, text="Square", width=8, command=lambda: set_preset("Square", 50, 3, 0)).grid(row=0, column=1, padx=3, pady=3)
tk.Button(preset_frame, text="Triangle", width=8, command=lambda: set_preset("Triangle", 60, 2, 0)).grid(row=1, column=0, padx=3, pady=3)
tk.Button(preset_frame, text="Sawtooth", width=8, command=lambda: set_preset("Sawtooth", 60, 4, 0)).grid(row=1, column=1, padx=3, pady=3)

button_frame = tk.Frame(left_frame, bg="#93c5fd")
button_frame.pack(pady=10)

reset_button = tk.Button(
    button_frame,
    text="Reset",
    font=("Arial", 10, "bold"),
    bg="#1d4ed8",
    fg="white",
    width=12,
    command=reset_values
)
reset_button.grid(row=0, column=0, padx=5, pady=5)

sound_button = tk.Button(
    button_frame,
    text="Play Tone",
    font=("Arial", 10, "bold"),
    bg="#2563eb",
    fg="white",
    width=12,
    command=play_tone
)
sound_button.grid(row=0, column=1, padx=5, pady=5)

save_button = tk.Button(
    button_frame,
    text="Save Graph",
    font=("Arial", 10, "bold"),
    bg="#3b82f6",
    fg="white",
    width=12,
    command=save_graph
)
save_button.grid(row=1, column=0, padx=5, pady=5)

help_button = tk.Button(
    button_frame,
    text="Help",
    font=("Arial", 10, "bold"),
    bg="#60a5fa",
    fg="black",
    width=12,
    command=show_help
)
help_button.grid(row=1, column=1, padx=5, pady=5)

animate_button = tk.Button(
    button_frame,
    text="Start Animation",
    font=("Arial", 10, "bold"),
    bg="#93c5fd",
    fg="black",
    width=12,
    command=start_animation
)
animate_button.grid(row=2, column=0, padx=5, pady=5)

stop_button = tk.Button(
    button_frame,
    text="Stop Animation",
    font=("Arial", 10, "bold"),
    bg="#bfdbfe",
    fg="black",
    width=12,
    command=stop_animation
)
stop_button.grid(row=2, column=1, padx=5, pady=5)

equation_label = tk.Label(
    left_frame,
    text="",
    font=("Arial", 11),
    bg="#93c5fd",
    justify="left",
    wraplength=260,
    relief="solid",
    bd=1,
    padx=8,
    pady=8
)
equation_label.pack(padx=10, pady=8, fill="x")

measurement_label = tk.Label(
    left_frame,
    text="",
    font=("Arial", 11),
    bg="#bfdbfe",
    justify="left",
    relief="solid",
    bd=1,
    padx=8,
    pady=8
)
measurement_label.pack(padx=10, pady=8, fill="x")

info_label = tk.Label(
    left_frame,
    text="",
    font=("Arial", 10),
    bg="#dbeafe",
    justify="left",
    wraplength=260,
    relief="solid",
    bd=1,
    padx=8,
    pady=8
)
info_label.pack(padx=10, pady=8, fill="x")

graph_title = tk.Label(
    right_frame,
    text="Live Wave Graph",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#1e3a8a"
)
graph_title.pack(pady=10)

fig = Figure(figsize=(7.5, 5), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 10),
    bg="#1e3a8a",
    fg="white",
    anchor="w",
    padx=10
)
status_label.pack(fill="x", side="bottom")

for button, message in [
    (reset_button, "Reset all settings to default"),
    (sound_button, "Play a tone based on the selected frequency"),
    (save_button, "Save the current graph as an image"),
    (help_button, "Open help and assessment criteria"),
    (animate_button, "Start wave animation"),
    (stop_button, "Stop wave animation")
]:
    button.bind("<Enter>", lambda e, m=message: set_status(m))
    button.bind("<Leave>", lambda e: set_status("Ready"))

update_graph()
root.mainloop()
