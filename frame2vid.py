import os
import shutil
import subprocess

def encode_video(folder_path):
    # Validate if the folder exists
    if not os.path.isdir(folder_path):
        print(f"The provided folder path does not exist: {folder_path}")
        return

    # Extract the folder name to use as the video name
    folder_name = os.path.basename(folder_path.rstrip(os.sep))
    
    # Define the input frame pattern and output video path
    input_pattern = os.path.join(folder_path, "%d.png")
    output_video = f"{folder_name}.mp4"

    # Construct the ffmpeg command
    ffmpeg_command = [
        "ffmpeg",
        "-loglevel", "error",
        "-r", "60",
        "-f", "image2",
        "-i", input_pattern,
        "-vf", "scale=3840x2160:flags=lanczos",
        "-c:v", "h264_nvenc",
        "-pix_fmt", "yuv420p",
        "-b:v", "20M",
        "-crf", "0",
        "-preset", "slow",
        "-progress", "pipe:1",
        output_video
    ]

    # Run the ffmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Video created successfully: {output_video}")

        # Delete the frames folder after successful encoding
        shutil.rmtree(folder_path)
        print(f"Deleted frames folder: {folder_path}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running ffmpeg for {folder_path}: {e}")

def main():
    # Get the folder locations from the user
    folder_paths_input = input("Please enter the folder locations containing the frames (separated by commas): ").strip('"')
    folder_paths = [fp.strip().strip('"') for fp in folder_paths_input.split('","')]

    # Process each folder
    for folder_path in folder_paths:
        print(f"Processing folder: {folder_path}")
        encode_video(folder_path)

if __name__ == "__main__":
    main()
