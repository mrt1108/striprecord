import os
import time
from datetime import datetime
import subprocess

def format_model_to_UI(models):
    result = []
    for model in models:
        elapsed_time = time.time() - model.start_time
        minutes, seconds = divmod(elapsed_time, 60)
        start_datetime = datetime.fromtimestamp(model.start_time).strftime('%H:%M:%S')
        result.append(f"{model.modelo} | Start From: {start_datetime} ({int(minutes)}m {int(seconds)}s)")
    return '\n'.join([f"{result[i]}" for i in range(len(result))])

def format_recording_history_to_UI(recording_history):
    # Get the model, filename, and isRecording values from the dictionary
    model = recording_history["model"]
    filename = recording_history["filename"]
    status = recording_history["status"]
    # Format the dictionary values into the desired format
    formatted_string = f"model: {model} | status: {status}\nFile: {filename}"
    # Join the formatted strings with a newline separator
    return formatted_string

def add_duration_to_mp4(path, duration):
    cmd = f'ffmpeg -i "{path}" -c copy -metadata duration={duration} "{path}_new.mp4"'
    subprocess.run(cmd, shell=True)

def repair_mp4_file(input_file):
    output_file = os.path.splitext(input_file)[0] + "_fix.mp4"
    vlc_process = subprocess.Popen(["vlc", "-I", "rc", input_file, "--sout", "#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100}:standard{access=file,mux=mp4,dst=" + output_file + "}", "vlc://quit"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Return the output file name
    vlc_process.wait()

    # Replace the input file with the output file
    # os.replace(output_file, input_file)
    return output_file

def repair_mp4_file_ffmpeg(input_file):
    output_file = os.path.splitext(input_file)[0] + "_fixed.mp4"  # Đổi tên file kết quả
    cmd = f'ffmpeg -err_detect ignore_err -i "{input_file}" -c copy "{output_file}"'  # Thêm -err_detect
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        os.rename(input_file, input_file + "_original")  # Đổi tên file gốc
        os.rename(output_file, input_file)  # Đổi tên file fixed thành tên gốc
        with open('log.txt', 'a') as f:
            f.write(f'Successfully repaired {input_file}\n')
    else:
        with open('log.txt', 'a') as f:
            f.write(f'Error repairing {input_file}: {result.stderr}\n')
