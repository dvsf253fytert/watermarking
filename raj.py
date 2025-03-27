from pydub import AudioSegment
import numpy as np

def embed_echo_watermark(input_file, output_file, delay_ms=2, decay=0.6):
    """Embeds an echo watermark into an audio file.

    Args:
        input_file (str): Path to the input audio file (must be a WAV file).
        output_file (str): Path to save the watermarked audio file.
        delay_ms (int): Delay of the echo in milliseconds.
        decay (float): Decay factor of the echo (0.0 to 1.0).
    """
    try:
        audio = AudioSegment.from_file(input_file, format="wav")
        samples = np.array(audio.get_array_of_samples())

        # Create echo watermark
        echo_samples = np.zeros_like(samples)
        delay_samples = int(delay_ms * audio.frame_rate / 1000)

        for i in range(delay_samples, len(samples)):
            echo_samples[i] = samples[i] + decay * samples[i - delay_samples]

        echo_audio = audio._spawn(echo_samples.astype(np.int16).tobytes())
        echo_audio.export(output_file, format="wav")
        print("✅ Watermarked audio saved!")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage (replace 'input.wav' with your audio file)
embed_echo_watermark("input.wav", "fake_watermarked.wav")