import pygame
import numpy as np
import sounddevice as sd
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Initialize pygame for music playback
pygame.init()

# Define screen dimensions and set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Musically Mathematics")

# Define constants and colors
width, height = screen.get_width(), screen.get_height()
font = pygame.font.SysFont('Corbel', 35)
color = (255, 255, 255)

# Load audio file for playback and analysis
audio_file = 'untitled.mp3'
waveform_file = 'untitled.wav'

# Function to draw text on the screen
def draw_text(text, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Function to play music using pygame
def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Function to stop music using pygame
def stop_music():
    pygame.mixer.music.stop()

# Function to generate a sine wave and play it
def play_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(sine_wave, sample_rate)
    sd.wait()

# Function to analyze music waveform and visualize
def analyze_music(file_path):
    # Load the audio file
    y, sr = librosa.load(file_path)

    # Plot the waveform
    plt.figure(figsize=(12, 6))
    librosa.display.waveshow(y, sr=sr, alpha=0.7)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

    # Perform FFT to get the frequency spectrum
    N = len(y)  # Number of samples
    fft_data = fft(y)  # Fourier transform
    freqs = fftfreq(N, d=1/sr)  # Frequency bins

    # Plot the positive half of the frequency spectrum (magnitude)
    plt.figure(figsize=(12, 6))
    plt.plot(freqs[:N//2], np.abs(fft_data[:N//2]), label="Frequency Spectrum", color="orange")
    plt.title('Frequency Spectrum (Fourier Transform)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()
    plt.show()

    # Plot the Fourier transformed data (complex values as real and imaginary)
    plt.figure(figsize=(12, 6))
    plt.plot(freqs[:N//2], np.real(fft_data[:N//2]), label="Real Part", color="blue")
    plt.plot(freqs[:N//2], np.imag(fft_data[:N//2]), label="Imaginary Part", color="red", linestyle="--")
    plt.title('Fourier Transformed Data (Real and Imaginary Parts)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()
    plt.show()


# Function to compute and display the waveform equation
def compute_equation(file_path):
    y, sr = librosa.load(file_path, sr=None)
    N = len(y)
    fft_data = fft(y)
    freqs = fftfreq(N, 1 / sr)

    # Identify dominant frequencies
    indices = np.argsort(np.abs(fft_data))[-5:]  # Top 5 frequencies
    equation_terms = []
    for idx in indices:
        amplitude = np.abs(fft_data[idx]) / N
        phase = np.angle(fft_data[idx])
        freq = freqs[idx]
        if freq > 0:  # Ignore negative frequencies
            equation_terms.append(f"{amplitude:.2f} * sin(2π * {freq:.2f} * t + {phase:.2f})")

    # Combine terms into a single equation
    equation = " + ".join(equation_terms)
    print("Waveform Equation:")
    print(equation)

    # Display the equation in the pygame window
    draw_text("Equation Generated (see console)", 50, 300)
    return equation

# Function to generate music from an equation
# Function to generate music from an equation
def generate_function_music():
    try:
        # Ask the user for the equation
        equation = input("Enter the waveform equation (use 't' for time variable): ")

        # Generate the time domain
        duration = 10  # Duration of the sound in seconds
        sample_rate = 44100  # Sampling rate
        time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

        # Safely evaluate the equation
        waveform = eval(equation, {"t": time, "np": np, "sin": np.sin, "cos": np.cos, "pi": np.pi})

        # Normalize the waveform to avoid clipping
        waveform = 0.5 * waveform / np.max(np.abs(waveform))

        # Play the waveform
        sd.play(waveform, sample_rate)
        sd.wait()

        # Plot the waveform
        plt.figure(figsize=(12, 6))
        plt.plot(time, waveform, label="Generated Waveform")
        plt.title("Generated Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid()
        plt.show()

        # Perform FFT for frequency spectrum
        fft_data = fft(waveform)
        freqs = fftfreq(len(fft_data), d=1/sample_rate)

        # Plot the frequency spectrum (magnitude of FFT)
        plt.figure(figsize=(12, 6))
        plt.plot(freqs[:len(freqs)//2], np.abs(fft_data[:len(fft_data)//2]), label="Frequency Spectrum")
        plt.title("Frequency Spectrum")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        print(f"Error generating music: {e}")

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black

    # Display UI elements
    draw_text("1. Play Music", 50, 50)
    draw_text("2. Play Sine Wave", 50, 100)
    draw_text("3. Analyze Music", 50, 150)
    draw_text("4. Compute Equation", 50, 200)
    draw_text("5. Generate Function Music", 50, 250)
    draw_text("6. Stop Music", 50, 300)
    draw_text("Press Q to Quit", 50, 350)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Play music
                play_music(audio_file)
            elif event.key == pygame.K_2:  # Play a sine wave
                play_sine_wave(frequency=440, duration=2)
            elif event.key == pygame.K_3:  # Analyze music
                analyze_music(waveform_file)
            elif event.key == pygame.K_4:  # Compute equation
                equation = compute_equation(waveform_file)
            elif event.key == pygame.K_5:  # Generate music from equation
                generate_function_music()
            elif event.key == pygame.K_6:  # Stop music
                stop_music()
            elif event.key == pygame.K_q:  # Quit program
                running = False

    pygame.display.update()

pygame.quit()